import styles from './retrieval.module.scss'
import { PlusOutlined, RightOutlined } from '@ant-design/icons';
import { getRetrievalList, createRetrieval, deleteRetrieval, updateRetrieval } from '../../axios/retrieval.ts'
import { getModelsList } from '../../axios/models.ts'
import RecordPage from '../recordPage/index';
import { useEffect, useState, useRef } from 'react'
import DeleteIcon from '../../assets/img/deleteIcon.svg?react'
import EditIcon from '../../assets/img/editIcon.svg?react'
import ModalTable from '../modalTable/index';
import ModelModal from '../modelModal/index'
import CustomError from '../../contant/index.ts'
// import {TKNegativeModal} from '@taskingai/taskingai-ui'
import { modelsTableColumn, collectionTableColumn } from '../../contents/index.tsx'
import { ChildRefType } from '../../contant/index.ts'

import ModalFooterEnd from '../modalFooterEnd/index'
import { toast } from 'react-toastify'
import { tooltipEditTitle, tooltipDeleteTitle } from '../../contents/index.tsx'
import { useNavigate } from 'react-router-dom';
import DeleteModal from '../deleteModal/index.tsx'
import RecordIcon from '../../assets/img/recordIcon.svg?react'
import closeIcon from '../../assets/img/x-close.svg'
import {
    Space, Drawer, Input, Tooltip, Spin, Select, Modal, Button
} from 'antd';


function Retrieval() {
    const columns = [...collectionTableColumn]
    columns.push({
        title: 'Actions',
        key: 'action',
        fixed: 'right',
        width: 157,
        render: (_:string, record:object) => (
            <Space size="middle">
                <div className='table-edit-icon' onClick={() => handleRecord(record)}>
                    <RecordIcon />
                </div>
                <div onClick={() => handleEdit(record)} className='table-edit-icon'>
                    <Tooltip placement='bottom' title={tooltipEditTitle} color='#fff' arrow={false} overlayClassName='table-tooltip'>
                        <EditIcon />
                    </Tooltip>
                </div>
                <div onClick={() => handleDelete(record)} className='table-edit-icon'>
                    <Tooltip placement='bottom' title={tooltipDeleteTitle} color='#fff' arrow={false} overlayClassName='table-tooltip'>
                        <DeleteIcon />
                    </Tooltip>
                </div>
            </Space>
        ),
    },)
    const [promptList, setPromptList] = useState([])
    const [hasMore, setHasMore] = useState(false)
    const [modelHasMore, setModelHasMore] = useState(false)
    const [OpenDrawer, setOpenDrawer] = useState(false)
    const [loading, setLoading] = useState(false);
    const [limit, setLimit] = useState(20)
    const [updatePrevButton, setUpdatePrevButton] = useState(false)
    const [updateRetrievalPrevButton, setUpdateRetrievalPrevButton] = useState(false)
    const [defaultSelectedRowKeys, setDefaultSelectedRowKeys] = useState([])
    const [modalTableOpen, setModalTableOpen] = useState(false)
    // const [chunkOverlap, setChunkOverlap] = useState<number>()
    const [OpenDeleteModal, setOpenDeleteModal] = useState(false)
    const [recordOpen, setRecordOpen] = useState(false)
    const [drawerTitle, setDrawerTitle] = useState('Create Collection')
    const [drawerName, setDrawerName] = useState('')
    const [embeddingSize, setEmbeddingSize] = useState(0)
    const [deleteValue, setDeleteValue] = useState('')
    const [recordsSelected, setRecordsSelected] = useState([])
    const [selectedRows, setSelectedRows] = useState<string[]>([])
    // const [modelId, setModelId] = useState(undefined)
    const [options, setOptions] = useState([])
    const childRef = useRef<ChildRefType | null>(null);
    const [selectValue, setSelectValue] = useState(1000)
    const [modelOne, setModelOne] = useState(false);
    const [descriptionText, setDescriptionText] = useState('')
    const [editDisabled, setEditDisabled] = useState(false)
    const [collectionId, setCollectionId] = useState('')
    const [collectionRecordId, setCollectionRecordId] = useState('')
    const navigate = useNavigate()
    useEffect(() => {
        const params = {
            limit: 20
        }
        fetchData(params);
        fetchModelsList(params)
    }, []);
    const handleRecordsSelected = (value:any, selectedRows:Array<any>) => {
        setRecordsSelected(value)
        const tag = selectedRows.map(item => (item.name + '-' + item.model_id))
        if (value.length === 0) {
            setSelectedRows([])
        } else {
            setSelectedRows(tag)
        }
    }
    const handleModalClose = () => {
        setModalTableOpen(false)
        setUpdatePrevButton(false)
    }
    const fetchData = async (params:Record<string,string | number>) => {
        setLoading(true);
        try {
            const res:any = await getRetrievalList(params)
            const data = res.data.map((item:any) => {
                return {
                    ...item,
                    capacity1: item.num_chunks + '/' + item.capacity,
                    key: item.collection_id,
                }
            })
            setPromptList(data);
            setHasMore(res.has_more)

        } catch (error) {
            console.log(error)
        }
        setLoading(false);
    };
    const fetchModelsList = async (params:Record<string, any>) => {

        try {
            const res = await getModelsList(params, 'text_embedding')
            const data = res.data.map((item:any) => {
                return {
                    ...item,
                    key: item.model_id,
                }
            })
            setModelHasMore(data.hasMore)
            setOptions(data)
        } catch (error) {
            console.log(error)
        }
    }
    const handleCreatePrompt = () => {
        setDrawerTitle('Create Collection')
        setDrawerName('')
        setCollectionId('')
        setRecordsSelected([])
        setDefaultSelectedRowKeys([])
        setDescriptionText('')
        // setChunkOverlap(10)
        setSelectedRows([])
        setSelectValue(1000)
        // setModelId(undefined)
        setEmbeddingSize(0)
        setOpenDrawer(true)
        setEditDisabled(false)
        setUpdatePrevButton(false)
    }
    const handleRecord = (val:any) => {
        setCollectionRecordId(val.collection_id)
        navigate(`/project/collections/${val.collection_id}/records`)
        setDrawerName(val.name || 'Untitled Collection')
        setRecordOpen(true)
    }
    const handleEdit = (val:any) => {
        setDrawerTitle('Edit Collection')
        setDrawerName(val.name)
        setEditDisabled(true)
        setSelectedRows(val.embedding_model_id ? [val.name + '-' + val.embedding_model_id] : [])
        setDescriptionText(val.description)
        setCollectionId(val.collection_id)
        setEmbeddingSize(val.embedding_size)
        setSelectValue(val.capacity)
        // setModelId(val.embedding_model_id)
        setOpenDrawer(true)
        setUpdatePrevButton(false)
    }

    const handleDelete = (val:any) => {
        setOpenDeleteModal(true)
        setDeleteValue(val.name)
        setUpdatePrevButton(false)
        setCollectionId(val.collection_id)
    }
    const onDeleteCancel = () => {
        setOpenDeleteModal(false)
        setUpdatePrevButton(false)
    }
    const handleRecordCancel = () => {
        setRecordOpen(false)
        setUpdatePrevButton(false)
        navigate(`/project/collections`)
    }
    const onDeleteConfirm = async () => {
        try {
            const params = {
                limit: limit || 20
            }
            await deleteRetrieval(collectionId)
            await fetchData(params)
            setOpenDeleteModal(false)
            setUpdateRetrievalPrevButton(true)

        } catch (error) {
            if (error instanceof CustomError) {
                toast.error(error.response.data.error.message)
            }
        }
    }

    const handleRequest = async () => {

        if (!selectedRows  || !selectValue) {
            return toast.error('Missing required parameters')
        }
        // if (modelId.length !== 8) {
        //     return toast.error('Model ID must be 8 characters')
        // }

        try {

            if (collectionId) {
                const params = {
                    name: drawerName || '',
                    description: descriptionText || ''
                }
                await updateRetrieval(collectionId, params)
            } else {
                const params = {
                    capacity: Number(selectValue),
                    embedding_model_id: selectedRows[0].slice(-8),
      
                    name: drawerName || '',
                    description: descriptionText || '',
                    embedding_size: embeddingSize || undefined,
                    metadata: {}
                }
                await createRetrieval(params)
            }
            const params1 = {
                limit: limit || 20
            }
            await fetchData(params1)
            setOpenDrawer(false)
            setUpdateRetrievalPrevButton(true)

        } catch (error) {
            if (error instanceof CustomError) {
                toast.error(error.response.data.error.message)
            }
        }
    }
    const handleNameChange = (e:React.ChangeEvent<HTMLInputElement>) => {
        setDrawerName(e.target.value)
    }
    const handleCancel = () => {
        setOpenDrawer(false)
        setUpdatePrevButton(false)
    }
    const handleModalCancel = () => {
        setModelOne(false)
    }
    const handleSetModelConfirmOne = () => {
        setModelOne(false)
        setUpdatePrevButton(true)
    }
    const handleCreateModelId = async () => {
        await setModelOne(true)
        childRef.current?.fetchAiModelsList()
    }
    const handleChildModelEvent = async (value:Record<string,any>) => {
        await fetchModelsList(value)
    }
    const handleSelectValue = (value:number) => {
        setSelectValue(value)
    }
    const handleSelectModelId = () => {
        if (editDisabled) {
            return
        }
        setModalTableOpen(true)
        setUpdatePrevButton(false)
        // if (value) {
        //     setModelId(value)
        // }
    }

    const handleChildEvent = async (value:any) => {
        setLimit(value.limit)
        setUpdateRetrievalPrevButton(false)
        await fetchData(value);
    }
    return (

        <div className={styles["retrieval"]}>
            <Spin spinning={loading} wrapperClassName={styles.spinloading}>
                <ModalTable updatePrevButton={updateRetrievalPrevButton} onChildEvent={handleChildEvent} name="collection" hasMore={hasMore} id='collection_id' columns={columns} ifSelect={false} onOpenDrawer={handleCreatePrompt} dataSource={promptList} />
            </Spin>
            <Drawer className={styles['drawer-retrievals']} closeIcon={<img src={closeIcon} alt="closeIcon" className={styles['img-icon-close']} />} onClose={handleCancel} title={drawerTitle} placement="right" open={OpenDrawer} size='large' footer={<ModalFooterEnd handleOk={() => handleRequest()} onCancel={handleCancel} />}>
                <div className={styles['drawer-retrieval']}>
                    <div className={styles['name-prompt']}>
                        Name
                    </div>
                    <Input className={styles['input']} value={drawerName} onChange={handleNameChange}></Input>
                    <div className={styles['desc-prompt']}>
                        Description
                    </div>
                    <div className={styles['label-desc']}>
                        Add a description to the collection you created.
                    </div>
                    <Input.TextArea autoSize={{ minRows: 3, maxRows: 10 }} showCount
                        placeholder='Enter description'
                        value={descriptionText}
                        className={styles['input']}
                        onChange={(e) => setDescriptionText(e.target.value)}
                        maxLength={200} />
                    <div className={styles['hr']}></div>
                    <div className={styles['label']}>
                        <span className={styles['span']}>*</span>
                        <span>{`Embedding model`}</span>

                    </div>
                    <div className={styles['label-desc']}>Enter a text embedding model ID that is available in your project.</div>
                    <Select
                        placeholder='Select a model'
                        open={false}
                        className={styles['input']}
                        mode="multiple"
                        disabled={editDisabled}
                        suffixIcon={<RightOutlined />}
                        maxTagCount={2} removeIcon={null}
                        value={selectedRows} onClick={handleSelectModelId}
                    >

                    </Select>
                    <div className={styles['hr']}></div>

                    <div className={styles['label']}>
                        <span className={styles['span']}>*</span>
                        <span>{`Capacity`}</span>
                    </div>
                    <div className={styles['label-desc']}>
                        {`Capacity refers to the maximum number of chunks the collection can store. Please choose a capacity value that best fits your needs. Note that pricing varies with capacity, and we now only offer free plan in beta.`}

                    </div>

                    <Select
                        placeholder="Choose a capacity"
                        onChange={handleSelectValue}
                        value={selectValue}
                        className={styles['input']}
                        disabled={editDisabled}
                        options={[
                            {
                                value: '1000',
                                label: '1000 chunks',
                            },
                        ]} />
                </div>
            </Drawer>
            <ModelModal ref={childRef} open={modelOne} handleSetModelOne={handleModalCancel} getOptionsList={fetchModelsList} modelType='text_embedding' handleSetModelConfirmOne={handleSetModelConfirmOne}></ModelModal>
            <Modal closeIcon={<img src={closeIcon} alt="closeIcon" className={styles['img-icon-close']} />} onCancel={handleModalClose} centered footer={[
                <div className='footer-group' key='footer'>
                    <Button key="model" icon={<PlusOutlined />} onClick={handleCreateModelId} className='cancel-button'>
                        New Model
                    </Button>
                    <div>
                        <span className='select-record'>
                            {recordsSelected.length} {recordsSelected.length > 1 ? 'items' : 'item'} selected
                        </span>
                        <Button key="cancel" onClick={handleModalClose} className={`cancel-button ${styles.cancelButton}`}>
                            Cancel
                        </Button>
                        <Button key="submit" onClick={handleModalClose} className='next-button'>
                            Confirm
                        </Button>
                    </div>
                </div>

            ]} title='Select Model' open={modalTableOpen} width={1000} className={`modal-inner-table ${styles['retrieval-model']}`}>
                <ModalTable name="model" onOpenDrawer={handleCreateModelId} updatePrevButton={updatePrevButton} defaultSelectedRowKeys={defaultSelectedRowKeys} handleRecordsSelected={handleRecordsSelected} ifSelect={true} columns={modelsTableColumn} hasMore={modelHasMore} id='model_id' dataSource={options} onChildEvent={handleChildModelEvent}></ModalTable>
            </Modal>
            {/* <TKNegativeModal open={OpenDeleteModal} objectClassName="Collection" objectName={deleteValue} description="This action cannot be undone and all retrieval integrations associated with the collection will be affected."></TKNegativeModal> */}
            <DeleteModal describe={`Are you sure you want to delete ${deleteValue || 'Untitled Collection'}? This action cannot be undone and all retrieval integrations associated with the collection will be affected.`} open={OpenDeleteModal} title='Delete Collection' projectName={deleteValue || 'Untitled Collection'} onDeleteCancel={onDeleteCancel} onDeleteConfirm={onDeleteConfirm} />
            <Drawer className={styles['drawer-inner-table']} closeIcon={<img src={closeIcon} alt="closeIcon" className={styles['img-icon-close']} />} onClose={handleRecordCancel} placement="right" size='large' open={recordOpen} width={1000} title={`${drawerName} / Records`}>
                <RecordPage collectionId={collectionRecordId} ></RecordPage>
            </Drawer>
        </div>)
}
export default Retrieval