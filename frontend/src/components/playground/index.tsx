import styles from './playground.module.scss'
import { useState, useEffect, useRef, } from 'react'
import { Select, Button, Checkbox, Input, Drawer, Spin, Modal, Collapse, Space, Upload, Image } from 'antd'
import { PlusOutlined, RightOutlined, LoadingOutlined, SearchOutlined, EyeOutlined } from '@ant-design/icons';
import PlayGroundImg from '@/assets/img/selectAssistantImg.svg?react'
import { FullApiResponse } from '@/constant/index.ts'
import type { GetProp, UploadProps } from 'antd';
import { toast } from 'react-toastify';
import { getPluginList } from '../../axios/plugin.ts'
import CreatePlugin from '../createPlugin/index.tsx';
import { setPlaygroundSelect, setPlaygroundAssistantId, } from '@/Redux/actions/playground.ts'
import PlaygroundModel from '../playgroundModel/index.tsx';
import CopyOutlined from '../../assets/img/copyIcon.svg?react'
import ModelModal from '../modelModal/index'
import ErrorIcon from '../../assets/img/errorIcon.svg?react'
import { getModelsList } from '../../axios/models.ts'
import CreateCollection from '../createCollection/index.tsx';
import ModalSettingIcon from '../../assets/img/modalSettingIcon.svg?react'
import { formatTimestamp, getFirstMethodAndEndpoint } from '@/utils/util'
import ModalTable from '../modalTable/index'
import { commonDataType } from '@/constant/assistant.ts'
import LoadingAnim from '../../assets/img/loadingAnim.svg?react'
import ApiErrorResponse, { ChildRefType } from '../../constant/index.ts'
import ChatIcon from '../../assets/img/chatIcon.svg?react'
import { getActionsList, createActions } from '../../axios/actions.ts'
import { getRetrievalList } from '../../axios/retrieval.ts';
import PlaygroundImg from '@/assets/img/playgroundImg.svg?react'
import { openChat, sendMessage, generateMessage, getListChats, getHistoryMessage, getChatItem, deleteChatItem } from '@/axios/playground'
import { getAssistantDetail, updateAssistant, getAssistantsList } from '@/axios/assistant'
import closeIcon from '../../assets/img/x-close.svg'
type FileType = Parameters<GetProp<UploadProps, 'beforeUpload'>>[0];
import AnimLoadingImg from '@/assets/img/loadingAnimImg.svg?react'
import RemoveIcon from '../../assets/img/removeIcon.svg?react'
import UploadImg from '@/assets/img/uploadImg.svg?react'
import ModalFooterEnd from '../modalFooterEnd/index'
import { SSE } from "sse.js";
import DeleteIcon from '../../assets/img/deleteIcon.svg?react'
import DeleteModal from '../deleteModal/index.tsx';
import EditIcon from '../../assets/img/editIcon.svg?react'
import MessageSuccess from '../../assets/img/messageSuccess.svg?react'
import ClipboardJS from 'clipboard';
import DrawerAssistant from '../drawerAssistant/index'
import ActionDrawer from '../actionDrawer/index.tsx';
import { useLocation, useNavigate } from 'react-router-dom';
import { useTranslation } from "react-i18next";
import CommonComponents from '../../contents/index'
import { useDispatch, useSelector } from 'react-redux';
import './index.css'
import { fetchAssistantsData } from '@/Redux/actions.ts'
import MarkdownMessageBlock from '@taskingai/taskingai-markdown'
const origin = window.location.origin;
const plainOptions = [
    { label: 'Stream', value: 1 },
    { label: 'Debug', value: 2 },
    { label: 'Markdown content', value: 4 }
]
function Playground() {
    const navigation = useNavigate();
    const { assistantTableColumn, modelsTableColumn, collectionTableColumn } = CommonComponents()
    const uploadUrl = `${origin}/api/v1/images`
    const { assistantPlaygroundId } = useSelector((state: any) => state.assistantId)
    const { playgroundType } = useSelector((state: any) => state.playgroundType)
    const { t } = useTranslation();
    const dispatch = useDispatch();
    const [assistantLimit, setAssistantLimit] = useState(20)
    const { search, pathname } = useLocation();
    const [assistantId, setAssistantId] = useState<any>()
    const [optionList, setOptionList] = useState<any>([])
    const divRef: any = useRef();
    const settingModal = useRef<any>()
    const [retrievalLimit, setRetrievalLimit] = useState(20)
    const [updateModelPrevButton, setUpdateModelPrevButton] = useState(false)
    const settingIcon = useRef<any>()
    const contentRef = useRef<any>();
    const [shouldSmoothScroll, setShouldSmoothScroll] = useState(true)
    const [Authentication, setAuthentication] = useState('')
    const [selectedActionsRows, setSelectedActionsRows] = useState<any[]>([])
    const [retrievalList, setRetrievalList] = useState<any[]>([])
    const [listChats, setListChats] = useState<any[]>([])
    const [OpenDrawer, setOpenDrawer] = useState(false)
    const [options, setOptions] = useState([])
    const [memoryValue, setMemoryValue] = useState('zero')
    const [recordsSelected, setRecordsSelected] = useState<string[]>([])
    const childRef = useRef<ChildRefType | null>(null);
    const [modelLimit, setModelLimit] = useState(20)
    const [modalTableOpen, setModalTableOpen] = useState(false)
    const [selectedModelRows, setSelectedRows] = useState<any[]>([])
    const [originalModelData, setOriginalModelData] = useState<any[]>()
    const [modelOne, setModelOne] = useState(false);
    const [OpenActionDrawer, setOpenActionDrawer] = useState(false)
    const [sendButtonLoading, setSendButtonLoading] = useState(false)
    const [generateButtonLoading, setGenerateButtonLoading] = useState(false)
    const [openModalTable, setOpenModalTable] = useState(false)
    const [systemPromptVariables, setSystemPromptVariable] = useState('')
    const [chatId, setChatId] = useState<any>('')
    const [actionList, setActionList] = useState([])
    const [tipSchema, setTipSchema] = useState(false)
    const [checkBoxValue, setCheckBoxValue] = useState([1, 2, 4])
    const [contentValue, setContentValue] = useState('')
    const [drawerName, setDrawerName] = useState('')
    const [schema, setSchema] = useState('')
    const [generateFlag, setGenerateFlag] = useState(false)
    const [retrievalConfig, setRetrievalConfig] = useState('user_message')
    const [custom, setCustom] = useState('')
    const [selectedPluginGroup, setSelectedPluginGroup] = useState<any>([])
    const [selectedActionsSelected, setSelectedActionSelected] = useState<any[]>([])
    const [inputValueOne, setInputValueOne] = useState(20)
    const [inputValueTwo, setInputValueTwo] = useState(200)
    const [radioValue, setRadioValue] = useState('none')
    const [openCollectionDrawer, setOpenCollectionDrawer] = useState(false)
    const [updateRetrievalPrevButton, setUpdateRetrievalPrevButton] = useState(false)
    const [selectedRetrievalRows, setSelectedRetrievalRows] = useState<any[]>([])
    const [hasMore, setHasMore] = useState(false)
    const [hasActionMore, setHasActionMore] = useState(false)
    const [hasModelMore, setHasModelMore] = useState(false)
    const [drawerDesc, setDrawerDesc] = useState('')
    const [contentTalk, setContentTalk] = useState<any[]>([])
    const [contentHasMore, setContentHasMore] = useState(false)
    const [contentLoading, setContentLoading] = useState(false)
    const [contentTalkLoading, setContentTalkLoading] = useState(false)
    const [loading, setLoading] = useState(false)
    const [recordsSelected1, setRecordsSelected1] = useState([])
    const [systemPromptTemplate, setSystemPromptTemplate] = useState<string[]>([]);
    const [openAssistantModalTable, setOpenAssistantModalTable] = useState(false)
    const { TextArea } = Input;
    const [sendGenerateLoading, setSendGenerateLoading] = useState(false)
    const [bundilesList, setBundlesList] = useState([])
    const [OpenDeleteModal, setOpenDeleteModal] = useState(false)
    const [errorContent, setErrorContent] = useState('')
    const [updatePrevButton, setUpdatePrevButton] = useState(false)
    const [defaultSelectedAssistant, setDefaultSelectedAssistant] = useState<string[]>([])
    const [modelHasMore, setModelHasMore] = useState(false)
    const [confirmLoading, setConfirmLoading] = useState(false);
    const [loadMoreHasMore, setLoadMoreHasMore] = useState(false)
    const [debugArray1, setDebugArray1] = useState<any[]>([])
    const [debugArray2, setDebugArray2] = useState<any[]>([])
    const [lottieAnimShow, setLottieAnimShow] = useState(false)
    const [contentDrawer, setContentDrawer] = useState(false)
    const [contentErrorDrawer, setContentErrorDrawer] = useState(false)
    const [chatCompletionCall, setChatCompletionCall] = useState('')
    const [chatCompletionResult, setChatCompletionResult] = useState('')
    const [collapseLabel1, setCollapseLabel1] = useState('')
    const [collapseLabel2, setCollapseLabel2] = useState('')
    const [noPreviousChat, setNoPreviousChat] = useState(false)
    const [noPreviousMessage, setNoPreviousMessage] = useState(false)
    const [searchChatID, setSearchChatID] = useState('')
    const [assistantName, setAssistantName] = useState('')
    const [imgList, setImgList] = useState<any[]>([])

    const [groupedMessages, setGroupedMessages] = useState({
        role: 'Assistant',
        content: { text: [{ event: '', color: '', event_id: '' }] },
        useId: 'user'
    });
    const [modelName, setModelName] = useState<any>('')
    const drawerAssistantRef = useRef<any>(null);
    const [topk, setTopk] = useState(3)
    const [maxTokens, setMaxToken] = useState(4096)
    const [pluginModalOpen, setPluginModalOpen] = useState(false)

    const handleCopy = (text: string) => {
        const clipboard = new ClipboardJS('.icon-copy', {
            text: () => text
        });
        clipboard.on('success', function () {
            toast.success(`${t('CopiedToClipboard')}`)
            clipboard.destroy()
        });
    }
    useEffect(() => {
        const handleClickOutside = (event: any) => {
            if (!(settingModal.current && settingModal.current.contains(event.target)) && !(settingIcon.current && settingIcon.current.contains(event.target))) {
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
        initialFunction()
    }, [])
    // useEffect(() => {
    //     setAssistantPlaygroundNewId(assistantPlaygroundId)
    // }, [assistantPlaygroundId])

    useEffect(() => {
        const storedValues = JSON.parse(localStorage.getItem('checkedValues') as string) || [1, 2, 4];
        setCheckBoxValue(storedValues);
    }, []);
    useEffect(() => {
        const queryParams = new URLSearchParams(search);
        if (queryParams.get('assistant_id')) {
            dispatch(setPlaygroundSelect('assistant'))
        } else if (queryParams.get('model_id')) {
            dispatch(setPlaygroundSelect('chat_completion'))
        }
    }, [search])
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
    const handleRetrievalConfigChange1 = (value: string) => {
        setRetrievalConfig(value)
    }
    useEffect(() => {
        const params1 = {
            limit: 100,
            offset: 0,
            lang: 'en'
        }
        getBundleList(params1)
    }, [])
    const getBundleList = async (params: object) => {
        try {
            const res: any = await getPluginList(params)
            setBundlesList(res.data)
        } catch (e) {
            const apiError = e as ApiErrorResponse;
            const errorMessage: string = apiError.response.data.error.message;
            toast.error(errorMessage)
        }


    }
    const handleChangeSearchChatID = (e: any) => {
        setSearchChatID(e.target.value)
    }
    const combineObjects = (item: any, arr: any) => {
        let updatedGroupedMessages = { ...groupedMessages };
        let str = ''
        const checkBoxValue1 = JSON.parse(localStorage.getItem('checkedValues') as string) || [1, 2]
        if (item.object === 'MessageGenerationLog') {
            const newItem = {
                ...item,
                event: item.event.split('_').map((word: string) => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')
            }
            setLottieAnimShow(true)
            const previousItems = arr.slice(0, arr.length - 1);
            const currentIsDuplicate = previousItems.some((existingItem: any) => existingItem.event_id === newItem.event_id);
            if (!currentIsDuplicate) {
                const indexToInsert = Math.max(updatedGroupedMessages.content.text.length - 1, 0);
                newItem.color = 'orange'
                updatedGroupedMessages.content.text.splice(indexToInsert, 0, newItem);
            } else {
                const duplicateIndex = updatedGroupedMessages.content.text.findIndex(existingItem => existingItem.event_id === newItem.event_id);
                if (duplicateIndex !== -1) {
                    updatedGroupedMessages.content.text[duplicateIndex] = newItem;
                    updatedGroupedMessages.content.text[duplicateIndex].color = 'green'
                }
            }
        } else if (item.object === 'MessageChunk') {
            item.color = 'green'
            str += item.delta
            updatedGroupedMessages.content.text[updatedGroupedMessages.content.text.length - 1].event += str;
        } else if (item.object === 'Message' && checkBoxValue1.indexOf(1) === -1 && checkBoxValue1.indexOf(2) !== -1) {
            updatedGroupedMessages.content.text[updatedGroupedMessages.content.text.length - 1].event = item.content.text;
        } else if (item.object === 'Error') {
            setErrorContent(JSON.stringify(item, null, 4))
            setGenerateButtonLoading(false)
            setLottieAnimShow(false)
            updatedGroupedMessages.content.text[updatedGroupedMessages.content.text.length - 1].event = 'Error Occurred';
        }
        return updatedGroupedMessages;
    }
    const fetchAssistantsList = async (value?: any) => {
        let res;
        if (value) {
            res = await getAssistantsList(value) as FullApiResponse
        } else {
            res = await getAssistantsList({ limit: assistantLimit || 20 }) as FullApiResponse
        }
        // const res: any = await getAssistantsList({ limit: assistantLimit || 20})
        const data = res.data.map((item: any) => {
            return {
                ...item,
                key: item.assistant_id
            }
        })
        setOptionList(data)
        if (assistantId) {
            const id = assistantId[0].split('-')[1] ? assistantId[0].split('-')[1] : assistantId[0]
            const item1 = data.find((item: any) => (item.assistant_id === id))
            setAssistantId([`${item1.name}-${item1.assistant_id}`])
        }
        setModelHasMore(res.has_more)

    }
    const initialFunction = async () => {
        const queryParams = new URLSearchParams(search);
        const assistantId = queryParams.get('assistant_id')
        const params = {
            limit: 20,
        }
        if (assistantId && assistantId === assistantPlaygroundId) {
            setLoading(true)
            setAssistantId([assistantId])
            setAssistantName(localStorage.getItem('assistantName') || 'Untitled Assistant')
            try {
                const listChats: any = localStorage.getItem('listChats')
                const chatsHasMore: any = localStorage.getItem('chatsHasMore')
                let chatId = localStorage.getItem('chatId')
                if (listChats) {
                    setListChats(JSON.parse(listChats))
                    setLoadMoreHasMore(JSON.parse(chatsHasMore))
                    if (chatId === 'undefined') {
                        setChatId(undefined)
                    } else {
                        setChatId(chatId)
                    }

                }
                const contentTalk: any = localStorage.getItem('contentTalk')
                const contentHasMore: any = localStorage.getItem('contentHasMore')
                if (contentTalk) {
                    setContentTalk(JSON.parse(contentTalk))
                    if (contentHasMore === 'true') {
                        setContentHasMore(true)
                    } else {
                        setContentHasMore(false)
                    }
                }
            } catch (e) {
                console.log(e)
                const apiError = e as ApiErrorResponse
                const message = apiError.response.data.error.message
                toast.error(message)
            }
            setLoading(false)
        } else if (assistantId) {
            setLoading(true)
            try {
                const assistantDetail = await getAssistantDetail(assistantId)
                setAssistantName(assistantDetail.data.name ? assistantDetail.data.name : 'Untitled Assistant')
                setAssistantId([assistantId])
                dispatch(setPlaygroundAssistantId(assistantId))
                const res2: any = await getListChats(assistantId, params)
                setListChats(res2.data)
                localStorage.setItem('listChats', JSON.stringify(res2.data))
                setLoadMoreHasMore(res2.has_more)
                setChatId(res2.data[0]?.chat_id)
                localStorage.setItem('chatId', res2.data[0]?.chat_id)
                const param = {
                    order: 'desc',
                }
                if (res2.data.length > 0) {
                    const res: any = await getHistoryMessage(assistantId, res2.data[0]?.chat_id, param)
                    const data = res.data.reverse()
                    setContentHasMore(res.has_more)
                    localStorage.setItem('contentHasMore', JSON.stringify(res.has_more))
                    setContentTalk(data)
                    localStorage.setItem('contentTalk', JSON.stringify(data))
                }
                setLoading(false)

            } catch (e) {
                navigation(`/project/playground`)
                console.log(e)
                setLoading(false)
            }
        }
        fetchAssistantsList()
        fetchModelsList(params)
        fetchActionsList(params)
        fetchDataRetrievalData(params)

    }
    const fetchHistoryMessage = async (assistantId: string, chatId: string, param: any) => {
        if (param.after) {
            setShouldSmoothScroll(false)
        } else {
            setShouldSmoothScroll(true)
        }
        try {
            const res: any = await getHistoryMessage(assistantId, chatId, param)
            const data = res.data.reverse()
            setContentHasMore(res.has_more)
            const contentTalk1: any = localStorage.getItem('contentTalk')
            localStorage.setItem('contentHasMore', JSON.stringify(res.has_more))
            localStorage.setItem('contentTalk', JSON.stringify([...data, ...JSON.parse(contentTalk1)]) as any)
            setContentTalk(prevValues => [...data, ...prevValues])
        } catch (error) {
            const apiError = error as ApiErrorResponse;
            const errorMessage: string = apiError.response.data.error.message;
            toast.error(errorMessage)
        }

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
    const handleMaxToken = (value: any) => {
        setMaxToken(value)
    }
    const handleToks = (value: any) => {
        setTopk(value)
    }
    const handleSelectModelId = (value: boolean) => {
        setModalTableOpen(value)
    }
    const combineObjectsWithSameMsgId = (arr: any[]) => {
        let groupedMessages = { role: 'Assistant', content: { text: '' } };
        arr.forEach((item) => {
            if (item.object === 'MessageChunk') {
                groupedMessages.content.text += item.delta
            }
        });
        return groupedMessages
    }
    const handleModalCancel = () => {
        setModelOne(false)
    }
    const handleChildModelEvent = async (value: any) => {
        await fetchModelsList(value)
        setUpdateModelPrevButton(false)
        setModelLimit(value.limit)
    }
    const fetchActionsList = async (params: Record<string, any>) => {
        try {
            const res: any = await getActionsList(params)
            const data = res.data.map((item: any) => {
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
            const apiResponse = error as ApiErrorResponse
            const message = apiResponse.response.data.error.message
            toast.error(message)
        }
    }
    const fetchModelsList = async (params: Record<string, any>) => {

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
            const apiResponse = error as ApiErrorResponse
            const message = apiResponse.response.data.error.message
            toast.error(message)
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
        const { name, description, model_name, model_id, system_prompt_template, tools, retrievals, memory, retrieval_configs } = data
        setDrawerName(name)
        setDrawerDesc(description)
        setSelectedRows(model_id)
        setOriginalModelData(model_id)
        setModelName(model_name)
        setSelectedActionSelected(tools.filter((item: any) => item.type === 'action').map((item: any) => {
            return {
                action_id: item.id,
                name: item.name
            }
        }))
        setSelectedPluginGroup(tools?.filter((item: any) => item.type === 'plugin').map((item: any) => item.id?.split('/')[1]));
        setRetrievalConfig(retrieval_configs.method || 'user_message')
        setTopk(retrieval_configs.top_k || 3)
        setMaxToken(retrieval_configs.max_tokens || 4096)
        setMemoryValue(memory.type)
        setInputValueOne(memory.max_messages)
        setInputValueTwo(memory.max_tokens)
        if (system_prompt_template.length === 0) {
            setSystemPromptTemplate([''])
        } else {
            setSystemPromptTemplate(system_prompt_template)
        }
        setSelectedActionsRows(tools.map((item: any) => { return { type: item.type, value: item.id, name: item.name } }))
        const tag = retrievals.map((item: any) => {
            return {
                collection_id: item.id,
                name: item.name || 'Untitled Collection'
            }
        })
        setRecordsSelected1(tag)

        setSelectedRetrievalRows(tag)
        setLoading(false)
        setOpenDrawer(true)
    }

    const handleCancel = () => {
        setOpenDrawer(false)
    }

    const handleDeletePromptInput = (index: number) => {
        const updatedInputValues = [...systemPromptTemplate];
        updatedInputValues.splice(index, 1);
        setSystemPromptTemplate(updatedInputValues);
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
        const params = {
            model_id: Array.isArray(originalModelData) ? originalModelData[0].slice(-8) : originalModelData,
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
        let id;
        if (assistantId[0].split('-')[1]) {
            const splitArray = assistantId[0].split('-')
            id = splitArray.slice(-1)[0]
        } else {
            id = assistantId[0]
        }

        try {
            if (id) {
                await updateAssistant(id, params)
                setAssistantName(drawerName)
                setOpenDrawer(false)
            }

            await fetchAssistantsList()
            dispatch(fetchAssistantsData() as any)
            setUpdatePrevButton(true)
        } catch (error) {
            const apiError = error as ApiErrorResponse;
            const errorMessage: string = apiError.response.data.error.message;
            toast.error(errorMessage)
        }

    }
    const handleNewChat = async () => {
        if (!assistantId) {
            return toast.error(`${t('projectAssistantRequired')}`)
        }
        if (sendButtonLoading || sendGenerateLoading || generateButtonLoading) {
            return toast.error('Cannot switch chat during message generation')
        }
        setLoading(true)
        const params = {
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
            localStorage.setItem('listChats', JSON.stringify([{ chat_id: data.chat_id, created_timestamp: data.created_timestamp }, ...listChats]))
            setListChats(prevValues => [{ chat_id: data.chat_id, created_timestamp: data.created_timestamp }, ...prevValues])
            setChatId(data.chat_id)
            localStorage.setItem('chatId', data.chat_id)
            setContentTalk([])
            setContentValue('')
            setImgList([])
            localStorage.setItem('contentTalk', JSON.stringify([]))
            localStorage.setItem('contentHasMore', JSON.stringify(false))
            setContentHasMore(false)
            setGenerateButtonLoading(false)
        } catch (error) {
            const apiResponse = error as ApiErrorResponse
            const message = apiResponse.response.data.error.message
            toast.error(message)
            console.log(error)
        }
        setLoading(false)
    }
    const handleCreateMessage = async (flag?: any) => {
        const imgLoading = imgList.some(item => item.loadingAnim)
        if (imgLoading) {
            return toast.error('The image is still uploading, please wait.')
        }
        const params = {
            role: 'user',
            content: {
                text: contentValue && imgList.length ?
                    contentValue + imgList.map(item => `![${item.name}](${item.url})`).join('') :
                    contentValue
            },
        }
        let id;
        if (assistantId[0].split('-')[1]) {
            const splitArray = assistantId[0].split('-')
            id = splitArray.slice(-1)[0]
        } else {
            id = assistantId[0]
        }
        const lastData = Array.isArray(contentTalk[contentTalk.length - 1]?.content.text)
        let lastMessage: boolean = false
        if (lastData) {
            const lastMessage1 = contentTalk[contentTalk.length - 1].content.text[contentTalk[contentTalk.length - 1].content.text.length - 1]
            if (lastMessage1.event === 'Error Occurred') {
                lastMessage = true
            } else {
                lastMessage = false
            }
        } else {
            lastMessage = false
            if (contentTalk[contentTalk.length - 1]?.role.toLowerCase() === 'user') {
                lastMessage = true
            }
        }
        if (flag === 'flag' && lastMessage) {
            setSendGenerateLoading(true)
            if (contentValue) {
                const res = await sendMessage(id, chatId, params)
                const { data } = res
                setContentTalk(prevValues => [...prevValues, {
                    role: 'user',
                    content: { text: imgList.length ? (contentValue + '\n' + imgList.map(item => `![${item.name}](${item.url})`).join('') + '\n') : data.content.text },
                    userId: true,
                    flag: true
                }])
                const contentTalk1: any = localStorage.getItem('contentTalk')
                localStorage.setItem('contentTalk', JSON.stringify([...JSON.parse(contentTalk1), {
                    role: 'user',
                    content: { text: imgList.length ? (contentValue + '\n' + imgList.map(item => `![${item.name}](${item.url})`).join('') + '\n') : data.content.text },
                    userId: true,
                    flag: true
                }]))

            }
            setGenerateFlag(true)
            setContentValue('')
            setImgList([])

        } else {
            if (contentValue === '' && imgList.length === 0) {
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
                const res = await sendMessage(id, chatId, params)
                const { data } = res
                setContentTalk(prevValues => [...prevValues, {
                    role: 'user',
                    content: { text: imgList.length ? (contentValue + '\n' + imgList.map(item => `![${item.name}](${item.url})`).join('') + '\n') : data.content.text },
                    userId: true,
                    flag: true
                }])
                const contentTalk1: any = localStorage.getItem('contentTalk')
                localStorage.setItem('contentTalk', JSON.stringify([...JSON.parse(contentTalk1), {
                    role: 'user',
                    content: { text: imgList.length ? (contentValue + '\n' + imgList.map(item => `![${item.name}](${item.url})`).join('') + '\n') : data.content.text },
                    userId: true,
                    flag: true
                }]))
                if (flag === 'flag') {
                    setGenerateFlag(true)
                } else {
                    setGenerateFlag(false)
                }
                setContentValue('')
                setImgList([])
            } catch (error) {
                const apiError = error as ApiErrorResponse;
                const errorMessage: string = apiError.response.data.error.message;
                toast.error(errorMessage)
                console.log(error)
            }
        }


        setSendButtonLoading(false)
    }
    const handleInputPromptChange = (index: number, newValue: string) => {
        setSystemPromptTemplate((prevValues) =>
            prevValues.map((item, i) =>
                i === index ? newValue : item
            )
        );
    };
    const handleCreateModelId = async () => {
        await setModelOne(true)
        childRef.current?.fetchAiModelsList()
        const params = {
            limit: modelLimit || 20
        }
        await fetchModelsList(params)
    }
    const handleSearchChatId = async () => {
        let id;
        if (assistantId[0].split('-')[1]) {
            const splitArray = assistantId[0].split('-')
            id = splitArray.slice(-1)[0]
        } else {
            id = assistantId[0]
        }
        if (searchChatID) {
            try {
                const res = await getChatItem(id, searchChatID)
                setListChats([res.data])
                localStorage.setItem('listChats', JSON.stringify([{ chat_id: res.data.chat_id, created_timestamp: res.data.created_timestamp }]))
            } catch (error) {
                const apiError = error as ApiErrorResponse;
                const errorMessage: string = apiError.response.data.error.message;
                toast.error(errorMessage)
            }
        } else {
            const res = await getListChats(id, { limit: 20 })
            setListChats(res.data)
            localStorage.setItem('listChats', JSON.stringify(res.data))
        }

    }
    const handleGenerateMessage = async (contentTalk1?: any) => {
        const imgLoading = imgList.some(item => item.loadingAnim)
        if (imgLoading) {
            return toast.error('The image is still uploading, please wait.')
        }
        const lastData = Array.isArray(contentTalk[contentTalk.length - 1]?.content.text)
        let lastMessage: boolean = false
        if (lastData) {
            const lastMessage1 = contentTalk[contentTalk.length - 1].content.text[contentTalk[contentTalk.length - 1].content.text.length - 1]
            if (lastMessage1.event === 'Error Occurred') {
                lastMessage = true
            } else {
                lastMessage = false
            }
        } else {
            lastMessage = false
        }
        if (generateButtonLoading) {
            return toast.error('Please wait for the assistant to respond.')
        }
        if (contentTalk1 !== 'flag' && contentTalk[contentTalk.length - 1]?.role.toLowerCase() === 'assistant' && !lastMessage) {
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
        const checkBoxValue1 = JSON.parse(localStorage.getItem('checkedValues') as string) || checkBoxValue
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
            source.addEventListener('error', (e: any) => {
                setGenerateButtonLoading(false)
                setSendGenerateLoading(false)
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
                const contentTalk1: any = localStorage.getItem('contentTalk')
                localStorage.setItem('contentTalk', JSON.stringify([...JSON.parse(contentTalk1), {
                    role: 'Assistant',
                    content: {
                        text: data.content.text
                    },
                    userId: false,
                    flag: true
                }]))
            } catch (error) {
                const apiError = error as ApiErrorResponse;
                const errorMessage: string = apiError.response.data.error.message;
                toast.error(errorMessage)
                console.log(error)
            } finally {
                setGenerateButtonLoading(false)
                setSendGenerateLoading(false)
            }
        } else if (stream && !debug) {
            let arr: any = []
            source?.addEventListener("message", (e: any) => {
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
                localStorage.setItem('contentTalk', JSON.stringify(binedArr))
            }

            );
        } else if (!stream && debug) {
            let arr1: any = []
            source?.addEventListener("message", (e: any) => {
                if (e.data === '[DONE]') {
                    setGenerateButtonLoading(false)
                    setSendGenerateLoading(false)
                    return
                }
                const data = JSON.parse(e.data)
                if (data.object === 'MessageGenerationLog') {
                    setDebugArray1(prevValues => {
                        const updatedValues = [...prevValues, data];
                        localStorage.setItem('inputResult', JSON.stringify(updatedValues));
                        return updatedValues;
                    });
                }
                arr1.push(data)
                const binedArr = [...contentTalk, combineObjects(data, arr1)]
                setContentTalk(binedArr)
                localStorage.setItem('contentTalk', JSON.stringify(binedArr))

            })
        } else {
            let arr1: any = []
            source?.addEventListener("message", (e: any) => {
                if (e.data === '[DONE]') {
                    setGenerateButtonLoading(false)
                    setSendGenerateLoading(false)
                    return
                }
                const data = JSON.parse(e.data)

                if (data.object === 'MessageGenerationLog') {
                    setDebugArray2(prevValues => {
                        const updatedValues = [...prevValues, data];
                        localStorage.setItem('outputResult', JSON.stringify(updatedValues));
                        return updatedValues;
                    });
                }
                arr1.push(data)
                const binedArr = [...contentTalk, combineObjects(data, arr1)]
                setContentTalk(binedArr)
                localStorage.setItem('contentTalk', JSON.stringify(binedArr))

            })
        }
        setGroupedMessages({
            role: 'Assistant',
            content: { text: [{ event: '', color: '', event_id: '' }] },
            useId: 'user'
        })

    }
    const handleDescriptionChange = (value: string) => {
        setDrawerDesc(value)
    }

    const handleCreateConfirm = () => {
        setOpenModalTable(false)
    }
    const hangleFilterData = (value: any[]) => {
        setRetrievalList(value)
    }
    const handleChildRetrievalEvent = async (value: Record<string, any>) => {
        setRetrievalLimit(value.limit)
        await fetchDataRetrievalData(value)
        setUpdateRetrievalPrevButton(false)

    }
    const fetchDataRetrievalData = async (params: Record<string, any>) => {
        try {
            const res: any = await getRetrievalList(params)
            const data = res.data.map((item: any) => {
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
            const apiResponse = e as ApiErrorResponse
            const message = apiResponse.response.data.error.message
            toast.error(message)
            console.log(e)
        }
    }
    const handleChangeName = (value: string) => {
        setDrawerName(value)
    }
    const handleModalCloseConfirm = () => {
        if (selectedModelRows) {
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
    const handleModalClose = () => {
        setOriginalModelData((prev: any) => prev)
        setSelectedRows(originalModelData as any)
        setModalTableOpen(false)
    }
    const handleAssistantModalClose = () => {
        const queryParams = new URLSearchParams(search);
        const data = queryParams.get('assistant_id')
        const assistantData = optionList.find((item: any) => item.assistant_id === data)
        if(assistantData) {
            if (assistantData.name) {
                setAssistantName(assistantData.name)
                localStorage.setItem('assistantName', assistantData.name)
            } else {
                setAssistantName('Untitled Assistant')
                localStorage.setItem('assistantName', 'Untitled Assistant')
            }
            setAssistantId([assistantData.assistant_id])
        }
        setOpenAssistantModalTable(false)
    }
    const handleListChats = async () => {
        const splitArray = assistantId[0].split('-')
        const id = splitArray.slice(-1)[0]
        const res = await getListChats(id, { limit: 20 })
        localStorage.setItem('listChats', JSON.stringify(res.data))
        setListChats(res.data)
        setChatId(res.data[0]?.chat_id)
        localStorage.setItem('chatId', res.data[0]?.chat_id)
        const param = {
            order: 'desc',
        }
        if (res.data[0]) {
            try {
                const res1 = await getHistoryMessage(id, res.data[0]?.chat_id, param)
                const data = res1.data.reverse()
                localStorage.setItem('contentTalk', JSON.stringify(data))
                setContentTalk(res1.data)
            } catch (e) {
                const apiResponse = e as ApiErrorResponse
                const message = apiResponse.response.data.error.message
                toast.error(message)
            }

        }
    }
    const handleAssistantModalClose1 = async () => {
        const splitArray = assistantId[0].split('-')
        const id = splitArray.slice(-1)[0]
        navigation(`${pathname}?assistant_id=${id}`)
        dispatch(setPlaygroundAssistantId(id))
        setConfirmLoading(true)
        await handleListChats()
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
            await fetchActionsList(params);
        } catch (error: any) {
            console.log(error)
        }

        setOpenActionDrawer(false)
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
    const handleRecordsSelected = (_value: any[], selectedRows: any[]) => {
        const tag = selectedRows.map(item => (item.name + '-' + item.model_id))
        setSelectedRows(tag)
        // setOriginalModelData(tag)
        // setModelName(selectedRows.map(item => item.name))
    }
    const handleRecordsAssistantSelected = (_value: string[], selectedRows: any[]) => {
        setRecordsSelected(selectedRows)
        const tag = selectedRows.map((item: any) => {
            if (item.name) {
                setAssistantName(item.name)
                localStorage.setItem('assistantName', item.name)
                return item.name + '-' + item.assistant_id
            } else {
                setAssistantName('Untitled Assistant')
                return item.assistant_id
            }
        })
        setAssistantId(tag)
        setDefaultSelectedAssistant(tag)
    }
    const handleCustom = (value: string) => {
        setCustom(value)
    }
    const handleCollectionSelected = (value: any, selectedRows: any[]) => {
        setRecordsSelected1(value)
        const tag = selectedRows.map(item => (item.name + '-' + item.collection_id))
        setSelectedRetrievalRows(tag)
    }

    const handleMemoryChange1 = (value: string) => {
        setMemoryValue(value)
    }
    const handleSchemaChange = (value: string) => {
        setSchema(value)
    }
    const handleAddPrompt = () => {
        if (systemPromptTemplate.length < 10) {
            setSystemPromptTemplate((prevValues => [...prevValues, '']))
        }
    }
    const handleChildAssistantEvent = async (value: Record<string, any>) => {
        await fetchAssistantsList(value)
        setUpdatePrevButton(false)
        setAssistantLimit(value.limit)
    }
    const handleOpenChat = async (value: string) => {
        if (sendButtonLoading || sendGenerateLoading || generateButtonLoading) {
            return toast.error('Cannot switch chat during message generation')
        }
        setChatId(value)
        localStorage.setItem('chatId', value)
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
        localStorage.setItem('contentTalk', JSON.stringify([]))
        setGenerateButtonLoading(false)
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
        localStorage.setItem('listChats', JSON.stringify([...listChats, ...res.data]))
        localStorage.setItem('chatsHasMore', JSON.stringify(res.has_more))
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
    const handleInputValueOne = (value: number) => {
        setInputValueOne(value)
    }
    const handleInputValueTwo = (value: number) => {
        setInputValueTwo(value)
    }
    const onRadioChange = (value: string) => {
        setRadioValue(value)
    }
    const handleChangeCheckbox = (checkedValues: any) => {
        setCheckBoxValue(checkedValues)
        localStorage.setItem('checkedValues', JSON.stringify(checkedValues))
        // if (checkedValues.includes(4)) {
        //     setShowMarkdown(true)
        // } else {
        //     setShowMarkdown(false)

        // }
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
            localStorage.setItem('listChats', JSON.stringify(res.data))
            localStorage.setItem('chatsHasMore', JSON.stringify(res.has_more))
            setLoadMoreHasMore(res.has_more)
            setChatId(res.data[0]?.chat_id)
            localStorage.setItem('chatId', res.data[0]?.chat_id)
            const param1 = {
                order: 'desc',
                limit: 20
            }
            setContentTalk([])
            setContentValue('')
            setImgList([])
            if (res.data[0]?.chat_id) {
                await fetchHistoryMessage(id, res.data[0]?.chat_id, param1)
            }

        } catch (error) {
            const apiError = error as ApiErrorResponse;
            const errorMessage: string = apiError.response.data.error.message;
            toast.error(errorMessage)
        }
        setOpenDeleteModal(false)
    }

    const handleConfirmRequest = async () => {
        getBundleList({ limit: 20 })
    }
    const handleClickDebug = (item: any) => {
        const inputResult: any = debugArray1.length ? debugArray1 : JSON.parse(localStorage.getItem('inputResult') as any)
        const outputResult: any = debugArray2.length ? debugArray2 : JSON.parse(localStorage.getItem('outputResult') as any)
        if (item.event === 'Error Occurred') {
            setContentErrorDrawer(true)
        } else {
            delete item.color
            const event1 = item.event.split('_').map((word: string) => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')
            const event2 = item.event_step?.charAt(0).toUpperCase() + item.event_step?.slice(1)
            setCollapseLabel2(`${event1}: ${event2}`)
            if (!item.event_id) return

            const data1 = inputResult?.find((item1: any) => (item1.event_id === item.event_id))
            const data2: any = outputResult?.find((item1: any) => (item1.event_id === item.event_id))
            if (data1) {
                delete data1.color
                const data3 = JSON.stringify(data1, null, 4)
                setChatCompletionCall(data3)
                const label = data1.event_step?.charAt(0).toUpperCase() + data1.event_step?.slice(1)
                const label1 = data1.event.split('_').map((word: string) => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')
                setCollapseLabel1(`${label1}: ${label}`)
            } else if (data2) {
                delete data2.color
                const data4 = JSON.stringify(data2, null, 4)
                const label = data2.event_step?.charAt(0).toUpperCase() + data2.event_step?.slice(1)
                const label1 = data2.event.split('_').map((word: string) => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')
                setCollapseLabel1(`${label1}: ${label}`)
                setChatCompletionCall(data4)
            }
            setChatCompletionResult(JSON.stringify(item, null, 4))
            setContentDrawer(true)

        }
    }
    const handleCloseContentDrawer = () => {
        setContentDrawer(false)
    }
    const handleNewActionModal = () => {
        setOpenActionDrawer(true)
    }

    const handleSendAndGenerateMessage = async () => {
        if (sendButtonLoading || generateButtonLoading) {
            return toast.error('Please wait for the info to respond.')
        }
        await handleCreateMessage('flag')
    }
    const handleCloseContentErrorDrawer = () => {
        setContentErrorDrawer(false)
    }
    const handleDeleteChat = async () => {
        if (sendButtonLoading || sendGenerateLoading || generateButtonLoading) {
            return toast.error('Cannot switch chat during message generation')
        }
        setOpenDeleteModal(true)
    }
    const handleSetModelConfirmOne = () => {
        setModelOne(false)
        setUpdateRetrievalPrevButton(true)
    }
    const handleClosePluginModal = () => {
        setPluginModalOpen(false)
    }
    const onhandleTipError = (value: boolean) => {
        setTipSchema(value)
    }

    const handleNewCollection = (value: boolean) => {
        setOpenCollectionDrawer(value)
    }

    const handleNewBundle = () => {
        setPluginModalOpen(true)
    }

    const customRequest = (options: any) => {
        const { file } = options;

        const formData = new FormData();
        formData.append('image', file);
        formData.append('purpose', 'user_message_image');
        fetch(uploadUrl, {
            method: 'POST',
            body: formData,
            headers: {
                Authorization: `Bearer ${localStorage.getItem('token')}`,
            }
        })
            .then(response => response.json())
            .then(data => {
                if (!data.data || !data.data.url) {
                    setImgList(prev => prev.filter((item) => item.uid !== file.uid))

                    throw new Error('URL not found in response');
                }
                setImgList(prev => prev.map((item, index) => {
                    (index === prev.length - 1 ? { ...item, url: data.data.url } : item)
                    if (item.uid === file.uid) {
                        return { ...item, url: data.data.url, loadingAnim: false };
                    }
                    return item;
                }));
            })
    };
    const handleRemoveCloseIcon = (url: string) => {
        setImgList(imgList.filter((item) => item.url !== url))
    }
    const handleChange: any = async ({ fileList: newFileList, file }: any) => {
        if (!file.url && !file.preview) {
            file.preview = await getBase64(file.originFileObj as FileType);
        }
        setImgList(newFileList.map((item: any) => {
            if (item.uid === file.uid) {
                return { ...item, loadingAnim: true };
            }
            return item;
        }));

    }
    const getBase64 = (file: FileType): Promise<string> =>
        new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = () => resolve(reader.result as string);
            reader.onerror = (error) => reject(error);
        });
    return (
        <>
            {playgroundType === 'assistant' ? <Spin spinning={loading}>
                {!assistantId ? <div className={styles['selectAssistant']}>
                    {<PlayGroundImg className={styles.svg} />}
                    <div className={styles['select-assistant']}>{t('projectPlaygroundSelectAssistantDesc')}</div>
                    <div className={styles['header-news']}>
                        <div className={styles['plusParent']}>
                            <Button icon={<PlusOutlined />} className={styles['prompt-button']} onClick={handleSelectAssistantID}>{t('projectPlaygroundSelectAssistant')}</Button>
                        </div>
                    </div>
                </div> : <div className={styles['playground']}>
                    <div className={styles['left-content']}>
                        <div className={styles['top']}>
                            <div className={styles['select-assistant']}>{t('projectAssistant')}</div>
                            {!assistantId && <div className={styles['select-desc']}>{t('projectPlaygroundSelectAssistantInfo')}</div>}
                            <div style={{ display: 'flex', alignItems: 'center' }}>
                                <Select open={false} suffixIcon={<RightOutlined />} onClick={handleSelectAssistantID} value={assistantName} className={styles['select']} removeIcon={null}>
                                </Select>
                                {assistantId && <Button icon={<EditIcon />} onClick={handleEditAssistant} className={styles['edit-button']}></Button>}
                            </div>
                        </div>
                        <div className={styles['selected-modal']}>
                            <div className={styles['generation-options']}>
                                {t('projectPlaygroundGenerationOptions')}
                                {/* <QuestionIcon /> */}
                            </div>
                            <div className={styles['desc']}></div>
                            <Checkbox.Group onChange={handleChangeCheckbox} options={plainOptions} defaultValue={JSON.parse(localStorage.getItem('checkedValues') as string) || checkBoxValue} />
                        </div>
                        <div className={styles['bottom']}>
                            <div className={styles['bottom-chats']}>
                                <div>{t('projectPlaygroundChats')}</div>
                                <div className={styles['actionbuttondownload']} onClick={handleNewChat}>
                                    <PlusOutlined />
                                    <div className={styles['text1']}>{t('projectPlaygroundNewChat')}</div>
                                </div>
                            </div>
                            <Space.Compact>
                                <Input readOnly className={styles['id-input']} style={{ width: '20%', borderRight: 0 }} defaultValue="ID" />
                                <Input style={{ width: '73%' }} onPressEnter={handleSearchChatId} value={searchChatID} onChange={(e) => handleChangeSearchChatID(e)} placeholder='Enter chat_id' suffix={<SearchOutlined onClick={handleSearchChatId} style={{ color: 'rgba(0,0,0,.45)' }} />} />
                            </Space.Compact>
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
                                        <div className={styles['noPreviousChat1']}>{t('projectPlaygroundNoPreviousChat')}</div>
                                        <div className={styles['frameChild']} />
                                    </div>}
                                </div>
                                {loadMoreHasMore && <div className={styles['lineParent']} style={{ marginTop: '10px' }}>
                                    <div className={styles['frameChild']} />
                                    <div className={styles['formbuttoncancel']} onClick={handleLodaMore}>
                                        <div className={styles['text1']}>{t('projectPlaygroundLoadMore')}</div>
                                    </div>
                                    <div className={styles['frameChild']} />
                                </div>}
                            </div>
                        </div>
                    </div>
                    <div className={styles['right-content']}>
                        <div className={styles['header-top']}>
                            <div className={styles['header-left']}>
                                <span className={styles['chat']}>{t('projectPlaygroundChat')}</span>
                                {listChats.length > 0 && <span className={styles['desc']}>{chatId}</span>}
                                {listChats.length > 0 && <CopyOutlined className='icon-copy' onClick={() => handleCopy(chatId)} />}
                            </div>

                            {listChats.length > 0 && <div className={styles['header-right']} onClick={handleDeleteChat}>
                                <Button icon={<DeleteIcon />} className='cancel-button'>{t('projectPlaygroundDeleteChat')}</Button>
                            </div>}
                        </div>
                        {!chatId && <div className={styles['content-center']}>
                            <div className={styles['content-img']}>
                                <PlaygroundImg />
                                <div className={styles['waiting-for-configuration']}>{t('projectPlaygroundWaitingForConfiguration')}</div>
                            </div>
                        </div>}
                        {chatId &&
                            <Spin spinning={contentTalkLoading}>
                                <div className={`${styles['content-talk']} playground-content-markdown`} ref={contentRef}>
                                    <div style={{ display: 'flex', justifyContent: 'center' }}>
                                        <Spin spinning={contentLoading} />
                                    </div>
                                    {(!contentHasMore && noPreviousMessage) && <div className={styles['lineParent']}>
                                        <div className={styles['frameChild']} />
                                        <div className={styles['noPreviousChat1']}>{t('projectPlaygroundNoPreviousMessage')} </div>
                                        <div className={styles['frameChild']} />
                                    </div>}
                                    {contentHasMore && <div className={styles['lineParent']} style={{ marginTop: '10px' }}>
                                        <div className={styles['frameChild']} />
                                        <div className={styles['formbuttoncancel']} onClick={handleContentLodaMore}>
                                            <div className={styles['text1']}>{t('projectPlaygroundLoadMore')}</div>
                                        </div>
                                        <div className={styles['frameChild']} />
                                    </div>}
                                    {contentTalk.map((item, index) => (
                                        <div className={styles['message']} key={index} ref={divRef}>
                                            <div className={`${styles.subText1} ${item.role === 'user' ? styles.user : ''}`}>{item.role.charAt(0).toUpperCase() + item.role.slice(1)}</div>
                                            {typeof (item.content.text) === 'string' && <div className={`${styles.text1} ${item.role === 'user' ? styles.userInfo : ''}`} style={{ whiteSpace: "pre-line" }}>{checkBoxValue.indexOf(4) !== -1 ? <MarkdownMessageBlock message={item.content.text} /> : item.content.text}</div>}
                                            {typeof (item.content.text) === 'object' && <div className={`text1 ${item.role === 'user' ? styles.userInfo : ''}`}>{item.content.text.map((item1: any, index1: number) => (<div key={index1} className={`${(item1.color === 'orange' && index === contentTalk.length - 1) ? 'orange' : 'green'} ${index1 === item.content.text.length - 1 && styles.lastItem}`}>
                                                {(item1.color === 'orange' && index === contentTalk.length - 1 && item1.event_step !== '') ?
                                                    (<div style={{ display: 'flex', alignItems: 'center', marginTop: '5px' }}>{lottieAnimShow && (
                                                        <>
                                                            {<LoadingAnim className={styles['loading-icon']} />}
                                                            <span style={{ fontSize: '14px', lineHeight: '20px' }}>{item1.event}</span>
                                                        </>
                                                    )}
                                                    </div>) :
                                                    (
                                                        item1.color !== 'orange' && (<div onClick={() => handleClickDebug(item1)} style={{ display: 'flex', alignItems: 'center', marginTop: '5px' }}>
                                                            {(item1.event !== 'Error Occurred') && (<> {index1 !== item.content.text.length - 1 && <MessageSuccess className={styles['message-success']} />}<span style={{ cursor: index1 !== item.content.text.length - 1 ? 'pointer' : 'text', whiteSpace: 'pre-wrap' }}>{checkBoxValue.indexOf(4) !== -1 ? <MarkdownMessageBlock message={item1.event} styles={{ marginBottom: 0 }} /> : item1.event}</span></>)}
                                                            {(item1.event === 'Error Occurred') && (<><ErrorIcon className={styles['message-success']}></ErrorIcon><span style={{ color: '#ec1943', cursor: 'pointer', lineHeight: '20px', fontSize: '14px' }}>Error Occurred</span></>)}
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
                            {imgList.length > 0 && <div className={styles['upload-list']}>
                                {imgList.map((item, index) => (
                                    <div key={index} className={styles['upload-item']}>
                                        {item.loadingAnim && <AnimLoadingImg className='anim-loading' />}
                                        <Image style={{
                                            filter: item.loadingAnim ? 'brightness(50%)' : 'brightness(100%)'
                                        }} src={item.preview} alt={item.name} preview={{
                                            mask: (
                                                <EyeOutlined />
                                            ),
                                        }}></Image>
                                        <RemoveIcon className={styles['close-icon']} onClick={() => handleRemoveCloseIcon(item.url)} />
                                    </div>
                                ))}
                            </div>}
                            <TextArea className={styles['textarea']} autoSize={{ minRows: 3, maxRows: 6 }} value={contentValue} onChange={(e) => setContentValue(e.target.value)}></TextArea>
                            <div className={styles['button-group']}>
                                <div style={{ display: 'flex' }}>
                                    <Button className={`next-button ${styles.button}`} onClick={handleSendAndGenerateMessage} loading={sendGenerateLoading}>Send and Generate</Button>
                                    <div className={`${styles.formbuttoncancel} ${sendButtonLoading ? styles.loading : ''}`} onClick={handleCreateMessage}>
                                        {sendButtonLoading && <LoadingOutlined style={{ marginRight: '3px' }} />}  <div className={styles['text1']}>{t('projectPlaygroundSend')}</div>
                                    </div>
                                    <div className={`${styles.formbuttoncancel} ${styles.button1} ${generateButtonLoading ? styles.loading : ''}`} onClick={handleGenerateMessage}>
                                        {generateButtonLoading && <LoadingOutlined style={{ marginRight: '3px' }} />}<div className={styles['text1']}>{t('projectPlaygroundChatGenerate')}</div>
                                    </div>

                                    <Upload onChange={handleChange} disabled={imgList.length === 4 ? true : false} accept=".png,.jpg" fileList={imgList} customRequest={customRequest} >
                                        <div className={styles['upload-img']}>
                                            <UploadImg />
                                        </div>
                                    </Upload>

                                </div>
                                <div className={styles['actionbuttonedit']} onMouseEnter={handleMouseEnter} ref={settingIcon}>
                                    <ModalSettingIcon className={styles['functionalicons']} />
                                </div>
                            </div>
                            <div className={styles['setting-modal']} ref={settingModal} style={{ display: 'none' }}>

                                <div className={styles['select-assistant']}>Prompt variables</div>
                                <TextArea style={{ height: '300px' }} placeholder={`{\n   key: value\n}`}
                                    value={systemPromptVariables} onChange={(e) => setSystemPromptVariable(e.target.value)}></TextArea>
                            </div>
                        </div>
                    </div>
                </div >}
            </Spin > : <PlaygroundModel />}
            <Drawer
                closeIcon={<img src={closeIcon} alt="closeIcon" className='img-icon-close' />}
                className={styles['assistant-drawer']}
                width={1280}
                onClose={handleCancel} title={t('projectEditAssistant')} placement="right" open={OpenDrawer} size='large' footer={<ModalFooterEnd handleOk={() => handleRequest()} onCancel={handleCancel} />}>
                <DrawerAssistant modelName={modelName} drawerTitle={t('projectEditAssistant')} openDrawer={OpenDrawer} selectedActionsSelected={selectedActionsSelected} selectedPluginGroup={selectedPluginGroup} handleNewBundle={handleNewBundle} retrievalConfig={retrievalConfig} topk={topk} maxTokens={maxTokens} handleMaxToken={handleMaxToken} handleToks={handleToks} bundilesList={bundilesList} handleNewActionModal={handleNewActionModal} handleNewCollection={handleNewCollection} selectedCollectionList={selectedRetrievalRows} actionHasMore={hasActionMore} actionList={actionList} collectionHasMore={hasMore} ref={drawerAssistantRef}
                    handleRetrievalConfigChange1={handleRetrievalConfigChange1} retrievalList={retrievalList} selectedActionsRows={selectedActionsRows} inputValue1={inputValueOne} inputValue2={inputValueTwo} handleMemoryChange1={handleMemoryChange1} memoryValue={memoryValue} handleAddPromptInput={handleAddPrompt} drawerName={drawerName} systemPromptTemplate={systemPromptTemplate} handleDeletePromptInput={handleDeletePromptInput} handleInputPromptChange={handleInputPromptChange} handleInputValueOne={handleInputValueOne} handleInputValueTwo={handleInputValueTwo} selectedRows={originalModelData} handleSelectModelId={handleSelectModelId} handleChangeName={handleChangeName} drawerDesc={drawerDesc} handleDescriptionChange={handleDescriptionChange} selectedRetrievalRows={selectedRetrievalRows}></DrawerAssistant>
            </Drawer>
            <ModelModal handleSetModelConfirmOne={handleSetModelConfirmOne} ref={childRef} open={modelOne} handleSetModelOne={handleModalCancel} getOptionsList={fetchModelsList} modelType='chat_completion'></ModelModal>
            <Modal closeIcon={<img src={closeIcon} alt="closeIcon" className='img-icon-close' />} centered footer={[
                <div className='footer-group' key='footer-group'>
                    <Button key="model" icon={<PlusOutlined />} onClick={handleNewModal} className='cancel-button'>
                        {t('projectRetrievalNew')}
                    </Button>
                    <div>
                        <span className='select-record'>
                            {recordsSelected1.length}  {recordsSelected1.length > 1 ? `${t('projectItemsSelected')}` : `${t('projectItemSelected')}`}
                        </span>
                        <Button key="cancel" onClick={handleCloseModal} className={`cancel-button ${styles.cancelButton}`}>
                            {t('cancel')}
                        </Button>
                        <Button key="submit" onClick={handleCreateConfirm} className='next-button'>
                            {t('confirm')}
                        </Button>
                    </div>
                </div>
            ]} title={t('projectAssistantRetrievalPlaceHolder')} open={openModalTable} width={1000} onCancel={handleCloseModal} className={`modal-inner-table ${styles['retrieval-model']}`}>
                <ModalTable title='New collection' name='collection' updatePrevButton={updateRetrievalPrevButton} defaultSelectedRowKeys={selectedRetrievalRows} hangleFilterData={hangleFilterData} mode='multiple' handleRecordsSelected={handleCollectionSelected} ifSelect={true} columns={collectionTableColumn} dataSource={retrievalList} hasMore={hasMore} id='collection_id' onChildEvent={handleChildRetrievalEvent} />
            </Modal>
            <Modal closeIcon={<img src={closeIcon} alt="closeIcon" className={styles['img-icon-close']} />} centered onCancel={handleModalClose} footer={[
                <div className='footer-group' key='group'>
                    <Button key="model" icon={<PlusOutlined />} onClick={handleCreateModelId} className='cancel-button'>
                        {t('projectNewModel')}
                    </Button>
                    <div>
                        <span className='select-record'>
                            1 {t('projectItemSelected')}
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
                <ModalTable title='New model' name="model" defaultSelectedRowKeys={Array.isArray(selectedModelRows) ? selectedModelRows : [selectedModelRows]} updatePrevButton={updateModelPrevButton} handleRecordsSelected={handleRecordsSelected} ifSelect={true} columns={modelsTableColumn} hasMore={hasModelMore} id='model_id' dataSource={options} onChildEvent={handleChildModelEvent}></ModalTable>
            </Modal>
            <Drawer zIndex={10001} className={styles.drawerCreate} closeIcon={<img src={closeIcon} alt="closeIcon" className={styles['img-icon-close']} />} onClose={handleActionCancel} title='Bulk Create Action' placement="right" open={OpenActionDrawer} size='large' footer={<ModalFooterEnd handleOk={() => handleActionRequest()} onCancel={handleActionCancel} />}>
                <ActionDrawer showTipError={tipSchema} onhandleTipError={onhandleTipError} schema={schema} onSchemaChange={handleSchemaChange} onRadioChange={onRadioChange} onChangeCustom={handleCustom} onChangeAuthentication={hangleChangeAuthorization} radioValue={radioValue} custom={custom} Authentication={Authentication} />
            </Drawer>
            <Modal closeIcon={<img src={closeIcon} alt="closeIcon" className={styles['img-icon-close']} />} onCancel={handleAssistantModalClose} centered footer={[
                <div className='footer-group' style={{ justifyContent: 'flex-end' }} key='footer'>
                    <div>
                        <span className='select-record'>
                            {recordsSelected.length} {t('projectItemSelected')}
                        </span>
                        <Button key="cancel" onClick={handleAssistantModalClose} className={`cancel-button ${styles.cancelButton}`}>
                            {t('cancel')}
                        </Button>
                        <Button key="submit" onClick={handleAssistantModalClose1} className='next-button' loading={confirmLoading}>
                            {t('confirm')}
                        </Button>
                    </div>

                </div>
            ]} title={t('projectPlaygroundSelectAssistant')} open={openAssistantModalTable} width={1000} className={`modal-inner-table ${styles.model1}`}>
                <ModalTable name='assistant' title='New assistant' ifAllowNew={true} updatePrevButton={updatePrevButton} defaultSelectedRowKeys={defaultSelectedAssistant} handleRecordsSelected={handleRecordsAssistantSelected} ifSelect={true} columns={assistantTableColumn} hasMore={modelHasMore} id='assistant_id' dataSource={optionList} onChildEvent={handleChildAssistantEvent}></ModalTable>
            </Modal>
            <CreateCollection handleFetchData={() => fetchDataRetrievalData({ limit: retrievalLimit || 20 })} handleModalCloseOrOpen={() => setOpenCollectionDrawer(false)} OpenDrawer={openCollectionDrawer}></CreateCollection>
            <Drawer width={700} open={contentDrawer} closeIcon={<img src={closeIcon} alt="closeIcon" className={styles['img-icon-close']} />} onClose={handleCloseContentDrawer} title={t('projectPlaygroundChatCompletion')}>
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
            <CreatePlugin handleConfirmRequest={handleConfirmRequest} open={pluginModalOpen} handleCloseModal={handleClosePluginModal}></CreatePlugin>
            <DeleteModal title={t('projectPlaygroundDeleteChatUpper')} projectName={chatId} open={OpenDeleteModal} describe={`${t('deleteItem')} ${t('projectPlaygroundChatLow')} ${chatId}`} onDeleteCancel={onDeleteCancel} onDeleteConfirm={onDeleteConfirm}></DeleteModal>
        </>
    );
}
export default Playground;