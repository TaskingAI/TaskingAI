import closeIcon from '../../assets/img/x-close.svg'
import {
    RightOutlined,
} from '@ant-design/icons';
import './modelModal.scss'
// import { TKFormItemSwitch, TKFormItemInput } from '@taskingai/taskingai-ui'
import IconComponent from '@/components/iconComponent';
import NoModel from '../../assets/img/NO_MODEL.svg?react'

import { Modal, Pagination, Button, Spin, Input, Form, Switch, ConfigProvider, InputNumber } from 'antd'
import { getAiModelsList, createModels, getAiModelsForm, getModelProviderList } from '../../axios/models'
import { toast } from 'react-toastify'
import react, { useState, useImperativeHandle } from 'react'
import { modelModalProps, projectIdType, ModelProviderType, formDataType, promptListType } from '../../contant/index'
const ModelModal = react.forwardRef((props: modelModalProps, ref) => {
    useImperativeHandle(ref, () => ({
        fetchAiModelsList: () => {
            fetchModelProviderList()
        }
    }));

    const [modelTwoOpen, setModelTwoOpen] = useState(false)
    const [formData, setFormData] = useState<formDataType>({
        properties: {},
        required: []
    })
    const [nextLoading, setNextLoading] = useState(false)
    const [oneModelLoading, setOneModelLoading] = useState(false)
    const [totalCount, setTotalCount] = useState(0)
    const [name, setName] = useState('')
    const [centerLoading, setCenterLoading] = useState(false)
    const [proerties, setProerties] = useState('')
    const [type, setType] = useState('instruct_completion')
    const [propertyForm] = Form.useForm()
    const [modalPagination, setModalPagination] = useState({
        current: 1,
        pageSize: 3,
        total: 10,
    })
    const typeReverse = {
        instruct_completion: 'Instruct Completion',
        chat_completion: 'Chat Completion',
        text_embedding: 'Text Embedding'
    }
    const [form] = Form.useForm()
    const [selectedOneId, setSelectedOneId] = useState('')
    const [providerId, setProviderId] = useState('')
    const [confirmLoading, setConfirmLoading] = useState(false)
    const [promptList, setPromptList] = useState<promptListType[]>([])
    const [form1] = Form.useForm()
    const [ModelProviderList, setModelProviderList] = useState<ModelProviderType[]>([])
    const [prividerName, setPrividerName] = useState('')

    const handleCancel = () => {
        props.handleSetModelOne(false)
    }

    const fetchAiModelsList = async (offset: number, providerId: string) => {
        try {
            const res: any = await getAiModelsList(offset, 10, props.modelType as string, providerId)
            setTotalCount(res.total_count)
            if (res.data.length !== 0) {
                setPromptList(res.data)
                setSelectedOneId(res.data[0].model_schema_id)
                setName(res.data[0].name)
                setType(res.data[0].type)
                setProerties(res.data[0].properties)
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
        setType(item.type)
    }
    const fetchModelProviderList = async () => {
        setOneModelLoading(true)
        const res = await getModelProviderList()
        setModelProviderList(res.data)
        setPrividerName(res.data[0].name)
        await fetchAiModelsList(0, res.data[0].provider_id)
        setOneModelLoading(false)
    }

    const handleNext = async () => {
        form.resetFields()
        form1.resetFields()
        propertyForm.resetFields()
        setNextLoading(true)
        await fetchFormData(providerId)
        setNextLoading(false)
        setModelTwoOpen(true)
    }

    const handleConfirm = async () => {
        const function_call = propertyForm.getFieldValue('function_call')
        if (!function_call) {
            propertyForm.setFieldValue('function_call', false)
        }
        const streaming = propertyForm.getFieldValue('streaming')
        if (!streaming) {
            propertyForm.setFieldValue('streaming', false)
        }
        const values = propertyForm.getFieldsValue();
        const numericValues = {};
        for (const key in values) {
            if (typeof values[key] === 'boolean') {
                numericValues[key] = values[key];
            } else {
                const value = Number(values[key]);
                numericValues[key] = isNaN(value) ? values[key] : value;
            }
        }
        form1.validateFields().then(async () => {
            await propertyForm.validateFields()
            form.validateFields().then(async () => {
                setConfirmLoading(true)
                const params = {
                    name: form1.getFieldValue('name'),
                    model_schema_id: selectedOneId,
                    credentials: form.getFieldsValue(),
                    properties: numericValues
                }
                try {
                    await createModels(params)
                    setConfirmLoading(false)
                    toast.success('Creation successful!')
                    setModelTwoOpen(false)
                    props.getOptionsList({ limit: 20 }, props.modelType as string)
                    props.handleSetModelConfirmOne(false)
                } catch (e) {
                    toast.error(e.response.data.error.message)
                } finally {
                    setConfirmLoading(false)
                }
            })
        })
    }
    const fetchFormData = async (providerId: string) => {
        const res = await getAiModelsForm(providerId)
        setFormData(res.data[0].credentials_schema)
    }
    const handleSecondCancel = () => {
        setModelTwoOpen(false)
    }
    const handlePageChange = async (page: number) => {
        setModalPagination({
            ...modalPagination,
            current: page
        })
        await fetchAiModelsList((page - 1) * 10, providerId)
    }
    const getCenterData = async (providerId: string,name) => {
        setProviderId(providerId)
        setPrividerName(name)
        setCenterLoading(true)
        await fetchAiModelsList(0, providerId)
    }

    return (
        <div>
            <Modal title="Create Model - Base Model Selection" width={totalCount === 0 ? 1000 : 1378} centered open={props.open} footer={[
                <Button key="cancel" onClick={handleCancel} className='cancel-button'>
                    Cancel
                </Button>,
                <Button key="submit" onClick={handleNext} className='next-button' loading={nextLoading}>
                    Next
                </Button>
            ]} onCancel={handleCancel} closeIcon={<img src={closeIcon} alt="closeIcon" />} className='create-model-one'>
                <Spin spinning={oneModelLoading}>
                    <div className='create-model'>
                        <div className='left'>
                            <div className='modal-provider'>Model provider</div>
                            {ModelProviderList?.map((item, index) => (
                                <div key={index} onClick={() => getCenterData(item.provider_id,item.name)} className={`provider ${item.provider_id === providerId && 'select-provider'}`}>
                                    <IconComponent providerId={item.provider_id} />
                                    <div className='name'>{item.name}</div>
                                </div>
                            ))}
                        </div>
                        <div className='center'>
                            <Spin spinning={centerLoading}>
                                <div className='inputWithLabel1'>
                                    <div className='label'>Select a base model and add it to your project</div>
                                </div>
                                {totalCount === 0 ? <div className='img-model'><NoModel className='img-no-model' /></div> : <div className='card-map'>
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
                                            <RightOutlined />
                                        </div>
                                    </div>))}
                                </div>
                                }
                                {totalCount > 10 && <Pagination
                                    total={totalCount}
                                    pageSize={10}
                                    onChange={handlePageChange}
                                    defaultCurrent={1}
                                    current={modalPagination.current}
                                />}
                            </Spin>

                        </div>
                        {totalCount !== 0 && <div className='right'>
                            <div className='chat-name'>{name}</div>
                            <div className='content'>
                                <div className='label3'>Provider</div>
                                <div className='modelproviderParent'>
                                    <div className='openai'>{prividerName}</div>
                                </div>
                                <div className='label3'>Type</div>
                                <span className='modeltypetag'>
                                    {typeReverse[type as keyof typeof typeReverse]}
                                </span>
                            </div>
                            <div className='feature'>
                             {proerties && <div className='label3'>Features</div>}   
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

                        </div>}


                    </div>
                </Spin>

            </Modal>
            <Modal className='modal-content' title='Create Model - Basic Information' width={1000} centered open={modelTwoOpen} footer={[
                <Button key="cancel" onClick={handleSecondCancel} className='cancel-button'>
                    Back
                </Button>,
                <Button key="submit" onClick={handleConfirm} className='next-button' loading={confirmLoading}>
                    Confirm
                </Button>
            ]} closeIcon={<img src={closeIcon} alt="closeIcon" />} onCancel={handleSecondCancel}>
                <div className='second-modals'>
                    <div className='label'>Base model</div>
                    <div className='frameParent'>
                        <div className='modelproviderParent'>
                            <IconComponent providerId={providerId} />
                            <div className='openai'>{selectedOneId}</div>

                        </div>
                    </div>
                    <Form layout="vertical" form={form1} autoComplete="off" className='input-form' >
                        <Form.Item rules={[
                            {
                                required: true,
                                message: 'Please input name.',
                            },
                        ]} label="Model name" name="name">
                            <div>
                                <Input className='input-name' placeholder='Enter model name' />
                            </div>
                        </Form.Item>
                    </Form>
                    {
                        !proerties && <>
                            <div className='hr'></div>
                            <div className='credentials'>Properties</div>
                            {type === 'chat_completion' && <Form layout="vertical" className='second-form' form={propertyForm}>
                                <Form.Item label="Fucntion call" required name='function_call' valuePropName="checked">
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
                                    <div className='description'>Indicates if the model supports streaming of text chunks.</div>
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
                                <Form.Item label="Input max tokens" name='input_token_limit'>
                                    <div>
                                        <div className='description'>The maximum number of tokens that can be included in the model's input.</div>
                                        <InputNumber parser={(value: any) => (isNaN(value) ? '' : parseInt(value, 10))} style={{ width: '100%' }} placeholder='Enter max input tokens' />
                                    </div>
                                </Form.Item>
                                <Form.Item label="Output max tokens" name='output_token_limit'>
                                    <div>
                                        <div className='description'>The maximum number of tokens allowed in the output.</div>
                                        <InputNumber style={{ width: '100%' }} parser={(value: any) => (isNaN(value) ? '' : parseInt(value, 10))} placeholder='Enter max output tokens' />
                                    </div>
                                </Form.Item>
                            </Form>}
                            {
                                type === 'text_embedding' && <Form layout="vertical" className='second-form' form={propertyForm} autoComplete='off'>
                                    <Form.Item label="Embedding size" required name='embedding_size' rules={[
                                        {
                                            required: true,
                                            message: `Please input Embedding size.`,
                                        },
                                    ]}>
                                        <div>
                                            <div className='description'>The maximum number of tokens that the model can generate as output.</div>
                                            <InputNumber style={{ width: '100%' }} parser={(value: any) => (isNaN(value) ? '' : parseInt(value, 10))} placeholder='Enter embedding size' />
                                        </div>
                                    </Form.Item>
                                </Form>
                            }
                        </>
                    }
                    <div className='hr'></div>
                    <div className='credentials'>Credentials</div>
                    <div className='label-desc' style={{ marginBottom: '24px' }}>
                        Please enter your model credentials, and we will send one token to the model provider to verify the validity of your credentials. All credentials are encrypted at rest with AES-256 and in transit with TLS 1.2. Refer to <a className='href' href='https://docs.tasking.ai/docs/guide/model/overview#required-credentials-for-model-access' target='_blank' rel='noopener noreferrer'>documentation</a> for more information.
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
                </div>
            </Modal>
        </div>
    )
})
export default ModelModal