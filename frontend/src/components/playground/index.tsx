import styles from './playground.module.scss'
import { useState, useEffect, useRef } from 'react'
import { Select, Button, Checkbox, Input, Drawer, Spin, Modal, Collapse } from 'antd'
import { PlusOutlined, RightOutlined, LoadingOutlined } from '@ant-design/icons';
import { toast } from 'react-toastify';
import CopyOutlined from '../../assets/img/copyIcon.svg?react'
import ModelModal from '../modelModal/index'
import ErrorIcon from '../../assets/img/errorIcon.svg?react'
import { getModelsList } from '../../axios/models.ts'
import PlayGroundImg from '../../assets/img/selectAssistantImg.svg?react'
import LoadingAnim from '../../assets/img/loadingAnim.svg?react'
import CreateCollection from '../createCollection/index.tsx';
import ModalSettingIcon from '../../assets/img/modalSettingIcon.svg?react'
import { formatTimestamp, getFirstMethodAndEndpoint } from '@/utils/util'
import ModalTable from '../modalTable/index'
import { commonDataType } from '@/contant/assistant.ts'
import ApiErrorResponse, { ChildRefType } from '../../contant/index.ts'
import ChatIcon from '../../assets/img/chatIcon.svg?react'
import { getActionsList, createActions } from '../../axios/actions.ts'
import { getRetrievalList } from '../../axios/retrieval.ts';
import PlaygroundImg from '@/assets/img/playgroundImg.svg?react'
import { openChat, sendMessage, generateMessage, getListChats, getHistoryMessage, deleteChatItem } from '@/axios/playground'
import { getAssistantsList, getAssistantDetail, updateAssistant } from '@/axios/assistant'
import closeIcon from '../../assets/img/x-close.svg'
import ModalFooterEnd from '../modalFooterEnd/index'
import { SSE } from "sse.js";
import ActionDrawer from '../actionDrawer/index.tsx';
import DeleteIcon from '../../assets/img/deleteIcon.svg?react'
import DeleteModal from '../deleteModal/index.tsx';
import EditIcon from '../../assets/img/editIcon.svg?react'
import MessageSuccess from '../../assets/img/messageSuccess.svg?react'
import ClipboardJS from 'clipboard';
import DrawerAssistant from '../drawerAssistant/index'
import { useLocation, useNavigate } from 'react-router-dom';
const origin = window.location.origin;
import { assistantTableColumn, modelsTableColumn, actionsTableColumn, collectionTableColumn } from '../../contents/index'
const plainOptions = [
    { label: 'Stream', value: 1 },
    { label: 'Debug', value: 2 },
]
function Playground() {
    const navigation = useNavigate();
    const { search, pathname } = useLocation();
    const [assistantId, setAssistantId] = useState<any>()
    const [optionList, setOptionList] = useState([])
    const divRef = useRef();
    const settingModal = useRef<any>()
    const [retrievalLimit, setRetrievalLimit] = useState(20)
    const [updateModelPrevButton, setUpdateModelPrevButton] = useState(false)
    const [updateActionPrevButton, setUpdateActionPrevButton] = useState(false)
    const [actionLimit, setActionLimit] = useState(20)
    const [assistantLimit, setAssistantLimit] = useState(20)
    const settingIcon = useRef<any>()
    const contentRef = useRef<any>();
    const [shouldSmoothScroll, setShouldSmoothScroll] = useState(true)
    const [Authentication, setAuthentication] = useState('')
    const [modalActionTableOpen, setModalActionTableOpen] = useState(false)
    const [selectedActionsRows, setSelectedActionsRows] = useState([])
    const [retrievalList, setRetrievalList] = useState([])
    const [listChats, setListChats] = useState([])
    const [OpenDrawer, setOpenDrawer] = useState(false)
    const [options, setOptions] = useState([])
    const [memoryValue, setMemoryValue] = useState('zero')
    const [recordsSelected, setRecordsSelected] = useState([])
    const [recordsActionSelected, setRecordsActionSelected] = useState([])
    const childRef = useRef<ChildRefType | null>(null);
    const [modelLimit, setModelLimit] = useState(20)
    const [modalTableOpen, setModalTableOpen] = useState(false)
    const [selectedRows, setSelectedRows] = useState([])
    const [modelOne, setModelOne] = useState(false);
    const [OpenActionDrawer, setOpenActionDrawer] = useState(false)
    const [sendButtonLoading, setSendButtonLoading] = useState(false)
    const [generateButtonLoading, setGenerateButtonLoading] = useState(false)
    const [openModalTable, setOpenModalTable] = useState(false)
    const [systemPromptVariables, setSystemPromptVariable] = useState('')
    const [chatId, setChatId] = useState('')
    const [tipSchema, setTipSchema] = useState(false)
    const [actionList, setActionList] = useState([])
    const [checkBoxValue, setCheckBoxValue] = useState([1, 2])
    const [contentValue, setContentValue] = useState('')
    const [drawerName, setDrawerName] = useState('')
    const [schema, setSchema] = useState('')
    const [custom, setCustom] = useState('')
    const [inputValueOne, setInputValueOne] = useState(20)
    const [inputValueTwo, setInputValueTwo] = useState(200)
    const [radioValue, setRadioValue] = useState('none')
    const [openCollectionDrawer, setOpenCollectionDrawer] = useState(false)
    const [updateRetrievalPrevButton, setUpdateRetrievalPrevButton] = useState(false)
    const [selectedRetrievalRows, setSelectedRetrievalRows] = useState([])
    const [hasMore, setHasMore] = useState(false)
    const [hasActionMore, setHasActionMore] = useState(false)
    const [hasModelMore, setHasModelMore] = useState(false)
    const [drawerDesc, setDrawerDesc] = useState('')
    const [contentTalk, setContentTalk] = useState([])
    const [contentHasMore, setContentHasMore] = useState(false)
    const [contentLoading, setContentLoading] = useState(false)
    const [contentTalkLoading, setContentTalkLoading] = useState(false)
    const [loading, setLoading] = useState(false)
    const [recordsSelected1, setRecordsSelected1] = useState([])
    const [systemPromptTemplate, setSystemPromptTemplate] = useState([]);
    const [openAssistantModalTable, setOpenAssistantModalTable] = useState(false)
    const { TextArea } = Input;
    const [OpenDeleteModal, setOpenDeleteModal] = useState(false)
    const [errorContent, setErrorContent] = useState('')
    const [updatePrevButton, setUpdatePrevButton] = useState(false)
    const [defaultSelectedAssistant, setDefaultSelectedAssistant] = useState([])
    const [modelHasMore, setModelHasMore] = useState(false)
    const [confirmLoading, setConfirmLoading] = useState(false);
    const [loadMoreHasMore, setLoadMoreHasMore] = useState(false)
    const [debugArray1, setDebugArray1] = useState([])
    const [debugArray2, setDebugArray2] = useState([])
    const [lottieAnimShow, setLottieAnimShow] = useState(false)
    const [contentDrawer, setContentDrawer] = useState(false)
    const [contentErrorDrawer, setContentErrorDrawer] = useState(false)
    const [chatCompletionCall, setChatCompletionCall] = useState('')
    const [chatCompletionResult, setChatCompletionResult] = useState('')
    const [collapseLabel1, setCollapseLabel1] = useState('')
    const [collapseLabel2, setCollapseLabel2] = useState('')
    const [noPreviousChat, setNoPreviousChat] = useState(false)
    const [noPreviousMessage, setNoPreviousMessage] = useState(false)
    const [generateFlag, setGenerateFlag] = useState(false)
    const [sendGenerateLoading, setSendGenerateLoading] = useState(false)
    const [groupedMessages, setGroupedMessages] = useState({
        role: 'Assistant',
        content: { text: [{ event_step: '', color: undefined, event_id: undefined }] },
        useId: 'user'
    });
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
    useEffect(() => {
        const handleClickOutside = (event) => {
            // Check if settingModal and settingIcon are defined and contain the event target
            if (!(settingModal.current && settingModal.current.contains(event.target)) && !(settingIcon.current && settingIcon.current.contains(event.target))) {
                // Additional check to ensure settingModal.current is defined before accessing its style
                if (settingModal.current) {
                    settingModal.current.style.display = 'none';
                }
            }
        };
    
        document.addEventListener('mousemove', handleClickOutside);
        return () => {
            document.removeEventListener('mousemove', handleClickOutside);
        };
    }, []);
    useEffect(() => {
        setCheckBoxValue([1, 2])
        initialFunction()
    }, [])
    useEffect(() => {
        if (generateFlag) {
            handleGenerateMessage('flag')
            setGenerateButtonLoading(false)
            setGenerateFlag(false)
        }
    }, [generateFlag])
    useEffect(() => {
        if (contentRef.current) {
            if (shouldSmoothScroll) {
                contentRef.current.scrollTop = contentRef.current.scrollHeight;
                contentRef.current.scrollTo({
                    top: contentRef.current.scrollHeight,
                    behavior: 'smooth',
                });
            }
        }
    }, [contentTalkLoading, contentTalk, shouldSmoothScroll]);
    const combineObjects = (item, arr) => {
        let updatedGroupedMessages = { ...groupedMessages };
        let str = ''
        const checkBoxValue1 = JSON.parse(localStorage.getItem('checkedValues')) || [1, 2]
        if (item.object === 'MessageGenerationLog') {
            setLottieAnimShow(true)
            const previousItems = arr.slice(0, arr.length - 1);
            const currentIsDuplicate = previousItems.some(existingItem => existingItem.event_id === item.event_id);
            if (!currentIsDuplicate) {
                const indexToInsert = Math.max(updatedGroupedMessages.content.text.length - 1, 0);
                item.color = 'orange'
                updatedGroupedMessages.content.text.splice(indexToInsert, 0, item);
            } else {
                const duplicateIndex = updatedGroupedMessages.content.text.findIndex(existingItem => existingItem.event_id === item.event_id);
                if (duplicateIndex !== -1) {
                    updatedGroupedMessages.content.text[duplicateIndex] = item;
                    updatedGroupedMessages.content.text[duplicateIndex].color = 'green'
                }
            }
        } else if (item.object === 'MessageChunk') {
            item.color = 'green'
            str += item.delta
            updatedGroupedMessages.content.text[updatedGroupedMessages.content.text.length - 1].event_step += str;
        } else if (item.object === 'Message' && checkBoxValue1.indexOf(1) === -1 && checkBoxValue1.indexOf(2) !== -1) {
            updatedGroupedMessages.content.text[updatedGroupedMessages.content.text.length - 1].event_step = item.content.text;
        } else if (item.object === 'Error') {
            setErrorContent(JSON.stringify(item, null, 4))
            setGenerateButtonLoading(false)
            setLottieAnimShow(false)
            updatedGroupedMessages.content.text[updatedGroupedMessages.content.text.length - 1].event_step = 'Error Occurred';
        }
        return updatedGroupedMessages;
    }
    const fetchAssistantsList = async () => {
        const res: any = await getAssistantsList({ limit: assistantLimit || 20 })
        const data = res.data.map((item) => {
            return {
                ...item,
                key: item.assistant_id
            }
        })

        setOptionList(data)
        setModelHasMore(res.has_more)
    }

    const initialFunction = async () => {
        fetchAssistantsList()

        const params = {
            limit: 20,
        }
        fetchModelsList(params)

        fetchActionsList(params)
        fetchDataRetrievalData(params)
        const queryParams = new URLSearchParams(search);
        const assistantId = queryParams.get('assistant_id')
        if (assistantId) {
            setAssistantId([assistantId])
            const res: any = await getListChats(assistantId, params)
            setListChats(res.data)
            setLoadMoreHasMore(res.has_more)
            setChatId(res.data[0]?.chat_id)
            const param1 = {
                order: 'desc',
                limit: 20
            }
            if (res.data[0]?.chat_id) {
                await fetchHistoryMessage(assistantId, res.data[0]?.chat_id, param1)
            }

        }
    }
    const fetchHistoryMessage = async (assistantId, chatId, param) => {
        if (param.after) {
            setShouldSmoothScroll(false)
        } else {
            setShouldSmoothScroll(true)
        }
        const res: any = await getHistoryMessage(assistantId, chatId, param)
        const data = res.data.reverse()
        setContentHasMore(res.has_more)
        setContentTalk(prevValues => [...data, ...prevValues])
    }
    const handleSelectAssistantID = () => {
        if (assistantId) {
            const id = assistantId[0].split('-')[1] ? assistantId[0].split('-')[1] : assistantId[0]
            setDefaultSelectedAssistant([id])
            setRecordsSelected([id])
        } else {
            setDefaultSelectedAssistant([])
            setRecordsSelected([])
        }
        setOpenAssistantModalTable(true)
        setUpdatePrevButton(false)
    }
    const handleSelectModelId = (value) => {
        setModalTableOpen(value)
    }
    const handleChildAssistantEvent = async (value: Record<string, any>) => {
        await fetchAssistantsList()
        setUpdatePrevButton(false)
        setAssistantLimit(value.limit)
    }
    const combineObjectsWithSameMsgId = (arr) => {
        let groupedMessages = { role: 'Assistant', content: { text: '' } };
        arr.forEach((item) => {
            if (item.object === 'MessageChunk') {
                groupedMessages.content.text += item.delta
            }
        });
        return groupedMessages
    }


    const handleModalCancel = (a) => {
        setModelOne(a)
    }
    const handleChildModelEvent = async (value) => {
        await fetchModelsList(value)
        setUpdateModelPrevButton(false)
        setModelLimit(value.limit)
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
    const fetchModelsList = async (params) => {

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

    const handleEditAssistant = async () => {
        setLoading(true)
        let id;
        if (assistantId[0].split('-')[1]) {
            const splitArray = assistantId[0].split('-')
            id = splitArray.slice(-1)[0]
        } else {
            id = assistantId[0]
        }
        const res = await getAssistantDetail(id)
        const { data } = res
        const { name, description, model_id, system_prompt_template, tools, retrievals, memory } = data
        setDrawerName(name)
        setDrawerDesc(description)
        setSelectedRows(model_id)
        setMemoryValue(memory.type)
        setInputValueOne(memory.max_messages)
        setInputValueTwo(memory.max_tokens)
        if (system_prompt_template.length === 0) {
            setSystemPromptTemplate([''])
        } else {
            setSystemPromptTemplate(system_prompt_template)
        }
        setSelectedActionsRows(tools.map(item => item.id))
        const tag = retrievals.map(item => item.id)
        setRecordsSelected1(tag)

        setSelectedRetrievalRows(tag)
        setLoading(false)
        setOpenDrawer(true)
    }

    const handleCancel = () => {
        setOpenDrawer(false)
    }

    const handleDeletePromptInput = (index) => {
        const updatedInputValues = [...systemPromptTemplate];
        updatedInputValues.splice(index, 1);
        setSystemPromptTemplate(updatedInputValues);
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
        let systemPromptTemplate1;
        if (systemPromptTemplate.length === 0 && systemPromptTemplate[0] === '') {
            systemPromptTemplate1 = []
        } else {
            systemPromptTemplate1 = systemPromptTemplate
        }
        const params = {
            model_id: Array.isArray(selectedRows) ? selectedRows[0].slice(-8) : selectedRows,
            name: drawerName || '',
            description: drawerDesc || '',
            system_prompt_template: systemPromptTemplate1,
            tools: inputPluginValues,
            retrievals: inputValueMap,
            memory: {
                type: memoryValue,
                max_messages: Number(inputValueOne) || undefined,
                max_tokens: Number(inputValueTwo) || undefined
            }
        }

        let id;
        if (assistantId[0].split('-')[1]) {
            const splitArray = assistantId[0].split('-')
            id = splitArray.slice(-1)[0]
        } else {
            id = assistantId[0]
        }
        try {
            await updateAssistant(id, params)
            await fetchAssistantsList()
            await handleListChats()
            setOpenDrawer(false)
        } catch (error) {
            console.log(error)
            const apiError = error as ApiErrorResponse;
            const errorMessage: string = apiError.response.data.error.message;
            toast.error(errorMessage)
        }
    }
    const handleNewChat = async () => {
        if (!assistantId) {
            return toast.error('Please select an assistant')
        }
        setLoading(true)
        const params = {
            metadata: {}
        }
        let id;
        if (assistantId[0].split('-')[1]) {
            const splitArray = assistantId[0].split('-')
            id = splitArray.slice(-1)[0]
        } else {
            id = assistantId[0]
        }
        try {
            const res = await openChat(id, params)
            const { data } = res
            setListChats(prevValues => [{ chat_id: data.chat_id, created_timestamp: data.created_timestamp }, ...prevValues])
            setChatId(data.chat_id)
            setContentTalk([])
            setContentHasMore(false)
            setGenerateButtonLoading(false)
        } catch (error) {
            console.log(error)
        }
        setLoading(false)
    }
    const handleCreateMessage = async (flag?: any) => {
        const params = {
            role: 'user',
            content: {
                text: contentValue
            },
            metadata: {}
        }
        if (contentValue === '') {
            toast.error('Empty message is not allowed')
            throw new Error('Empty message is not allowed');
        }
        if (sendButtonLoading) {
            throw new Error('Please wait for the assistant to respond.');
        }
        try {
            if (flag === 'flag') {
                setSendGenerateLoading(true)
            } else {
                setSendButtonLoading(true)
            }
            let id;
            if (assistantId[0].split('-')[1]) {
                const splitArray = assistantId[0].split('-')
                id = splitArray.slice(-1)[0]
            } else {
                id = assistantId[0]
            }
            const res = await sendMessage(id, chatId, params)
            const { data } = res
            setContentTalk(prevValues => [...prevValues, {
                role: 'user',
                content: { text: data.content.text },
                userId: true,
                flag: true
            }])
            if (flag === 'flag') {
                setGenerateFlag(true)
            } else {
                setGenerateFlag(false)
            }
            setContentValue('')
        } catch (error) {
            console.log(error)
        }
        setSendButtonLoading(false)
    }
    const handleInputPromptChange = (index, newValue) => {
        setSystemPromptTemplate((prevValues) =>
            prevValues.map((item, i) =>
                i === index ? newValue : item
            )
        );
    };
    const handleCreateModelId = async (e) => {
        e.stopPropagation()
        await setModelOne(true)
        childRef.current?.fetchAiModelsList()
        const params = {
            limit: modelLimit || 20
        }
        await fetchModelsList(params)
    }

    const handleGenerateMessage = async (contentTalk1?: any) => {
        if (generateButtonLoading) {
            return toast.error('Please wait for the assistant to respond.')
        }
        if (contentTalk1 !== 'flag' && contentTalk[contentTalk.length - 1]?.role.toLowerCase() === 'assistant') {
            return toast.error('Please send the user message first.')
        }
        let id;
        if (assistantId[0].split('-')[1]) {
            const splitArray = assistantId[0].split('-')
            id = splitArray.slice(-1)[0]
        } else {
            id = assistantId[0]
        }

        const token = localStorage.getItem('token')
        const project_base_url = `api/v1`
        setGenerateButtonLoading(true)
        let stream = false
        let debug = false
        const checkBoxValue1 = JSON.parse(localStorage.getItem('checkedValues')) || checkBoxValue
        checkBoxValue1.indexOf(1) !== -1 ? stream = true : stream = false
        checkBoxValue1.indexOf(2) !== -1 ? debug = true : debug = false

        const params = {
            system_prompt_variables: systemPromptVariables ? JSON.parse(systemPromptVariables) : {},
            stream: stream,
            debug: debug
        }

        let source;
        if (stream || debug) {
            source = new SSE(`${origin}/${project_base_url}/assistants/${id}/chats/${chatId}/generate`, {
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
                method: "POST",
                payload: JSON.stringify(params)
            })
            source.addEventListener('error', (e) => {
                setGenerateButtonLoading(false)
                setSendGenerateLoading(false)
                console.log(e)
                if (e.data) {
                    toast.error(JSON.parse(e.data).error.message, { autoClose: 10000 })
                }
            })
        }

        if (!stream && !debug) {
            try {
                const res = await generateMessage(id, chatId, params)
                const { data } = res
                setContentTalk(prevValues => [...prevValues, {
                    role: 'Assistant',
                    content: {
                        text: data.content.text
                    },
                    userId: false,
                    flag: true
                }])
            } catch (error) {
                console.log(error)
            } finally {
                setGenerateButtonLoading(false)
                setSendGenerateLoading(false)
            }
        } else if (stream && !debug) {
            let arr = []
            source.addEventListener("message", (e) => {
                if (e.data === '[DONE]') {
                    setGenerateButtonLoading(false)
                    setSendGenerateLoading(false)

                    return
                }
                const exJson = JSON.parse(e.data);
                arr.push(exJson)
                const comb = combineObjectsWithSameMsgId(arr)
                const binedArr = [...contentTalk, comb]
                setContentTalk(binedArr)
            }

            );
        } else if (!stream && debug) {
            let arr1 = []
            source.addEventListener("message", (e) => {
                if (e.data === '[DONE]') {
                    setGenerateButtonLoading(false)
                    setSendGenerateLoading(false)
                    return
                }
                const data = JSON.parse(e.data)
                if (data.object === 'MessageGenerationLog') {
                    setDebugArray1(prevValues => [...prevValues, data])
                }
                arr1.push(data)
                const binedArr = [...contentTalk, combineObjects(data, arr1)]
                setContentTalk(binedArr)

            })
        } else {
            let arr1 = []
            source.addEventListener("message", (e) => {
                if (e.data === '[DONE]') {
                    setGenerateButtonLoading(false)
                    setSendGenerateLoading(false)
                    return
                }
                const data = JSON.parse(e.data)

                if (data.object === 'MessageGenerationLog') {
                    setDebugArray2(prevValues => [...prevValues, data])
                }
                arr1.push(data)
                const binedArr = [...contentTalk, combineObjects(data, arr1)]
                setContentTalk(binedArr)

            })
        }
        setGroupedMessages({
            role: 'Assistant',
            content: { text: [{ event_step: '', color: undefined, event_id: undefined }] },
            useId: 'user'
        })

    }
    const handleDescriptionChange = (value) => {
        setDrawerDesc(value)
    }
    const handleModalTable = (value) => {
        setOpenModalTable(value)
    }
    const handleCreateConfrim = () => {
        setOpenModalTable(false)
    }
    const hangleFilterData = (value) => {
        setRetrievalList(value)
    }
    const handleChildRetrievalEvent = async (value) => {
        setRetrievalLimit(value.limit)
        await fetchDataRetrievalData(value)
        setUpdateRetrievalPrevButton(false)

    }
    const handleChildActionEvent = async (value) => {
        await fetchActionsList(value)
        setUpdateActionPrevButton(false)
        setActionLimit(value.limit)

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
    const handleChangeName = (value) => {
        setDrawerName(value)
    }
    const handleModalClose = () => {
        setModalTableOpen(false)
    }
    const handleAssistantModalClose = () => {
        const queryParams = new URLSearchParams(search);
        const assistantId = queryParams.get('assistant_id')
        if (!assistantId) {
            setAssistantId('')
        }
        setDefaultSelectedAssistant([])

        setOpenAssistantModalTable(false)
    }
    const handleListChats = async () => {
        const splitArray = assistantId[0].split('-')
        const id = splitArray.slice(-1)[0]
        const res = await getListChats(id, { limit: 20 })
        setListChats(res.data)
        setChatId(res.data[0]?.chat_id)
        const param = {
            order: 'asc',
        }
        if (res.data[0]) {
            const res1 = await getHistoryMessage(id, res.data[0]?.chat_id, param)
            setContentTalk(res1.data)
        }
    }
    const handleAssistantModalClose1 = async () => {
        const splitArray = assistantId[0].split('-')
        const id = splitArray.slice(-1)[0]
        navigation(`${pathname}?assistant_id=${id}`)
        // setAssistantId(tempAssistantId)
        // console.log(tempAssistantId)
        setConfirmLoading(true)
        try {
            await handleListChats()
        } catch (e) {
            console.log(e)
        }
        setDefaultSelectedAssistant(id)
        setOpenAssistantModalTable(false)
        setConfirmLoading(false)
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
                content: undefined,
                secret: undefined
            }
        };
        if (radioValue === 'custom') {
            if (commonData.authentication) {
                commonData.authentication.content = { [custom]: Authentication };
            }
        } else {
            if (radioValue === 'none') {
                commonData.authentication = undefined
            } else {
                if (commonData.authentication) {
                    commonData.authentication.secret = Authentication;
                }
            }
        }
        try {
            await createActions(commonData);
            const params = {
                limit: actionLimit || 20,
            }
            await fetchActionsList(params);
        } catch (error: any) {
            console.error(error);
            toast.error(error.message)
        }

        setOpenDrawer(false)
    }
    const handleNewModal = () => {
        setOpenCollectionDrawer(true)
    }
    const handleCloseModal = () => {
        setOpenModalTable(false)
    }
    const hangleChangeAuthorization = (value: string) => {
        setAuthentication(value)
    }
    const handleRecordsSelected = (value, selectedRows) => {
        setRecordsSelected(value)
        const tag = selectedRows.map(item => (item.name + '-' + item.model_id))
        setSelectedRows(tag)
    }
    const handleActionRecordsSelected = (value, selectedRows) => {
        setRecordsSelected(value)
        const tag = selectedRows.map(item => (item.name + '-' + item.action_id))
        setRecordsActionSelected(tag)
        setSelectedActionsRows(tag)
    }
    const handleRecordsAssistantSelected = (_value, selectedRows) => {
        setRecordsSelected(selectedRows)
        const tag = selectedRows.map(item => (item.name + '-' + item.assistant_id))
        setAssistantId(tag)
        setDefaultSelectedAssistant(tag)
    }
    const handleCustom = (value: string) => {
        setCustom(value)
    }
    const handleCollectionSelected = (value, selectedRows) => {
        setRecordsSelected1(value)
        const tag = selectedRows.map(item => (item.name + '-' + item.collection_id))
        setSelectedRetrievalRows(tag)
    }
    const handleMemoryChange1 = (value) => {
        setMemoryValue(value)
    }
    const handleSchemaChange = (value: string) => {
        setSchema(value)
    }
    const handleCreateAction = () => {
        setSchema('')
        setRadioValue('none')
        setAuthentication('')
        setOpenActionDrawer(true)
    }
    const handleAddPrompt = () => {
        if (systemPromptTemplate.length < 10) {
            setSystemPromptTemplate((prevValues => [...prevValues, '']))
        }
    }
    const handleOpenChat = async (value) => {
        setChatId(value)
        setContentTalkLoading(true)
        let id;
        if (assistantId[0].split('-')[1]) {
            const splitArray = assistantId[0].split('-')
            id = splitArray.slice(-1)[0]
        } else {
            id = assistantId[0]
        }
        const param = {
            order: 'desc',
            limit: 20
        }
        setContentTalk([])
        setGenerateButtonLoading(false)
        setSendGenerateLoading(false)
        await fetchHistoryMessage(id, value, param)
        setContentTalkLoading(false)
    }
    const handleMouseEnter = () => {
        settingModal.current.style.display = 'block'
    };
    const handleActionCancel = () => {
        setOpenActionDrawer(false)
    }
    const handleLodaMore = async () => {
        const params = {
            limit: 20,
            after: listChats[listChats.length - 1].chat_id
        }
        let id;
        if (assistantId[0].split('-')[1]) {
            const splitArray = assistantId[0].split('-')
            id = splitArray.slice(-1)[0]
        } else {
            id = assistantId[0]
        }
        setNoPreviousChat(true)
        const res: any = await getListChats(id, params)
        setListChats(prevValues => [...prevValues, ...res.data])
        setLoadMoreHasMore(res.has_more)
    }
    const handleContentLodaMore = async () => {
        setContentLoading(true)
        const params = {
            limit: 20,
            order: 'desc',
            after: contentTalk[0]?.message_id
        }
        setNoPreviousMessage(true)
        fetchHistoryMessage(assistantId, chatId, params)
        setContentLoading(false)
    }
    const handleInputValueOne = (value) => {
        setInputValueOne(value)
    }
    const handleInputValueTwo = (value) => {
        setInputValueTwo(value)
    }
    const onRadioChange = (value: string) => {
        setRadioValue(value)
    }
    const handleActionModalTable = () => {
        setModalActionTableOpen(true)
        setRecordsActionSelected(selectedActionsRows)
    }
    const handleActionModalClose = () => {
        setModalActionTableOpen(false)
    }
    const handleChangeCheckbox = (checkedValues) => {
        localStorage.setItem('checkedValues', JSON.stringify(checkedValues))
    }
    const onDeleteCancel = () => {
        setOpenDeleteModal(false)
    }
    const onDeleteConfirm = async () => {
        try {
            let id;
            if (assistantId[0].split('-')[1]) {
                const splitArray = assistantId[0].split('-')
                id = splitArray.slice(-1)[0]
            } else {
                id = assistantId[0]
            }
            await deleteChatItem(id, chatId)
            const res: any = await getListChats(id, { limit: 20 })
            setListChats(res.data)
            setLoadMoreHasMore(res.has_more)
            setChatId(res.data[0]?.chat_id)
            const param1 = {
                order: 'desc',
                limit: 20
            }
            if (res.data[0]?.chat_id) {
                await fetchHistoryMessage(assistantId, res.data[0]?.chat_id, param1)
            }

        } catch (error) {
            console.log(error)
        }
        setOpenDeleteModal(false)
    }
    const handleClickDebug = (item) => {
        if (item.event_step === 'Error Occurred') {
            setContentErrorDrawer(true)
        } else {
            delete item.color
            setCollapseLabel2(item.event_step)
            if (!item.event_id) return
            const data1 = debugArray1.find(item1 => (item1.event_id === item.event_id))
            const data2 = debugArray2.find(item1 => (item1.event_id === item.event_id))
            if (data1) {
                delete data1.color
                const data3 = JSON.stringify(data1, null, 4)
                setChatCompletionCall(data3)
                const label = data1.event_step
                setCollapseLabel1(label)
            } else if (data2) {
                delete data2.color
                const data4 = JSON.stringify(data2, null, 4)
                const label = data2.event_step
                setCollapseLabel1(label)
                setChatCompletionCall(data4)
            }
            setChatCompletionResult(JSON.stringify(item, null, 4))
            setContentDrawer(true)
        }
    }
    const handleCloseContentDrawer = () => {
        setContentDrawer(false)
    }
    const onhandleTipError = (value: boolean) => {
        setTipSchema(value)
    }
    const handleCloseContentErrorDrawer = () => {
        setContentErrorDrawer(false)
    }
    const handleDeleteChat = async () => {
        setOpenDeleteModal(true)
    }
    const handleSetModelConfirmOne = () => {
        setModelOne(false)
        setUpdateRetrievalPrevButton(true)
    }
    const handleSendAndGenerateMessage = async () => {
        if (sendButtonLoading || generateButtonLoading) {
            return toast.error('Please wait for the info to respond.')
        }
        try {
            await handleCreateMessage('flag')
        } catch (error) {
            console.log(error)
        }
    }
    return (
        <Spin spinning={loading}>
            {!assistantId ? <div className={styles['selectAssistant']}>
                {<PlayGroundImg className={styles.svg} />}
                <div className={styles['select-assistant']}>Select an assistant to start.</div>
                <div className={styles['header-news']}>
                    <div className={styles['plusParent']}>
                        <Button icon={<PlusOutlined />} className={styles['prompt-button']} onClick={handleSelectAssistantID}>Select assistant</Button>
                    </div>
                </div>
            </div> : <div className={styles['playground']}>
                <div className={styles['left-content']}>
                    <div className={styles['top']}>
                        <div className={styles['select-assistant']}>Assistant</div>
                        {!assistantId && <div className={styles['select-desc']}>Select or enter a valid assistant ID to start chatting</div>}
                        <div style={{ display: 'flex', alignItems: 'center' }}>
                            <Select open={false} suffixIcon={<RightOutlined />} onClick={handleSelectAssistantID} value={assistantId} className={styles['select']} removeIcon={null}>
                            </Select>
                            {assistantId && <Button icon={<EditIcon />} onClick={handleEditAssistant} className={styles['edit-button']}></Button>}
                        </div>
                    </div>
                    <div className={styles['bottom']}>
                        <div className={styles['bottom-chats']}>
                            <div>Chats</div>
                            <div className={styles['actionbuttondownload']} onClick={handleNewChat}>
                                <PlusOutlined />
                                <div className={styles['text1']}>New chat</div>
                            </div>
                        </div>
                        <div className={styles['chats']}>
                            <div className={styles['chat-message']}>
                                {listChats?.map((item, index) => (<div key={index} className={`${styles.functionaliconsParent} ${chatId === item.chat_id && styles.chatId}`} onClick={() => handleOpenChat(item.chat_id)}>
                                    <ChatIcon className={styles['functionalicons']}></ChatIcon>
                                    <div className={styles['Parent']}>
                                        <div className={styles['son']}>{item.chat_id}</div>
                                        <div className={styles['son1']}>{formatTimestamp(item.created_timestamp)}</div>
                                    </div>
                                </div>))}
                                {(!loadMoreHasMore && noPreviousChat) && <div className={styles['lineParent']}>
                                    <div className={styles['frameChild']} />
                                    <div className={styles['noPreviousChat1']}>No previous chat</div>
                                    <div className={styles['frameChild']} />
                                </div>}
                            </div>
                            {loadMoreHasMore && <div className={styles['lineParent']} style={{ marginTop: '10px' }}>
                                <div className={styles['frameChild']} />
                                <div className={styles['formbuttoncancel']} onClick={handleLodaMore}>
                                    <div className={styles['text1']}>Load more</div>
                                </div>
                                <div className={styles['frameChild']} />
                            </div>}
                        </div>

                    </div>
                </div>
                <div className={styles['right-content']}>
                    <div className={styles['header-top']}>
                        <div className={styles['header-left']}>
                            <span className={styles['chat']}>Chat</span>
                            <span className={styles['desc']}>{chatId}</span>
                            <CopyOutlined className='icon-copy' onClick={() => handleCopy(chatId)} />
                        </div>

                        <div className={styles['header-right']} onClick={handleDeleteChat}>
                            <Button icon={<DeleteIcon />} className='cancel-button'>Delete chat</Button>
                        </div>
                    </div>
                    {!chatId && <div className={styles['content-center']}>
                        <div className={styles['content-img']}>
                            <PlaygroundImg />
                            <div className={styles['waiting-for-configuration']}>Waiting for Configuration</div>
                        </div>
                    </div>}
                    {chatId &&
                        <Spin spinning={contentTalkLoading}>
                            <div className={styles['content-talk']} ref={contentRef}>
                                <div style={{ display: 'flex', justifyContent: 'center' }}>
                                    <Spin spinning={contentLoading} />
                                </div>
                                {(!contentHasMore && noPreviousMessage) && <div className={styles['lineParent']}>
                                    <div className={styles['frameChild']} />
                                    <div className={styles['noPreviousChat1']}>No previous message </div>
                                    <div className={styles['frameChild']} />
                                </div>}
                                {contentHasMore && <div className={styles['lineParent']} style={{ marginTop: '10px' }}>
                                    <div className={styles['frameChild']} />
                                    <div className={styles['formbuttoncancel']} onClick={handleContentLodaMore}>
                                        <div className={styles['text1']}>Load more</div>
                                    </div>
                                    <div className={styles['frameChild']} />
                                </div>}
                                {contentTalk.map((item, index) => (
                                    <div className={styles['message']} key={index} ref={divRef}>
                                        <div className={`${styles.subText1} ${item.role === 'user' ? 'user' : ''}`}>{item.role.charAt(0).toUpperCase() + item.role.slice(1)}</div>
                                        {typeof (item.content.text) === 'string' && <div className={`${styles.text1} ${item.role === 'user' ? styles.userInfo : ''}`} style={{ whiteSpace: "pre-line" }}>{item.content.text}</div>}
                                        {typeof (item.content.text) === 'object' && <div className={`text1 ${item.role === 'user' ? styles.userInfo : ''}`}>{item.content.text.map((item1, index1) => (<div key={index1} className={`${(item1.color === 'orange' && index === contentTalk.length - 1) ? 'orange' : 'green'} ${index1 === item.content.text.length - 1 && styles.lastItem}`}>
                                            {(item1.color === 'orange' && index === contentTalk.length - 1 && item1.event_step !== '') ?
                                                (<div style={{ display: 'flex', alignItems: 'center' }}>{lottieAnimShow && (
                                                    <>
                                                        {<LoadingAnim className={styles['loading-icon']} />}
                                                        {item1.event_step}
                                                    </>
                                                )}
                                                </div>) :
                                                (
                                                    item1.color !== 'orange' && (<div onClick={() => handleClickDebug(item1)} style={{ display: 'flex', alignItems: 'center' }}>
                                                        {(item1.event_step !== 'Error Occurred') && (<> {index1 !== item.content.text.length - 1 && <MessageSuccess className={styles['message-success']} />}<span style={{ cursor: index1 !== item.content.text.length - 1 ? 'pointer' : 'text', whiteSpace: "pre-line" }}>{item1.event_step}</span></>)}
                                                        {(item1.event_step === 'Error Occurred') && (<><ErrorIcon className={styles['message-success']}></ErrorIcon><span style={{ color: '#ec1943', cursor: 'pointer' }}>Error Occurred</span></>)}
                                                    </div>
                                                    )
                                                )

                                            }</div>))}</div>}
                                    </div>
                                ))}
                            </div>
                        </Spin>
                    }

                    <div className={`${styles['content-bottom']} ${!chatId ? styles.none : ''}`}>
                        <TextArea className={styles['textarea']} autoSize={{ minRows: 3, maxRows: 6 }} value={contentValue} onChange={(e) => setContentValue(e.target.value)}></TextArea>
                        <div className={styles['button-group']}>
                            <div style={{ display: 'flex' }}>
                                <Button className={`next-button ${styles.button}`} onClick={handleSendAndGenerateMessage} loading={sendGenerateLoading}>Send and Generate</Button>
                                <div className={`${styles.formbuttoncancel} ${sendButtonLoading ? styles.loading : ''}`} onClick={handleCreateMessage}>
                                    {sendButtonLoading && <LoadingOutlined style={{ marginRight: '3px' }} />}  <div className={styles['text1']}>Send</div>
                                </div>
                                <div className={`${styles.formbuttoncancel} ${styles.button1} ${generateButtonLoading ? styles.loading : ''}`} onClick={handleGenerateMessage}>
                                    {generateButtonLoading && <LoadingOutlined style={{ marginRight: '3px' }} />}<div className={styles['text1']}>Generate</div>
                                </div>
                            </div>
                            <div className={styles['actionbuttonedit']} onMouseEnter={handleMouseEnter} ref={settingIcon}>
                                <ModalSettingIcon className={styles['functionalicons']} />
                            </div>
                        </div>
                        <div className={styles['setting-modal']} ref={settingModal} style={{ display: 'none' }}>
                            <div className={styles['generation-options']}>
                                Generation options
                            </div>
                            <div className={styles['desc']}>Select the type of messages that will be returned to the frontend.</div>
                            <Checkbox.Group onChange={handleChangeCheckbox} options={plainOptions} defaultValue={JSON.parse(localStorage.getItem('checkedValues')) || checkBoxValue} />
                            <div className={styles['select-assistant']}>Prompt variables</div>
                            <TextArea style={{ height: '300px' }} placeholder={`{\n   key: value\n}`}
                                value={systemPromptVariables} onChange={(e) => setSystemPromptVariable(e.target.value)}></TextArea>
                        </div>
                    </div>
                </div>
            </div>}


            <Drawer
                closeIcon={<img src={closeIcon} alt="closeIcon" className='img-icon-close' />}
                className={styles['assistant-drawer']}
                onClose={handleCancel} title='Edit Assistant' placement="right" open={OpenDrawer} size='large' footer={<ModalFooterEnd handleOk={() => handleRequest()} onCancel={handleCancel} />}>
                <DrawerAssistant selectedActionsRows={selectedActionsRows} memoryValue={memoryValue} inputValue1={inputValueOne} handleMemoryChange1={handleMemoryChange1} inputValue2={inputValueTwo} handleInputValueOne={handleInputValueOne} handleInputValueTwo={handleInputValueTwo} handleAddPromptInput={handleAddPrompt} handleActionModalTable={handleActionModalTable} drawerName={drawerName} systemPromptTemplate={systemPromptTemplate} handleDeletePromptInput={handleDeletePromptInput} handleInputPromptChange={handleInputPromptChange} selectedRows={selectedRows} handleSelectModelId={handleSelectModelId} handleChangeName={handleChangeName} drawerDesc={drawerDesc} handleDescriptionChange={handleDescriptionChange} handleModalTable={handleModalTable} selectedRetrievalRows={selectedRetrievalRows}></DrawerAssistant>
            </Drawer>
            <ModelModal handleSetModelConfirmOne={handleSetModelConfirmOne} ref={childRef} open={modelOne} handleSetModelOne={handleModalCancel} getOptionsList={fetchModelsList} modelType='chat_completion'></ModelModal>
            <Modal closeIcon={<img src={closeIcon} alt="closeIcon" className='img-icon-close' />} centered footer={[
                <div className='footer-group' key='footer-group'>
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
                <ModalTable name='Collection' updatePrevButton={updateRetrievalPrevButton} defaultSelectedRowKeys={selectedRetrievalRows} hangleFilterData={hangleFilterData} mode='multiple' handleRecordsSelected={handleCollectionSelected} ifSelect={true} columns={collectionTableColumn} dataSource={retrievalList} hasMore={hasMore} id='collection_id' onChildEvent={handleChildRetrievalEvent} />
            </Modal>
            <Modal closeIcon={<img src={closeIcon} alt="closeIcon" className={styles['img-icon-close']} />} centered footer={[
                <div className='footer-group' key='footer'>
                    <Button key="model" icon={<PlusOutlined />} onClick={handleCreateAction} className='cancel-button'>
                        New Action
                    </Button>
                    <div>
                        <span className='select-record'>
                            {recordsActionSelected.length}  {recordsActionSelected.length > 1 ? 'items' : 'item'} selected
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
                <ModalTable updatePrevButton={updateActionPrevButton} defaultSelectedRowKeys={selectedActionsRows} mode='multiple' handleRecordsSelected={handleActionRecordsSelected} ifSelect={true} columns={actionsTableColumn} hasMore={hasActionMore} id='action_id' dataSource={actionList} onChildEvent={handleChildActionEvent}></ModalTable>
            </Modal>
            <Modal closeIcon={<img src={closeIcon} alt="closeIcon" className={styles['img-icon-close']} />} centered onCancel={handleModalClose} footer={[
                <div className='footer-group' key='group'>
                    <Button key="model" icon={<PlusOutlined />} onClick={handleCreateModelId} className='cancel-button'>
                        New model
                    </Button>
                    <div>
                        <span className='select-record'>
                            1 item selected
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
                <ModalTable name="model" defaultSelectedRowKeys={Array.isArray(selectedRows) ? selectedRows : [selectedRows]} updatePrevButton={updateModelPrevButton} handleRecordsSelected={handleRecordsSelected} ifSelect={true} columns={modelsTableColumn} hasMore={hasModelMore} id='model_id' dataSource={options} onChildEvent={handleChildModelEvent}></ModalTable>
            </Modal>
            <Drawer className={styles.drawerCreate} closeIcon={<img src={closeIcon} alt="closeIcon" className={styles['img-icon-close']} />} onClose={handleActionCancel} title='Bulk Create Action' placement="right" open={OpenActionDrawer} size='large' footer={<ModalFooterEnd handleOk={() => handleActionRequest()} onCancel={handleActionCancel} />}>
                <ActionDrawer showTipError={tipSchema} onhandleTipError={onhandleTipError} drawerTitle={'Bulk Create Action'} schema={schema} onSchemaChange={handleSchemaChange} onRadioChange={onRadioChange} onChangeCustom={handleCustom} onChangeAuthentication={hangleChangeAuthorization} radioValue={radioValue} custom={custom} Authentication={Authentication} />
            </Drawer>
            <Modal closeIcon={<img src={closeIcon} alt="closeIcon" className={styles['img-icon-close']} />} onCancel={handleAssistantModalClose} centered footer={[
                <div className='footer-group' style={{ justifyContent: 'flex-end' }} key='footer'>
                    <div>
                        <span className='select-record'>
                            {recordsSelected.length} item selected
                        </span>
                        <Button key="cancel" onClick={handleAssistantModalClose} className={`cancel-button ${styles.cancelButton}`}>
                            Cancel
                        </Button>
                        <Button key="submit" onClick={handleAssistantModalClose1} className='next-button' loading={confirmLoading}>
                            Confirm
                        </Button>
                    </div>

                </div>

            ]} title='Select Assistant' open={openAssistantModalTable} width={1000} className={`modal-inner-table ${styles.model1}`}>
                <ModalTable name='Assistant' ifAllowNew={true} updatePrevButton={updatePrevButton} defaultSelectedRowKeys={defaultSelectedAssistant} handleRecordsSelected={handleRecordsAssistantSelected} ifSelect={true} columns={assistantTableColumn} hasMore={modelHasMore} id='assistant_id' dataSource={optionList} onChildEvent={handleChildAssistantEvent}></ModalTable>
            </Modal>
            <CreateCollection handleFetchData={() => fetchDataRetrievalData({ limit: retrievalLimit || 20 })} handleModalCloseOrOpen={() => setOpenCollectionDrawer(false)} OpenDrawer={openCollectionDrawer}></CreateCollection>
            <Drawer width={700} open={contentDrawer} closeIcon={<img src={closeIcon} alt="closeIcon" className={styles['img-icon-close']} />} onClose={handleCloseContentDrawer} title='Chat Completion'>
                <Collapse expandIconPosition='end' items={[
                    {
                        key: '1',
                        label: collapseLabel1,
                        children: <div className={styles['content-drawer']}>
                            <div className={styles['content']}>
                                <CopyOutlined className='icon-copy' onClick={() => handleCopy(chatCompletionCall)} />
                            </div>
                            <TextArea autoSize={true} value={chatCompletionCall} disabled />
                        </div>
                    }]}></Collapse>
                <Collapse className={styles['collapse-drawer']} expandIconPosition='end' items={[
                    {
                        key: '2',
                        label: collapseLabel2,
                        children: <div className={styles['content-drawer']}>
                            <div className={styles['content']}>
                                <CopyOutlined className='icon-copy' onClick={() => handleCopy(chatCompletionResult)} />
                            </div>
                            <TextArea autoSize={true} value={chatCompletionResult} disabled />
                        </div>
                    }]}></Collapse>

            </Drawer>
            <Drawer width={700} open={contentErrorDrawer} closeIcon={<img src={closeIcon} alt="closeIcon" className={styles['img-icon-close']} />} onClose={handleCloseContentErrorDrawer} title='Chat Completion'>
                <Collapse expandIconPosition='end' items={[
                    {
                        key: '1',
                        label: 'Error Occurred',
                        children: <div className={styles['content-drawer']}>
                            <div className={styles['content']}>
                                <CopyOutlined className='icon-copy' onClick={() => handleCopy(errorContent)} />
                            </div>
                            <TextArea autoSize={true} value={errorContent} disabled />
                        </div>
                    }]}></Collapse>
            </Drawer>
            <DeleteModal title='Delete Chat' projectName={chatId} open={OpenDeleteModal} describe={`Are you sure you want to delete chat ${chatId}`} onDeleteCancel={onDeleteCancel} onDeleteConfirm={onDeleteConfirm}></DeleteModal>
        </Spin >
    );
}
export default Playground;