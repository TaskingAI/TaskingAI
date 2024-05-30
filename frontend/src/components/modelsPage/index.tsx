import { useEffect, useState, useRef, ChangeEvent } from 'react'
import { Modal, Button, Spin, Space, Input, Form, Drawer, Tooltip, ConfigProvider, Select, InputNumber, Switch, Popover } from 'antd'
import styles from './modelsPage.module.scss'
import { getModelsList, updateModels, deleteModels, getModelsForm, getAiModelsForm, getAiModelsList, getModelSchema } from '@/axios/models'
import tooltipTitle from '../../contents/tooltipTitle'
import { useSelector, useDispatch } from 'react-redux';
import { fetchModelsData } from '../../Redux/actions';
import JumpIcon from '../../assets/img/assistantJumpIcon.svg?react'
import { setPlaygroundSelect } from '@/Redux/actions/playground.ts'
import EditIcon from '../../assets/img/editIcon.svg?react'
import MoreIcon from '@/assets/img/moreIcon.svg?react'
import ViewCode from '@/commonComponent/viewCode/index.tsx'
import { getViewCode } from '@/axios/index'
import CommonComponents from '../../contents/index.tsx'
import ModalTable from '@/components/modalTable';
import ModelModal from '@/components/modelModal';
import closeIcon from '../../assets/img/x-close.svg'
import { toast } from 'react-toastify';
import { useNavigate } from 'react-router-dom'
import { useTranslation } from "react-i18next";
import IconComponent from '@/commonComponent/iconComponent';
import { setLoading } from '../../Redux/actions.ts'
import ApiErrorResponse, { RecordType, ChildRefType, formDataType } from '../../constant/index.ts'
function ModelsPage() {
    const { modelLists, loading } = useSelector((state: any) => state.model);
    const dispatch = useDispatch()
    const navigate = useNavigate()
    const [propertyForm] = Form.useForm()
    const [viewCodeData, setViewCodeData] = useState('')
    const [viewCodeOpen, setViewCodeOpen] = useState(false)
    const {  tooltipEditTitle, tooltipPlaygroundTitle,tooltipMoreTitle } = tooltipTitle();
    const { modelsTableColumn } = CommonComponents();
    const { t } = useTranslation();
    const [form] = Form.useForm()
    const [form1] = Form.useForm()
    const [confirmloading, setConfirmLoading] = useState(false);
    const childRef = useRef<ChildRefType | null>(null);
    const [modelOne, setModelOne] = useState(false);
    const [modelId, setModelId] = useState('');
    const [openDeleteModal, setOpenDeleteModal] = useState(false)
    const [modelList, setModelList] = useState([])
    const [formData, setFormData] = useState<formDataType>({
        properties: {},
        required: []
    })
    const [resetButtonShow, setResetButtonShow] = useState(true)
    const [record, setRecord] = useState<RecordType>({
        name: '',
        model_id: '',
        model_schema_id: '',
        provider_id: '',
        type: '',
        properties: {},
        provider_model_id: ''
    });
    const [limit, setLimit] = useState(20)
    const [isVisible, setIsVisible] = useState(true);
    const [formShow, setFormShow] = useState(false)
    const [updatePrevButton, setUpdatePrevButton] = useState(false)
    const [disabled, setDisabled] = useState(true);
    const [drawerEditOpen, setDrawerEditOpen] = useState(false)
    const [secondModalNameValue, setSecondModalNameValue] = useState('')
    const [selectedSecondId, setSelectedSecondId] = useState('')
    const [deleteValue, setDeleteValue] = useState('');
    const [providerId, setProviderId] = useState('')
    const [hasMore, setHasMore] = useState(false)
    const [type, setType] = useState('')
    const [deleteLoading, setDeleteLoading] = useState(false)
    const [properties, setProperties] = useState({})
    const [wildcardForm] = Form.useForm()
    const [functionCall, setFunctionCall] = useState(false)
    const [streaming, setStreaming] = useState(false)
    const [modelType, setModelType] = useState('')
    const [editLoading, setEditLoading] = useState(false)
    const handleViewCode = () => {
        setIsVisible(false)
        setViewCodeOpen(true)
    }
    const content = (
        <div style={{ cursor: 'pointer' }}>
            <p className={styles['popover-eidt']} onClick={handleViewCode}>View code</p>
            <p className={styles['popover-delete']} onClick={() => handleDelete(record as RecordType)}>Delete</p>
        </div>
    );
    useEffect(() => {
        const fetchCodeData = async () => {
            const res = await getViewCode('model')
            setViewCodeData(res.data)
        }
        fetchCodeData()
    }, [])
    const fetchData = async (params: Record<string, any>) => {
        try {
            const res: any = await getModelsList(params)
            const data = res.data.map((item: RecordType) => {
                return {
                    ...item,
                    key: item.model_id,
                }
            })
            setHasMore(res.has_more)
            setModelList(data)
        } catch (e) {
            console.log(e)
        }
    }
    useEffect(() => {
        dispatch(setLoading(true));
        if (modelLists.data.length > 0) {
            const data = modelLists.data.map((item: RecordType) => {
                return {
                    ...item,
                    key: item.model_id,
                }
            })
            setModelList(data)
            setHasMore(modelLists.has_more)

        } else {
            setModelList([])
        }
        dispatch(setLoading(false));

    }, [modelLists])
    const columns = [...modelsTableColumn]
    columns.push(
        {
            title: `${t('projectColumnActions')}`,
            key: 'action',
            width: 157,
            fixed: 'right',
            render: (_: string, record: RecordType) => (
                <Space size="middle">
                    <div onClick={record.type !== 'chat_completion' ? undefined : () => handleJump(record as RecordType)} className={`table-edit-icon ${record.type !== 'chat_completion' && styles.typeDisabled} `}>
                        <Tooltip placement='bottom' title={record.type === 'chat_completion' && tooltipPlaygroundTitle} color='#fff' arrow={false} overlayClassName='table-tooltip'>
                            <JumpIcon />
                        </Tooltip>
                    </div>
                    <div onClick={()=>handleEdit(record)} className='table-edit-icon' >
                        <Tooltip placement='bottom' title={tooltipEditTitle} color='#fff' arrow={false} overlayClassName='table-tooltip'>
                            <EditIcon />
                        </Tooltip>

                    </div>
                    <div className='table-edit-icon' onClick={()=>setRecord(record)}>
                    {isVisible ? <Tooltip placement='bottom' title={tooltipMoreTitle} color='#fff' arrow={false} overlayClassName='table-tooltip'>
                        <Popover trigger="click" placement='bottom' content={content} arrow={false}>
                        <MoreIcon  />
                        </Popover>
                    </Tooltip> : <MoreIcon  />}

                    </div>
                </Space>
            )
        }
    );
    const handleModalCancel = () => {
        setModelOne(false)
    }
    const handleSetModelConfirmOne = () => {
        setModelOne(false)
        setUpdatePrevButton(true)

    }
    const handleDelete = (record: RecordType) => {
        setIsVisible(false)
        setOpenDeleteModal(true)
        setDeleteValue('')
        setDisabled(true)
        setRecord(record)

    }
 
    const handleJump = async (value: RecordType) => {
        dispatch(setLoading(true));
        localStorage.setItem('modelSchemaId', value.model_schema_id)
        localStorage.setItem('providerId', value.provider_id)
        const res = await getModelSchema(value.model_schema_id)
        localStorage.setItem('allowedConfigs', JSON.stringify(res.data.allowed_configs))
        const res1 = await getModelsForm(value.model_id)
        localStorage.setItem('streaming', JSON.stringify(res1.data.properties.streaming))
        dispatch(setLoading(false));
        dispatch(setPlaygroundSelect('chat_completion'))
        navigate(`/project/playground?model_id=${value.model_id}&model_name=${value.name}`)
    }
    const handleDeleteValue = (e: ChangeEvent<HTMLInputElement>) => {
        setDeleteValue(e.target.value)
        if (e.target.value === record.name) {
            setDisabled(false)
        } else {
            setDisabled(true)
        }
    }
    const handleDeleteConfirm = async () => {
        setDeleteLoading(true)
        const params = {
            model_id: record.model_id
        }

        const limit1: number = limit || 20
        await deleteModels(params.model_id as string)
        dispatch(fetchModelsData(limit1) as any);
        setDeleteLoading(false)
        setUpdatePrevButton(true)
        setOpenDeleteModal(false)
        setIsVisible(true)
    }
    const handleCreateModel = async () => {
        setModelOne(true)
        childRef.current?.fetchAiModelsList()
    }
    const onClose = () => {
        setDrawerEditOpen(false);
        setIsVisible(true)
    };
    const handleEdit = async (record: RecordType) => {
        setIsVisible(false)
        setDrawerEditOpen(true)

        setEditLoading(true)
        const res = await getAiModelsList(0, 100, record.provider_id)
        const item = res.data.find((item: any) => {
            return item.model_schema_id === record.model_schema_id
        }).type
        setModelType(item)
        setFormShow(true)
        setResetButtonShow(true)
        form1.setFieldsValue({
            name: record.name,
            provider_model_id: record.provider_model_id
        })
        propertyForm.setFieldsValue({
            function_call: record.properties?.function_call,
            streaming: record.properties?.streaming,
            input_token_limit: record.properties?.input_token_limit,
            output_token_limit: record.properties?.output_token_limit,
            embedding_size: record.properties?.embedding_size,
            max_batch_size: record.properties?.max_batch_size

        })
        wildcardForm.setFieldsValue({
            function_call: record.properties?.function_call,
            streaming: record.properties?.streaming,
            input_token_limit: record.properties?.input_token_limit,
            output_token_limit: record.properties?.output_token_limit,
            embedding_size: record.properties?.embedding_size,
            max_batch_size: record.properties?.max_batch_size
        })
        setSelectedSecondId(record.model_schema_id)
        setSecondModalNameValue(record.name)
        setModelId(record.model_id)
        setType(record.type)
        setFunctionCall(record.properties?.function_call)
        setStreaming(record.properties?.streaming)
        setProperties(record.properties)
        setProviderId(record.provider_id)
        await fetchEditFormData(record.model_id, record.provider_id)
        setEditLoading(false)
    }
    const fetchEditFormData = async (model_id: string, provider_id: string) => {
        try {
            const res = await getModelsForm(model_id)
            const res1 = await getAiModelsForm(provider_id)
            setFormData(res1.data.credentials_schema)
            form.setFieldsValue(res.data.display_credentials)
        } catch (e) {
            const error = e as ApiErrorResponse
            const errorMessage = error.response.data.error.message
            toast.error(errorMessage)
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
        await form1.validateFields().then(async () => {
            await propertyForm.validateFields()
            await wildcardForm.validateFields()
            await form.validateFields().then(async () => {
                const params = {
                    name: form1.getFieldValue('name'),
                    credentials: resetButtonShow ? undefined : form.getFieldsValue(),
                    properties: numericValues,
                    model_schema_id: selectedSecondId,
                    host_type: 'provider'

                }
                const wildcardParams = {
                    name: form1.getFieldValue('name'),
                    model_schema_id: selectedSecondId,
                    provider_model_id: form1.getFieldValue('provider_model_id'),
                    credentials: resetButtonShow ? undefined : form.getFieldsValue(),
                    properties: numericValues1,
                    type: type,
                    host_type: 'provider'
                }
                try {
                    setConfirmLoading(true)
                    await updateModels(modelId, modelType === 'wildcard' ? wildcardParams : params)
                    toast.success(`${t('updateSuccessful')}`)
                    setDrawerEditOpen(false)
                
                    const limit1 = limit || 20
                    dispatch(fetchModelsData(limit1) as any);
                } catch (error) {
                    const errorType = error as ApiErrorResponse;
                    const errorMessage: string = errorType.response.data.error.message;
                    toast.error(errorMessage)
                } finally {
                    setIsVisible(true)
                }
                setUpdatePrevButton(true)
                setConfirmLoading(false)
            })
        })
    }
    const handleDeleteCancel = () => {
        setDeleteValue('')
        setOpenDeleteModal(false)
        setIsVisible(true)
    }
    const handleValuesChange = (changedValues: object) => {
        form.validateFields(Object.keys(changedValues));
    };
    const handleResetCredentials = async () => {
        form.resetFields();
        setFormShow(false)
        setResetButtonShow(false)
    }
    const handleChildEvent = async (value: Record<string, any>) => {
        setUpdatePrevButton(false)
        setLimit(value.limit)
        await fetchData(value);
    }

    const fetchData1 = async () => {
        dispatch(fetchModelsData(20) as any);
    }
    const handleModelTypes = (value: string) => {
        setType(value)
    }
   const handleCloseViewCode = () => {
        setIsVisible(true)
        setViewCodeOpen(false)
   }
    return (
        <div className={styles["models-page"]}>
            <Spin spinning={loading} wrapperClassName={styles.spinloading}>
                <ModalTable title='New model' updatePrevButton={updatePrevButton} onChildEvent={handleChildEvent} name="model" hasMore={hasMore} id='model_id' columns={columns} ifSelect={false} onOpenDrawer={handleCreateModel} dataSource={modelList} />
            </Spin>
            <ModelModal getOptionsList={fetchData1} ref={childRef} open={modelOne} handleSetModelOne={handleModalCancel} handleSetModelConfirmOne={handleSetModelConfirmOne}></ModelModal>

            <Drawer title={t('projectEditModel')} width={700} closeIcon={<img src={closeIcon} alt="closeIcon" />} footer={[
                <Button key="cancel" onClick={onClose} className='cancel-button'>
                    {t('cancel')}
                </Button>,
                <Button key="submit" loading={confirmloading} onClick={handleConfirm} className={`next-button ${styles.button}`}>
                    {t('confirm')}
                </Button>
            ]} placement="right" onClose={onClose} open={drawerEditOpen} className={styles['editModal']}>
                <Spin spinning={editLoading}>
                    <div className={styles['second-modal']}>
                        <div className={styles['label']}>{t('projectModelColumnBaseModel')}</div>
                        <div className={styles['frameParent']}>
                            <div className={styles['modelproviderParent']}>
                                <IconComponent providerId={providerId} />
                                <div className={styles['openai']}>{selectedSecondId}</div>
                            </div>
                        </div>
                        <ConfigProvider theme={{
                            components: {
                                Form: {
                                    labelFontSize: 16, labelColor: '#2b2b2b'
                                }
                            }
                        }}>
                            <Form layout="vertical" form={form1} autoComplete="off" className={styles['input-form']} >
                                <Form.Item rules={[
                                    {
                                        required: true,
                                        message: `${t('projectInputName')}`,
                                    },
                                ]} label={t('projectModelCreateModelName')} name="name">
                                    <Input className={styles['input-name']} placeholder={t('projectModelCreatePlaceholder')} key={secondModalNameValue} />
                                </Form.Item>
                                {modelType === 'wildcard' && <Form.Item rules={[
                                    {
                                        required: true,
                                        message: 'please enter provider model ID',
                                    },
                                ]} label='Provider model ID' name="provider_model_id">
                                    <Input className={styles['input-name']} placeholder='Enter provider model ID' />
                                </Form.Item>}
                            </Form>
                        </ConfigProvider>
                        {
                            modelType === 'wildcard' && <>
                                <div className={styles['hr']}></div>
                                <div className={styles['credentials']}>{t('projectModelColumnProperties')}</div>
                                <ConfigProvider theme={{
                                    components: {
                                        Form: {
                                            labelFontSize: 16, labelColor: '#2b2b2b'
                                        }
                                    }
                                }}>
                                    <Form layout="vertical" className={styles['second-form']} form={wildcardForm}>
                                        <Form.Item label='Model type' required>
                                            <Select placeholder='Select model type' options={[{
                                                label: 'Text Embedding',
                                                value: 'text_embedding'
                                            }, {
                                                label: 'Chat Completion',
                                                value: 'chat_completion'
                                            }
                                            ]} onChange={handleModelTypes} value={type}>
                                            </Select>
                                        </Form.Item>
                                        {type === 'text_embedding' && <>
                                            <Form.Item label={t('projectModelEmbeddingSize')} required name='embedding_size' rules={[
                                                {
                                                    required: true,
                                                    message: `${t('projectModelEmbeddingSizeRequired')}`,
                                                },
                                            ]}>
                                                <div className={styles['description']}>{t('projectModelEmbeddingSizeDesc')}</div>
                                                <Form.Item required name='embedding_size' rules={[
                                                    {
                                                        required: true,
                                                        message: `${t('projectModelEmbeddingSizeRequired')}`,
                                                    },
                                                ]}>
                                                    <InputNumber style={{ width: '100%' }} parser={(value: any) => (isNaN(value) ? '' : parseInt(value, 10))} placeholder={t('projectModelEmbeddingSizePlaceholder')} />
                                                </Form.Item>
                                            </Form.Item>
                                            <Form.Item label={t('projectModelInputMaxTokens')} name='input_token_limit'>
                                                <div className={styles['description']}>{t('projectModelInputMaxTokensDesc')}</div>

                                                <Form.Item name='input_token_limit'>
                                                    <InputNumber parser={(value: any) => (isNaN(value) ? '' : parseInt(value, 10))} style={{ width: '100%' }} placeholder={t('projectModelInputMaxTokensPlaceholder')} />
                                                </Form.Item>
                                            </Form.Item>
                                            <Form.Item label={'Max batch size'} name='max_batch_size'>
                                                <div className={styles['description']}>The maximum number of text chunks that a provider's API can process in one call. Default value is 512.</div>

                                                <Form.Item name='max_batch_size'>
                                                    <InputNumber parser={(value: any) => (isNaN(value) ? '' : parseInt(value, 10))} style={{ width: '100%' }} placeholder={'Enter batch size'} />
                                                </Form.Item>
                                            </Form.Item>
                                        </>}
                                        {type === 'chat_completion' && <>
                                            <Form.Item label="Function call" required name='function_call' valuePropName="checked">
                                                <div className={styles['description']}>{t('projectModelPropertiesDesc')}</div>
                                                <ConfigProvider theme={{
                                                    components: {
                                                        Switch: {
                                                            colorPrimary: '#087443',
                                                            colorPrimaryHover: '#087443',
                                                        }
                                                    }
                                                }}>
                                                    <Form.Item name='function_call' className={styles['switch']}>
                                                        <Switch value={functionCall} />
                                                    </Form.Item>
                                                </ConfigProvider>
                                            </Form.Item>
                                            <Form.Item label="Streaming" required name='streaming' valuePropName="checked">
                                                <div className={styles['description']}>{t('projectModelStreamingDesc')}</div>
                                                <ConfigProvider theme={{
                                                    components: {
                                                        Switch: {
                                                            colorPrimary: '#087443',
                                                            colorPrimaryHover: '#087443',
                                                        }
                                                    }
                                                }}>
                                                    <Form.Item name='streaming' className={styles['switch']}>
                                                        <Switch value={streaming} />
                                                    </Form.Item>
                                                </ConfigProvider>
                                            </Form.Item>
                                            <Form.Item label={t('projectModelInputMaxTokens')} name='input_token_limit'>
                                                <div className={styles['description']}>{t('projectModelInputMaxTokensDesc')}</div>
                                                <Form.Item name='input_token_limit'>
                                                    <InputNumber parser={(value: any) => (isNaN(value) ? '' : parseInt(value, 10))} style={{ width: '100%' }} placeholder={t('projectModelInputMaxTokensPlaceholder')} />
                                                </Form.Item>
                                            </Form.Item>
                                            <Form.Item label="Output max tokens" name='output_token_limit'>
                                                <div className={styles['description']}>{t('projectModelOutputMaxTokensDesc')}</div>
                                                <Form.Item name='output_token_limit'>
                                                    <InputNumber style={{ width: '100%' }} parser={(value: any) => (isNaN(value) ? '' : parseInt(value, 10))} placeholder={t('projectModelOutputMaxTokensPlaceholder')} />
                                                </Form.Item>
                                            </Form.Item>
                                        </>}
                                    </Form>
                                </ConfigProvider>
                            </>
                        }
                        {
                            !properties && <>
                                {modelType !== 'wildcard' && <>
                                    <div className={styles['hr']}></div>
                                    <div className='credentials'>{t('projectModelColumnProperties')}</div>
                                </>}

                                {modelType === 'chat_completion' && <Form layout="vertical" className='second-form' form={propertyForm}>
                                    <Form.Item label="Function call" required name='function_call' valuePropName="checked">
                                        <div className={styles['description']}>{t('projectModelPropertiesDesc')}</div>
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
                                        <div className={styles['description']}>{t('projectModelStreamingDesc')}</div>
                                        <ConfigProvider theme={{
                                            components: {
                                                Switch: {
                                                    colorPrimary: '#087443',
                                                    colorPrimaryHover: '#087443',
                                                }
                                            }
                                        }}>
                                            <Form.Item name='streaming' className={styles['switch']}>
                                                <Switch />
                                            </Form.Item>
                                        </ConfigProvider>
                                    </Form.Item>
                                    <Form.Item label={t('projectModelInputMaxTokens')} name='input_token_limit'>
                                        <div className={styles['description']}>{t('projectModelInputMaxTokensDesc')}</div>

                                        <Form.Item name='input_token_limit'>
                                            <InputNumber parser={(value: any) => (isNaN(value) ? '' : parseInt(value, 10))} style={{ width: '100%' }} placeholder={t('projectModelInputMaxTokensPlaceholder')} />
                                        </Form.Item>
                                    </Form.Item>
                                    <Form.Item label="Output max tokens" name='output_token_limit'>
                                        <div className={styles['description']}>{t('projectModelOutputMaxTokensDesc')}</div>
                                        <Form.Item name='output_token_limit'>
                                            <InputNumber parser={(value: any) => (isNaN(value) ? '' : parseInt(value, 10))} placeholder={t('projectModelOutputMaxTokensPlaceholder')} />
                                        </Form.Item>
                                    </Form.Item>
                                </Form>}
                                {
                                    modelType === 'text_embedding' && <Form layout="vertical" className={styles['second-form']} form={propertyForm} autoComplete='off'>
                                        <Form.Item label={t('projectModelEmbeddingSize')} required name='embedding_size' rules={[
                                            {
                                                required: true,
                                                message: `${t('projectModelEmbeddingSizeRequired')}`,
                                            },
                                        ]}>
                                            <div className={styles['description']}>{t('projectModelEmbeddingSizeDesc')}</div>

                                            <Form.Item required name='embedding_size'>
                                                <InputNumber style={{ width: '100%' }} parser={(value: any) => (isNaN(value) ? '' : parseInt(value, 10))} placeholder={t('projectModelEmbeddingSizePlaceholder')} />
                                            </Form.Item>
                                        </Form.Item>
                                    </Form>
                                }
                            </>
                        }
                        <div className={styles['hr']}></div>

                        <div className={styles['credentials']} style={{ marginBottom: '8px' }}>{t('projectModelCredentials')}</div>
                        <div className={styles['label-desc']} >
                            {t('projectModelCredentialsDesc')} {t('referTo')} <a className='href' href='https://docs.tasking.ai/docs/guide/model/overview#required-credentials-for-model-access' target='_blank' rel='noopener noreferrer'>{t('projectModelCredentialsLink')}</a> {t('projectModelCredentialsDescEnd')}
                        </div>
                        {resetButtonShow && <div className={styles['formbuttoncancel']} onClick={handleResetCredentials}>
                            <div className={styles['text1']}>{t('projectModelResetCredentials')}</div>
                        </div>}
                        <Form
                            layout="vertical"
                            autoComplete="off"
                            form={form}
                            disabled={formShow}
                            onValuesChange={handleValuesChange}
                            className={styles['second-form']}
                        >
                            {formData && formData.properties && Object.entries(formData.properties).map(([key, property]) => (
                                <Form.Item label={key} key={key} name={key} rules={[
                                    {
                                        required: formData.required.includes(key) ? true : false,
                                        message: `Please input ${key}.`,
                                    },
                                ]}>
                                    <div className={styles['description']}>{(property as { description: string }).description}</div>
                                    <Form.Item
                                        name={key}
                                        key={key}
                                        className={styles['form-item']}
                                    >
                                        <Input placeholder={`Enter ${key}`} className={styles['input']} />
                                    </Form.Item>
                                </Form.Item>
                            ))}
                        </Form>

                    </div>
                </Spin>

            </Drawer>
            <ViewCode open={viewCodeOpen} data={viewCodeData} handleClose={handleCloseViewCode}/>
            <Modal title={t('projectDeleteModelTitle')}
                onCancel={handleDeleteCancel}
                open={openDeleteModal}
                centered
                className={styles['delete-model-modal']}
                closeIcon={<img src={closeIcon} alt="closeIcon" />}
                footer={[
                    <Button key="cancel" onClick={handleDeleteCancel} className='cancel-button'>
                        {t('cancel')}
                    </Button>,
                    <Button key="delete" onClick={handleDeleteConfirm} className={disabled ? 'disabled-button' : 'delete-button'} disabled={disabled} loading={deleteLoading}>
                        {t('delete')}
                    </Button>
                ]}
            >
                <p className={styles.desc}>{t('deleteItem')}<span className={styles.span}> {record.name}</span>? {t('projectDeleteModelDesc')} </p>
                <Input value={deleteValue} onChange={handleDeleteValue} placeholder={t('projectDeleteModelPlaceholder')}></Input>
            </Modal>
        </div>

    )
}
export default ModelsPage