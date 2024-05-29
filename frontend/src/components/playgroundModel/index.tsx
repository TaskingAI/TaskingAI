import { Spin, Select, Slider, Input, ConfigProvider, Button, InputNumber, Checkbox } from 'antd'
import { useState, useEffect, useRef } from 'react'
import styles from './playgroundModal.module.scss'
import { useLocation, useNavigate } from 'react-router-dom';
import { setPlaygroundModelId, setPlaygroundModelName,setTemperatureData, setMaxTokenData, setTopPData, setTopKData, setStopSequencesData } from '@/Redux/actions/playground'
import { useDispatch } from 'react-redux';
import { getModelSchema, getModelsForm } from '@/axios/models'
import { RightOutlined, PlusOutlined } from '@ant-design/icons';
import DeleteInputIcon from '../../assets/img/deleteInputIcon.svg?react'
import NoModel from '@/assets/img/NO_MODEL.svg?react'
import ModelComponent from '../modelComponent';
import { modalGenerate } from '@/axios/playground'
import { SSE } from "sse.js";
import { useSelector } from 'react-redux';
import { toast } from 'react-toastify';
const origin = window.location.origin;
import IconComponent from '@/commonComponent/iconComponent/index.jsx';
function PlaygroundModel() {
    const [loading, setLoading] = useState(false)
    const { search, pathname } = useLocation();
    const [selectedModel, setSelectedModel] = useState<any>([{
        id: '',
        name: ''
    }])
    const navigation = useNavigate();
    const { modelReduxId } = useSelector((state: any) => state.modelId)
    const {temperatureRedux,maxTokenRedux,topPValueRedux,topKValueRedux,stopSequenceValueRedux }= useSelector((state: any) => state.playgroundModelRedux)
    const dispatch = useDispatch();
    const [systemContent, setSystemContent] = useState('')
    const [temperatureValue, setTemperatureValue] = useState(0.8)
    const [maxTokenValue, setMaxTokenValue] = useState(4096)
    const [topValue, setTopValue] = useState(0.1)
    const [topkValue, setTopkValue] = useState(5)
    const [providerId, setProviderId] = useState('')
    const [generateLoading, setGenerateLoading] = useState(false)
    const [streamSwitch, setStreamSwitch] = useState(true)
    const [open, setOpen] = useState(false)
    const [stopSequences, setStopSequences] = useState<any>()
    const [allowedConfigs, setAllowedConfigs] = useState<any>([])
    const [selectedData, setSelectedData] = useState<any>([])
    const [streamShow, setStreamShow] = useState(false)
    const contentListRef = useRef(null);
    const [temperatureCheckbox, setTemperatureCheckbox] = useState(false)
    const [maxTokenCheckbox, setMaxTokenCheckbox] = useState(false)
    const [stopSequencesCheckbox, setStopSequenceCheckbox] = useState(false)
    const [topPCheckbox, setTopPCheckbox] = useState(false)
    const [topKCheckbox, setTopKCheckbox] = useState(false)
    const [modelSchemaId, setModelSchemaId] = useState('')
    const [contentList, setContentList] = useState([{
        role: 'user',
        content: ''
    }])
    useEffect(() => {
        const list: any = contentListRef.current;
        if (list) {
            setTimeout(() => {
                list.scrollTop = list.scrollHeight;
                list.scrollTo({
                    top: list.scrollHeight,
                    behavior: 'smooth'
                });
            }, 0);
        }
    }, [contentList]);
    useEffect(() => {
        const fetchData = async () => {
            setLoading(true)
            const queryParams = new URLSearchParams(search);
            const modelSchemaId = localStorage.getItem('modelSchemaId')
            const providerId = localStorage.getItem('providerId')
            if (modelSchemaId && providerId) {
                setModelSchemaId(modelSchemaId)
                setProviderId(providerId)
                const modelId = queryParams.get('model_id');
                if (modelReduxId === modelId && modelId) {
                    dispatch(setPlaygroundModelId(modelId))
                    const allowedConfigs = JSON.parse(localStorage.getItem('allowedConfigs') as any)
                    const streaming = JSON.parse(localStorage.getItem('streaming') as any)
                    const contentModelList = JSON.parse(localStorage.getItem('modelContentList') as any)
                    setContentList(contentModelList)
                    setStreamShow(streaming)
                    setAllowedConfigs(allowedConfigs)
                    setSelectedData([modelId])
                    setMaxTokenCheckbox(maxTokenRedux)
                    setTemperatureCheckbox(temperatureRedux)
                    setTopPCheckbox(topPValueRedux)
                    setTopKCheckbox(topKValueRedux)
                    setStopSequenceCheckbox(stopSequenceValueRedux)
                } else if (modelId) {
                    const res = await getModelSchema(modelSchemaId)
                    setAllowedConfigs(res.data.allowed_configs || [])
                    dispatch(setPlaygroundModelId(modelId))
                    localStorage.setItem('allowedConfigs', JSON.stringify(res.data.allowed_configs))
                    setSelectedData([modelId])

                    const res1 = await getModelsForm(modelId)

                    setStreamShow(res1.data.properties.streaming)
                    localStorage.setItem('streaming', JSON.stringify(res1.data.properties.streaming))
                }
            }
            setLoading(false)
        }
        fetchData()
    }, [])
    useEffect(() => {
        const queryParams = new URLSearchParams(search);
        const modelId = queryParams.get('model_id');
        const modelName = queryParams.get('model_name');
        if (modelId && modelName) {
            dispatch(setPlaygroundModelId(modelId))
            dispatch(setPlaygroundModelName(modelName))
            setSelectedModel([{
                id: modelId,
                name: modelName
            }])
        }
    }, [search])
    const handleSelectModel = () => {
        setOpen(true)
    }
    const handleAddData = () => {
        setContentList((prev) => {
            const last = prev.length ? prev[prev.length - 1] : { role: 'assistant', content: '' }
            localStorage.setItem('modelContentList', JSON.stringify([...prev, {
                role: last.role === 'user' ? 'assistant' : 'user',
                content: ''
            }]))
            return [...prev, {
                role: last.role === 'user' ? 'assistant' : 'user',
                content: ''
            }]
        })
    }
    const handleDeletedata = (item: any) => {
        setContentList((prev) => {
            prev.splice(item, 1)
            localStorage.setItem('modelContentList', JSON.stringify([...prev]))
            return [...prev]
        })
    }
    const handleCloseModal = () => {
        setOpen(false)
    }
    const handleChangeValue = (value: any, index: number) => {
        setContentList((prev) => {
            prev[index].content = value
            localStorage.setItem('modelContentList', JSON.stringify([...prev]))
            return [...prev]
        })
    }
    const combineObject = (arr: any[]) => {
        let generateData = { role: '', content: '' }
        let hasError = false;
        arr.forEach((item) => {
            if (item.object === 'ChatCompletionChunk') {
                generateData.role = item.role
                generateData.content += item.delta
            }
            if (item.object === 'Error') {
                hasError = true;
                return toast.error(item.message)
            }
        })
        return hasError ? null : generateData
    }
    const handleModalConfirm = async (detailData: any) => {
        setLoading(true)
        setSelectedModel([{
            id: detailData.model_id,
            name: detailData.name
        }])
        const res = await getModelSchema(detailData.model_schema_id)
        console.log(res)
        localStorage.setItem('modelSchemaId', detailData.model_schema_id)
        setModelSchemaId(detailData.model_schema_id)
        setProviderId(detailData.provider_id)
        localStorage.setItem('providerId', detailData.provider_id)
        const res1 = await getModelsForm(detailData.model_id)
        setOpen(false)

        localStorage.setItem('streaming', JSON.stringify(res1.data.properties.streaming))
        localStorage.setItem('allowedConfigs', JSON.stringify(res.data.allowed_configs))
        setStreamShow(res1.data.properties.streaming)
        setAllowedConfigs(res.data.allowed_configs || [])
        dispatch(setPlaygroundModelId(detailData.model_id))
        dispatch(setPlaygroundModelName(detailData.name))
        navigation(`${pathname}?model_id=${detailData.model_id}&model_name=${detailData.name}`)
        setLoading(false)
    }
    const handleGenerate = async () => {
        const message = contentList.every((item) => {
            return item.content === ''
        })
        if (message) {
            return toast.error('Please enter the message')
        }
        let contentListNew = contentList
        if (systemContent !== '') {
            contentListNew = [{ role: 'system', content: systemContent }, ...contentList]
        }
        if (contentListNew[contentListNew.length - 1].role === 'assistant') {
            return toast.error('Last message should not be assistant message')
        }
        const configs = allowedConfigs.reduce((acc: any, key: any) => {
            if (key === 'temperature' && temperatureValue !== undefined && temperatureCheckbox) {
                acc[key] = temperatureValue;
            } else if (key === 'max_tokens' && maxTokenValue !== undefined && maxTokenCheckbox) {
                acc[key] = maxTokenValue;
            } else if (key === 'stop' && stopSequences !== undefined && stopSequencesCheckbox) {
                acc[key] = stopSequences;
            } else if (key === 'top_p' && topValue !== undefined && topPCheckbox) {
                acc[key] = topValue;
            } else if (key === 'top_k' && topkValue !== undefined && topKCheckbox) {
                acc[key] = topkValue;
            }
            return acc;
        }, {});

        const params = {
            model_id: selectedModel[0].id,
            configs: configs,
            stream: streamShow && streamSwitch,
            messages: contentListNew

        }
        setGenerateLoading(true)


        let arr: any[] = []
        if (streamShow && streamSwitch) {
            const token = localStorage.getItem('token')
            const project_base_url = `api/v1`
            let source;
            source = new SSE(`${origin}/${project_base_url}/inference/chat_completion`, {
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
                method: "POST",
                payload: JSON.stringify(params)
            })

            source.addEventListener("message", (event: any) => {
                if (event.data === '[DONE]') {
                    setGenerateLoading(false)
                    setContentList((prev) => {
                        localStorage.setItem('modelContentList', JSON.stringify([...prev, { role: 'user', content: '' }]))
                        return [...prev, { role: 'user', content: '' }]
                    }
                    )
                    return
                }
                const data = JSON.parse(event.data)
                arr.push(data)
                const comb = combineObject(arr)
                if (comb) {
                    const bindArr = [...contentList, comb]
                    localStorage.setItem('modelContentList', JSON.stringify(bindArr))
                    setContentList(bindArr)

                } else {
                    const bindArr = [...contentList]
                    localStorage.setItem('modelContentList', JSON.stringify(bindArr))
                    setContentList(bindArr)
                }
            })
            source.addEventListener('error', (e: any) => {
                setGenerateLoading(false)
                if (e.data) {
                    toast.error(JSON.parse(e.data).error.message, { autoClose: 10000 })
                }
            })

        } else {
            try {
                const res: any = await modalGenerate(params)
                setContentList((prev) => {
                    const data = [{
                        content: res.data.message.content,
                        role: res.data.message.role
                    },
                    {
                        content: '',
                        role: 'user'
                    }]
                    localStorage.setItem('modelContentList', JSON.stringify([...prev, ...data]))
                    return [...prev, ...data]
                })
            } catch (e) {
                const apiError = e as any
                if (apiError.response.data.error) {
                    toast.error(apiError.response.data.error.message)
                }
            } finally {
                setGenerateLoading(false)
            }
        }
    }

    const handleTemperatureValue = (value: any) => {
        setTemperatureValue(value)
    }
    const handleMaxTokenValue = (value: any) => {
        setMaxTokenValue(value)
    }
    const handleTopPValue = (value: any) => {
        setTopValue(value)
    }
    const handleTopkValue = (value: any) => {
        setTopkValue(value)
    }
    // const handleStopSequences = (e: any) => {
    //     setStopSequences(e.target.value)
    // }
    const handleStreamSwitch = (e: any) => {
        setStreamSwitch(e.target.checked)
    }
    const handleRoleChange = (value: any, index: number) => {
        setContentList((prev) => {
            prev[index].role = value
            localStorage.setItem('modelContentList', JSON.stringify([...prev]))
            return [...prev]
        })
    }
    const handleChangeContentValue = (value: any) => {
        setSystemContent(value)
    }
    const handleTemperatureCheckbox = (e:any) => {
        setTemperatureCheckbox(e.target.checked)
        dispatch(setTemperatureData(e.target.checked))
    }
    const handleMaxTokenCheckbox = (e:any) => {
        setMaxTokenCheckbox(e.target.checked)
        dispatch(setMaxTokenData(e.target.checked))
    }
    const handleStopSequencesCheckbox = (e:any) => {
        setStopSequenceCheckbox(e.target.checked)
        dispatch(setStopSequencesData(e.target.checked))
    }
    const handleTopPCheckbox = (e:any) => {
        setTopPCheckbox(e.target.checked)
        dispatch(setTopPData(e.target.checked))
    }
    const handleTopKCheckbox = (e:any) => {
        setTopKCheckbox(e.target.checked)
        dispatch(setTopKData(e.target.checked))
    }
    return (
        <Spin spinning={loading}>
            {selectedModel[0].id ? <div className={styles.playgroundModal}>
                <div className={styles.left}>
                    <div className={styles.leftTop}>
                        <div className={styles.modal}>Model</div>
                        <Select
                            placeholder='Select a model'
                            open={false}
                            className={styles['select-model']}
                            suffixIcon={<RightOutlined />}
                            removeIcon={null}
                            style={{caretColor: 'transparent'}}
                            value={selectedModel[0].name} onClick={handleSelectModel}
                        >
                        </Select>
                    </div>
                    <div className={styles.leftBottom}>
                        <div className={styles.generateOptions}>
                            <div className={styles.configuration}>Generation options</div>
                            <div style={{ display: 'flex', margin: '12px 0 0 0' }}>
                                <IconComponent providerId={providerId} />  <div className={styles.responseStream}>{modelSchemaId}</div>
                            </div>

                            {streamShow && <div style={{ marginTop: '12px' }}><Checkbox value={streamSwitch} defaultChecked={true} onChange={(e) => handleStreamSwitch(e)} /><span style={{ marginLeft: '8px' }}>Stream</span></div>}
                        </div>
                        <div style={{ margin: '24px' }}>
                            <div className={styles.configuration}>Configuration</div>
                            <ConfigProvider theme={{
                                components: {
                                    Slider: {
                                        dotActiveBorderColor: '#099250',
                                        handleColor: '#099250',
                                        handleActiveColor: '#099250',
                                        trackBg: '#099250',
                                        trackHoverBg: '#099250',
                                    }
                                },
                                token: {
                                    colorPrimaryBorderHover: '#099250',
                                }
                            }}>
                                {allowedConfigs.includes('temperature') && <div style={{ display: 'flex', alignItems: 'center', marginTop: '12px' }}>
                                    <Checkbox value={temperatureCheckbox} defaultChecked={temperatureCheckbox} onChange={handleTemperatureCheckbox} />
                                    <div style={{ flex: 1, marginLeft: '12px' }}>
                                        <div className={styles.temperature}>
                                            <span style={{ color: temperatureCheckbox ? '#2B2B2B' : '#BFBFBF' }}>Temperature</span>
                                            {temperatureCheckbox && <InputNumber
                                                className={styles['code-input']} step={0.01} onChange={(value: number | null) => setTemperatureValue(value as number)} min={0} max={1} value={temperatureValue}></InputNumber>}
                                        </div>
                                        {temperatureCheckbox && <Slider max={1} min={0} step={0.01} value={temperatureValue} onChange={handleTemperatureValue} />}

                                    </div>

                                </div>}
                                {allowedConfigs.includes('max_tokens') && <div style={{ display: 'flex', alignItems: 'center', marginTop: '12px' }}>
                                    <Checkbox value={maxTokenCheckbox} defaultChecked={maxTokenCheckbox} onChange={handleMaxTokenCheckbox} />
                                    <div style={{ flex: 1, marginLeft: '12px' }}>
                                        <div className={styles.temperature}>
                                            <span style={{ color: maxTokenCheckbox ? '#2B2B2B' : '#BFBFBF' }}>Max Tokens</span>
                                            {maxTokenCheckbox && <InputNumber parser={(value: any) => {
                                                const parsedValue = parseInt(value, 10);
                                                return isNaN(parsedValue) ? 1 : Math.max(parsedValue, 1);
                                            }} className={styles['code-input']} step={1} value={maxTokenValue} onChange={(value: number | null) => setMaxTokenValue(value as number)} min={1} max={8192}></InputNumber>}

                                        </div>
                                        {maxTokenCheckbox && <Slider max={8192} min={1} step={1} value={maxTokenValue} onChange={handleMaxTokenValue}></Slider>}

                                    </div>
                                </div>}
                                {allowedConfigs.includes('stop') && <div style={{ display: 'flex', alignItems: 'center', marginTop: '12px' }}>
                                    <Checkbox value={stopSequencesCheckbox} defaultChecked={stopSequencesCheckbox} onChange={handleStopSequencesCheckbox} />
                                    <div style={{ flex: 1, marginLeft: '12px' }}>
                                        <div className={styles.temperature} style={{ color: stopSequencesCheckbox ? '#2B2B2B' : '#BFBFBF' }}>
                                            Stop sequences
                                        </div>
                                        {stopSequencesCheckbox && <Input className={styles['code-input']} onChange={(e: any) => setStopSequences([e.target.value])} value={stopSequences}></Input>}
                                    </div>
                                </div>}
                                {allowedConfigs.includes('top_p') && <div style={{ display: 'flex', alignItems: 'center', marginTop: '12px' }}>
                                    <Checkbox value={topPCheckbox} defaultChecked={topPCheckbox} onChange={handleTopPCheckbox} />
                                    <div style={{ flex: 1, marginLeft: '12px' }}>
                                        <div className={styles.temperature}>
                                            <span style={{ color: topPCheckbox ? '#2B2B2B' : '#BFBFBF' }}>Top P</span>
                                            {topPCheckbox && <InputNumber
                                                parser={(value: any) => value.replace(/\$\s?|(,*)/g, '')} className={styles['code-input']} step={0.01} value={topValue} onChange={(value: number | null) => setTopValue(value as number)} min={0} max={1}></InputNumber>}
                                        </div>
                                        {topPCheckbox && <Slider max={1} step={0.01} value={topValue} onChange={handleTopPValue}></Slider>}
                                    </div>
                                </div>}
                                {allowedConfigs.includes('top_k') && <div style={{ display: 'flex', alignItems: 'center', marginTop: '12px' }}>
                                    <Checkbox value={topKCheckbox} defaultChecked={topKCheckbox} onChange={handleTopKCheckbox} />
                                    <div style={{ flex: 1, marginLeft: '12px' }}>
                                        <div className={styles.temperature}>
                                            <span style={{ color: topKCheckbox ? '#2B2B2B' : '#BFBFBF' }}>Top K</span>
                                            {topKCheckbox && <InputNumber parser={(value: any) => value.replace(/\\B(?=(\d{3})+(?!\d))/g, '').replace(/,/g, '')} className={styles['code-input']} step={1} value={topkValue} onChange={(value: number | null) => setTopkValue(value as number)} min={0} max={2048}></InputNumber>}
                                        </div>
                                        {topKCheckbox && <Slider max={2048} min={0} step={1} value={topkValue} onChange={handleTopkValue}></Slider>}
                                    </div>

                                </div>}

                            </ConfigProvider>
                        </div>

                    </div>
                </div>
                <div className={styles.right} >
                    <div className={styles.content} ref={contentListRef}>
                        <div className={styles.contentItem}>
                            <Select style={{ cursor: 'auto' }} className={styles.systemSelect} options={[{ value: 'system', label: 'System' }]} value='system' open={false}></Select>
                            <Input.TextArea placeholder='Enter system message' autoSize value={systemContent} className={styles.input} onChange={(e) => handleChangeContentValue(e.target.value)}></Input.TextArea>
                        </div>
                        {contentList.map((item: any, index: number) => (
                            <div className={styles.contentItem} key={index}>
                                <Select className={styles.select} onChange={(value) => handleRoleChange(value, index)} value={item.role} options={[{
                                    value: 'user',
                                    label: 'User'
                                },
                                {
                                    value: 'assistant',
                                    label: 'Assistant'

                                }]}></Select>
                                <Input.TextArea placeholder={item.role === 'assistant' ? 'Enter assistant message' : 'Enter user message'} autoSize value={item.content} className={styles.input} onChange={(e) => handleChangeValue(e.target.value, index)}></Input.TextArea>
                                <DeleteInputIcon onClick={() => handleDeletedata(index)} style={{ cursor: 'pointer' }} />
                            </div>
                        ))}
                        <Button onClick={handleAddData} icon={<PlusOutlined />} style={{ marginTop: '12px', background: 'white' }}>Add</Button>
                    </div>
                    <div className={styles.generate}>
                        <Button className='next-button' onClick={handleGenerate} loading={generateLoading}>Generate</Button>
                    </div>
                </div>
            </div> : <div className={styles['selectAssistant']}>
                {<NoModel className={styles.svg} />}
                <div className={styles['select-assistant']}>Select a chat completion model to start</div>
                <div className={styles['header-news']}>
                    <Button className={styles['prompt-button']} onClick={handleSelectModel}>Select model</Button>
                </div>
            </div>}
            <ModelComponent defaultSelectedData={selectedData} modalTableOpen={open} handleCloseModal={handleCloseModal} handleModalConfirm={handleModalConfirm} />

        </Spin>
    )
}
export default PlaygroundModel