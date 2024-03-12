import closeIcon from '../../assets/img/x-close.svg'
import {
    LeftOutlined, RightOutlined
} from '@ant-design/icons';
import './modelModal.scss'
import QuestionCircleOutlined from '../../assets/img/questionCircleOutlined.svg?react'
import RightArrow from '../../assets/img/rightarrow.svg?react'

import IconComponent from '@/components/iconComponent';
import NoModel from '../../assets/img/NO_MODEL.svg?react'
import ApiErrorResponse from '../../constant/index';

import { Modal, Button, Spin, Input, Form, Switch, ConfigProvider, InputNumber, Select } from 'antd'
import { getAiModelsList, createModels, getAiModelsForm, getModelProviderList } from '../../axios/models'
import { toast } from 'react-toastify'
import react, { useState, useImperativeHandle } from 'react'
import { useTranslation } from "react-i18next";
import { modelModalProps, projectIdType, ModelProviderType, formDataType, promptListType } from '../../constant/index'
const ModelModal = react.forwardRef((props: modelModalProps, ref) => {
    useImperativeHandle(ref, () => ({
        fetchAiModelsList: () => {
            fetchModelProviderList(props.type)
        }
    }));

    const [modelTwoOpen, setModelTwoOpen] = useState(false)
    const [providerUrl, setProviderUrl] = useState('')
    const [formData, setFormData] = useState<formDataType>({
        properties: {},
        required: []
    })
    const { t } = useTranslation()
    const [nextLoading, setNextLoading] = useState(false)
    const [modelOneLoading, setModelOneLoading] = useState(false)
    const [nextLoading1, setNextLoading1] = useState(false)
    const [modelTypes, setModelTypes] = useState('chat_completion')
    const [name, setName] = useState('')
    const [centerLoading, setCenterLoading] = useState(false)
    const [proerties, setProerties] = useState('')

    const [type, setType] = useState('')
    const [propertyForm] = Form.useForm()
    const [wildcardForm] = Form.useForm()

    const typeReverse = {
        chat_completion: 'Chat Completion',
        text_embedding: 'Text Embedding',
        wildcard: 'Wildcard',
    }
    const [form] = Form.useForm()
    const [selectedOneId, setSelectedOneId] = useState('')
    const [providerId, setProviderId] = useState('')
    const [confirmLoading, setConfirmLoading] = useState(false)
    const [promptList, setPromptList] = useState<promptListType[]>([])
    const [form1] = Form.useForm()
    const [ModelProviderList, setModelProviderList] = useState<ModelProviderType[]>([])
    const [prividerName, setPrividerName] = useState('')
    const [openModalOne, setOpenModalOne] = useState(false)
    const [discription, setDiscription] = useState('')
    const handleCancel = () => {
        setOpenModalOne(false)
    }

    const fetchAiModelsList = async (offset: number, providerId: string) => {
        try {
            const res: any = await getAiModelsList(offset, 100, props.modelType as string, providerId)
            if (res.data.length !== 0) {
                setPromptList(res.data)
                setSelectedOneId(res.data[0].model_schema_id)
                setName(res.data[0].name)
                setType(res.data[0].type)
                setProerties(res.data[0].properties)
                setDiscription(res.data[0].description)

                setProviderId(res.data[0].provider_id)
            }

        } catch (e) {
            console.log(e)

        } finally {
            setCenterLoading(false)
        }
    }
    const handleClickModel = (item: projectIdType) => () => {
        setName(item.name)
        setSelectedOneId(item.model_schema_id)
        setProerties(item.properties)
        setDiscription(item.description)
        setType(item.type)
    }
    const fetchModelProviderList = async (type?: any) => {
        setModelOneLoading(true)
        const res: Record<string, any> = await getModelProviderList(type)
        setModelProviderList(res.data)
        setPrividerName(res.data[0].name)
        setProviderUrl(res.data[0].resources.taskingai_documentation_url)
        await fetchAiModelsList(0, res.data[0].provider_id)
        setModelOneLoading(false)
    }

    const handleNext = async () => {
        form.resetFields()
        form1.resetFields()
        propertyForm.resetFields()
        wildcardForm.resetFields()
        setNextLoading(true)
        try {
            await fetchFormData(providerId)
            setModelTwoOpen(true)
        } catch (e) {
            const apiError = e as ApiErrorResponse;
            toast.error(apiError.response.data.error.message)
        } finally {
            setNextLoading(false)
        }
    }

    const handleConfirm = async () => {
        const function_call = propertyForm.getFieldValue('function_call')
        const wildcardFunctioncall = wildcardForm.getFieldValue('function_call')
        if (!function_call) {
            propertyForm.setFieldValue('function_call', false)
        }
        if (!wildcardFunctioncall) {
            wildcardForm.setFieldValue('function_call', false)
        }
        const streaming = propertyForm.getFieldValue('streaming')
        const wildcardStreaming = wildcardForm.getFieldValue('streaming')
        if (!streaming) {
            propertyForm.setFieldValue('streaming', false)
        }
        if (!wildcardStreaming) {
            wildcardForm.setFieldValue('streaming', false)
        }
        const values = propertyForm.getFieldsValue();
        const wildcardValues = wildcardForm.getFieldsValue();
        const numericValues: any = {};
        const numericValues1: any = {}
        for (const key in values) {
            if (typeof values[key] === 'boolean') {
                numericValues[key] = values[key];
            } else {
                const value = Number(values[key]);
                numericValues[key] = isNaN(value) ? values[key] : value;
            }
        }
        for (const key in wildcardValues) {
            if (typeof wildcardValues[key] === 'boolean') {
                numericValues1[key] = wildcardValues[key];
            } else {
                const value = Number(wildcardValues[key]);
                numericValues1[key] = isNaN(value) ? wildcardValues[key] : value;
            }
        }
        form1.validateFields().then(async () => {
            await propertyForm.validateFields()
            await wildcardForm.validateFields()
            form.validateFields().then(async () => {
                setConfirmLoading(true)
                const params = {
                    name: form1.getFieldValue('name'),
                    model_schema_id: selectedOneId,
                    credentials: form.getFieldsValue(),
                    properties: numericValues,

                }
                const wildcardParams = {
                    name: form1.getFieldValue('name'),
                    model_schema_id: selectedOneId,
                    provider_model_id: form1.getFieldValue('provider_model_id'),
                    credentials: form.getFieldsValue(),
                    properties: numericValues1,
                    type: modelTypes
                }
                try {
                    await createModels(type === 'wildcard' ? wildcardParams : params)
                    setModelTwoOpen(false)
                    props.getOptionsList({ limit: 20 }, props.modelType as string)
                    props.handleSetModelConfirmOne(false)
                    setOpenModalOne(false)
                    setConfirmLoading(false)
                    toast.success(`${t('creationSuccessful')}`)

                } catch (e) {
                    const apiError = e as ApiErrorResponse;
                    toast.error(apiError.response.data.error.message)
                } finally {
                    setConfirmLoading(false)
                }
            })
        })
    }
    const fetchFormData = async (providerId: string) => {
        const res = await getAiModelsForm(providerId)
        setFormData(res.data.credentials_schema)
    }
    const handleSecondCancel = () => {
        setModelTwoOpen(false)
    }
    const handleModelTypes = (value: string) => {
        setModelTypes(value)
    }

    const getCenterData = async (providerId: string, name: string, item: any) => {
        setProviderId(providerId)
        setPrividerName(name)
        setProviderUrl(item.resources.taskingai_documentation_url)
        setCenterLoading(true)
    }
    const handleCancel1 = () => {
        setOpenModalOne(false)
        props.handleSetModelOne(false)
    }
    const handleNext1 = async () => {
        setNextLoading1(true)
        try {
            const res: any = await getAiModelsList(0, 100, props.modelType as string, providerId)
            if (res.data.length !== 0) {
                setPromptList(res.data)
                setSelectedOneId(res.data[0].model_schema_id)
                setName(res.data[0].name)
                setType(res.data[0].type)
                setProerties(res.data[0].properties)
                setDiscription(res.data[0].description)

                setProviderId(res.data[0].provider_id)
            } else {
                setPromptList([])
            }
            setCenterLoading(false)

            setOpenModalOne(true)
        } catch (e) {
            const apiError = e as ApiErrorResponse;
            toast.error(apiError.response.data.error.message)
        } finally {
            setNextLoading1(false)
        }
    }
    return (
        <div>
            <Modal zIndex={10001} title={openModalOne ? t('projectModelBaseModelSelection') : (!props.type ? t('projectProviderSelection') : (props.type === 'chat_completion' ? 'Provider Selection - Chat Completion' : 'Provider Selection - Text Embedding'))} onCancel={handleCancel1} footer={
                <>
                    {openModalOne ? <>
                        <Button key="cancel" onClick={handleCancel} className='cancel-button'>
                            <LeftOutlined />
                            {t('back')}
                        </Button>
                        <Button key="submit" onClick={handleNext} className='next-button' loading={nextLoading}>
                            {t('confirm')}
                        </Button>

                    </> : <>
                        <Button key="cancel" onClick={handleCancel1} className='cancel-button'>
                            {t('cancel')}
                        </Button>
                        <Button key="submit" onClick={handleNext1} className='next-button' loading={nextLoading1} >
                            {t('next')}
                            <RightOutlined />
                        </Button>
                    </>}
                </>} centered width={1280} open={props.open} closeIcon={<img src={closeIcon} alt="closeIcon" />} className={openModalOne ? 'create-model-one' : 'create-models'}>
                {openModalOne ?
                    <div className='create-model'>
                    
                        <div className='center'>
                            <Spin spinning={centerLoading}>
                                <div className='inputWithLabel1'>
                                    <div className='label'>{t('projectModelCreateModelSelectBaseModel')}</div>
                                </div>
                                {promptList.length === 0 ? <div className='img-model'><NoModel className='img-no-model' /></div> : <div className='card-map' >
                                    {promptList.map((item: promptListType, index: number) => (<div key={index} className={`providermodelcard ${selectedOneId === item.model_schema_id ? 'providermodelcardInner1' : ''}`} onClick={handleClickModel(item)}>
                                        <div className='providermodelcardInner'>
                                            <div className='frameWrapper'>
                                                <div className='frameDiv'>
                                                    <div className='modelproviderParent'>
                                                        <IconComponent providerId={item.provider_id} />
                                                        <div className='openaigpt4'>{item.model_schema_id}</div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                        <div className='chatCompletionParent'>
                                            <div className='chatCompletion'>{typeReverse[item.type as keyof typeof typeReverse]}</div>
                                            <RightArrow />
                                        </div>
                                    </div>))}
                                </div>
                                }

                            </Spin>

                        </div>
                        {promptList.length !== 0 ? <div className='right'>
                            <div className='chat-name'>{name}</div>
                            <div className='content'>
                                <div className='label3'>{t('projectModelProvider')}</div>
                                <div className='modelproviderParent'>
                                    <div className='openai'>{prividerName}</div>
                                </div>
                                <div className='label3'>{t('projectModelColumnType')}</div>
                                <span className='modeltypetag'>
                                    {typeReverse[type as keyof typeof typeReverse]}
                                </span>
                                <div className='label3' style={{ marginTop: '22px' }}>{t('projectAssistantsColumnDescription')}</div>
                                <div className='desc-info'>{discription}</div>
                            </div>
                            <div className='feature'>
                                {proerties && <div className='label3'>{t('projectModelFeatures')}</div>}
                                <div className='instanceParent'>
                                    {proerties && Object.entries(proerties).map(([key, property]) => (
                                        <div className='streamParent' key={key}>
                                            <div className='stream'>{key}</div>
                                            <div className='instanceChild' />
                                            <div className='on'>{String(property)}</div>
                                        </div>
                                    ))}
                                </div>
                            </div>

                        </div> : null}
                    </div>
                    : <Spin spinning={modelOneLoading}>
                        <div className='content'>
                            <div className='left'>
                                <div className='title'>
                                    {t('projectSelectProvider')}
                                </div>
                                <div className='content-list'>
                                    {ModelProviderList.map((item, index) => (
                                        <div key={index} onClick={() => getCenterData(item.provider_id, item.name, item)} className={`openai-card ${item.provider_id === providerId && 'select-provider'}`}>
                                            <div className='card-top'>
                                                <div className='provider'>
                                                    <IconComponent providerId={item.provider_id} />
                                                    <div className='name'>{item.name}</div>
                                                </div>
                                                <RightArrow />
                                            </div>
                                            <div className='desc'><span>{item.description}</span></div>
                                            {!props.type && <div className='choices'>{item.num_model_schemas} {item.num_model_schemas <= 1 ? t('projectModelLow') : t('projectModelLows')}</div>}
                                            {/* <div className='chat-text-type'>
                                        <span className='type-single'>Chat Completion</span>
                                    </div> */}
                                        </div>
                                    ))}
                                </div>
                                {/* <Paginations hasMore={hasMore} onFetchData={fetchModelProviderList}></Paginations> */}
                            </div>
                            {/* <div className='right'>
                        <div className='right-title'>
                            <IconComponent providerId={providerId} />
                            <span className='openAI'>{prividerName}</span>
                        </div>
                        <div className='desc'>OpenAI is a research organization that focuses on developing and promoting artificial intelligence (AI) in a manner that is safe and beneficial for humanity.</div>
                        <div className='resources'>
                            <div className='resource-title'>{t('projectModelResources')}</div>
                            {
                                resources.map((item, index) => (
                                    <div key={index} className='official-website'>{item.icon} <span style={{ marginLeft: '8px' }}>{item.name}</span></div>
                                ))
                            }
                        </div>
                    </div> */}
                        </div>
                    </Spin>
                }
            </Modal>

            <Modal zIndex={10001} className='modal-content' title={t('projectModelCreateModalOneTitle')} width={1000} centered open={modelTwoOpen} footer={[
                <Button key="cancel" onClick={handleSecondCancel} className='cancel-button'>
                    {t('back')}
                </Button>,
                <Button key="submit" onClick={handleConfirm} className='next-button' loading={confirmLoading}>
                    {t('confirm')}
                </Button>
            ]} closeIcon={<img src={closeIcon} alt="closeIcon" />} onCancel={handleSecondCancel}>
                <div className='second-modals'>
                    <div className='base-model' style={{ marginTop: '24px' }}>{t('projectModelColumnBaseModel')}</div>
                    <div className='frameParent'>
                        <div className='modelproviderParent'>
                            <IconComponent providerId={providerId} />
                            <div className='openai'>{selectedOneId}</div>
                        </div>
                    </div>
                    <ConfigProvider theme={{
                        components: {
                            Form: {
                                labelFontSize: 16, labelColor: '#2b2b2b'
                            }
                        }
                    }}>
                        <Form layout="vertical" form={form1} autoComplete="off" className='input-form' >
                            <Form.Item rules={[
                                {
                                    required: true,
                                    message: 'please enter name',
                                },
                            ]} label={t('projectModelCreateModelName')} name="name">
                                <div>
                                    <Input className='input-name' placeholder={t('projectModelCreatePlaceholder')} />
                                </div>
                            </Form.Item>
                            {type === 'wildcard' && <Form.Item rules={[
                                {
                                    required: true,
                                    message: 'please enter provider model ID',
                                },
                            ]} label='Provider model ID' name="provider_model_id">
                                <div>
                                    <Input className='input-name' placeholder='Enter provider model ID' />
                                </div>
                            </Form.Item>}

                        </Form>
                    </ConfigProvider>
                    {
                        type === 'wildcard' && <>
                            <div className='hr'></div>
                            <div className='credentials'>{t('projectModelColumnProperties')}</div>
                            <ConfigProvider theme={{
                                components: {
                                    Form: {
                                        labelFontSize: 16, labelColor: '#2b2b2b'
                                    }
                                }
                            }}>
                                <Form layout="vertical" className='second-form' form={wildcardForm}>
                                    <Form.Item label='Model type' required>
                                        <Select placeholder='Select model type' options={[{
                                            label: 'Text Embedding',
                                            value: 'text_embedding'
                                        }, {
                                            label: 'Chat Completion',
                                            value: 'chat_completion'
                                        }
                                        ]} onChange={handleModelTypes} value={modelTypes}>

                                        </Select>
                                    </Form.Item>
                                    {modelTypes === 'text_embedding' && <>
                                        <Form.Item label={t('projectModelEmbeddingSize')} required name='embedding_size' rules={[
                                            {
                                                required: true,
                                                message: `${t('projectModelEmbeddingSizeRequired')}`,
                                            },
                                        ]}>
                                            <div>
                                                <div className='description'>{t('projectModelEmbeddingSizeDesc')}</div>
                                                <InputNumber style={{ width: '100%' }} parser={(value: any) => (isNaN(value) ? '' : parseInt(value, 10))} placeholder={t('projectModelEmbeddingSizePlaceholder')} />
                                            </div>
                                        </Form.Item>
                                        <Form.Item label={t('projectModelInputMaxTokens')} name='input_token_limit'>
                                            <div>
                                                <div className='description'>{t('projectModelInputMaxTokensDesc')}</div>
                                                <InputNumber parser={(value: any) => (isNaN(value) ? '' : parseInt(value, 10))} style={{ width: '100%' }} placeholder={t('projectModelInputMaxTokensPlaceholder')} />
                                            </div>
                                        </Form.Item>
                                        <Form.Item label={'Max batch size'} name='max_batch_size'>
                                            <div>
                                                <div className='description'>The maximum number of text chunks that a provider's API can process in one call. Default value is 512.</div>
                                                <InputNumber parser={(value: any) => (isNaN(value) ? '' : parseInt(value, 10))} style={{ width: '100%' }} placeholder={'Enter batch size'} />
                                            </div>
                                        </Form.Item>
                                    </>}
                                    {modelTypes === 'chat_completion' && <>
                                        <Form.Item label="Function call" required name='function_call' valuePropName="checked">
                                            <div className='description'>{t('projectModelProoertiesDesc')}</div>
                                            <ConfigProvider theme={{
                                                components: {
                                                    Switch: {
                                                        colorPrimary: '#087443',
                                                        colorPrimaryHover: '#087443',
                                                    }
                                                }
                                            }}>
                                                <Form.Item name='function_call' className='switch'>
                                                    <Switch />
                                                </Form.Item>
                                            </ConfigProvider>
                                        </Form.Item>
                                        <Form.Item label="Streaming" required name='streaming' valuePropName="checked">
                                            <div className='description'>{t('projectModelStreamingDesc')}</div>
                                            <ConfigProvider theme={{
                                                components: {
                                                    Switch: {
                                                        colorPrimary: '#087443',
                                                        colorPrimaryHover: '#087443',
                                                    }
                                                }
                                            }}>
                                                <Form.Item name='streaming' className='switch'>
                                                    <Switch />
                                                </Form.Item>
                                            </ConfigProvider>
                                        </Form.Item>
                                        <Form.Item label={t('projectModelInputMaxTokens')} name='input_token_limit'>
                                            <div>
                                                <div className='description'>{t('projectModelInputMaxTokensDesc')}</div>
                                                <InputNumber parser={(value: any) => (isNaN(value) ? '' : parseInt(value, 10))} style={{ width: '100%' }} placeholder={t('projectModelInputMaxTokensPlaceholder')} />
                                            </div>
                                        </Form.Item>
                                        <Form.Item label="Output max tokens" name='output_token_limit'>
                                            <div>
                                                <div className='description'>{t('projectModelOutputMaxTokensDesc')}</div>
                                                <InputNumber style={{ width: '100%' }} parser={(value: any) => (isNaN(value) ? '' : parseInt(value, 10))} placeholder={t('projectModelOutputMaxTokensPlaceholder')} />
                                            </div>
                                        </Form.Item>
                                    </>}
                                </Form>
                            </ConfigProvider>
                        </>
                    }
                    {
                        !proerties && <>
                            {type !== 'wildcard' && <>
                                <div className='hr'></div>
                                <div className='credentials'>{t('projectModelColumnProperties')}</div>
                            </>}

                            {type === 'chat_completion' && <Form layout="vertical" className='second-form' form={propertyForm}>
                                <Form.Item label="Function call" required name='function_call' valuePropName="checked">
                                    <div className='description'>Indicates if the model supports function call.</div>
                                    <ConfigProvider theme={{
                                        components: {
                                            Switch: {
                                                colorPrimary: '#087443',
                                                colorPrimaryHover: '#087443',
                                            }
                                        }
                                    }}>
                                        <Form.Item name='function_call' className='switch'>
                                            <Switch />
                                        </Form.Item>
                                    </ConfigProvider>
                                </Form.Item>
                                <Form.Item label="Streaming" required name='streaming' valuePropName="checked">
                                    <div className='description'>{t('projectModelStreamingDesc')}</div>
                                    <ConfigProvider theme={{
                                        components: {
                                            Switch: {
                                                colorPrimary: '#087443',
                                                colorPrimaryHover: '#087443',
                                            }
                                        }
                                    }}>
                                        <Form.Item name='streaming' className='switch'>
                                            <Switch />
                                        </Form.Item>
                                    </ConfigProvider>
                                </Form.Item>
                                <Form.Item label={t('projectModelInputMaxTokens')} name='input_token_limit'>
                                    <div>
                                        <div className='description'>{t('projectModelInputMaxTokensDesc')}</div>
                                        <InputNumber parser={(value: any) => (isNaN(value) ? '' : parseInt(value, 10))} style={{ width: '100%' }} placeholder={t('projectModelInputMaxTokensPlaceholder')} />
                                    </div>
                                </Form.Item>
                                <Form.Item label="Output max tokens" name='output_token_limit'>
                                    <div>
                                        <div className='description'>{t('projectModelOutputMaxTokensDesc')}</div>
                                        <InputNumber style={{ width: '100%' }} parser={(value: any) => (isNaN(value) ? '' : parseInt(value, 10))} placeholder={t('projectModelOutputMaxTokensPlaceholder')} />
                                    </div>
                                </Form.Item>
                            </Form>}
                            {
                                type === 'text_embedding' && <Form layout="vertical" className='second-form' form={propertyForm} autoComplete='off'>
                                    <Form.Item label={t('projectModelEmbeddingSize')} required name='embedding_size' rules={[
                                        {
                                            required: true,
                                            message: `${t('projectModelEmbeddingSizeRequired')}`,
                                        },
                                    ]}>
                                        <div>
                                            <div className='description'>{t('projectModelEmbeddingSizeDesc')}</div>
                                            <InputNumber style={{ width: '100%' }} parser={(value: any) => (isNaN(value) ? '' : parseInt(value, 10))} placeholder={t('projectModelEmbeddingSizePlaceholder')} />
                                        </div>
                                    </Form.Item>
                                </Form>
                            }
                        </>
                    }
                    <div className='hr'></div>
                    <div className='credentials'>{t('projectModelCredentials')}</div>
                    <div className='label-desc' style={{ marginBottom: '24px' }}>
                        We will send a request to the provider to verify your credentials. All credentials are encrypted at rest with AES-256 and in transit with TLS 1.2.
                    </div>
                    <Form
                        layout="vertical"
                        autoComplete="off"
                        form={form}
                        className='second-form'
                    >
                        {formData.properties && Object.entries(formData.properties).map(([key, property]) => (
                            <Form.Item
                                key={key}
                                name={key}
                                label={key}
                                className='form-item'
                                rules={[
                                    {
                                        required: formData.required.includes(key) ? true : false,
                                        message: `Please input ${key}.`,
                                    },
                                ]}
                            >
                                <div>
                                    <div className='description'>{(property as { description: string }).description}</div>
                                    <Input placeholder={`Enter ${key}`} className='input' />
                                </div>
                            </Form.Item>
                        ))}
                    </Form>
                    {providerUrl && <div className='label-desc' style={{ marginBottom: '24px', display: 'flex', alignItems: 'center', marginTop: '15px', lineHeight: 1 }} >
                        <QuestionCircleOutlined style={{marginRight: '4px'}} />  Having trouble configuring the model?   <a href={providerUrl} target="_blank" rel="noreferrer" className='href' style={{marginLeft:'4px'}}>  See the documentation to learn more.</a>
                    </div>}
                </div>
            </Modal>
        </div>
    )
})
export default ModelModal
