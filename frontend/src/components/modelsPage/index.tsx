import { useEffect, useState, useRef, ChangeEvent } from 'react'
import { Modal, Button, Spin, Space, Input, Form, Drawer, Tooltip } from 'antd'
import styles from './modelsPage.module.scss'
import { getModelsList, updateModels, deleteModels, getModelsForm, getAiModelsForm } from '@/axios/models'
import tooltipTitle from '../../contents/tooltipTitle.tsx'
import { useSelector, useDispatch } from 'react-redux';
import { fetchModelsData } from '../../Redux/actions';
import EditIcon from '../../assets/img/editIcon.svg?react'
import DeleteIcon from '../../assets/img/deleteIcon.svg?react'
import CommonComponents from '../../contents/index.tsx'
import ModalTable from '@/components/modalTable';
import ModelModal from '@/components/modelModal';
import closeIcon from '../../assets/img/x-close.svg'
import { toast } from 'react-toastify';
import { useTranslation } from "react-i18next";
import IconComponent from '@/components/iconComponent';
import { setLoading } from '../../Redux/actions.ts'
import ApiErrorResponse, { RecordType, ChildRefType, formDataType } from '../../constant/index.ts'
function ModelsPage() {
    const { modelLists, loading } = useSelector((state: any) => state.model);
    const dispatch = useDispatch()
    const { tooltipEditTitle, tooltipDeleteTitle } = tooltipTitle();
    const { modelsTableColumn, typeReverse } = CommonComponents();
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
        properties: {}
    });
    const [limit, setLimit] = useState(20)
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
            width: 118,
            fixed: 'right',
            render: (_: string, record: object) => (
                <Space size="middle">
                    <div onClick={() => handleEdit(record as RecordType)} className='table-edit-icon' >
                        <Tooltip placement='bottom' title={tooltipEditTitle} color='#fff' arrow={false} overlayClassName='table-tooltip'>
                            <EditIcon />
                        </Tooltip>

                    </div>
                    <div onClick={() => handleDelete(record as RecordType)} className='table-edit-icon'>
                        <Tooltip placement='bottom' title={tooltipDeleteTitle} color='#fff' arrow={false} overlayClassName='table-tooltip'>
                            <DeleteIcon />
                        </Tooltip>
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
        setOpenDeleteModal(true)
        setDeleteValue('')
        setDisabled(true)
        setRecord(record)

    }
    const handleDeleteValue = (e: ChangeEvent<HTMLInputElement>) => {
        setDeleteValue(e.target.value)
        if (e.target.value === record.name) {
            setDisabled(false)
        } else {
            setDisabled(true)
        }
    }
    const handleDeleteConfrim = async () => {
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
    }
    const handleCreateModel = async () => {
        setModelOne(true)
        childRef.current?.fetchAiModelsList()
    }
    const onClose = () => {
        setDrawerEditOpen(false);
    };
    const handleEdit = async (record: RecordType) => {
        setFormShow(true)
        setResetButtonShow(true)
        form1.setFieldsValue({
            name: record.name
        })
        setSelectedSecondId(record.model_schema_id)
        setSecondModalNameValue(record.name)
        setModelId(record.model_id)
        setType(record.type)
        setProperties(record.properties)
        setProviderId(record.provider_id)
        await fetchEditFormData(record.model_id, record.provider_id)
        setDrawerEditOpen(true)
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
        await form1.validateFields().then(async () => {

            await form.validateFields().then(async () => {
                const params = {
                    name: form1.getFieldValue('name'),
                    credentials: resetButtonShow ? undefined : form.getFieldsValue()
                }
                try {
                    setConfirmLoading(true)
                    await updateModels(modelId, params)
                    toast.success(`${t('updateSuccessful')}`)
                    setDrawerEditOpen(false)
             
                    const limit1 = limit || 20
                    dispatch(fetchModelsData(limit1) as any);
                } catch (error) {
                    const errorType = error as ApiErrorResponse;
                    const errorMessage: string = errorType.response.data.error.message;
                    toast.error(errorMessage)
                }
                setUpdatePrevButton(true)
                setConfirmLoading(false)
            })
        })
    }
    const handleDeleteCancel = () => {
        setDeleteValue('')
        setOpenDeleteModal(false)
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
    return (
        <div className={styles["models-page"]}>
            <Spin spinning={loading} wrapperClassName={styles.spinloading}>
                <ModalTable updatePrevButton={updatePrevButton} onChildEvent={handleChildEvent} name="model" hasMore={hasMore} id='model_id' columns={columns} ifSelect={false} onOpenDrawer={handleCreateModel} dataSource={modelList} />
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
                <div className={styles['second-modal']}>
                    <div className={styles['label']}>{t('projectModelColumnBaseModel')}</div>
                    <div className={styles['frameParent']}>
                        <div className={styles['modelproviderParent']}>
                            <IconComponent providerId={providerId} />
                            <div className={styles['openai']}>{selectedSecondId}</div>
                        </div>
                    </div>
                    <div className={styles['label']} style={{ marginTop: '24px' }}>{t('Type')}</div>
                    <div className={styles.modeltypetag}>
                        <div className={styles.chatCompletion}>{typeReverse[type as keyof typeof typeReverse]}</div>
                    </div>
                    <div className={styles['label']} style={{ marginTop: '24px' }}>{t('projectModelColumnProperties')}</div>
                    <div className={styles.feature}>
                        {Object.entries(properties).map(([key, property]) => (
                            <div className={styles['streamParent']} key={key} style={{ display: 'flex', border: '1px solid #e4e4e4', borderRadius: '8px', padding: '0 4px', marginRight: '12px' }}>
                                <span className={styles['stream']} style={{ borderRight: '1px solid #e4e4e4', paddingRight: '2px' }}>{key}</span>
                                <span className={styles['on']} style={{ paddingLeft: '2px' }}>{String(property)}</span>
                            </div>
                        ))}
                    </div>

                    <div className={styles['hr']}></div>
                    <Form layout="vertical" form={form1} autoComplete="off" className={styles['input-form']} >
                        <Form.Item rules={[
                            {
                                required: true,
                                message: `${t('projectInputName')}`,
                            },
                        ]} label={t('projectModelCreateModelName')} name="name">
                            <Input className={styles['input-name']} placeholder={t('projectModelCreatePlaceholder')} key={secondModalNameValue} />
                        </Form.Item>
                    </Form>
                    <div className={styles['hr']}></div>
                    <div className={styles['credentials']}>{t('projectModelCredentials')}</div>
                    <div className={styles['label-desc']} style={{ marginBottom: '24px' }}>
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
            </Drawer>
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
                    <Button key="delete" onClick={handleDeleteConfrim} className={disabled ? 'disabled-button' : 'delete-button'} disabled={disabled} loading={deleteLoading}>
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