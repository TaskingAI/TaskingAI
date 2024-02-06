
import { Tag } from 'antd';
import { formatTimestamp } from '@/utils/util'

import ClipboardJS from 'clipboard';
import { toast } from 'react-toastify';
import IconComponent from '@/components/iconComponent';

import CopyOutlined from '@/assets/img/copyIcon.svg?react';
const tooltipEditTitle = <span style={{ color: '#777' }}>Edit</span>;
const tooltipPlaygroundTitle = <span style={{ color: '#777' }}>Playground</span>;
const tooltipDeleteTitle = <span style={{ color: '#777' }}>Delete</span>;
const tooltipShowTitle = <span style={{ color: '#777' }}>Show</span>
const tooltipHideTitle = <span style={{ color: '#777' }}>Hide</span>
const tooltipRecordTitle = <span style={{ color: '#777' }}>Records</span>
const tooltipChunkTitle = <span style={{ color: '#777' }}>Chunks</span>
const statusReverse = {
    creating: 'orange',
    ready: 'green',
    error: 'red',
    deleting: 'red'
}
const revereseLabel = {
    naive: 'Naive',
    zero: 'Zero',
    [`message_window`]: 'Message Window',
}
const handleCopy = (text: string) => {
    const clipboard = new ClipboardJS('.icon-copy', {
        text: () => text
    });
    clipboard.on('success', function () {
        toast.success('Copied to clipboard')
        clipboard.destroy()
    });
    clipboard.on('error', function (e) {
        console.log(e);
    });
}


const typeReverse: Record<string, string> = {
    instruct_completion: 'Instruct Completion',
    chat_completion: 'Chat Completion',
    text_embedding: 'Text Embedding'
}
const modelsTableColumn: any = [
    {
        title: 'Name',
        dataIndex: 'name',
        key: 'name',
        fixed: 'left',
        width: 240,
        render: (text: string, record: any) =>
            <div>
                <p className='table-text' style={{ fontSize: '14px' }}>{text || 'Untitled Model'}</p>
                <p style={{ display: 'flex', alignItems: 'center', margin: 0 }}>
                    <span style={{ fontSize: '12px', color: '#777' }}>{record.model_id}</span><CopyOutlined className='icon-copy' onClick={() => handleCopy(record.model_id)} />

                </p>
            </div>
        ,
    },
    {
        title: 'Base model',
        dataIndex: 'model_schema_id',
        key: 'base_model_id',
        width: 240,
        render: (text: string, record: any) =>
            <div className='img-text'>
                {<IconComponent providerId={record.provider_id} />} <span className='a'>{text}</span>
            </div>

        ,
    },
    {
        title: 'Type',
        dataIndex: 'type',
        key: 'type',
        width: 240,
        render: (type: string) => (
            <>

                <Tag color='green'>
                    {typeReverse[type]}
                </Tag>
            </>
        ),
    },
    {
        title: 'Properties',
        dataIndex: 'properties',
        key: 'properties',
        width: 360,
        render: (proerties: object) => (
            <div style={{ display: 'flex' }}>
                {
                    proerties &&
                    typeof proerties === "object" &&
                    Object.entries(proerties)
                        .filter(([_key, property]) => property !== null)
                        .map(([key, property]) => (
                            <div
                                className="streamParent"
                                key={key}
                                style={{
                                    display: "flex",
                                    border: "1px solid #e4e4e4",
                                    borderRadius: "8px",
                                    width: "auto",
                                    padding: "0 4px",
                                    marginRight: "12px",
                                }}
                            >
                                <span
                                    className="stream"
                                    style={{ borderRight: "1px solid #e4e4e4", paddingRight: "2px" }}
                                >
                                    {key}
                                </span>
                                <span className="on" style={{ paddingLeft: "2px" }}>
                                    {String(property)}
                                </span>
                            </div>
                        ))
                        .slice(0, 2)
                }
                {
                    proerties &&
                    typeof proerties === "object" &&
                    Object.entries(proerties).filter(([_key, property]) => property !== null)
                        .length > 2 && (
                        <div
                            className="streamParent"
                            style={{
                                border: "1px solid #e4e4e4",
                                borderRadius: "8px",
                                width: "auto",
                                padding: "0 4px",
                            }}
                        >
                            <span className="stream" style={{ paddingRight: "2px" }}>
                                +
                                {Object.entries(proerties).filter(([_key, property]) => property !== null)
                                    .length - 2}
                            </span>
                        </div>
                    )
                }
            </div>
        ),
    },
    {
        title: 'Created at',
        width: 180,
        dataIndex: 'created_timestamp',
        key: 'created_timestamp',
        render: (time: number) => <div>{formatTimestamp(time)}</div>
    },

];
const collectionTableColumn: any = [
    {
        title: 'Name',
        dataIndex: 'name',
        key: 'name',
        width: 240,
        fixed: 'left',
        render: (text: string, record: any) =>
            <div>
                <p className='table-text' style={{ fontSize: '14px' }}>{text || 'Untitled Collection'}</p>
                <p style={{ display: 'flex', alignItems: 'center', margin: 0 }}>
                    <span style={{ fontSize: '12px', color: '#777' }}>{record.collection_id}</span><CopyOutlined className='icon-copy' onClick={() => handleCopy(record.collection_id)} />

                </p>
            </div>
        ,
    },
    {
        title: 'Description',
        dataIndex: 'description',
        key: 'description',
        width: 360,
        render: (text: string) => (
            <>
                <div>{text}</div>
            </>
        ),
    },
    {
        title: 'Records',
        dataIndex: 'num_records',
        key: 'num_records',
        width: 180,
        render: (text: string) => (
            <>
                <div>{text}</div>
            </>
        ),
    },
    {
        title: 'Capacity',
        dataIndex: 'capacity1',
        key: 'capacity1',
        width: 180,
        render: (text: string) => (
            <div>{text}</div>
        )
    },
    {
        title: 'Status',
        dataIndex: 'status',
        key: 'status',
        width: 180,
        render: (text: string) => (
            <Tag color={statusReverse[text as keyof typeof statusReverse] || 'defaultColor'}
            >
                {text}
            </Tag>
        )
    },
    {
        title: 'Embedding model ID',
        dataIndex: 'embedding_model_id',
        key: 'ModelID',
        ellipsis: true,
        width: 180,
        render: (_: string) => (
            <div>{_}</div>
        )
    },
    {
        title: 'Created at',
        dataIndex: 'created_timestamp',
        key: 'created_timestamp',
        width: 180,
        render: (time: number) => <div>{formatTimestamp(time)}</div>
    },

];
const actionsTableColumn: any = [
    {
        title: 'Name',
        dataIndex: 'name',
        key: 'name',
        fixed: 'left',
        width: 240,
        render: (text, record) =>
            <div>
                <p className='table-text' style={{ fontSize: '14px' }}>{text}</p>
                <p style={{ display: 'flex', alignItems: 'center', margin: 0 }}>
                    <span style={{ color: '#777', fontSize: '12px' }}>{record.action_id}</span><CopyOutlined className='icon-copy' onClick={() => handleCopy(record.action_id)} />

                </p>
            </div>
        ,
    },
    {
        title: 'Description',
        dataIndex: 'description',
        key: 'description',
        width: 360,
        render: (text) => (
            <>
                <div>{text}</div>
            </>
        ),
    },
    {
        title: 'Method',
        dataIndex: 'method',
        key: 'method',
        width: 180,
        render: (_) => (
            <>
                {_}
            </>
        ),
    },
    {
        title: 'Endpoint',
        dataIndex: 'endpoint',
        key: 'endpoint',
        width: 360,
        render: (_) => (
            <>
                {_}
            </>
        ),
    },
    {
        title: 'Created at',
        width: 180,
        dataIndex: 'created_timestamp',
        key: 'created_timestamp',
        render: (time) => <div>{formatTimestamp(time)}</div>
    }]
const apikeysTableColumn: any = [
    {
        title: 'Name',
        dataIndex: 'name',
        key: 'name',
        fixed: 'left',
        width: 240,
        render: (text) =>
            <div>
                {text}
            </div>
        ,
    },
    {
        title: 'Key',
        dataIndex: 'apikey',
        key: 'apikey',
        width: 360,
        render: (apiKey) => (
            <>
                <div style={{ display: 'flex', alignItems: 'center', margin: 0 }}><span style={{ fontSize: '12px', color: '#777' }}>{apiKey}</span> {!apiKey.includes('****') && <CopyOutlined className='icon-copy' onClick={() => handleCopy(apiKey)} />}</div>
            </>
        ),
    },
    {
        title: 'Created at',
        dataIndex: 'created_timestamp',
        key: 'created_timestamp',
        width: 180,
        render: (time) => <div>{formatTimestamp(time)}</div>
    },
    {
        title: 'Last updated',
        dataIndex: 'updated_timestamp',
        key: 'updated_timestamp',
        width: 180,
        render: (time) => <div>{formatTimestamp(time)}</div>
    }

];
const assistantTableColumn: any = [
    {
        title: 'Name',
        dataIndex: 'name',
        key: 'name',
        width: 240,
        height: 45,
        fixed: 'left',
        render: (text, record) =>
            <div>
                <p className='table-text' style={{ fontSize: '14px' }}>{text || 'Untitled Assistant'}</p>
                <p style={{ display: 'flex', alignItems: 'center', margin: 0 }}>
                    <span style={{ fontSize: '12px', color: '#777' }}>{record.assistant_id}</span><CopyOutlined className='icon-copy' onClick={() => handleCopy(record.assistant_id)} />

                </p>
            </div>
        ,
    },
    {
        title: 'Description',
        width: 360,
        dataIndex: 'description',
        key: 'description',
        render: (text) => (
            <>
                <div>{text}</div>
            </>
        ),
    },
    {
        title: 'Language model',
        dataIndex: 'model_id',
        width: 360,
        key: 'model_id',
        ellipsis: true,
        render: (_) => (
            <div>{_}</div>

        )
    },
    {
        title: 'Prompt template',
        width: 360,
        dataIndex: 'promptTemplate',
        ellipsis: true,
        render: (_) => (
            <div>{_}</div>

        )
    },
    {
        title: 'Memory',
        width: 180,
        dataIndex: 'memory',
        render: (_) => (
            <div>{revereseLabel[_]}</div>

        )
    },
    {
        title: 'Created at',
        width: 180,
        dataIndex: 'created_timestamp',
        key: 'created_timestamp',
        render: (time) => <div>{formatTimestamp(time)}</div>
    },
]

export { collectionTableColumn, tooltipChunkTitle, assistantTableColumn, apikeysTableColumn, actionsTableColumn, tooltipEditTitle, tooltipRecordTitle, tooltipDeleteTitle, tooltipPlaygroundTitle, tooltipShowTitle, tooltipHideTitle, modelsTableColumn };