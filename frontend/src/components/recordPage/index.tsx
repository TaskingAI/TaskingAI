import { useState, useEffect } from 'react';
import ModalTable from '../modalTable/index.js';
import {
    Button,
    Space, Tag, Input, Spin, Tooltip, Modal
} from 'antd';
import './recordPage.scss'
import { toast } from 'react-toastify';
import { tooltipDeleteTitle, tooltipShowTitle } from '../../contents/index.js'

import DeleteModal from '../deleteModal/index.js';
import CopyOutlined from '../../assets/img/copyIcon.svg?react'
import { getRecordsList, createRecord, deleteRecord, updateRecord, getRecord } from '../../axios/record.js'
import { formatTimestamp } from '@/utils/util'
// import EditIcon from '../../assets/img/editIcon.svg?react'
import DeleteIcon from '../../assets/img/deleteIcon.svg?react'
import closeIcon from '../../assets/img/x-close.svg'
import ShowEye from '../../assets/img/showEye.svg?react'
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
                <Tooltip title={text.text} placement='bottom'><span style={{ maxWidth: '480px', overflow: 'hidden', display: 'inline-block' }}>{text.text}</span></Tooltip>
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
                        <Tooltip placement='bottom' title={tooltipShowTitle} color='#fff' arrow={false} overlayClassName='table-tooltip'>
                            <ShowEye />

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
    const [inputDisabeld, setInputDisabeld] = useState(false)
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
    const fetchData = async (collectionId, params) => {
        setLoading(true);
        try {
            const res = await getRecordsList(collectionId, params)
            const data = res.data.map((item) => {
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
        setDrawerTitle('Create Record')
        setInputDisabeld(false)
        setCreateOpenModal(true)
    }
    const handleCancel = () => {
        setCreateOpenModal(false)
    }
    const handleDelete = async (record) => {
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
    const handleEdit = async (record) => {
        setDrawerTitle('Edit Record')
        setInputDisabeld(true)
        setRecordId(record.record_id)
        setCreateOpenModal(true)
        const res = await getRecord(collectionId, record.record_id)
        setContentValue(res.data.content.text)
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
                text: contentValue
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
    const handleContentChange = (e) => {
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
            ]} title={drawerTitle} className='record-create-model' open={createOpenModal} width={720} onCancel={handleCancel} closeIcon={<img src={closeIcon} alt="closeIcon" />}>
                <div className='text-content'>
                    <div className='text-title'>Text content</div>
                    <div className='desc'>The content of the record. Upon creation, it will be segmented into smaller chunks and converted into computationally manageable vectors, following the rules set in the collection configuration. Currently only content in raw text format is supported.</div>
                    <Input.TextArea disabled={inputDisabeld} placeholder='Enter description' showCount minLength={0} maxLength={32768} value={contentValue} onChange={handleContentChange} className='input'></Input.TextArea>
                </div>
            </Modal>
            <DeleteModal open={OpenDeleteModal} describe={`Are you sure you want to delete reocrd ${deleteId}? This action cannot be undone and all chunks associated with the reocrd will be deleted.`} title="Delete Record" projectName={deleteId} onDeleteCancel={onDeleteCancel} onDeleteConfirm={onDeleteConfirm}></DeleteModal>
        </Spin>
    );
}
export default RecordPage;