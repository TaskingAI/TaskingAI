import styles from './assistants.module.scss'
import { fetchModelsData, fetchRetrievalData, fetchActionData } from '../../Redux/actions.ts'
import { useDispatch, useSelector } from 'react-redux';
import { PlusOutlined } from '@ant-design/icons';
import { getAssistantsList, createAssistant, deleteAssistant, updateAssistant } from '../../axios/assistant.ts'
import { getModelsList } from '../../axios/models.ts'
import { useEffect, useState, useRef } from 'react'
import ModelModal from '../modelModal/index'
import { fetchPluginData } from '../../Redux/actions';
import ModalTable from '../modalTable/index'
import tooltipTitle from '../../contents/tooltipTitle.tsx'
import { fetchAssistantsData } from '@/Redux/actions.ts'
import CreateCollection from '../createCollection/index.tsx';
import { setPlaygroundSelect, setPlaygroundAssistantId, } from '@/Redux/actions/playground.ts'
import { getActionsList, createActions } from '../../axios/actions.ts'
import EditIcon from '../../assets/img/editIcon.svg?react'
import ViewCode from '@/commonComponent/viewCode/index.tsx'
import MoreIcon from '@/assets/img/moreIcon.svg?react'
import { getViewCode } from '@/axios/index'
import JumpIcon from '../../assets/img/assistantJumpIcon.svg?react'
import { getFirstMethodAndEndpoint } from '@/utils/util'
import { toast } from 'react-toastify'
import DeleteModal from '../deleteModal/index.tsx'
import DrawerAssistant from '../drawerAssistant/index'
import closeIcon from '../../assets/img/x-close.svg'
import { useNavigate } from 'react-router-dom';
import { ChildRefType } from '../../constant/index.ts'
import ApiErrorResponse from '@/constant/index.ts'
import ActionDrawer from '../actionDrawer/index.tsx';
import ModalFooterEnd from '../modalFooterEnd/index'
import { useTranslation } from "react-i18next";
import { formatTimestamp } from '@/utils/util.ts'
import CreatePlugin from '../createPlugin/index.tsx';
import { valueLimit, assistantListType, commonDataType } from '@/constant/assistant.ts'
import CommonComponents from '../../contents/index'
import {
    Button,
    Space, Drawer, Spin, Modal, Tooltip,Popover
} from 'antd';
function Assistant() {
    const dispatch = useDispatch();
    const { pluginLists } = useSelector((state: any) => state.plugin);
    const { retrievalLists } = useSelector((state: any) => state.retrieval);
    const { users, loading } = useSelector((state: any) => state.user);
    const { assistantTableColumn, modelsTableColumn, } = CommonComponents();
    const { assistantPlaygroundId } = useSelector((state: any) => state.assistantId)
    const { tooltipEditTitle, tooltipPlaygroundTitle,tooltipMoreTitle } = tooltipTitle();
    const [bundilesList, setBundlesList] = useState([])
    const [isVisible, setIsVisible] = useState(true);
    const [record, setRecord] = useState<any>({})
    const [originalModelData, setOriginalModelData] = useState<any>()
    const { t } = useTranslation();
    const columns = [...assistantTableColumn]
    columns.push(
        {
            title: `${t('projectColumnActions')}`,
            key: 'action',
            width: 157,
            fixed: 'right',
            render: (_action: string, record: assistantListType) => (
                <Space size="middle">
                    <div onClick={() => handleJump(record)} className='table-edit-icon'>
                        <Tooltip placement='bottom' title={tooltipPlaygroundTitle} color='#fff' arrow={false} overlayClassName='table-tooltip'>
                            <JumpIcon />
                        </Tooltip>
                    </div>
                    <div onClick={() => handleEdit(record)} className='table-edit-icon'>
                        <Tooltip placement='bottom' title={tooltipEditTitle} color='#fff' arrow={false} overlayClassName='table-tooltip'>
                        <EditIcon/>
                        </Tooltip>
                    </div>
                    <div className='table-edit-icon' onClick={()=>setRecord(record)}>
                    {isVisible ? <Tooltip placement='bottom' title={tooltipMoreTitle} color='#fff' arrow={false} overlayClassName='table-tooltip'>
                        <Popover trigger="click" placement='bottom' content={content} arrow={false}>
                            <MoreIcon  />
                        </Popover>
                    </Tooltip> :  <MoreIcon  />}
                    </div>
                </Space>
            ),
        },
    );
    const [assistantsList, setAssistantsList] = useState([])
    const drawerAssistantRef = useRef<any>(null);
    const [OpenDrawer, setOpenDrawer] = useState(false)
    const [Authentication, setAuthentication] = useState('')
    const [radioValue, setRadioValue] = useState('none')
    const [recordsSelected, setRecordsSelected] = useState<any>([])
    const [selectedModelRows, setSelectedRows] = useState<any[]>([])
    const [selectedActionsSelected, setSelectedActionSelected] = useState<any[]>([])
    const [selectedRetrievalRows, setSelectedRetrievalRows] = useState<any[]>([])
    const [options, setOptions] = useState([])
    const [limit, setLimit] = useState(20)
    const [modelLimit, setModelLimit] = useState(20)
    const [updatePrevButton, setUpdatePrevButton] = useState(false)
    const [updateModelPrevButton, setUpdateModelPrevButton] = useState(false)
    const [selectedActionsRows, setSelectedActionsRows] = useState<any[]>([])
    const [OpenDeleteModal, setOpenDeleteModal] = useState(false)
    const [drawerTitle, setDrawerTitle] = useState('Create Assistant')
    const [drawerName, setDrawerName] = useState<any>('')
    const [hasActionMore, setHasActionMore] = useState(false)
    const [tipSchema, setTipSchema] = useState(false)
    const [deleteValue, setDeleteValue] = useState('')
    const [drawerDesc, setDrawerDesc] = useState('')
    const [modalTableOpen, setModalTableOpen] = useState(false)
    const [memoryValue, setMemoryValue] = useState('zero')
    const [retrievalConfig, setRetrievalConfig] = useState('user_message')
    const [OpenActionDrawer, setOpenActionDrawer] = useState(false)
    const [actionList, setActionList] = useState([])
    const [editLoading, setLoading] = useState(false)
    const childRef = useRef<ChildRefType | null>(null);
    const [hasModelMore, setHasModelMore] = useState(false)
    const [custom, setCustom] = useState('')
    const [assistantId, setAssistantId] = useState('')
    const [retrievalList, setRetrievalList] = useState([])
    const [schema, setSchema] = useState('')
    const [hasMore, setHasMore] = useState(false)
    const [assistantHasMore, setAssistantHasMore] = useState(false)
    const [modelOne, setModelOne] = useState(false);
    const [systemPromptTemplate, setSystemPromptTemplate] = useState(['']);
    const [inputValueOne, setInputValueOne] = useState(20)
    const [openCollectionDrawer, setOpenCollectionDrawer] = useState(false)
    const [inputValueTwo, setInputValueTwo] = useState(2000)
    const [pluginModalOpen, setPluginModalOpen] = useState(false)
    const [selectedPluginGroup, setSelectedPluginGroup] = useState<any>([])
    const [assistantPlaygroundIdParams, setAssistantPlaygroundIdParams] = useState('')
    const navigate = useNavigate()
    const [topk, setTopk] = useState(3)
    const [maxTokens, setMaxToken] = useState(4096)
    const [viewCodeOpen, setViewCodeOpen] = useState(false)
    const [viewCodeData, setViewCodeData] = useState('')
    const [modelName, setModelName] = useState<any>('')
    useEffect(() => {
        const params = {
            limit: 20,
        }

        fetchActionsList(params)
        fetchModelsList()
        fetchDataRetrievalData(params)
        const fetchCodeData = async () => {
            const res = await getViewCode('assistant')
            setViewCodeData(res.data)
        }
        fetchCodeData()
    }, []);
    useEffect(() => {
        setAssistantPlaygroundIdParams(assistantPlaygroundId)
    }, [assistantPlaygroundId])
    useEffect(() => {
        // setLoading(true);
        if (users.data.length > 0) {
            const data = users.data.map((item: any) => {
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
            setAssistantHasMore(users.has_more)
        } else {
            setAssistantsList([])
        }
        const data = retrievalLists.data.map((item: any) => {
            return {
                ...item,
                capacity1: item.num_chunks + '/' + item.capacity,
                key: item.collection_id,
                created_timestamp: formatTimestamp(item.created_timestamp),
            }
        })
        setRetrievalList(data);
        setBundlesList(pluginLists.data)
        setHasMore(retrievalLists.has_more)
    }, [users, retrievalLists, pluginLists]);
    const handleViewCode = () => {
        setIsVisible(false)
        setViewCodeOpen(true)
    }
    const content = (
        <div style={{ cursor: 'pointer' }}>
            <p className={styles['popover-eidt']} onClick={handleViewCode}>View code</p>
            <p className={styles['popover-delete']} onClick={() => handleDelete(record)} >Delete</p>
        </div>
    );
    const fetchData = async (params: object) => {
        try {
            const res: any = await getAssistantsList(params)
            const data = res.data.map((item: any) => {
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
    };
    const handleJump = (value: assistantListType) => {
        dispatch(setPlaygroundSelect('assistant'))
        localStorage.setItem('assistantName', value.name || 'Untitled Assistant')
        navigate(`/project/playground?assistant_id=${value.assistant_id}`)
    }
    const handleModalClose = () => {
        setOriginalModelData((prev: any) => prev)
        setSelectedRows(originalModelData as any)
        setModalTableOpen(false)
    }
    const handleModalCloseConfirm = ()=> {
        if(selectedModelRows) {
            let str = selectedModelRows[0];
            let index = str.lastIndexOf('-');
            if (index !== -1) {
                let result = str.substring(0, index);
                setModelName(result)
            }
            setOriginalModelData(selectedModelRows)
        } 
      
        setModalTableOpen(false)
    }
    const handleSchemaChange = (value: string) => {
        setSchema(value)
    }
    const handleActionRequest = async () => {
        if (!schema) {
            setTipSchema(true)
            return
        }
        const commonData: commonDataType = {
            openapi_schema: JSON.parse(schema),
            authentication: {
                type: radioValue,

            }
        };
        if (radioValue === 'custom') {
            if (commonData.authentication) {
                commonData.authentication.content = { [custom]: Authentication };
            }
        } else {
            if (radioValue === 'none') {
                (commonData.authentication as any).type = 'none'
            } else {
                if (commonData.authentication) {
                    commonData.authentication.secret = Authentication;
                }
            }
        }
        try {

            await createActions(commonData);
            const params = {
                limit: 20,
            }
            await fetchActionsList(params, 'create');
        } catch (error) {
            console.error(error);
            const ErrorType = error as ApiErrorResponse;
            const errorMessage: string = ErrorType.response.data.error.message;
            toast.error(errorMessage)
        } finally {
            setOpenActionDrawer(false)
        
        }
    }
    const fetchDataRetrievalData = async (params:any) => {
        try {
            dispatch(fetchRetrievalData(params) as any);

        } catch (e) {
            console.log(e)
        }
    }

    const handleInputPromptChange = (index: number, newValue: any) => {
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
    const fetchActionsList = async (params: Record<string, string | number>, type?: string) => {
        if (type) {
            dispatch(fetchActionData(20) as any);
        }
        try {
            const res: any = await getActionsList(params)
            const data = res.data.map((item: any) => {
                return {
                    ...item,
                    key: item.action_id,
                    method: getFirstMethodAndEndpoint(item.openapi_schema)?.method,
                    endpoint: getFirstMethodAndEndpoint(item.openapi_schema)?.endpoint,
                    created_timestamp: formatTimestamp(item.created_timestamp)
                }
            })
            setActionList(data)
            setHasActionMore(res.has_more)
        } catch (error) {
            console.log(error)
        }
    }

    const handleCreateModelId = async () => {
        await setModelOne(true)
        childRef.current?.fetchAiModelsList()
        await fetchModelsList()
        setOptions(prevOptions => [...prevOptions]);
    }
    const handleCreatePrompt = () => {
        setDrawerTitle('Create Assistant')
        setAssistantId('')
        setSystemPromptTemplate([''])
        setSelectedPluginGroup([])
        setSelectedRetrievalRows([''])
        setSelectedActionsRows([{ type: 'plugin', value: '' }])
        setSelectedActionSelected([])
        setDrawerName('')
        setSelectedRows([])
        setModelName(undefined)
        setMemoryValue('zero')
        setDrawerDesc('')
        setRecordsSelected([])
        setOpenDrawer(true)
        setIsVisible(false)
    }
    const handleEdit = (val: assistantListType) => {
        console.log(val)
        setModelName(val.model_name)
        setDrawerTitle(`${t('projectEditAssistant')}`)
        const tag = val.retrievals.map(item => {
            return {
                collection_id: item.id,
                name: item.name || 'Untitled Collection'
            }
        })
        setSelectedRetrievalRows(tag)
        setSelectedActionSelected(val.tools.filter(item=>item.type === 'action').map(item=>{
            return {
                action_id: item.id,
                name: item.name
            }
        }))
        setSelectedPluginGroup(val.tools?.filter(item => item.type === 'plugin').map(item => item.id?.split('/')[1]));
        setSelectedActionsRows(val.tools.map(item => { return { type: item.type, value: item.id,name: item.name } }))
        setDrawerName(val.name)
        setDrawerDesc(val.description)
        setRetrievalConfig(val.retrieval_configs.method || 'user_message')
        setTopk(val.retrieval_configs.top_k || 3)
        setMaxToken(val.retrieval_configs.max_tokens || 4096)
        setInputValueOne(val.max_messages)
        setInputValueTwo(val.max_tokens)
        setMemoryValue(val.memory)
        setRecordsSelected([val.model_id])

        setAssistantId(val.assistant_id)
        setSystemPromptTemplate(val.system_prompt_template)
        setSelectedRows([val.model_id])
        setOriginalModelData([val.model_id])
        setOpenDrawer(true)
        setIsVisible(false)
    }

    const handleDelete = (val: assistantListType) => {
        setOpenDeleteModal(true)
        setIsVisible(false)

        setDeleteValue(val.name)
        setAssistantId(val.assistant_id)
    }
    const onDeleteCancel = () => {
        setIsVisible(true)
        setOpenDeleteModal(false)
    }
    const handleRetrievalConfigChange1 = (value: string) => {
        setRetrievalConfig(value)
    }
    const onDeleteConfirm = async () => {
        const params = {
            limit: limit || 20,
        }
        setUpdatePrevButton(true)

        try {
            if (assistantId === assistantPlaygroundIdParams) {
                await dispatch(setPlaygroundAssistantId(''))
            }
            await deleteAssistant(assistantId)
            dispatch(fetchAssistantsData() as any)
            await fetchData(params)
            setOpenDeleteModal(false)

        } catch (error) {
            console.log(error)
            const errorType = error as ApiErrorResponse
            const errorMessage: string = errorType.response.data.error.message;
            toast.error(errorMessage)
        } finally {
            setIsVisible(true)
        
        }
    }
    const handleMemoryChange1 = (value: string) => {
        setMemoryValue(value)
    }
    const handleRequest = async () => {
        const inputValueMap = (drawerAssistantRef.current?.getRetrievalSelectedList() || []).map((item: any) => {
            return {
                type: 'collection', id: item
            }
        }).filter((item: any) => item.id)
        const inputPluginValues = (drawerAssistantRef.current?.getActionSelectedList() || []).map((item: any) => ({ type: item.type, id: item.value })).filter((item: any) => item.id)

        let systemTemplate: string[] = [];
        if (systemPromptTemplate.length === 1 && systemPromptTemplate[0] === '') {
            systemTemplate = []
        } else {
            systemTemplate = systemPromptTemplate
        }
        if (originalModelData.length === 0) {
            return toast.error(`${t('projectModelRequired')}`)
        }
        const params = {
            model_id: originalModelData[0].slice(-8),
            name: drawerName || '',
            description: drawerDesc || '',
            system_prompt_template: systemTemplate,
            tools: inputPluginValues,
            retrievals: inputValueMap,
            memory: {
                type: memoryValue,
                max_messages: Number(inputValueOne) || undefined,
                max_tokens: Number(inputValueTwo) || undefined
            },
            retrieval_configs: {
                top_k: Number(topk) || undefined,
                method: retrievalConfig,
                max_tokens: Number(maxTokens) || undefined
            }
        }
        let count = 0

        systemPromptTemplate.forEach(item => {
            const length = item.length
            count += length
        })
        if (count > 16384) {
            return toast.error(`${t('projectAssistantSystemPromptRequired')}`)
        }
        if (originalModelData[0].slice(-8).length !== 8) {
            return toast.error(`${t('projectAssistantModelIDRequired')}`)
        }
        try {
            setLoading(true)
            if (assistantId) {
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
            dispatch(fetchAssistantsData() as any)
            setUpdatePrevButton(true)
        } catch (error) {
            console.log(error)
            const apiError = error as ApiErrorResponse;
            const errorMessage: string = apiError.response.data.error.message;
            toast.error(errorMessage)
        } finally {
            setLoading(false)
            setIsVisible(true)
        }

    }

    const fetchModelsList = async (value?: any, type?: string) => {
        if (type) {
            dispatch(fetchModelsData(20) as any);
        }
        const params = {
            limit: modelLimit || 20,
            ...value
        }
        try {
            const res: any = await getModelsList(params, 'chat_completion')
            const data = res.data.map((item: any) => {
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
        setIsVisible(true)
    }


    const handleChildEvent = async (value: valueLimit) => {
        setLimit(value.limit)
        setUpdatePrevButton(false)
        await fetchData(value);
    }


    const handleDeletePromptInput = (index: number) => {
        const updatedInputValues = [...systemPromptTemplate];
        updatedInputValues.splice(index, 1);
        setSystemPromptTemplate(updatedInputValues);
    }
    const handleNewCollection = (value: boolean) => {
        setOpenCollectionDrawer(value)
    }
    const hangleChangeAuthorization = (value: string) => {
        setAuthentication(value)
    }

    const handleAddPrompt = () => {
        if (systemPromptTemplate.length < 10) {
            setSystemPromptTemplate((prevValues => [...prevValues, '']))
        }
    }

    const handleSelectModelId = (value: boolean) => {
        setModalTableOpen(value)
    }

    const handleChildModelEvent = async (value: valueLimit) => {
        setModelLimit(value.limit)
        setUpdateModelPrevButton(false)
        await fetchModelsList(value)
    }


    const handleChangeName = (value: string) => {
        setDrawerName(value)
    }
    const handleInputValueOne = (value: number) => {
        setInputValueOne(value)
    }
    const handleInputValueTwo = (value: number) => {
        setInputValueTwo(value)
    }
    const handleDescriptionChange = (value: string) => {
        setDrawerDesc(value)
    }

    const onRadioChange = (value: string) => {
        setRadioValue(value)
    }
    const handleActionCancel = () => {
        setOpenActionDrawer(false)
    }
    const handleRecordsSelected = (value: any, selectedRows: any[]) => {
        setRecordsSelected(value)
        const tag = selectedRows.map(item => (item.name + '-' + item.model_id))
        setSelectedRows(tag)
    }

    const handleCustom = (value: string) => {
        setCustom(value)
    }

    const onhandleTipError = (value: boolean) => {
        setTipSchema(value)
    }
    const handleClosePluginModal = () => {
        setPluginModalOpen(false)
    }
    const handleConfirmRequest = async () => {
        dispatch(fetchPluginData(20) as any);
    }
    const handleNewActionModal = () => {
        setOpenActionDrawer(true)
    }
    const handleMaxToken = (value: any) => {
        setMaxToken(value)
    }
    const handleToks = (value: any) => {
        setTopk(value)
    }
    const handleNewBundle = () => {
        setPluginModalOpen(true)
    }
    const handleCloseViewCode = () => {
        setIsVisible(true)
        setViewCodeOpen(false)
   }
    return (
        <div className={styles["assistants"]}>

            <Spin spinning={loading} wrapperClassName={styles.spinloading}>
                <ModalTable title='New assistant' loading={loading} updatePrevButton={updatePrevButton} hasMore={assistantHasMore} id="assistant_id" ifSelect={false} columns={columns} name="assistant" dataSource={assistantsList} onChildEvent={handleChildEvent} onOpenDrawer={handleCreatePrompt} />
            </Spin>
            <Drawer
                className={styles['drawer-assistants']}
                width={1280}
                closeIcon={<img src={closeIcon} alt="closeIcon" className={styles['img-icon-close']} />}
                onClose={handleCancel} title={drawerTitle} placement="right" open={OpenDrawer} size='large' footer={[
                    <Button key="cancel" onClick={handleCancel} className='cancel-button'>
                        {t('cancel')}
                    </Button>,
                    <Button key="submit" loading={editLoading} onClick={handleRequest} className={`next-button ${styles['button']}`}>
                        {t('confirm')}
                    </Button>
                ]}>
                <DrawerAssistant modelName={modelName} drawerTitle={drawerTitle} openDrawer={OpenDrawer} selectedActionsSelected={selectedActionsSelected} selectedPluginGroup={selectedPluginGroup} handleNewBundle={handleNewBundle} retrievalConfig={retrievalConfig} topk={topk} maxTokens={maxTokens} handleMaxToken={handleMaxToken} handleToks={handleToks} bundilesList={bundilesList} handleNewActionModal={handleNewActionModal} handleNewCollection={handleNewCollection} selectedCollectionList={selectedRetrievalRows} actionHasMore={hasActionMore} actionList={actionList} collectionHasMore={hasMore} ref={drawerAssistantRef}
                    handleRetrievalConfigChange1={handleRetrievalConfigChange1} retrievalList={retrievalList} selectedActionsRows={selectedActionsRows} inputValue1={inputValueOne} inputValue2={inputValueTwo} handleMemoryChange1={handleMemoryChange1} memoryValue={memoryValue} handleAddPromptInput={handleAddPrompt} drawerName={drawerName} systemPromptTemplate={systemPromptTemplate} handleDeletePromptInput={handleDeletePromptInput} handleInputPromptChange={handleInputPromptChange} handleInputValueOne={handleInputValueOne} handleInputValueTwo={handleInputValueTwo} selectedRows={originalModelData} handleSelectModelId={handleSelectModelId} handleChangeName={handleChangeName} drawerDesc={drawerDesc} handleDescriptionChange={handleDescriptionChange}  ></DrawerAssistant>
            </Drawer>

            <ModelModal type='chat_completion' ref={childRef} open={modelOne} handleSetModelConfirmOne={handleSetModelConfirmOne} handleSetModelOne={handleModalCancel} getOptionsList={fetchModelsList} modelType='chat_completion'></ModelModal>
            <Modal closeIcon={<img src={closeIcon} alt="closeIcon" className={styles['img-icon-close']} />} centered onCancel={handleModalClose} footer={[
                <div className='footer-group' key='footer1'>
                    <Button key="model" icon={<PlusOutlined />} onClick={handleCreateModelId} className='cancel-button'>
                        {t('projectNewModel')}
                    </Button>
                    <div>
                        <span className='select-record'>
                            {recordsSelected.length}  {recordsSelected.length > 1 ? `${t('projectItemsSelected')}` : `${t('projectItemSelected')}`}
                        </span>
                        <Button key="cancel" onClick={handleModalClose} className={`cancel-button ${styles.cancelButton}`}>
                            {t('cancel')}
                        </Button>
                        <Button key="submit" onClick={handleModalCloseConfirm} className='next-button'>
                            {t('confirm')}
                        </Button>
                    </div>
                </div>
            ]} title={t('projectSelectModel')} open={modalTableOpen} width={1000} className={`modal-inner-table ${styles['retrieval-model']}`}>
                <ModalTable title='New model' onOpenDrawer={handleCreateModelId} name="model" updatePrevButton={updateModelPrevButton} defaultSelectedRowKeys={selectedModelRows} handleRecordsSelected={handleRecordsSelected} ifSelect={true} columns={modelsTableColumn} hasMore={hasModelMore} id='model_id' dataSource={options} onChildEvent={handleChildModelEvent}></ModalTable>
            </Modal>
            <ViewCode open={viewCodeOpen} data={viewCodeData} handleClose={handleCloseViewCode}/>
            <CreatePlugin handleConfirmRequest={handleConfirmRequest} open={pluginModalOpen} handleCloseModal={handleClosePluginModal}></CreatePlugin>
            <DeleteModal open={OpenDeleteModal} describe={`${t('deleteItem')} ${deleteValue || 'Untitled Assistant'}? This action cannot be undone and all integrations associated with the assistant will be affected.`} title='Delete Assistant' projectName={deleteValue || 'Untitled Assistant'} onDeleteCancel={onDeleteCancel} onDeleteConfirm={onDeleteConfirm} />
            <Drawer zIndex={10001} className={styles['drawer-action']} closeIcon={<img src={closeIcon} alt="closeIcon" className={styles['img-icon-close']} />} onClose={handleActionCancel} title='Bulk Create Action' placement="right" open={OpenActionDrawer} size='large' footer={<ModalFooterEnd handleOk={() => handleActionRequest()} onCancel={handleActionCancel} />}>
                <ActionDrawer showTipError={tipSchema} onhandleTipError={onhandleTipError} schema={schema} onSchemaChange={handleSchemaChange} onRadioChange={onRadioChange} onChangeCustom={handleCustom} onChangeAuthentication={hangleChangeAuthorization} radioValue={radioValue} custom={custom} Authentication={Authentication} />
            </Drawer>
            <CreateCollection handleFetchData={() => fetchDataRetrievalData({limit: 20})} handleModalCloseOrOpen={() => setOpenCollectionDrawer(false)} OpenDrawer={openCollectionDrawer}></CreateCollection>
        </div>)
}
export default Assistant