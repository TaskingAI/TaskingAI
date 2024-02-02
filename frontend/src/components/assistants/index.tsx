import styles from './assistants.module.scss'
import { PlusOutlined } from '@ant-design/icons';
import { getAssistantsList, createAssistant, deleteAssistant, updateAssistant } from '../../axios/assistant.ts'
import { getModelsList } from '../../axios/models.ts'
import { useEffect, useState, useRef } from 'react'
import ModelModal from '../modelModal/index'
import ModalTable from '../modalTable/index'
import { tooltipEditTitle, tooltipDeleteTitle, tooltipPlaygroundTitle } from '../../contents/index'
import CreateCollection from '../createCollection/index.tsx';
import { getActionsList, createActions } from '../../axios/actions.ts'
import EditIcon from '../../assets/img/editIcon.svg?react'
import DeleteIcon from '../../assets/img/deleteIcon.svg?react'
import JumpIcon from '../../assets/img/assistantJumpIcon.svg?react'
import ModalFooterEnd from '../modalFooterEnd/index'
import { getFirstMethodAndEndpoint } from '@/utils/util'
import { toast } from 'react-toastify'
import DeleteModal from '../deleteModal/index.tsx'
import DrawerAssistant from '../drawerAssistant/index'
import closeIcon from '../../assets/img/x-close.svg'
import { useNavigate } from 'react-router-dom';
import { ChildRefType } from '../../contant/index.ts'

import { assistantTableColumn, modelsTableColumn, actionsTableColumn, collectionTableColumn } from '../../contents/index'
import {
    Button,
    Space, Radio, Drawer, Input, Spin, Modal, Tooltip
} from 'antd';
import { getRetrievalList } from '../../axios/retrieval.ts';
const titleCase = (str) => {
    const newStr = str.slice(0, 1).toUpperCase() + str.slice(1).toLowerCase();
    return newStr;
}
function Assistant() {
    const columns = [...assistantTableColumn]
    columns.push(
        {
            title: 'Actions',
            key: 'action',
            width: 157,
            fixed: 'right',
            render: (_, record) => (
                <Space size="middle">
                    <div onClick={() => handleJump(record)} className='table-edit-icon'>
                        <Tooltip placement='bottom' title={tooltipPlaygroundTitle} color='#fff' arrow={false} overlayClassName='table-tooltip'>
                            <JumpIcon />
                        </Tooltip>

                    </div>

                    <div onClick={() => handleEdit(record)} className='table-edit-icon'>
                        <Tooltip placement='bottom' title={tooltipEditTitle} color='#fff' arrow={false} overlayClassName='table-tooltip'>
                            <EditIcon />
                        </Tooltip>
                    </div>
                    <div onClick={() => handleDelete(record)} className='table-edit-icon' >
                        <Tooltip placement='bottom' title={tooltipDeleteTitle} color='#fff' arrow={false} overlayClassName='table-tooltip'>
                            <DeleteIcon />
                        </Tooltip>
                    </div>
                </Space>
            ),
        },
    );
    const [assistantsList, setAssistantsList] = useState([])
    const [OpenDrawer, setOpenDrawer] = useState(false)
    const [loading, setLoading] = useState(false);
    const [Authentication, setAuthentication] = useState('')
    const [modalActionTableOpen, setModalActionTableOpen] = useState(false)
    const [radioValue, setRadioValue] = useState('none')
    const [recordsSelected, setRecordsSelected] = useState([])
    const [recordsSelected1, setRecordsSelected1] = useState([])
    const [selectedRows, setSelectedRows] = useState([])
    const [selectedRetrievalRows, setSelectedRetrievalRows] = useState([])
    const [options, setOptions] = useState([])
    const [limit, setLimit] = useState(20)
    const [modelLimit, setModelLimit] = useState(20)
    const [retrievalLimit, setRetrievalLimit] = useState(20)
    const [actionLimit, setActionLimit] = useState(20)
    const [updatePrevButton, setUpdatePrevButton] = useState(false)
    const [updateModelPrevButton, setUpdateModelPrevButton] = useState(false)
    const [updateRetrievalPrevButton, setUpdateRetrievalPrevButton] = useState(false)
    const [updateActionPrevButton, setUpdateActionPrevButton] = useState(false)
    const [selectedActionsRows, setSelectedActionsRows] = useState([])
    const [OpenDeleteModal, setOpenDeleteModal] = useState(false)
    const [drawerTitle, setDrawerTitle] = useState('Create Assistant')
    const [drawerName, setDrawerName] = useState('')
    const [hasActionMore, setHasActionMore] = useState(false)

    const [deleteValue, setDeleteValue] = useState('')
    const [drawerDesc, setDrawerDesc] = useState('')
    const [openModalTable, setOpenModalTable] = useState(false)
    const [modalTableOpen, setModalTableOpen] = useState(false)
    const [memoryValue, setMemoryValue] = useState('zero')
    const [OpenActionDrawer, setOpenActionDrawer] = useState(false)
    const [actionList, setActionList] = useState([])
    const childRef = useRef<ChildRefType | null>(null);
    const [hasModelMore, setHasModelMore] = useState(false)
    const [custom, setCustom] = useState('')
    const [assistantId, setAssistantId] = useState('')
    const [tipSchema, setTipSchema] = useState(false)
    const [retrievalList, setRetrievalList] = useState([])
    const [schema, setSchema] = useState('')
    const [hasMore, setHasMore] = useState(false)
    const [assistantHasMore, setAssistantHasMore] = useState(false)
    const [modelOne, setModelOne] = useState(false);
    const [systemPromptTemplate, setSystemPromptTemplate] = useState(['']);

    const [inputValueOne, setInputValueOne] = useState(20)
    const [openCollectionDrawer, setOpenCollectionDrawer] = useState(false)
    const [inputValueTwo, setInputValueTwo] = useState(2000)
    const navigate = useNavigate()
    useEffect(() => {
        fetchModelsList()
        const params = {
            limit: 20,
        }
        fetchData(params);
        fetchActionsList(params)
        fetchDataRetrievalData(params)
    }, []);
    const handleChildActionEvent = async (value) => {
        setUpdateActionPrevButton(false)
        setActionLimit(value.limit)
        await fetchActionsList(value)
    }
    const fetchData = async (params) => {
        setLoading(true);
        try {
            const res: any = await getAssistantsList(params)
            const data = res.data.map((item) => {
                return {
                    ...item,
                    key: item.assistant_id,
                    promptTemplate: item.system_prompt_template.join(' '),
                    memory: item.memory.type,
                    max_messages: item.memory.max_messages,
                    max_tokens: item.memory.max_tokens,
                }
            })
            setAssistantsList(data);
            setAssistantHasMore(res.has_more)

        } catch (error) {
            console.log(error)
        }
        setLoading(false);
    };
    const handleJump = (value) => {
        navigate(`/project/playground?assistant_id=${value.assistant_id}`)
    }
    const handleModalClose = () => {
        setModalTableOpen(false)
    }

    const handleSchemaChange = (e) => {
        setSchema(e.target.value)
        if (!e.target.value) {
            setTipSchema(true)
        } else {
            setTipSchema(false)
        }
    }
    const handleActionRequest = async () => {
        if (!schema) {
            setTipSchema(true)
            return
        }
        setTipSchema(false)
        const commonData = {
            openapi_schema: JSON.parse(schema),
            authentication: {
                type: radioValue,
                content: undefined,
                secret: undefined
            }
        };
        if (radioValue === 'custom') {
            commonData.authentication.content = { [custom]: Authentication };
        } else {
            if (radioValue === 'none') {
                commonData.authentication = undefined
            } else {
                commonData.authentication.secret = Authentication;
            }
        }
        try {

            await createActions(commonData);
            const params = {
                limit: actionLimit || 20,
            }
            setUpdateActionPrevButton(true)
            await fetchActionsList(params);
        } catch (error) {
            console.error(error);
            toast.error(error.response.data.error.message)
        }
        setOpenActionDrawer(false)
    }
    const fetchDataRetrievalData = async (params) => {
        try {
            const res: any = await getRetrievalList(params)
            const data = res.data.map((item) => {
                return {
                    ...item,
                    capacity1: item.num_chunks + '/' + item.capacity,
                    key: item.collection_id
                }
            })
            setRetrievalList(data);
            setHasMore(res.has_more)
            setUpdateRetrievalPrevButton(true)
        } catch (e) {
            console.log(e)
        }
    }

    const handleInputPromptChange = (index, newValue) => {
        setSystemPromptTemplate((prevValues) =>
            prevValues.map((item, i) =>
                i === index ? newValue : item
            )
        );
    }
    const handleModalCancel = () => {
        setModelOne(false)
    }
    const handleSetModelConfirmOne = () => {
        setModelOne(false)
        setUpdateModelPrevButton(true)
    }
    const fetchActionsList = async (params) => {
        try {
            const res: any = await getActionsList(params)
            const data = res.data.map((item) => {
                return {
                    ...item,
                    key: item.action_id,
                    method: getFirstMethodAndEndpoint(item.openapi_schema)?.method,
                    endpoint: getFirstMethodAndEndpoint(item.openapi_schema)?.endpoint
                }
            })

            setActionList(data)
            setHasActionMore(res.has_more)
        } catch (error) {
            console.log(error)
        }
    }
    const handleCreateModelId = async () => {
        // e.stopPropagation()
        await setModelOne(true)
        childRef.current?.fetchAiModelsList()
        await fetchModelsList()
        setOptions(prevOptions => [...prevOptions]);
    }
    const handleCreatePrompt = () => {
        setDrawerTitle('Create Assistant')
        // setInputValues([])
        setSystemPromptTemplate([''])
        setDrawerName('')
        setSelectedRows([])
        setSelectedActionsRows([])
        setSelectedRetrievalRows([])
        setMemoryValue('zero')
        setSelectedRetrievalRows(undefined)

        setDrawerDesc('')
        setOpenDrawer(true)
    }
    const handleEdit = (val) => {
        setDrawerTitle('Edit Assistant')
        const tag = val.retrievals.map(item => item.id)
        setSelectedRetrievalRows(tag)
        setSelectedActionsRows(val.tools.map(item => item.id))
        setDrawerName(val.name)
        setDrawerDesc(val.description)
        setInputValueOne(val.max_messages)
        setInputValueTwo(val.max_tokens)
        setMemoryValue(val.memory)
        setAssistantId(val.assistant_id)
        setSystemPromptTemplate(val.system_prompt_template)
        setSelectedRows([val.model_id])
        setOpenDrawer(true)
    }

    const handleDelete = (val) => {
        setOpenDeleteModal(true)
        setDeleteValue(val.name)
        setAssistantId(val.assistant_id)
    }
    const onDeleteCancel = () => {
        setOpenDeleteModal(false)
    }

    const onDeleteConfirm = async () => {
        const params = {
            limit: limit || 20,
        }
        setUpdatePrevButton(true)

        try {
            await deleteAssistant(assistantId)
            await fetchData(params)
            setOpenDeleteModal(false)

        } catch (error) {
            console.log(error)
            toast.error(error.response.data.error.message)
        }
    }
    const handleMemoryChange1 = (value) => {
        setMemoryValue(value)
    }
    const handleRequest = async () => {
        const inputValueMap = selectedRetrievalRows?.map(item => {
            const id = item.substr(item.indexOf('-') + 1, item.length)
            return {
                type: 'collection', id
            }
        })
        const inputPluginValues = selectedActionsRows?.map(item => {
            const id = item.substr(item.indexOf('-') + 1, item.length)
            return {
                type: 'action', id
            }
        })
        let systemTemplate;
        if (systemPromptTemplate.length === 1 && systemPromptTemplate[0] === '') {
            systemTemplate = []
        } else {
            systemTemplate = systemPromptTemplate
        }
        if (selectedRows.length === 0) {
            return toast.error('Please select a model')
        }
        const params = {
            model_id: selectedRows[0].slice(-8),
            name: drawerName || '',
            description: drawerDesc || '',
            system_prompt_template: systemTemplate,
            tools: inputPluginValues,
            retrievals: inputValueMap,
            memory: {
                type: memoryValue,
                max_messages: Number(inputValueOne) || undefined,
                max_tokens: Number(inputValueTwo) || undefined
            }
        }
        let count = 0

        systemPromptTemplate.forEach(item => {
            const length = item.length
            count += length
        })
        if (count > 16384) {
            return toast.error('System prompt template cannot exceed 16384 characters')
        }
        if (selectedRows[0].slice(-8).length !== 8) {
            return toast.error('Model ID must be 8 characters')
        }
        try {
            if (drawerTitle === 'Edit Assistant') {
                await updateAssistant(assistantId, params)
                setOpenDrawer(false)
            } else {
                await createAssistant(params)
                setOpenDrawer(false)
            }
            const params1 = {
                limit: limit || 20,
            }
            await fetchData(params1)
            setUpdatePrevButton(true)
        } catch (error) {
            console.log(error)
            toast.error(error.response.data.error.message)
        }

    }

    const fetchModelsList = async (value?: any) => {
        const params = {
            limit: modelLimit || 20,
            ...value
        }
        try {
            const res: any = await getModelsList(params, 'chat_completion')
            const data = res.data.map((item) => {
                return {
                    ...item,
                    key: item.model_id
                }
            })
            setOptions(data)
            setHasModelMore(res.has_more)
        } catch (error) {
            console.log(error)
        }
    }
    const handleCancel = () => {
        setOpenDrawer(false)
    }

    const handleCloseModal = () => {
        setOpenModalTable(false)
    }
    const handleChildEvent = async (value) => {
        setLimit(value.limit)
        setUpdatePrevButton(false)
        await fetchData(value);
    }
    const handleCreateConfrim = () => {
        setOpenModalTable(false)
    }

    const handleDeletePromptInput = (index) => {
        const updatedInputValues = [...systemPromptTemplate];
        updatedInputValues.splice(index, 1);
        setSystemPromptTemplate(updatedInputValues);
    }
    const handleNewModal = () => {
        setOpenCollectionDrawer(true)

    }
    const hangleChangeAuthorization = (e) => {
        setAuthentication(e.target.value)
    }

    const handleAddPrompt = () => {
        if (systemPromptTemplate.length < 10) {
            setSystemPromptTemplate((prevValues => [...prevValues, '']))
        }
    }

    const handleModalTable = (value) => {
        setOpenModalTable(value)
    }
    const hangleFilterData = (value) => {
        setRetrievalList(value)
    }
    const handleSelectModelId = (value) => {
        setModalTableOpen(value)
        // if (value) {
        //     setModelId(value)
        // }
    }

    const handleChildRetrievalEvent = async (value) => {
        setRetrievalLimit(value.limit)
        await fetchDataRetrievalData(value)
        setUpdateRetrievalPrevButton(false)
    }
    const handleChildModelEvent = async (value) => {
        setModelLimit(value.limit)
        setUpdateModelPrevButton(false)
        await fetchModelsList(value)
    }
    const handleActionModalClose = () => {
        setModalActionTableOpen(false)
    }

    const handleChangeName = (value) => {
        setDrawerName(value)
    }
    const handleInputValueOne = (value) => {
        setInputValueOne(value)
    }
    const handleInputValueTwo = (value) => {
        setInputValueTwo(value)
    }
    const handleDescriptionChange = (value) => {
        setDrawerDesc(value)
    }
    const handleCreateAction = () => {
        setSchema('')
        setRadioValue('none')
        setAuthentication('')
        setOpenActionDrawer(true)
    }
    const handleActionModalTable = (value) => {
        setModalActionTableOpen(value)
    }
    const onRadioChange = (e) => {
        setRadioValue(e.target.value)
    }
    const handleActionCancel = () => {
        setOpenActionDrawer(false)
    }
    const handleRecordsSelected = (value, selectedRows) => {
        setRecordsSelected(value)
        const tag = selectedRows.map(item => (item.name + '-' + item.model_id))
        setSelectedRows(tag)
    }

    const handleRecordsActionSelected = (value, selectedRows) => {
        setRecordsSelected(value)
        const tag = selectedRows.map(item => (item.name + '-' + item.action_id))
        setSelectedActionsRows(tag)
    }
    const hangleFilterActionData = (value) => {
        setActionList(value)
    }
    const handleCustom = (e) => {
        setCustom(e.target.value)
    }
    const handleCollectionSelected = (value, selectedRows) => {
        setRecordsSelected1(value)
        const tag = selectedRows.map(item => (item.name + '-' + item.collection_id))
        setSelectedRetrievalRows(tag)
    }

    return (
        <div className={styles["assistants"]}>

            <Spin spinning={loading} wrapperClassName={styles.spinloading}>
                <ModalTable updatePrevButton={updatePrevButton} hasMore={assistantHasMore} id="assistant_id" ifSelect={false} columns={columns} name="assistant" dataSource={assistantsList} onChildEvent={handleChildEvent} onOpenDrawer={handleCreatePrompt} />
            </Spin>
            <Drawer
                className={styles['drawer-assistants']}
                closeIcon={<img src={closeIcon} alt="closeIcon" className={styles['img-icon-close']} />}
                onClose={handleCancel} title={drawerTitle} placement="right" open={OpenDrawer} size='large' footer={<ModalFooterEnd handleOk={() => handleRequest()} onCancel={handleCancel} />}>
                <DrawerAssistant selectedActionsRows={selectedActionsRows} inputValue1={inputValueOne} inputValue2={inputValueTwo} handleMemoryChange1={handleMemoryChange1} memoryValue={memoryValue} handleAddPromptInput={handleAddPrompt} handleActionModalTable={handleActionModalTable} drawerName={drawerName} systemPromptTemplate={systemPromptTemplate} handleDeletePromptInput={handleDeletePromptInput} handleInputPromptChange={handleInputPromptChange} handleInputValueOne={handleInputValueOne} handleInputValueTwo={handleInputValueTwo} selectedRows={selectedRows} handleSelectModelId={handleSelectModelId} handleChangeName={handleChangeName} drawerDesc={drawerDesc} handleDescriptionChange={handleDescriptionChange} handleModalTable={handleModalTable} selectedRetrievalRows={selectedRetrievalRows}></DrawerAssistant>
            </Drawer>
            <Modal closeIcon={<img src={closeIcon} alt="closeIcon" className={styles['img-icon-close']} />} centered footer={[
                <div className='footer-group' style={{ display: 'flex', justifyContent: 'space-between' }} key='footer2'>
                    <Button key="model" icon={<PlusOutlined />} onClick={handleNewModal} className='cancel-button'>
                        New Collection
                    </Button>
                    <div>
                        <span className='select-record'>
                            {recordsSelected1.length}  {recordsSelected1.length > 1 ? 'items' : 'item'} selected
                        </span>
                        <Button key="cancel" onClick={handleCloseModal} className={`cancel-button ${styles.cancelButton}`}>
                            Cancel
                        </Button>
                        <Button key="submit" onClick={handleCreateConfrim} className='next-button'>
                            Confirm
                        </Button>
                    </div>

                </div>
            ]} title='Select Collection' open={openModalTable} width={1000} onCancel={handleCloseModal} className={`modal-inner-table ${styles['retrieval-model']}`}>
                <ModalTable onOpenDrawer={handleNewModal} name='Collection' updatePrevButton={updateRetrievalPrevButton} defaultSelectedRowKeys={selectedRetrievalRows} hangleFilterData={hangleFilterData} mode='multiple' handleRecordsSelected={handleCollectionSelected} ifSelect={true} columns={collectionTableColumn} dataSource={retrievalList} hasMore={hasMore} id='collection_id' onChildEvent={handleChildRetrievalEvent} />
            </Modal>

            <ModelModal ref={childRef} open={modelOne} handleSetModelConfirmOne={handleSetModelConfirmOne} handleSetModelOne={handleModalCancel} getOptionsList={fetchModelsList} modelType='chat_completion'></ModelModal>
            <Modal closeIcon={<img src={closeIcon} alt="closeIcon" className={styles['img-icon-close']} />} centered onCancel={handleModalClose} footer={[
                <div className='footer-group' key='footer1'>
                    <Button key="model" icon={<PlusOutlined />} onClick={handleCreateModelId} className='cancel-button'>
                        New Model
                    </Button>
                    <div>
                        <span className='select-record'>
                            {recordsSelected.length}  {recordsSelected.length > 1 ? 'items' : 'item'} selected
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
                <ModalTable onOpenDrawer={handleCreateModelId} name="model" updatePrevButton={updateModelPrevButton} defaultSelectedRowKeys={selectedRows} handleRecordsSelected={handleRecordsSelected} ifSelect={true} columns={modelsTableColumn} hasMore={hasModelMore} id='model_id' dataSource={options} onChildEvent={handleChildModelEvent}></ModalTable>
            </Modal>

            <Modal closeIcon={<img src={closeIcon} alt="closeIcon" className={styles['img-icon-close']} />} centered footer={[
                <div className='footer-group' key='footer3'>
                    <Button key="model" icon={<PlusOutlined />} onClick={handleCreateAction} className='cancel-button'>
                        New Action
                    </Button>
                    <div>
                        <span className='select-record'>
                            {recordsSelected.length}  {recordsSelected.length > 1 ? 'items' : 'item'} selected
                        </span>
                        <Button key="cancel" onClick={handleActionModalClose} className={`cancel-button ${styles.cancelButton}`}>
                            Cancel
                        </Button>
                        <Button key="submit" onClick={handleActionModalClose} className='next-button'>
                            Confirm
                        </Button>
                    </div>

                </div>

            ]} title='Select Action' open={modalActionTableOpen} width={1000} className={`modal-inner-table ${styles['retrieval-model']}`} onCancel={handleActionModalClose}>
                <ModalTable onOpenDrawer={handleCreateAction} name="Action" updatePrevButton={updateActionPrevButton} defaultSelectedRowKeys={selectedActionsRows} hangleFilterData={hangleFilterActionData} handleRecordsSelected={handleRecordsActionSelected} ifSelect={true} mode='multiple' columns={actionsTableColumn} hasMore={hasActionMore} id='action_id' dataSource={actionList} onChildEvent={handleChildActionEvent}></ModalTable>
            </Modal>
            <DeleteModal open={OpenDeleteModal} describe={`Are you sure you want to delete ${deleteValue || 'Untitled Assistant'}? This action cannot be undone and all integrations associated with the assistant will be affected.`} title='Delete Assistant' projectName={deleteValue || 'Untitled Assistant'} onDeleteCancel={onDeleteCancel} onDeleteConfirm={onDeleteConfirm} />
            <Drawer className={styles.drawerCreate} closeIcon={<img src={closeIcon} alt="closeIcon" className={styles['img-icon-close']} />} onClose={handleActionCancel} title='Bulk Create Action' placement="right" open={OpenActionDrawer} size='large' footer={<ModalFooterEnd handleOk={() => handleActionRequest()} onCancel={handleActionCancel} />}>
                <div className={styles['action-drawer']}>
                    <div className={styles['label']}>
                        <span className={styles['span']}> *</span>
                        <span>Schema</span>

                    </div>
                    <div className={styles['label-description']}> The action schema, Which is compliant with the OpenAPI
                        Specification. It should only have exactly one path and one method.</div>
                    <Input.TextArea className={styles['input-drawer']} autoSize={{ minRows: 10, maxRows: 20 }} value={schema}
                        onChange={handleSchemaChange} showCount maxLength={32768}></Input.TextArea>
                    {/* <span onClick={handleValidate} className='valid-schema'>Valid schema</span> */}
                    <div className={`${styles['desc-action-error']} ${tipSchema ? styles.show : ''}`}>Schema is required</div>
                    <div className={styles['label']}>
                        <span className={styles['span']}> *</span>
                        <span>Authentication</span>

                    </div>
                    <div className={styles['label-description']}>Authentication Type</div>
                    <Radio.Group onChange={onRadioChange} value={radioValue}>
                        <Radio value='none'>None</Radio>
                        <Radio value='basic'>Basic</Radio>
                        <Radio value='bearer'>Bearer</Radio>
                        <Radio value='custom'>Custom</Radio>
                    </Radio.Group>
                    {radioValue !== 'none' && <div style={{ display: 'flex', justifyContent: 'space-around', alignItems: 'center', margin: '15px 0' }}>
                        {radioValue !== 'custom' ? <span className={styles['desc-description']}>Authorization </span> : <Input placeholder='X-Custom' onChange={handleCustom} value={custom} style={{ width: '14%' }} />} <span className={styles['desc-description']}>:</span>  <Input prefix={<span style={{ color: '#999' }} >{radioValue !== 'custom' && titleCase(radioValue)}</span>} value={Authentication} placeholder='<Secret>' onChange={hangleChangeAuthorization} style={{ width: '83%' }}></Input>
                    </div>
                    }
                </div>
            </Drawer>
            <CreateCollection handleFetchData={() => fetchDataRetrievalData({ limit: retrievalLimit || 20 })} handleModalCloseOrOpen={() => setOpenCollectionDrawer(false)} OpenDrawer={openCollectionDrawer}></CreateCollection>
        </div>)
}
export default Assistant