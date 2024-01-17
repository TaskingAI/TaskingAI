import { useState, useEffect,useRef } from 'react';
import closeIcon from '../../assets/img/x-close.svg'
import ModalFooterEnd from '../modalFooterEnd/index'
import { RightOutlined,PlusOutlined } from '@ant-design/icons';
import { toast } from 'react-toastify';
import { getModelsList } from '../../axios/models'
import ModelModal from '../modelModal/index'
import {
     Input, Select, InputNumber, Tag, Modal, Button
} from 'antd';
import CopyOutlined from '../../assets/img/copyIcon.svg?react'
import ModelProvider from '../../assets/img/ModelProvider.svg?react'
import { formatTimestamp } from '@/utils/util'
import CohereIcon from '../../assets/img/cohereIcon.svg?react'

import { getRetrievalList,createRetrieval } from '../../axios/retrieval';
import GoogleIcon from '../../assets/img/googleIcon.svg?react'
import Anthropic from '../../assets/img/Anthropic.svg?react'
import Frame from '../../assets/img/Frame.svg?react'
import ModalTable from '../modalTable/index';
import './createCollection.module.scss'
const typeReverse = {
    instruct_completion: 'Instruct Completion',
    chat_completion: 'Chat Completion',
    text_embedding: 'Text Embedding'
}
function CreateCollection({ OpenDrawer,handleModalCloseOrOpen,handleFetchData }) {
    const [drawerName, setDrawerName] = useState('')
    const [descriptionText, setDescriptionText] = useState('')
    const [selectedRows, setSelectedRows] = useState([])
    const [selectValue, setSelectValue] = useState(1000)
    const [chunkOverlap, setChunkOverlap] = useState(10)
    const [chunkSize, setChunkSize] = useState(200)
    const [modelOne, setModelOne] = useState(false);
    const [recordsSelected, setRecordsSelected] = useState([])
    const [updatePrevButton, setUpdatePrevButton] = useState(false)
    const [defaultSelectedRowKeys, setDefaultSelectedRowKeys] = useState([])
    const [modelHasMore, setModelHasMore] = useState(false)
    const [options, setOptions] = useState([])
    const childRef = useRef();
    useEffect(() => {
        const params = {
            limit: 20,
        }
        fetchModelsList(params)

    }, []);
    const [modalTableOpen, setModalTableOpen] = useState(false)
    const imgReverse = (providerId:string) => {
        if (providerId === 'openai') {
            return <ModelProvider width='16px' height='16px' />
        }
        else if (providerId === 'anthropic') {
            return <Anthropic width='16px' height='16px' />
        } else if (providerId === 'azure_openai') {
            return <Frame width='16px' height='16px' />
        } else if (providerId === 'google_gemini') {
            return <GoogleIcon width='16px' height='16px' />
        } else if (providerId === 'cohere') {
            return <CohereIcon width='16px' height='16px' />
        }
    }
    const modelsColumns = [
        {
            title: 'Name',
            dataIndex: 'name',
            key: 'name',
            fixed: 'left',
            width: 240,
            render: (text:string, record:Record<string,any>) =>
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
            dataIndex: 'base_model_id',
            key: 'base_model_id',
            width: 240,
            render: (text:string, record) =>
                <div className='img-text'>
                    {imgReverse(record.provider_id)} <span className='a'>{text}</span>
                </div>
            ,
        },
        {
            title: 'Type',
            dataIndex: 'type',
            key: 'type',
            width: 180,
            render: (_,) => (
                <>

                    <Tag color='green'>
                        {typeReverse[_]}
                    </Tag>
                </>
            ),
        },
        {
            title: 'Properties',
            dataIndex: 'properties',
            key: 'properties',
            width: 360,
            render: (proerties) => (
                <div style={{ display: 'flex' }}>
                    {Object.entries(proerties).map(([key, property]) => (
                        <div className='streamParent' key={key} style={{ display: 'flex', border: '1px solid #e4e4e4', borderRadius: '8px', width: 'auto', padding: '0 4px', marginRight: '12px' }}>
                            <span className='stream' style={{ borderRight: '1px solid #e4e4e4', paddingRight: '2px' }}>{key}</span>
                            <span className='on' style={{ paddingLeft: '2px' }}>{String(property)}</span>
                        </div>
                    )).slice(0, 2)}
                    {Object.entries(proerties).length > 2 && (
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
            render: (time) => <div>{formatTimestamp(time)}</div>
        }
    ]
    const fetchModelsList = async (params) => {

        try {
            const res = await getModelsList(params, 'text_embedding')
            const data = res.data.map((item) => {
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
    const handleCancel = () => {
        handleModalCloseOrOpen(false)
        setDrawerName('')
        setDescriptionText('')
        setSelectedRows([])
        setSelectValue(1000)
        setChunkOverlap(10)
        setChunkSize(200)
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
        if (!selectedRows || !chunkSize || !selectValue) {
            return toast.error('Missing required parameters')
        }
        try {
                const params = {
                    capacity: Number(selectValue),
                    embedding_model_id: selectedRows[0].slice(-8),
                    configs: {
                        chunk_size: Number(chunkSize),
                        chunk_overlap: Number(chunkOverlap)
                    },
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
                setChunkOverlap(10)
                setChunkSize(200)
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
    const handleSetModelConfirmOne = ()=>{
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
        childRef.current.fetchAiModelsList()
    }
    const handleChildModelEvent = async (value) => {
        await fetchModelsList(value)
    }
    return (
        <div>
            <Modal onCancel={handleCancel} className='create-collection' width={1000} centered closeIcon={<img src={closeIcon} alt="closeIcon" className='img-icon-close' />} onClose={handleCancel} title='Create Collection' placement="right" open={OpenDrawer} size='large' footer={<ModalFooterEnd handleOk={() => handleRequest()} onCancel={handleCancel} />}>
                <div className='drawer-retrieval'>
                    <div className='name-prompt'>
                        Name
                    </div>
                    <Input value={drawerName} onChange={handleNameChange} className='input'></Input>
                    <div className='desc-prompt'>
                        Description
                    </div>
                    <div className='label-desc'>
                        Add a description to the collection you created.
                    </div>
                    <Input.TextArea className='input' type="text" autoSize={{ minRows: 3, maxRows: 10 }} showCount
                        placeholder='Enter description'
                        value={descriptionText}
                        onChange={(e) => setDescriptionText(e.target.value)}
                        maxLength={200} />
                         <div className='hr'></div>
                    <div className='label'>
                        <span className='span'>*</span>
                        <span>{`Embedding model`}</span>

                    </div>
                    <div className='label-desc'>Enter a text embedding model ID that is available in your project.</div>
                    <Select
                        placeholder='Select a model'
                        open={false}
                        mode="multiple"
                        className='input'
                        suffixIcon={<RightOutlined />}
                        maxTagCount={2} removeIcon={null}
                        value={selectedRows} onClick={handleSelectModelId}
                    >
             
                    </Select>
                    <div className='hr'></div>

                    <div className='label'>
                        <span className='span'>*</span>
                        <span>{`Capacity`}</span>
                    </div>
                    <div className='label-desc'>
                        {`Capacity refers to the maximum number of chunks the collection can store. Please choose a capacity value that best fits your needs. Note that pricing varies with capacity, and we now only offer free plan in beta.`}
                        {/*<a href="https://tasking.ai/pricing" className='referToThe href' target="_blank" rel="noopener noreferrer">*/}
                        {/*    visit the page for detailed pricing information.*/}
                        {/*</a>*/}
                    </div>
                    <Select
                        placeholder="Choose a capacity"
                        onChange={handleSelectValue}
                        value={selectValue}
                        className='input'
                        options={[
                            {
                                value: '1000',
                                label: '1000 chunks',
                            },
                        ]} />
                </div>
            </Modal>
            <Modal closeIcon={<img src={closeIcon} alt="closeIcon" className='img-icon-close' />} onCancel={handleModalClose} centered footer={[
                <div className='footer-group' key='footer'>
                    <Button key="model" icon={<PlusOutlined />} onClick={handleCreateModelId} className='cancel-button'>
                        New Model
                    </Button>
                    <div>
                        <span className='select-record'>
                            {recordsSelected.length} {recordsSelected.length > 1 ? 'items' : 'item'} selected
                        </span>
                        <Button key="cancel" onClick={handleModalClose} className='cancel-button'>
                            Cancel
                        </Button>
                        <Button key="submit" onClick={handleModalClose} className='next-button'>
                            Confirm
                        </Button>
                    </div>

                </div>

            ]} title='Select Model' open={modalTableOpen} width={1000} className='modal-inner-table'>
                <ModalTable name="model" onOpenDrawer={handleCreateModelId}  updatePrevButton={updatePrevButton} defaultSelectedRowKeys={defaultSelectedRowKeys} handleRecordsSelected={handleRecordsSelected} ifSelect={true} columns={modelsColumns} hasMore={modelHasMore} id='model_id' dataSource={options} onChildEvent={handleChildModelEvent}></ModalTable>
            </Modal>
            <ModelModal getOptionsList={fetchModelsList}  ref={childRef} open={modelOne} handleSetModelOne={handleModalCancel}  modelType='text_embedding' handleSetModelConfirmOne={handleSetModelConfirmOne}></ModelModal>

        </div>

    );
}
export default CreateCollection;