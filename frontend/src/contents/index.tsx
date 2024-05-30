
import { Tag } from 'antd';
import { formatTimestamp } from '@/utils/util'
import ModelIcon from '@/commonComponent/modelIcon/index';

import ClipboardJS from 'clipboard';
import { toast } from 'react-toastify';
import CopyOutlined from '@/assets/img/copyIcon.svg?react';
import { useTranslation } from 'react-i18next';
import IconComponent from '@/commonComponent/iconComponent';
import ChatCompletionIcon from '@/assets/img/chatCompletion.svg?react'
import TextEmbeddingIcon from '@/assets/img/textEmbedding.svg?react'
import WildCardIcon from '@/assets/img/wildcard.svg?react'
import RerankIcon from '@/assets/img/rerankIcon.svg?react'
function CommonComponents() {
    const { t } = useTranslation()
    const statusReverse = {
        creating: 'orange',
        ready: 'green',
        error: 'red',
        deleting: 'red',
        Inviting: 'orange',
        Active: 'green',
        Rejected: 'red'
    }
    const typeIcon = {
        chat_completion: <ChatCompletionIcon />,
        text_embedding: <TextEmbeddingIcon />,
        wildcard: <WildCardIcon />,
        rerank: <RerankIcon/>
    }
    const reverseLabel: Record<string, any> = {
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
            title: `${t('projectModelColumnName')}`,
            dataIndex: 'name',
            key: 'name',
            fixed: 'left',
            width: 240,
            render: (text: string, record: any) =>
                <div>
                    <p className='table-text' style={{ fontSize: '14px' }}>{text || 'Untitled Model'}</p>
                    <p style={{ display: 'flex', alignItems: 'center', margin: 0, lineHeight: '18px' }}>
                        <span style={{ fontSize: '12px', color: '#777', lineHeight: '18px' }}>{record.model_id}</span><CopyOutlined className='icon-copy' onClick={() => handleCopy(record.model_id)} />
                    </p>
                </div>
            ,
        },
        {
            title: `${t('projectModelColumnBaseModel')}`,
            dataIndex: 'model_schema_id',
            key: 'base_model_id',
            width: 240,
            render: (text: string, record: any) =>
                <div className='img-text'>
                    <IconComponent providerId={record.provider_id} /> <span className='a'>{text}</span>
                </div>

            ,
        },
        {
            title: `${t('projectModelColumnType')}`,
            dataIndex: 'type',
            key: 'type',
            width: 240,
            render: (type: string) => (
                <>
                    <div className='model-types'>
                        <div className={type}>
                            {typeIcon[type as keyof typeof typeIcon]}{type.split('_').join(' ')}
                        </div>
                    </div>
                </>
            ),
        },
        {
            title: `${t('projectModelColumnProperties')}`,
            dataIndex: 'properties',
            key: 'properties',
            width: 360,
            render: (properties: object) => (
                <ModelIcon properties={properties} />
            ),
        },
        {
            title: `${t('projectModelColumnCreatedAt')}`,
            width: 180,
            dataIndex: 'created_timestamp',
            key: 'created_timestamp',
            render: (time: number) => <div>{formatTimestamp(time)}</div>
        },

    ];
    const bundleTableColumn: any = [
        {
            title: `${t('projectBundleColumnName')}`,
            dataIndex: 'name',
            key: 'name',
            fixed: 'left',
            width: 280,
            render: (text: string, record: any) =>
                <div style={{ display: 'flex', alignItems: 'center' }}>
                    <img src={record.icon_url} alt="" style={{ width: '36px', height: '36px' }} />
                    <div style={{ marginLeft: '12px' }}>
                        <p className='table-text' style={{ fontSize: '14px', marginBottom: '4px', marginTop: '4px' }}>{text}</p>
                        <p style={{ display: 'flex', alignItems: 'center', margin: 0, lineHeight: '18px' }}>
                            <span style={{ color: '#777', fontSize: '12px' }}>{record.bundle_id}</span><CopyOutlined className='icon-copy' onClick={() => handleCopy(record.bundle_id)} />
                        </p>
                    </div>

                </div>
            ,
        },
        {
            title: `${t('projectAssistantsColumnDescription')}`,
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
            title: 'Plugins',
            dataIndex: 'plugins',
            key: 'plugins',
            width: 360,
            render: (plugins: any) => (
                <div style={{ display: 'flex', alignItems: 'center', flexWrap: 'wrap', }}>
                    {plugins.map((plugin: any, index: any) => (
                        <div key={index} style={{ display: 'flex', marginBottom: '5px', borderRadius: '8px', width: 'auto', padding: '4px', marginRight: '12px', background: '#F8F8F8' }}>
                            <span style={{ color: '#8F8F8F', fontWeight: 500, fontSize: '12px' }}>{plugin.name}</span>
                        </div>
                    ))}
                </div>
            ),
        },
        {
            title: `${t('projectModelColumnCreatedAt')}`,
            dataIndex: 'created_timestamp',
            key: 'created_timestamp',
            width: 180,
            render: (time: number) => <div>{formatTimestamp(time)}</div>
        },
        {
            title: `${t('projectColumnLastUpdated')}`,
            dataIndex: 'updated_timestamp',
            key: 'updated_timestamp',
            width: 180,
            render: (time: number) => <div>{formatTimestamp(time)}</div>
        }
    ]
    const collectionTableColumn: any = [
        {
            title: `${t('projectModelColumnName')}`,
            dataIndex: 'name',
            key: 'name',
            width: 240,
            fixed: 'left',
            render: (text: string, record: any) =>
                <div>
                    <p className='table-text' style={{ fontSize: '14px' }}>{text || 'Untitled Collection'}</p>
                    <p style={{ display: 'flex', alignItems: 'center', margin: 0, lineHeight: '18px' }}>
                        <span style={{ fontSize: '12px', color: '#777' }}>{record.collection_id}</span><CopyOutlined className='icon-copy' onClick={() => handleCopy(record.collection_id)} />

                    </p>
                </div>
            ,
        },
        {
            title: `${t('projectAssistantsColumnDescription')}`,
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
            title: `${t('projectRetrievalColumnRecords')}`,
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
            title: `${t('projectRetrievalColumnCapacity')}`,
            dataIndex: 'capacity1',
            key: 'capacity1',
            width: 180,
            render: (text: string) => (
                <div>{text}</div>
            )
        },
        {
            title: `${t('projectRetrievalColumnStatus')}`,
            dataIndex: 'status',
            key: 'status',
            width: 180,
            render: (text: string) => (
                <div className={text}>
                    {text}
                </div>
            )
        },
        {
            title: `${t('projectRetrievalColumnEmbeddingModelID')}`,
            dataIndex: 'model_name',
            key: 'ModelID',
            ellipsis: true,
            width: 360,
            render: (text: string, record: any) =>
            <div>
                <p className='table-text' style={{ fontSize: '14px' }}>{text || 'Untitled Model'}</p>
                <p style={{ display: 'flex', alignItems: 'center', margin: 0, lineHeight: '18px' }}>
                    <span style={{ fontSize: '12px', color: '#777' }}>{record.embedding_model_id}</span><CopyOutlined className='icon-copy' onClick={() => handleCopy(record.embedding_model_id)} />

                </p>
            </div>
        },
        {
            title: `${t('projectModelColumnCreatedAt')}`,
            dataIndex: 'created_timestamp',
            key: 'created_timestamp',
            width: 180,
            render: (time: number) => <div>{formatTimestamp(time)}</div>
        },

    ];
    const actionsTableColumn: any = [
        {
            title: `${t('projectModelColumnName')}`,
            dataIndex: 'name',
            key: 'name',
            fixed: 'left',
            width: 240,
            render: (text: string, record: any) =>
                <div>
                    <p className='table-text' style={{ fontSize: '14px' }}>{text}</p>
                    <p style={{ display: 'flex', alignItems: 'center', margin: 0 }}>
                        <span style={{ color: '#777', fontSize: '12px' }}>{record.action_id}</span><CopyOutlined className='icon-copy' onClick={() => handleCopy(record.action_id)} />

                    </p>
                </div>
            ,
        },
        {
            title: `${t('projectAssistantsColumnDescription')}`,
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
            title: `${t('projectToolsActionColumnMethod')}`,
            dataIndex: 'method',
            key: 'method',
            width: 180,
            render: (_: any) => (
                <>
                    {_}
                </>
            ),
        },
        {
            title: `${t('projectToolsActionColumnEndpoint')}`,
            dataIndex: 'endpoint',
            key: 'endpoint',
            width: 360,
            render: (_: any) => (
                <>
                    {_}
                </>
            ),
        },
        {
            title: `${t('projectModelColumnCreatedAt')}`,
            width: 180,
            dataIndex: 'created_timestamp',
            key: 'created_timestamp',
            render: (time: number) => <div>{formatTimestamp(time)}</div>
        }]
    const apikeysTableColumn: any = [
        {
            title: `${t('projectModelColumnName')}`,
            dataIndex: 'name',
            key: 'name',
            fixed: 'left',
            width: 240,
            render: (text: string) =>
                <div>
                    {text}
                </div>
            ,
        },
        {
            title: `${t('projectAPIKeysColumnKey')}`,
            dataIndex: 'apikey',
            key: 'apikey',
            width: 360,
            render: (apikey: string) => (
                <>
                    <div style={{ display: 'flex', alignItems: 'center', margin: 0 }}><span style={{ fontSize: '12px', color: '#777' }}>{apikey}</span> {!apikey?.includes('****') && <CopyOutlined className='icon-copy' onClick={() => handleCopy(apikey)} />}</div>
                </>
            ),
        },
        {
            title: `${t('projectModelColumnCreatedAt')}`,
            dataIndex: 'created_timestamp',
            key: 'created_timestamp',
            width: 180,
            render: (time: number) => <div>{formatTimestamp(time)}</div>
        },
        {
            title: `${t('projectColumnLastUpdated')}`,
            dataIndex: 'updated_timestamp',
            key: 'updated_timestamp',
            width: 180,
            render: (time: number) => <div>{formatTimestamp(time)}</div>
        }

    ];
    const assistantTableColumn: any = [
        {
            title: `${t('projectModelColumnName')}`,
            dataIndex: 'name',
            key: 'name',
            width: 240,
            height: 45,
            fixed: 'left',
            render: (text: string, record: any) =>
                <div>
                    <p className='table-text' style={{ fontSize: '14px' }}>{text || 'Untitled Assistant'}</p>
                    <p style={{ display: 'flex', alignItems: 'center', margin: 0, lineHeight: '18px' }}>
                        <span style={{ fontSize: '12px', color: '#777' }}>{record.assistant_id}</span><CopyOutlined className='icon-copy' onClick={() => handleCopy(record.assistant_id)} />

                    </p>
                </div>
            ,
        },
        {
            title: `${t('projectAssistantsColumnDescription')}`,
            width: 360,
            dataIndex: 'description',
            key: 'description',
            render: (text: string) => (
                <>
                    <div>{text}</div>
                </>
            ),
        },
        {
            title: `${t('projectAssistantsColumnLangModel')}`,
            dataIndex: 'model_name',
            width: 360,
            key: 'model_id',
            ellipsis: true,
            render: (text: string, record: any) =>
                <div>
                    <p className='table-text' style={{ fontSize: '14px' }}>{text || 'Untitled Model'}</p>
                    <p style={{ display: 'flex', alignItems: 'center', margin: 0, lineHeight: '18px' }}>
                        <span style={{ fontSize: '12px', color: '#777' }}>{record.model_id}</span><CopyOutlined className='icon-copy' onClick={() => handleCopy(record.model_id)} />
                    </p>
                </div>
            ,
        },
        {
            title: `${t('projectAssistantsColumnPromptTemp')}`,
            width: 360,
            dataIndex: 'promptTemplate',
            ellipsis: true,
            render: (_: any) => (
                <div>{_}</div>

            )
        },
        {
            title: `${t('projectAssistantsColumnMemory')}`,
            width: 180,
            dataIndex: 'memory',
            render: (_: any) => (
                <div>{reverseLabel[_]}</div>

            )
        },
        {
            title: `${t('projectModelColumnCreatedAt')}`,
            width: 180,
            dataIndex: 'created_timestamp',
            key: 'created_timestamp',
            render: (time: number) => <div>{formatTimestamp(time)}</div>
        },
    ]
    const billingsColumns: any = [
        {
            title: `${t('spaceBillingColumnsDate')}`,
            dataIndex: 'BillingDate',
            key: 'date',
            width: 240,
            fixed: 'left',
        },
        {
            title: `${t('spacceBillingColumnInvoiceID')}`,
            dataIndex: 'InvoiceId',
            key: 'InvoiceId',
            width: 240,
        },
        {
            title: `${t('projectAssistantsColumnDescription')}`,
            dataIndex: 'Description',
            key: 'Description',
            width: 360
        },
        {
            title: `${t('spaceBillingColumnAmount')}`,
            dataIndex: 'Amount',
            key: 'Amount',
            width: 180

        },
        {
            title: `${t('projectRetrievalColumnStatus')}`,
            dataIndex: 'status',
            key: 'status',
            width: 180
        },
        {
            title: `${t('projectModelColumnCreatedAt')}`,
            width: 180,
            dataIndex: 'created_timestamp',
            key: 'created_timestamp',
            render: (time: number) => <div>{formatTimestamp(time)}</div>
        },

    ]
    const memberTableColumn: any = [
        {
            title: `${t('projectModelColumnName')}`,
            key: 'name',
            dataIndex: 'name',
            fixed: 'left',
            width: 240,
        },
        {
            title: `${t('authEmail')}`,
            key: 'email',
            dataIndex: 'email',
            width: 240
        },
        {
            title: `${t('spaceRole')}`,
            key: 'role',
            dataIndex: 'role',
            width: 180,
        },
        {
            title: `${t('projectRetrievalColumnStatus')}`,
            key: 'status',
            dataIndex: 'status',
            width: 180,
            render: (text: string) => (
                <Tag color={statusReverse[text as keyof typeof statusReverse] || 'defaultColor'}
                >
                    {text}
                </Tag>
            )
        },

        {
            title: `${t('spaceBillingColumnJoinTime')}`,
            key: 'created_timestamp',
            dataIndex: 'created_timestamp',
            width: 180,
            render: (time: number) => <div>{formatTimestamp(time)}</div>
        },
    ]
    return (
        { collectionTableColumn, bundleTableColumn, typeReverse, memberTableColumn, billingsColumns, assistantTableColumn, apikeysTableColumn, actionsTableColumn, modelsTableColumn }
    )
}
export default CommonComponents;
