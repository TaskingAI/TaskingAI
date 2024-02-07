import { useState, useEffect } from 'react';
import ModalTable from '../modalTable/index.tsx';
import {
    Button,
    Space, Input, Spin, Tooltip, Modal
} from 'antd';
import styles from './chunkPage.module.scss'
import { toast } from 'react-toastify';
import { tooltipDeleteTitle,tooltipEditTitle } from '../../contents/index.tsx'
import DeleteModal from '../deleteModal/index.tsx';
import CopyOutlined from '../../assets/img/copyIcon.svg?react'
import { getRecordsList, createRecord, deleteRecord, updateRecord, getRecord } from '../../axios/chunk.ts'
import { formatTimestamp } from '@/utils/util'
import DeleteIcon from '../../assets/img/deleteIcon.svg?react'
import closeIcon from '../../assets/img/x-close.svg'
import EditIcon from '../../assets/img/editIcon.svg?react'
import ClipboardJS from 'clipboard';
function ChunkPage({ collectionId }) {
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
            dataIndex: 'chunk_id',
            key: 'chunk_id',
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
                <Tooltip overlayClassName='content-tooltip' title={text} placement='bottom'><span style={{ maxWidth: '480px', overflow: 'hidden', display: 'inline-block' }}>{text}</span></Tooltip>
            ),
        },
        {
            title: 'Record',
            dataIndex: 'record_id',
            key: 'record_id',
            width: 180,
            render: (text) => (
                <div>
                    {text}
                </div>
            )
        },
        {
            title: '# Tokens',
            dataIndex: 'num_tokens',
            key: 'num_tokens',
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
                    key: item.chunk_id
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

        setDrawerTitle('Create Record')
        setCreateOpenModal(true)
    }
    const handleCancel = () => {
        setCreateOpenModal(false)
    }
    const handleDelete = async (record: any) => {
        try {
            setOpenDeleteModal(true)
            setDeleteId(record.chunk_id)
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
        setDrawerTitle('Edit Chunk')
        setRecordId(record.chunk_id)
        setCreateOpenModal(true)
        const res = await getRecord(collectionId, record.chunk_id)
        setContentValue(res.data.content)
    }
    const handleConfirm = async () => {
        if (!contentValue) {
            toast.error('Please enter content')
            return
        }
        setConfirmLoading(true)
        try {
            const params = {
                content: contentValue,
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
            <ModalTable ifOnlyId={true} onOpenDrawer={handleCreatePrompt} onChildEvent={handleChildEvent} updatePrevButton={updatePrevButton} dataSource={recordList} ifSelect={false} name="chunk" columns={columns} hasMore={hasMore} id="chunk_id"></ModalTable>
            <Modal footer={[
                <Button key="cancel" onClick={handleCancel} className='cancel-button'>
                    Cancel
                </Button>,
                <Button key="submit" onClick={() => handleConfirm()} className='next-button' loading={confirmLoading}>
                    Confirm
                </Button>
            ]} title={drawerTitle} centered className={styles['record-create-model']} open={createOpenModal} width={720} onCancel={handleCancel} closeIcon={<img src={closeIcon} alt="closeIcon" />}>
                <div className={styles['text-content']}>
                    <div className={styles['text-title']}>Text content</div>
                    <div className={styles['desc']}>The text content of the chunk. Once created, it is converted into a computation-manageable vector via the collection's embedding model.</div>
                    <Input.TextArea placeholder='Enter text content' showCount minLength={0} maxLength={4096} value={contentValue} onChange={handleContentChange} className={styles['input']}></Input.TextArea>
                </div>
            </Modal>
            <DeleteModal open={OpenDeleteModal} describe={`Are you sure you want to delete record ${deleteId}? This action cannot be undone and all chunks associated with the record will be deleted.`} title="Delete Record" projectName={deleteId} onDeleteCancel={onDeleteCancel} onDeleteConfirm={onDeleteConfirm}></DeleteModal>
        </Spin>
    );
}
export default ChunkPage;