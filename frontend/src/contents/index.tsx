
import { Tag } from 'antd';
import { formatTimestamp } from '@/utils/util'
import GoogleIcon from '@/assets/img/googleIcon.svg?react'
import ModelProvider from '@/assets/img/ModelProvider.svg?react'
import Anthropic from '@/assets/img/Anthropic.svg?react'
import Frame from '@/assets/img/Frame.svg?react'
import ClipboardJS from 'clipboard';
import { toast } from 'react-toastify';
import CohereIcon from '@/assets/img/cohereIcon.svg?react'
import CopyOutlined from '@/assets/img/copyIcon.svg?react';
const tooltipEditTitle = <span style={{ color: '#777' }}>Edit</span>;
const tooltipPlaygroundTitle = <span style={{ color: '#777' }}>Playground</span>;
const tooltipDeleteTitle = <span style={{ color: '#777' }}>Delete</span>;
const tooltipShowTitle = <span style={{ color: '#777' }}>Show</span>
const tooltipHideTitle = <span style={{ color: '#777' }}>Hide</span>
const statusReverse = {
    creating: 'orange',
    ready: 'green',
    error: 'red',
    deleting: 'red'
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
const imgReverse = (providerId: string) => {
    if (providerId === 'openai') {
        return <ModelProvider width='16px' height='16px' />
    } else if (providerId === 'anthropic') {
        return <Anthropic width='16px' height='16px' />
    } else if (providerId === 'azure_openai') {
        return <Frame width='16px' height='16px' />
    } else if (providerId === 'google_gemini') {
        return <GoogleIcon width='16px' height='16px' />
    } else if (providerId === 'cohere') {
        return <CohereIcon width='16px' height='16px' />
    }
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
                {imgReverse(record.provider_id)} <span className='a'>{text}</span>
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

                {proerties && typeof proerties === 'object' && Object.entries(proerties).map(([key, property]) => (
                    <div className='streamParent' key={key} style={{ display: 'flex', border: '1px solid #e4e4e4', borderRadius: '8px', width: 'auto', padding: '0 4px', marginRight: '12px' }}>
                        <span className='stream' style={{ borderRight: '1px solid #e4e4e4', paddingRight: '2px' }}>{key}</span>
                        <span className='on' style={{ paddingLeft: '2px' }}>{String(property)}</span>
                    </div>
                )).slice(0, 2)}
                {proerties && typeof proerties === 'object' && Object.entries(proerties).length > 2 && (
                    <div className='streamParent' style={{ border: '1px solid #e4e4e4', borderRadius: '8px', width: 'auto', padding: '0 4px' }}>
                        <span className='stream' style={{ paddingRight: '2px' }}>+{Object.entries(proerties).length - 2}</span>
                    </div>
                )}
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
        render: (text:string, record:any) =>
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
        render: (text:string) => (
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
        render: (text:string) => (
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
        render: (text:string) => (
            <div>{text}</div>
        )
    },
    {
        title: 'Status',
        dataIndex: 'status',
        key: 'status',
        width: 180,
        render: (text:string) => (
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
        render: (_:string) => (
            <div>{_}</div>
        )
    },
    {
        title: 'Created at',
        dataIndex: 'created_timestamp',
        key: 'created_timestamp',
        width: 180,
        render: (time:number) => <div>{formatTimestamp(time)}</div>
    },

];
export { collectionTableColumn, tooltipEditTitle, tooltipDeleteTitle, tooltipPlaygroundTitle, tooltipShowTitle, tooltipHideTitle, modelsTableColumn };