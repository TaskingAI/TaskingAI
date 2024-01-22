import { useState, useEffect } from 'react';
import ModalTable from '../modalTable/index.tsx';
import {
    Button,
    Space, Tag, Input, Spin, Tooltip, Modal, InputNumber
} from 'antd';
import styles from './recordPage.module.scss'
import { toast } from 'react-toastify';
import { tooltipDeleteTitle,tooltipEditTitle } from '../../contents/index.tsx'

import DeleteModal from '../deleteModal/index.tsx';
import CopyOutlined from '../../assets/img/copyIcon.svg?react'
import { getRecordsList, createRecord, deleteRecord, updateRecord, getRecord } from '../../axios/record.ts'
import { formatTimestamp } from '@/utils/util'
import DeleteIcon from '../../assets/img/deleteIcon.svg?react'
import closeIcon from '../../assets/img/x-close.svg'
import EditIcon from '../../assets/img/editIcon.svg?react'
import ClipboardJS from 'clipboard';

const statusReverse = {
    Creating: 'orange',
    ready: 'green',
    error: 'red',
    deleting: 'red'
}

function RecordPage({ collectionId }) {
    const handleCopy = (text) => {
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
    const columns = [
        {
            title: 'ID',
            dataIndex: 'record_id',
            key: 'record_id',
            width: 240,
            fixed: 'left',
            render: (text) =>
                <div style={{ display: 'flex', alignItems: 'center', margin: 0 }}>
                    <span style={{ fontSize: '12px', color: '#777' }}>{text}</span><CopyOutlined className='icon-copy' onClick={() => handleCopy(text)} />
                </div>
            ,
        },
        {
            title: 'Content',
            width: 480,
            dataIndex: 'content',
            key: 'content',
            ellipsis: true,
            render: (text) => (
                <Tooltip title={text.text} placement='bottom'><span style={{ maxWidth: '480px', overflow: 'hidden', display: 'inline-block' }}>{text}</span></Tooltip>
            ),
        },
        {
            title: 'Status',
            dataIndex: 'status',
            key: 'status',
            width: 180,
            render: (text) => (
                <Tag color={statusReverse[text]}>
                    {text}
                </Tag>
            )
        },
        {
            title: 'Chunk',
            dataIndex: 'num_chunks',
            key: 'num_chunks',
            width: 180,
            render: (text) => (
                <div>
                    {text}
                </div>
            )
        },
        {
            title: 'Created at',
            width: 180,
            dataIndex: 'created_timestamp',
            key: 'created_timestamp',
            render: (time) => <div>{formatTimestamp(time)}</div>
        },
        {
            title: 'Actions',
            key: 'action',
            width: 118,
            fixed: 'right',
            render: (_, record) => (
                <Space size="middle">
                    <div onClick={() => handleEdit(record)} className='table-edit-icon' style={{ height: '34px', width: '34px', padding: '0', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                        {/* <span className='edit-icon'>Edit</span> */}
                        <Tooltip placement='bottom' title={tooltipEditTitle} color='#fff' arrow={false} overlayClassName='table-tooltip'>
                            <EditIcon />

                        </Tooltip>
                    </div>
                    <div onClick={() => handleDelete(record)} className='table-edit-icon' style={{ height: '34px', width: '34px', padding: '0', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                        <Tooltip placement='bottom' title={tooltipDeleteTitle} color='#fff' arrow={false} overlayClassName='table-tooltip'>
                            <DeleteIcon />
                        </Tooltip>
                    </div>
                </Space>
            ),
        },
    ];
    const [updatePrevButton, setUpdatePrevButton] = useState(false)
    const [hasMore, setHasMore] = useState(false)
    const [recordList, setRecordList] = useState([])
    const [loading, setLoading] = useState(false);
    const [createOpenModal, setCreateOpenModal] = useState(false)
    const [limit, setLimit] = useState(20)
    const [contentValue, setContentValue] = useState('')
    const [recordId, setRecordId] = useState('')
    const [confirmLoading, setConfirmLoading] = useState(false);
    const [OpenDeleteModal, setOpenDeleteModal] = useState(false)
    const [drawerTitle, setDrawerTitle] = useState('Create Record')
    const [deleteId, setDeleteId] = useState('')
    const [chunkSize, setChunkSize] = useState(200)
    const [title, setTitle] = useState('')
    const [chunkOverlap, setChunkOverlap] = useState(10)
    const handleChildEvent = async (value) => {
        setLimit(value.limit)
        setUpdatePrevButton(false)
        await fetchData(collectionId, value);
    }
    useEffect(() => {
        const params = {
            limit: 20
        }
        fetchData(collectionId, params)
    }, [collectionId])
    const fetchData = async (collectionId: string, params: Record<string, any>) => {
        setLoading(true);
        try {
            const res: any = await getRecordsList(collectionId, params)
            const data = res.data.map((item: any) => {
                return {
                    ...item,
                    key: item.record_id
                }
            })
            setRecordList(data);
            setHasMore(res.has_more)

        } catch (error) {
            console.log(error)
        }
        setLoading(false);
    };
    const handleCreatePrompt = () => {
        setContentValue('')
        setTitle('')
        setChunkSize(200)
        setChunkOverlap(10)

        setDrawerTitle('Create Record')
        setCreateOpenModal(true)
    }
    const handleCancel = () => {
        setCreateOpenModal(false)
    }
    const handleDelete = async (record: any) => {
        try {
            setOpenDeleteModal(true)
            setDeleteId(record.record_id)
        } catch (e) {
            console.log(e)
        }
    }
    const onDeleteCancel = () => {
        setOpenDeleteModal(false)
    }
    const onDeleteConfirm = async () => {
        try {
            await deleteRecord(collectionId, deleteId)
            const params = {
                limit: limit || 20,
            }
            await fetchData(collectionId, params)
            setUpdatePrevButton(true)
        } catch (error) {
            console.log(error)
        }
        setOpenDeleteModal(false)
    }
    const handleEdit = async (record: any) => {
        setDrawerTitle('Edit Record')
        setRecordId(record.record_id)
        setCreateOpenModal(true)
        const res = await getRecord(collectionId, record.record_id)
        setContentValue(res.data.content)
        setTitle(res.data.title)
        setChunkSize(Number(localStorage.getItem('chunkSize')))
        setChunkOverlap(Number(localStorage.getItem('chunkOverlap')))   
    }
    const handleConfirm = async () => {
        if (!contentValue) {
            toast.error('Please enter content')
            return
        }
        setConfirmLoading(true)
        try {
            const params = {
                type: 'text',
                title,
                content: contentValue,
                text_splitter: {
                    type: 'token',
                    chunk_size: chunkSize,
                    chunk_overlap: chunkOverlap
                }

            }
            if (drawerTitle === 'Create Record') {
                await createRecord(collectionId, params)
            } else {
                const param1 = {
                    ...params,
                    metadata: {}
                }
                await updateRecord(collectionId, recordId, param1)
            }
            localStorage.setItem('chunkSize', String(chunkSize) || '200')
            localStorage.setItem('chunkOverlap', String(chunkOverlap) || '20')
            const params3 = {
                limit: limit || 20,
            }
            await fetchData(collectionId, params3)
        } catch (e) {
            console.log(e)
        }
        setUpdatePrevButton(true)
        setCreateOpenModal(false)
        setConfirmLoading(false)
    }
    const handleContentChange = (e: any) => {
        setContentValue(e.target.value)
    }
    return (
        <Spin spinning={loading} >
            <ModalTable ifOnlyId={true} onOpenDrawer={handleCreatePrompt} onChildEvent={handleChildEvent} updatePrevButton={updatePrevButton} dataSource={recordList} ifSelect={false} name="record" columns={columns} hasMore={hasMore} id="record_id"></ModalTable>
            <Modal footer={[
                <Button key="cancel" onClick={handleCancel} className='cancel-button'>
                    Cancel
                </Button>,
                <Button key="submit" onClick={() => handleConfirm()} className='next-button' loading={confirmLoading}>
                    Confirm
                </Button>
            ]} title={drawerTitle} centered className={styles['record-create-model']} open={createOpenModal} width={720} onCancel={handleCancel} closeIcon={<img src={closeIcon} alt="closeIcon" />}>
                <div className={styles['text-content']}>
                    <div className={styles['text-title']}>Title</div>
                    <div className={styles.desc}>The title of the record. It will be appended to the top of each chunk derived from the record to improve semantic relevance.</div>
                    <Input className={styles['input1']} placeholder='Enter name' value={title} onChange={(e) => setTitle(e.target.value)}></Input>
                    <div className={styles['text-title']}>Text content</div>
                    <div className={styles['desc']}>The content of the record. Upon creation, it will be segmented into smaller chunks and converted into computationally manageable vectors, following the rules set in the collection configuration. Currently only content in raw text format is supported.</div>
                    <Input.TextArea placeholder='Enter description' showCount minLength={0} maxLength={32768} value={contentValue} onChange={handleContentChange} className={styles['input']}></Input.TextArea>
                    <div className={styles.label1}>Text Splitter</div>
                    <div className={styles['label']}>
                        <span className={styles['span']}>*</span>
                        <span>{`Chunk size`}</span>
                    </div>
                    <div className={styles['label-desc']}>The collection's records will be segmented into separate chunks to optimize data retrieval. Each chunk's capacity, known as the chunk size,ranges from 100 to 500 tokens.</div>
                    <InputNumber className={styles['input-number1']} placeholder='Enter chunk size(range:100-500)' parser={(value: string) => (isNaN(Number(value)) ? 1 : parseInt(value, 10))} value={chunkSize} onChange={(value:number) => setChunkSize(value)} min={100} max={500}></InputNumber>
                    <div className={styles['label']}>
                        <span className={styles['span']}>*</span>
                        <span>{`Chunk overlap`}</span>

                    </div>
                    <div className={styles['label-desc']}>{`Chunk overlap specifies how much overlap there should be between chunks,counted by number of chunk text tokens.It cannot be larger then chunk_size.`}</div>
                    <InputNumber className={styles['input-number']}  placeholder='Enter chunk overlap' value={chunkOverlap} onChange={(value) => setChunkOverlap(value)} parser={(value: string) => (isNaN(Number(value)) ? 1 : parseInt(value, 10))} min={0} max={100}></InputNumber>
                </div>
            </Modal>
            <DeleteModal open={OpenDeleteModal} describe={`Are you sure you want to delete reocrd ${deleteId}? This action cannot be undone and all chunks associated with the reocrd will be deleted.`} title="Delete Record" projectName={deleteId} onDeleteCancel={onDeleteCancel} onDeleteConfirm={onDeleteConfirm}></DeleteModal>
        </Spin>
    );
}
export default RecordPage;