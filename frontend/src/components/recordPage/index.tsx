import { useState, useEffect } from 'react';
import ModalTable from '../modalTable/index.tsx';
import {
    Button,
    Space, Input, Spin, Tooltip, Modal, InputNumber, Select, Upload
} from 'antd';
import type { UploadProps } from 'antd';
import PdfIcon from '../../assets/img/pdfIcon.svg?react'
import TxtIcon from '../../assets/img/txtIcon.svg?react'
import DocsIcon from '../../assets/img/docsIcon.svg?react'
import HtmlIcon from '../../assets/img/htmlIcon.svg?react'
import MdIcon from '../../assets/img/mdIcon.svg?react'
import TextIcon from '../../assets/img/textIcon.svg?react'
import WebIcon from '../../assets/img/webIcon.svg?react'
import LoadingAnim from '../../assets/img/loadingAnim.svg?react'
import ApiErrorResponse from '@/constant/index'
import UploadIcon from '../../assets/img/uploadIcon.svg?react'
import styles from './recordPage.module.scss'
import { toast } from 'react-toastify';
import tooltipTitle from '../../contents/tooltipTitle'
import DeleteModal from '../deleteModal/index.tsx';
import CopyOutlined from '../../assets/img/copyIcon.svg?react'
import { getRecordsList, createRecord, deleteRecord, updateRecord, uploadFile } from '../../axios/record.ts'
import { formatTimestamp } from '@/utils/util'
import DeleteIcon from '../../assets/img/deleteIcon.svg?react'
import CloseIcon from '../../assets/img/x-close.svg?react'
import EditIcon from '../../assets/img/editIcon.svg?react'
import ClipboardJS from 'clipboard';
import { useTranslation } from 'react-i18next';


function RecordPage({ collectionId,fetChData }: { collectionId: string,fetChData:Function }) {
    const { t } = useTranslation(['components/recordPage/index']);
    const { tooltipEditTitle, tooltipDeleteTitle } = tooltipTitle();
    const { Dragger } = Upload;
    const handleCopy = (text: string) => {
        const clipboard = new ClipboardJS('.icon-copy', {
            text: () => text
        });
        clipboard.on('success', function () {
            toast.success(`${t('copiedToClipboard')}`)
            clipboard.destroy()
        });
        clipboard.on('error', function (e) {
            console.log(e);
        });
    }
    const IconReverse = (name: string) => {
        name = name.split('.').pop() as string
        switch (name) {
            case 'pdf':
                return <PdfIcon style={{ marginRight: '4px' }} />
            case 'txt':
                return <TxtIcon style={{ marginRight: '4px' }} />
            case 'docx':
                return <DocsIcon style={{ marginRight: '4px' }} />
            case 'html':
                return <HtmlIcon style={{ marginRight: '4px' }} />
            case 'md':
                return <MdIcon style={{ marginRight: '4px' }} />
            default:
                return <TextIcon />
        }
    }
    const columns = [
        {
            title: t('record'),
            dataIndex: 'title',
            key: 'title',
            width: 240,
            fixed: 'left',
            render: (text: string, record: any) =>
                <div>
                    <p className='table-text' style={{ fontSize: '14px' }}>{text || t('untitled')}</p>
                    <p style={{ display: 'flex', alignItems: 'center', margin: 0, lineHeight: '18px' }}>
                        <span style={{ fontSize: '12px', color: 'var(--color-text-secondary)' }}>{record.record_id}</span><CopyOutlined className='icon-copy' onClick={() => handleCopy(record.record_id)} />

                    </p>
                </div>
        },
        {
            title: `${t('content')}`,
            width: 480,
            dataIndex: 'content',
            key: 'content',
            ellipsis: true,
            render: (text: string, record: any) => (
                record.type === 'text' ? <Tooltip title={text} placement='bottom'><span style={{ maxWidth: '480px', overflow: 'hidden', display: 'flex', alignItems: 'center' }}><TextIcon style={{ marginRight: '4px' }} />{text}</span></Tooltip> : (record.type === 'web' ? <span style={{ maxWidth: '480px', overflow: 'hidden', display: 'flex', alignItems: 'center' }}><WebIcon style={{ marginRight: '4px' }} />{JSON.parse(record.content).url}</span> : <span style={{ maxWidth: '480px', overflow: 'hidden', display: 'flex', alignItems: 'center' }}>{IconReverse(JSON.parse(record.content).file_name)}{JSON.parse(record.content).file_name}</span>)
            ),
        },
        {
            title: `${t('status')}`,
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
            title: `${t('createdAt')} `,
            width: 180,
            dataIndex: 'created_timestamp',
            key: 'created_timestamp',
            render: (time: number) => <div>{formatTimestamp(time)}</div>
        },
        {
            title: `${t('actions')}`,
            key: 'action',
            width: 118,
            fixed: 'right',
            render: (_text: string, record: any) => (
                <Space size="middle">
                    <div onClick={record.type !=='file' ? () => handleEdit(record) : undefined} className={`table-edit-icon ${record.type ==='file' && styles.typeDisabled}`} style={{ height: '34px', width: '34px', padding: '0', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                        <Tooltip placement='bottom' title={record.type !=='file' && tooltipEditTitle} color='#fff' arrow={false} overlayClassName='table-tooltip'>
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
    const [fileId, setFileId] = useState('')
    const [loading, setLoading] = useState(false);
    const [createOpenModal, setCreateOpenModal] = useState(false)
    const [limit, setLimit] = useState(20)
    const [contentValue, setContentValue] = useState('')
    const [recordId, setRecordId] = useState('')
    const [confirmLoading, setConfirmLoading] = useState(false);
    const [OpenDeleteModal, setOpenDeleteModal] = useState(false)
    const [drawerTitle, setDrawerTitle] = useState(t('createRecord'))
    const [deleteId, setDeleteId] = useState('')
    const [chunkSize, setChunkSize] = useState(200)
    const [title, setTitle] = useState('')
    const [chunkOverlap, setChunkOverlap] = useState(10)
    const [type, setType] = useState('text')
    const [fileList, setFileList] = useState<any>([]);
    const [websiteValue, setWebsiteValue] = useState('')
    const [fileLoading, setFileLoading] = useState(false);

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
    const props: UploadProps = {
        name: 'file',
        accept: '.txt,.docx,.pdf,.html,.md',
        multiple: false,
        maxCount: 1,

        onChange(info) {
            setFileLoading(true)
            const { status } = info.file;
            if (status !== 'uploading') {
                setFileList(info.fileList)
            }
            if (status === 'done') {
                setFileList(info.fileList);
                setFileLoading(false)
            } else if (status === 'error') {
                setFileLoading(false)
            }
        },
        onDrop(e) {
            const fileType = ['txt', 'docx', 'pdf', 'html', 'md'];
            const fileExtension = e.dataTransfer.files[0].name.slice(((e.dataTransfer.files[0].name.lastIndexOf(".") - 1) >>> 0) + 2);
            if (!fileType.includes(fileExtension.toLowerCase())) {
                toast.error(t('fileTypeNotAllowed'));
                return false;
            }
        },
        beforeUpload(file) {
            const fileType = ['txt', 'docx', 'pdf', 'html', 'md'];
            const fileExtension = file.name.slice(((file.name.lastIndexOf(".") - 1) >>> 0) + 2);
            if (!fileType.includes(fileExtension.toLowerCase())) {
                toast.error(t('fileTypeNotAllowed'));
                return false;
            }
            return true;
        },
        customRequest: async (file) => {
            const payload = new FormData();
            setFileLoading(true);
            payload.append("module", 'retrieval')
            payload.append("purpose", 'record_file')
            payload.append("file", file.file);
            setFileList([file.file]);
            setFileLoading(true);
            try {
                const res = await uploadFile(payload)
                setFileId(res.data.file_id)
            } catch (error) {
                const apiError = error as ApiErrorResponse
                const message = apiError.response.data.error.message
                setFileList([])
                setFileId('')
                toast.error(message)
            } finally {
                setFileLoading(false);
            }
        },
    };

    const customItem = (file: any) => {
        return (
            <div className="file_container">
                <div className="file_main">
                    <div style={{ display: "flex", gap: "10px", alignItems: "center" }}>
                        {
                            file.name.includes(".pdf")
                                ? <div className='file_icons'><PdfIcon /></div>
                                : file.name.includes(".txt")
                                    ? <div className='file_icons'><TxtIcon /></div>
                                    : file.name.includes(".docx")
                                        ? <div className='file_icons'><DocsIcon /></div>
                                        : file.name.includes(".html")
                                            ? <div className='file_icons'><HtmlIcon /></div>
                                            : file.name.includes(".md")
                                                ? <div className='file_icons'><MdIcon /></div>
                                                : <TextIcon />
                        }



                        <div style={{ display: "flex", flexDirection: "column" }}>
                            <div className="file_name">
                                {file.name.length > 50
                                    ? file.name.slice(0, 6).split(".")[0] +
                                    "... ." +
                                    file.name.split(".")[1]
                                    : file.name}
                            </div>
                            <span className="file_kb">{file?.size ? ((file.size / 1024) > 1024 ? (file.size / 1024 / 1024).toFixed(2) + 'MB' : (file.size / 1024 > 0 ? (file.size / 1024).toFixed(2) + "KB" : file.size + "B")) : 0 + "KB"} {fileLoading && '- uploading...'}</span>
                        </div>
                    </div>
                    <div>
                        {fileLoading ? (
                            <LoadingAnim className='loading-icon' />
                        ) : (
                            <CloseIcon onClick={handleRemoveFileList} />
                        )}
                    </div>
                </div>
            </div>
        );
    };
    const handleRemoveFileList = ()=> {
        setFileList([])
        setFileId('')
    }
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
        setType('text')
        setWebsiteValue('')
        setFileList([])
        setChunkSize(200)
        setChunkOverlap(10)
        setRecordId('')
        setFileId('')
        setDrawerTitle(`${t('createRecord')}`)
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
            fetChData()
        } catch (error) {
            console.log(error)
        }
        setOpenDeleteModal(false)
    }
    const handleEdit = async (record: any) => {
        if (record.type === 'file') {
            return
        }
        setDrawerTitle(`${t('editRecord')}`)
        setRecordId(record.record_id)
        setType(record.type)
        setTitle(record.title)

        setCreateOpenModal(true)
        if (record.type === 'web') {
            setContentValue(JSON.parse(record.content).url)
        } else if (record.type === 'file') {
            setFileId(JSON.parse(record.content).file_id)
            setFileList([{
                name: JSON.parse(record.content).file_name,
                size: JSON.parse(record.content).file_size
            }])
        } else if (record.type === 'text') {
            setContentValue(record.content)
        }
        setChunkSize(Number(localStorage.getItem('chunkSize')))
        setChunkOverlap(Number(localStorage.getItem('chunkOverlap')))
    }
    const handleConfirm = async () => {
        if (type === 'text' && !contentValue) {
            toast.error(`${t('chunkContentRequired')}`)
            return
        }
        if (type === 'web' && websiteValue) {
            const websiteValueRequired = /^https:\/\//.test(websiteValue)
            if (!websiteValueRequired) {
                toast.error(t('mustStartWithHTTPS'))
                return
            }
        }
        if (type === 'web' && !websiteValue) {
            return toast.error(t('urlRequired'))
        }
        if(type === 'file' && fileLoading && fileList.length !== 0) {
            return toast.error(t('fileUploading'))
        }
        if(type === 'file' && fileList.length === 0) {
            return toast.error(t('fileRequired'))
        }
        setConfirmLoading(true)
        try {
            const params = {
                type: type,
                title,
                content: type === 'text' ? contentValue : undefined,
                url: type === 'web' ? websiteValue : undefined,
                file_id: type === 'file' ? fileId : undefined,
                text_splitter: {
                    type: 'token',
                    chunk_size: chunkSize,
                    chunk_overlap: chunkOverlap
                }

            }
            if (!recordId) {
                try {
                    await createRecord(collectionId, params)
                } catch (error) {
                    const apiError = error as ApiErrorResponse
                    const message = apiError.response.data.error.message
                    toast.error(message)
                }
            } else {
                const param1 = {
                    ...params,
                    metadata: {}
                }
                try {
                    await updateRecord(collectionId, recordId, param1)

                } catch (error) {
                    const apiError = error as ApiErrorResponse
                    const message = apiError.response.data.error.message
                    toast.error(message)
                }
            }
            localStorage.setItem('chunkSize', String(chunkSize) || '200')
            localStorage.setItem('chunkOverlap', String(chunkOverlap) || '20')
            const params3 = {
                limit: limit || 20,
            }
            await fetchData(collectionId, params3)
            fetChData()
            setUpdatePrevButton(true)
            setCreateOpenModal(false)
        } catch (e) {
            console.log(e)
        }
    
        setConfirmLoading(false)
    }
    const handleContentChange = (e: any) => {
        setContentValue(e.target.value)
    }
    const handleTypeChange = (value: string) => {

        setType(value)
    }
    const handleWebsiteUrl = (e: any) => {
        setWebsiteValue(e.target.value)
    }
    return (
        <Spin spinning={loading} >
            <ModalTable ifOnlyId={true} title={t('newRecord')} onOpenDrawer={handleCreatePrompt} onChildEvent={handleChildEvent} updatePrevButton={updatePrevButton} dataSource={recordList} ifSelect={false} name="record" columns={columns} hasMore={hasMore} id="record_id"></ModalTable>
            <Modal footer={[
                <Button key="cancel" onClick={handleCancel} className='cancel-button'>
                    {t('cancel')}
                </Button>,
                <Button key="submit" onClick={() => handleConfirm()} className='next-button' loading={confirmLoading}>
                    {t('confirm')}
                </Button>
            ]} title={drawerTitle} centered className={styles['record-create-model']} open={createOpenModal} width={720} onCancel={handleCancel} closeIcon={<CloseIcon className={styles['img-icon-close']} />}>
                <div className={styles['text-content']}>
                    <div className={styles['text-title']}>{t('title')}</div>
                    <div className={styles.desc}>{t('recordDesc')}</div>
                    <Input className={styles['input1']} placeholder={t('enterName')} value={title} onChange={(e) => setTitle(e.target.value)}></Input>
                    <div className={styles['text-title']} style={{ display: 'flex', alignItems: 'center' }}>
                        <span className={styles['red-span']}> * </span> <div >{t('type')}</div>
                    </div>
                    <Select value={type} onChange={handleTypeChange} className={styles['input1']} options={[{ label: t('text'), value: 'text' }, { label: t('website'), value: 'web' }, { label: t('file'), value: 'file' }]}></Select>
                    {type === 'text' && <>
                        <div className={styles['text-title']} style={{ display: 'flex', alignItems: 'center' }}><span className={styles['red-span']}> * </span> {t('textContent')}</div>
                        <div className={styles['desc']}>{t('recordContentDesc')}</div>
                        <Input.TextArea placeholder={t('enterDescription')} showCount minLength={0} maxLength={32768} value={contentValue} onChange={handleContentChange} className={styles['input']}></Input.TextArea>
                    </>}
                    {type === 'web' && <>
                        <div className={styles['text-title']} style={{ display: 'flex', alignItems: 'center' }}>
                            <span className={styles['red-span']}> * </span>  <div >URL</div>
                        </div>

                        <div className={styles['desc']}>{t('shouldStartWithHTTPS')}</div>
                        <Input onChange={handleWebsiteUrl} value={websiteValue} className={styles['urlInput']} placeholder={t('enterWebsiteURL')}></Input>
                    </>}
                    {type === 'file' && (
                        fileList.length ? <div>
                            {fileList.map((item: any, index: number) => (
                                <div key={index}>
                                    {customItem(item)}
                                </div>
                            ))}
                        </div> : (
                            <Dragger {...props}>
                                <p className="ant-upload-drag-icon">
                                    <UploadIcon />
                                </p>
                                <p className="ant-upload-text"><span className={styles['click-to-upload']}>{t('clickToUpload')}</span>{t('orDragAndDrop')}</p>
                                <p className="ant-upload-hint">
                                    {t('allowedFileTypes')}
                                </p>
                            </Dragger>
                        )
                    )}

                    <div className={styles.label1}>{t('textSplitter')}</div>
                    <div className={styles['label']}>
                        <span className={styles['span']}>*</span>
                        <span>{t('chunkSize')}</span>
                    </div>
                    <div className={styles['label-desc']}>{t('chunkSizeDesc')}</div>
                    <InputNumber className={styles['input-number1']} placeholder={t('chunkSizePlaceholder')} parser={(value: string | undefined) => (isNaN(Number(value)) ? 1 : parseInt(value as string, 10))} value={chunkSize} onChange={(value: number | null) => setChunkSize(value as number)} min={100} max={500}></InputNumber>
                    <div className={styles['label']}>
                        <span className={styles['span']}>*</span>
                        <span>{t('chunkOverlap')}</span>

                    </div>
                    <div className={styles['label-desc']}>{t('chunkOverlapDesc')}</div>
                    <InputNumber className={styles['input-number']} placeholder={t('chunkOverlapPlaceholder')} value={chunkOverlap} onChange={(value: number | null) => setChunkOverlap(value as number)} parser={(value: string | undefined) => (isNaN(Number(value)) ? 1 : parseInt(value as string, 10))} min={0} max={100}></InputNumber>
                </div>
            </Modal>
            <DeleteModal open={OpenDeleteModal} describe={`${t('deleteItem',{ deleteValue: `${t('record')} ${deleteId}`})} ${t('deleteChunkDesc')}`} title={t('deleteRecord')} projectName={deleteId} onDeleteCancel={onDeleteCancel} onDeleteConfirm={onDeleteConfirm}></DeleteModal>
        </Spin>
    );
}
export default RecordPage;