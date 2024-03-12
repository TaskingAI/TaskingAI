import { useState, useEffect } from 'react';
import ModalTable from '../modalTable/index.tsx';
import {
    Button,
    Space, Tag, Input, Spin, Tooltip, Modal, InputNumber
} from 'antd';
import styles from './recordPage.module.scss'
import { toast } from 'react-toastify';
import tooltipTitle from '../../contents/tooltipTitle'
import DeleteModal from '../deleteModal/index.tsx';
import CopyOutlined from '../../assets/img/copyIcon.svg?react'
import { getRecordsList, createRecord, deleteRecord, updateRecord, getRecord } from '../../axios/record.ts'
import { formatTimestamp } from '@/utils/util'
import DeleteIcon from '../../assets/img/deleteIcon.svg?react'
import closeIcon from '../../assets/img/x-close.svg'
import EditIcon from '../../assets/img/editIcon.svg?react'
import ClipboardJS from 'clipboard';
import { useTranslation } from 'react-i18next';
const statusReverse: Record<string, string> = {
    Creating: 'orange',
    ready: 'green',
    error: 'red',
    deleting: 'red'
}

function RecordPage({ collectionId }: { collectionId: string }) {
    const { t } = useTranslation();
    const { tooltipEditTitle, tooltipDeleteTitle } = tooltipTitle();

    const handleCopy = (text: string) => {
        const clipboard = new ClipboardJS('.icon-copy', {
            text: () => text
        });
        clipboard.on('success', function () {
            toast.success(`${t('CopiedToClipboard')}`)
            clipboard.destroy()
        });
        clipboard.on('error', function (e) {
            console.log(e);
        });
    }
    const columns = [
        {
            title: `${t('projectModelID')}`,
            dataIndex: 'record_id',
            key: 'record_id',
            width: 240,
            fixed: 'left',
            render: (text: string) =>
                <div style={{ display: 'flex', alignItems: 'center', margin: 0 }}>
                    <span style={{ fontSize: '12px', color: '#777' }}>{text}</span><CopyOutlined className='icon-copy' onClick={() => handleCopy(text)} />
                </div>
            ,
        },
        {
            title: `${t('projectChunkColumnContent')}`,
            width: 480,
            dataIndex: 'content',
            key: 'content',
            ellipsis: true,
            render: (text: string) => (
                <Tooltip title={text} placement='bottom'><span style={{ maxWidth: '480px', overflow: 'hidden', display: 'inline-block' }}>{text}</span></Tooltip>
            ),
        },
        {
            title: `${t('projectRetrievalColumnStatus')}`,
            dataIndex: 'status',
            key: 'status',
            width: 180,
            render: (text: string) => (
                <Tag color={statusReverse[text]}>
                    {text}
                </Tag>
            )
        },
        {
            title: `${t('chunk')}`,
            dataIndex: 'num_chunks',
            key: 'num_chunks',
            width: 180,
            render: (text: string) => (
                <div>
                    {text}
                </div>
            )
        },
        {
            title: `${t('projectModelColumnCreatedAt')} `,
            width: 180,
            dataIndex: 'created_timestamp',
            key: 'created_timestamp',
            render: (time: number) => <div>{formatTimestamp(time)}</div>
        },
        {
            title: `${t('projectColumnActions')}`,
            key: 'action',
            width: 118,
            fixed: 'right',
            render: (_text: any, record: object) => (
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
    const handleChildEvent = async (value: any) => {
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
        setRecordId('')
        setDrawerTitle(`${t('projectRecordCreateRecord')}`)
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
        setDrawerTitle(`${t('projectRecordEditRecord')}`)
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
            toast.error(`${t('projectChunkContentRequired')}`)
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
            if (!recordId) {
                await createRecord(collectionId, params)
            } else {
                const param1 = {
                    ...params,
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
                    {t('cancel')}
                </Button>,
                <Button key="submit" onClick={() => handleConfirm()} className='next-button' loading={confirmLoading}>
                    {t('confirm')}
                </Button>
            ]} title={drawerTitle} centered className={styles['record-create-model']} open={createOpenModal} width={720} onCancel={handleCancel} closeIcon={<img src={closeIcon} alt="closeIcon" />}>
                <div className={styles['text-content']}>
                    <div className={styles['text-title']}>{t('title')}</div>
                    <div className={styles.desc}>{t('projectRecordTitleDesc')}</div>
                    <Input className={styles['input1']} placeholder='Enter name' value={title} onChange={(e) => setTitle(e.target.value)}></Input>
                    <div className={styles['text-title']}>{t('projectChunkTextContent')}</div>
                    <div className={styles['desc']}>{t('projectRecordContentDesc')}</div>
                    <Input.TextArea placeholder={t('projectRecordEnterDescription')} showCount minLength={0} maxLength={32768} value={contentValue} onChange={handleContentChange} className={styles['input']}></Input.TextArea>
                    <div className={styles.label1}>{t('projectRecordTextSplitter')}</div>
                    <div className={styles['label']}>
                        <span className={styles['span']}>*</span>
                        <span>{t('projectRecordChunkSize')}</span>
                    </div>
                    <div className={styles['label-desc']}>{t('projectRecordChunkSizeDesc')}</div>
                    <InputNumber className={styles['input-number1']} placeholder={t('projectRecordChunkSizePlaceholder')} parser={(value: string | undefined) => (isNaN(Number(value)) ? 1 : parseInt(value as string, 10))} value={chunkSize} onChange={(value: number | null) => setChunkSize(value as number)} min={100} max={500}></InputNumber>
                    <div className={styles['label']}>
                        <span className={styles['span']}>*</span>
                        <span>{t('projectRecordChunkOverlap')}</span>

                    </div>
                    <div className={styles['label-desc']}>{t('projectRecordChunkOverlapDesc')}</div>
                    <InputNumber className={styles['input-number']} placeholder={t('projectRecordChunkOverlapPlaceholder')} value={chunkOverlap} onChange={(value: number | null) => setChunkOverlap(value as number)} parser={(value: string | undefined) => (isNaN(Number(value)) ? 1 : parseInt(value as string, 10))} min={0} max={100}></InputNumber>
                </div>
            </Modal>
            <DeleteModal open={OpenDeleteModal} describe={`${t('deleteItem')} ${t('projectRecord')} ${deleteId}? ${t('projectDeleteChunkDesc')}`} title={t('projectRecordDeleteRecord')} projectName={deleteId} onDeleteCancel={onDeleteCancel} onDeleteConfirm={onDeleteConfirm}></DeleteModal>
        </Spin>
    );
}
export default RecordPage;