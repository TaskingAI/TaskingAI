import styles from './assistants.module.scss'
import { PlusOutlined } from '@ant-design/icons';
import { getAssistantsList, createAssistant, deleteAssistant, updateAssistant } from '../../axios/assistant.js'
import { getModelsList } from '../../axios/models.js'
import { useEffect, useState, useRef } from 'react'
import ModelModal from '../modelModal/index'
import ModalTable from '../modalTable/index'
import ClipboardJS from 'clipboard';
import { tooltipEditTitle, tooltipDeleteTitle, tooltipPlaygroundTitle } from '../../contents/index.js'
import CreateCollection from '../createCollection/index.jsx';
import ModelProvider from '../../assets/img/ModelProvider.svg?react'
import GoogleIcon from '../../assets/img/googleIcon.svg?react'
import CohereIcon from '../../assets/img/cohereIcon.svg?react'
import { getActionsList, createActions } from '../../axios/actions.js'
import EditIcon from '../../assets/img/editIcon.svg?react'
import DeleteIcon from '../../assets/img/deleteIcon.svg?react'
import JumpIcon from '../../assets/img/assistantJumpIcon.svg?react'
import ModalFooterEnd from '../modalFooterEnd/index'
import { formatTimestamp, getFirstMethodAndEndpoint } from '@/utils/util'
import { toast } from 'react-toastify'
import CopyOutlined from '../../assets/img/copyIcon.svg?react'
import DeleteModal from '../deleteModal/index.jsx'
import DrawerAssistant from '../drawerAssistant/index'
import closeIcon from '../../assets/img/x-close.svg'
import { useNavigate } from 'react-router-dom';
import Anthropic from '../../assets/img/Anthropic.svg?react'
import Frame from '../../assets/img/Frame.svg?react'
import {
    Button,
    Space, Radio, Tag, Drawer, Input, Spin, Modal, Tooltip
} from 'antd';
import { getRetrievalList } from '../../axios/retrieval.js';
const statusReverse = {
    Creating: 'orange',
    ready: 'green',
    error: 'red',
    deleting: 'red'
}
const imgReverse = (providerId) => {
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
const typeReverse = {
    instruct_completion: 'Instruct Completion',
    chat_completion: 'Chat Completion',
    text_embedding: 'Text Embedding'
}
const titleCase = (str) => {
    const newStr = str.slice(0, 1).toUpperCase() + str.slice(1).toLowerCase();
    return newStr;
}
const revereseLabel = {
    naive: 'Naive',
    zero: 'Zero',
    [`message_window`]: 'Message Window',
}
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

function Assistant() {
    const columns = [
        {
            title: 'Name',
            dataIndex: 'name',
            key: 'name',
            width: 240,
            height: 45,
            fixed: 'left',
            render: (text, record) =>
                <div>
                    <p className='table-text' style={{ fontSize: '14px' }}>{text || 'Untitled Assistant'}</p>
                    <p style={{ display: 'flex', alignItems: 'center', margin: 0 }}>
                        <span style={{ fontSize: '12px', color: '#777' }}>{record.assistant_id}</span><CopyOutlined className='icon-copy' onClick={() => handleCopy(record.assistant_id)} />

                    </p>
                </div>
            ,
        },
        {
            title: 'Description',
            width: 360,
            dataIndex: 'description',
            key: 'description',
            render: (text) => (
                <>
                    <div>{text}</div>
                </>
            ),
        },
        {
            title: 'Language model',
            dataIndex: 'model_id',
            width: 360,
            key: 'model_id',
            ellipsis: true,
            render: (_) => (
                <div>{_}</div>

            )
        },
        {
            title: 'Prompt template',
            width: 360,
            dataIndex: 'promptTemplate',
            ellipsis: true,
            render: (_) => (
                <div>{_}</div>

            )
        },
        {
            title: 'Memory',
            width: 180,
            dataIndex: 'memory',
            render: (_) => (
                <div>{revereseLabel[_]}</div>

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
    ];
    const modalTableColumn = [
        {
            title: 'Name',
            dataIndex: 'name',
            key: 'name',
            width: 240,
            fixed: 'left',
            render: (text, record) =>
                <div>
                    <p className='table-text' style={{ fontSize: '14px' }}>{text || 'Untitled Collection'}</p>
                    <p style={{ display: 'flex', alignItems: 'center', margin: 0 }}>
                        <span style={{ fontSize: '12px', color: '#777' }}>{record.collection_id}</span><CopyOutlined className='icon-copy' onClick={() => handleCopy(record.collection_id)} />

                    </p>
                </div>
            ,
        },
        {
            title: 'Description',
            dataIndex: 'description',
            key: 'description',
            width: 360,
            render: (text) => (
                <>
                    <div>{text}</div>
                </>
            ),
        },
        {
            title: 'Records',
            dataIndex: 'num_records',
            key: 'num_records',
            width: 180,
            render: (text) => (
                <>
                    <div>{text}</div>
                </>
            ),
        },
        {
            title: 'Capacity',
            dataIndex: 'capacity1',
            key: 'capacity1',
            width: 180,
            render: (text) => (
                <div>{text}</div>
            )
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
            title: 'Embedding model ID',
            dataIndex: 'embedding_model_id',
            key: 'ModelID',
            ellipsis: true,
            width: 180,
            render: (_) => (
                <div>{_}</div>
            )
        },
        {
            title: 'Created at',
            dataIndex: 'created_timestamp',
            key: 'created_timestamp',
            width: 180,
            render: (time) => <div>{formatTimestamp(time)}</div>
        }
    ]
    const actionColumn = [
        {
            title: 'Name',
            dataIndex: 'name',
            key: 'name',
            fixed: 'left',
            width: 240,
            render: (text, record) =>
                <div>
                    <p className='table-text' style={{ fontSize: '14px' }}>{text}</p>
                    <p style={{ display: 'flex', alignItems: 'center', margin: 0 }}>
                        <span style={{ fontSize: '12px', color: '#777' }}>{record.action_id}</span><CopyOutlined className='icon-copy' onClick={() => handleCopy(record.action_id)} />

                    </p>
                </div>
            ,
        },
        {
            title: 'Description',
            dataIndex: 'description',
            key: 'description',
            width: 360,
            render: (text) => (
                <>
                    <div>{text}</div>
                </>
            ),
        },
        {
            title: 'Method',
            dataIndex: 'method',
            key: 'method',
            width: 180,
            render: (_) => (
                <>
                    {_}
                </>
            ),
        },
        {
            title: 'Endpoint',
            dataIndex: 'endpoint',
            key: 'endpoint',
            width: 360,
            render: (_) => (
                <>
                    {_}
                </>
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
    const modelsColumns = [
        {
            title: 'Name',
            dataIndex: 'name',
            key: 'name',
            fixed: 'left',
            width: 240,
            render: (text, record) =>
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
            render: (text, record) =>
                <div className='img-text'>
                    {imgReverse(record.provider_id)} <span className='a'>{text}</span>
                </div>
            ,
        },
        {
            title: 'Type',
            width: 240,
            dataIndex: 'type',
            key: 'type',
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
    const [assistantsList, setAssistantsList] = useState([])
    const [OpenDrawer, setOpenDrawer] = useState(false)
    const [loading, setLoading] = useState(false);
    const [Authentication, setAuthentication] = useState('')
    // const [selectType, setSelectType] = useState('action')
    const [modalActionTableOpen, setModalActionTableOpen] = useState(false)
    const [radioValue, setRadioValue] = useState('none')
    const [recordsSelected, setRecordsSelected] = useState([])
    // const [recordsRetrievalSelected, setRecordsRetrievalSelected] = useState([])
    const [recordsSelected1, setRecordsSelected1] = useState([])
    const [selectedRows, setSelectedRows] = useState([])
    // const [selectedRetrievalModelRows, setSelectedRetrievalModelRows] = useState([])
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
    // const [modelId, setModelId] = useState(undefined)
    // const [templateDesc, setTemplateDesc] = useState('')
    const [deleteValue, setDeleteValue] = useState('')
    const [drawerDesc, setDrawerDesc] = useState('')
    const [openModalTable, setOpenModalTable] = useState(false)
    const [modalTableOpen, setModalTableOpen] = useState(false)
    const [memoryValue, setMemoryValue] = useState('zero')
    const [OpenActionDrawer, setOpenActionDrawer] = useState(false)
    const [actionList, setActionList] = useState([])
    const childRef = useRef();
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
        // fetchModelsList()
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
            const res = await getAssistantsList(params)
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
        navigate(`/projects/playground?assistant_id=${value.assistant_id}`)
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
            schema: JSON.parse(schema),
            authentication: {
                type: radioValue
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
            const res = await getRetrievalList(params)
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
            const res = await getActionsList(params)
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
        childRef.current.fetchAiModelsList()
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
        // const isSystemPromptTemplate = systemPromptTemplate.every(item => item !== '')
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

    const fetchModelsList = async (value) => {
        const params = {
            limit: modelLimit || 20,
            ...value
        }
        try {
            const res = await getModelsList(params, 'chat_completion')
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
        // setModelIdModal(tag)
    }
    // const handleRetrievalModelSelected = (value, selectedRows) => {
    //     setRecordsRetrievalSelected(value)
    //     const tag = selectedRows.map(item => (item.name + '-' + item.model_id))
    //     setSelectedRetrievalModelRows(tag)
    //     setModelNewIdModal(tag)
    // }
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
    // const handleChangeSelect = (index, value) => {
    //     const newValues = [...inputPluginValues];
    //     newValues[index].type = value;
    //     setInputPluginValues(newValues);
    // }
    return (
        <div className={styles["assistants"]}>
       
            <Spin spinning={loading} wrapperClassName={styles.spinloading}>
                <ModalTable updatePrevButton={updatePrevButton} hasMore={assistantHasMore} id="assistant_id" ifSelect={false} columns={columns} name="assistant" dataSource={assistantsList} onChildEvent={handleChildEvent} onOpenDrawer={handleCreatePrompt} />
            </Spin>
            <Drawer
                className={styles['drawer-assistants']}
                closePosition='right'
                closeIcon={<img src={closeIcon} alt="closeIcon" className={styles['img-icon-close']} />}
                onClose={handleCancel} title={drawerTitle} placement="right" open={OpenDrawer} size='large' footer={<ModalFooterEnd handleOk={() => handleRequest()} onCancel={handleCancel} closeIcon={<img src={closeIcon} alt="closeIcon" />} />}>
                <DrawerAssistant selectedActionsRows={selectedActionsRows} inputValue1={inputValueOne} inputValue2={inputValueTwo} handleMemoryChange1={handleMemoryChange1} memoryValue={memoryValue} handleAddPromptInput={handleAddPrompt} handleActionModalTable={handleActionModalTable} drawerName={drawerName} systemPromptTemplate={systemPromptTemplate} handleDeletePromptInput={handleDeletePromptInput} handleInputPromptChange={handleInputPromptChange} handleInputValueOne={handleInputValueOne} handleInputValueTwo={handleInputValueTwo} selectedRows={selectedRows} handleSelectModelId={handleSelectModelId} handleChangeName={handleChangeName} drawerDesc={drawerDesc} handleDescriptionChange={handleDescriptionChange} handleModalTable={handleModalTable} selectedRetrievalRows={selectedRetrievalRows}></DrawerAssistant>
            </Drawer>
            <Modal closeIcon={<img src={closeIcon} alt="closeIcon" className={styles['img-icon-close']} />} centered footer={[
                <div className={styles['footer-group']} style={{ display: 'flex', justifyContent: 'space-between' }} key='footer2'>
                    <Button key="model" icon={<PlusOutlined />} onClick={handleNewModal} className='cancel-button'>
                        New Collection
                    </Button>
                    <div>
                        <span className={styles['select-record']}>
                            {recordsSelected1.length}  {recordsSelected1.length > 1 ? 'items' : 'item'} selected
                        </span>
                        <Button key="cancel" onClick={handleCloseModal} className='cancel-button'>
                            Cancel
                        </Button>
                        <Button key="submit" onClick={handleCreateConfrim} className='next-button'>
                            Confirm
                        </Button>
                    </div>

                </div>
            ]} title='Select Collection' open={openModalTable} width={1000} onCancel={handleCloseModal} className={`${styles['modal-inner-table']} ${styles['retrieval-model']}`}>
                <ModalTable onOpenDrawer={handleNewModal} name='Collection' updatePrevButton={updateRetrievalPrevButton} defaultSelectedRowKeys={selectedRetrievalRows} hangleFilterData={hangleFilterData} mode='multiple' handleRecordsSelected={handleCollectionSelected} ifSelect={true} columns={modalTableColumn} dataSource={retrievalList} hasMore={hasMore} id='collection_id' onChildEvent={handleChildRetrievalEvent} />
            </Modal>

            <ModelModal ref={childRef} open={modelOne} handleSetModelConfirmOne={handleSetModelConfirmOne} handleSetModelOne={handleModalCancel} getOptionsList={fetchModelsList} modelType='chat_completion'></ModelModal>
            <Modal closeIcon={<img src={closeIcon} alt="closeIcon" className={styles['img-icon-close']} />} centered onCancel={handleModalClose} footer={[
                <div className={styles['footer-group']} key='footer1'>
                    <Button key="model" icon={<PlusOutlined />} onClick={handleCreateModelId} className='cancel-button'>
                        New Model
                    </Button>
                    <div>
                        <span className={styles['select-record']}>
                            {recordsSelected.length}  {recordsSelected.length > 1 ? 'items' : 'item'} selected
                        </span>
                        <Button key="cancel" onClick={handleModalClose} className='cancel-button'>
                            Cancel
                        </Button>
                        <Button key="submit" onClick={handleModalClose} className='next-button'>
                            Confirm
                        </Button>
                    </div>

                </div>

            ]} title='Select Model' open={modalTableOpen} width={1000} className='modal-inner-table retrieval-model'>
                <ModalTable onOpenDrawer={handleCreateModelId} name="model" updatePrevButton={updateModelPrevButton} defaultSelectedRowKeys={selectedRows} handleRecordsSelected={handleRecordsSelected} ifSelect={true} columns={modelsColumns} hasMore={hasModelMore} id='model_id' dataSource={options} onChildEvent={handleChildModelEvent}></ModalTable>
            </Modal>
    
            <Modal closeIcon={<img src={closeIcon} alt="closeIcon" className={styles['img-icon-close']} />} centered footer={[
                <div className={styles['footer-group']} key='footer3'>
                    <Button key="model" icon={<PlusOutlined />} onClick={handleCreateAction} className='cancel-button'>
                        New Action
                    </Button>
                    <div>
                        <span className={styles['select-record']}>
                            {recordsSelected.length}  {recordsSelected.length > 1 ? 'items' : 'item'} selected
                        </span>
                        <Button key="cancel" onClick={handleActionModalClose} className='cancel-button'>
                            Cancel
                        </Button>
                        <Button key="submit" onClick={handleActionModalClose} className='next-button'>
                            Confirm
                        </Button>
                    </div>

                </div>

            ]} title='Select Action' open={modalActionTableOpen} width={1000} className='modal-inner-table retrieval-model' onCancel={handleActionModalClose}>
                <ModalTable onOpenDrawer={handleCreateAction} name="Action" updatePrevButton={updateActionPrevButton} defaultSelectedRowKeys={selectedActionsRows} hangleFilterData={hangleFilterActionData} handleRecordsSelected={handleRecordsActionSelected} ifSelect={true} mode='multiple' columns={actionColumn} hasMore={hasActionMore} id='action_id' dataSource={actionList} onChildEvent={handleChildActionEvent}></ModalTable>
            </Modal>
            <DeleteModal open={OpenDeleteModal} describe={`Are you sure you want to delete ${deleteValue || 'Untitled Assistant'}? This action cannot be undone and all integrations associated with the assistant will be affected.`} title='Delete Assistant' projectName={deleteValue || 'Untitled Assistant'} onDeleteCancel={onDeleteCancel} onDeleteConfirm={onDeleteConfirm} />
            <Drawer closeIcon={<img src={closeIcon} alt="closeIcon" className={styles['img-icon-close']} />} onClose={handleActionCancel} title='Bulk Create Action' placement="right" open={OpenActionDrawer} size='large' footer={<ModalFooterEnd handleOk={() => handleActionRequest()} onCancel={handleActionCancel} />}>
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
                    <div className={`desc-action-error ${tipSchema ? 'show' : ''}`}>Schema is required</div>
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