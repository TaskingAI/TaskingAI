import { useState, useEffect, useRef } from 'react';
import closeIcon from '../../assets/img/x-close.svg'
import ModalFooterEnd from '../modalFooterEnd/index'
import { RightOutlined, PlusOutlined } from '@ant-design/icons';
import { toast } from 'react-toastify';
import { getModelsList } from '../../axios/models'
import ModelModal from '../modelModal/index'
import {
    Input, Select, Modal, Button
} from 'antd';
import {createCollectionType} from '@/contant/createCollection.ts'
import {  createRetrieval } from '../../axios/retrieval';
import ModalTable from '../modalTable/index';
import styles from './createCollection.module.scss'
import { modelsTableColumn } from '../../contents/index'
import { ChildRefType } from '../../contant/index.ts'
function CreateCollection({ OpenDrawer, handleModalCloseOrOpen, handleFetchData }: createCollectionType) {
    const [drawerName, setDrawerName] = useState('')
    const [descriptionText, setDescriptionText] = useState('')
    const [selectedRows, setSelectedRows] = useState([])
    const [selectValue, setSelectValue] = useState(1000)
    const [modelOne, setModelOne] = useState(false);
    const [recordsSelected, setRecordsSelected] = useState([])
    const [updatePrevButton, setUpdatePrevButton] = useState(false)
    const [defaultSelectedRowKeys, setDefaultSelectedRowKeys] = useState([])
    const [modelHasMore, setModelHasMore] = useState(false)
    const [options, setOptions] = useState([])
    const childRef = useRef<ChildRefType | null>(null);
    useEffect(() => {
        const params = {
            limit: 20,
        }
        fetchModelsList(params)
    }, []);
    const [modalTableOpen, setModalTableOpen] = useState(false)
    const fetchModelsList = async (params) => {
        try {
            const res:any = await getModelsList(params, 'text_embedding')
            const data = res.data.map((item) => {
                return {
                    ...item,
                    key: item.model_id,
                }
            })
            setModelHasMore(res.has_more)
            setOptions(data)
        } catch (error) {
            console.log(error)
        }
    }
    const handleCancel = () => {
        handleModalCloseOrOpen(false)
        setDrawerName('')
        setDescriptionText('')
        setSelectedRows([])
        setSelectValue(1000)
        setRecordsSelected([])
        setDefaultSelectedRowKeys([])
        setUpdatePrevButton(false)
    }
    const handleNameChange = (e) => {
        setDrawerName(e.target.value)
    }
    const handleSelectModelId = () => {
        setModalTableOpen(true)
        setUpdatePrevButton(false)
    }
    const handleSelectValue = (value) => {
        setSelectValue(value)
    }
    const handleRequest = async () => {
        if (!selectedRows  || !selectValue) {
            return toast.error('Missing required parameters')
        }
        try {
            const params = {
                capacity: Number(selectValue),
                embedding_model_id: selectedRows[0].slice(-8),
        
                name: drawerName || '',
                description: descriptionText || '',
                metadata: {}
            }
            await createRetrieval(params)
            handleFetchData()
            setDrawerName('')
            setDescriptionText('')
            setSelectedRows([])
            setSelectValue(1000)
            setRecordsSelected([])
            setDefaultSelectedRowKeys([])
            handleModalCloseOrOpen(false)
            setUpdatePrevButton(true)

        } catch (error) {
            console.log(error)
            toast.error(error.response.data.error.message)
        }
    }
    const handleModalCancel = () => {
        setModelOne(false)
    }
    const handleSetModelConfirmOne = () => {
        setModelOne(false)
        setUpdatePrevButton(true)
    }
    const handleModalClose = () => {
        setModalTableOpen(false)
        setUpdatePrevButton(false)
    }
    const handleRecordsSelected = (value, selectedRows) => {
        setRecordsSelected(value)
        const tag = selectedRows.map(item => (item.name + '-' + item.model_id))
        if (value.length === 0) {
            setSelectedRows([])
        } else {
            setSelectedRows(tag)
        }
    }
    const handleCreateModelId = async () => {
        setModelOne(true)
        childRef.current?.fetchAiModelsList()
    }
    const handleChildModelEvent = async (value) => {
        await fetchModelsList(value)
    }
    return (
        <div>
            <Modal onCancel={handleCancel} className={styles['create-collection']} width={1000} centered closeIcon={<img src={closeIcon} alt="closeIcon" className='img-icon-close' />}  title='Create Collection'  open={OpenDrawer} footer={<ModalFooterEnd handleOk={() => handleRequest()} onCancel={handleCancel} />}>
                <div className={styles['drawer-retrieval']}>
                    <div className={styles['name-prompt']}>
                        Name
                    </div>
                    <Input value={drawerName} onChange={handleNameChange} className={styles['input']}></Input>
                    <div className={styles['desc-prompt']}>
                        Description
                    </div>
                    <div className={styles['label-desc']}>
                        Add a description to the collection you created.
                    </div>
                    <Input.TextArea className={styles['input']}  autoSize={{ minRows: 3, maxRows: 10 }} showCount
                        placeholder='Enter description'
                        value={descriptionText}
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
                        mode="multiple"
                        className={styles['input']}
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
                        options={[
                            {
                                value: '1000',
                                label: '1000 chunks',
                            },
                        ]} />
                </div>
            </Modal>
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
            <ModelModal getOptionsList={fetchModelsList} ref={childRef} open={modelOne} handleSetModelOne={handleModalCancel} modelType='text_embedding' handleSetModelConfirmOne={handleSetModelConfirmOne}></ModelModal>
        </div>

    );
}
export default CreateCollection;