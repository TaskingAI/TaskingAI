import { useEffect, useState, useRef, ChangeEvent } from 'react'
import { Modal, Button, Spin, Space, Input, Form, Drawer, Tooltip } from 'antd'
import styles from './modelsPage.module.scss'
import IconComponent from '@/components/iconComponent';
// import { TKButton } from '@taskingai/taskingai-ui'
import { getModelsList, updateModels, deleteModels, getModelsForm, getAiModelsForm } from '@/axios/models'
import { tooltipEditTitle, tooltipDeleteTitle } from '../../contents/index.tsx'
import EditIcon from '../../assets/img/editIcon.svg?react'
import DeleteIcon from '../../assets/img/deleteIcon.svg?react'
import { modelsTableColumn } from '../../contents/index.tsx'
import ModalTable from '@/components/modalTable';
import ModelModal from '@/components/modelModal';
import closeIcon from '../../assets/img/x-close.svg'
import { toast } from 'react-toastify';
import { RecordType, ChildRefType, formDataType } from '../../contant/index.ts'
const typeReverse = {
    instruct_completion: 'Instruct Completion',
    chat_completion: 'Chat Completion',
    text_embedding: 'Text Embedding'
}
function ModelsPage() {
    const [form] = Form.useForm()
    const [form1] = Form.useForm()
    const [type, setType] = useState('')
    const [proerties, setProerties] = useState('')
    const [loading, setLoading] = useState(false);
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
    const [deleteLoading, setDeleteLoading] = useState(false)
    const fetchData = async (params: Record<string, any>) => {
        try {
            setLoading(true)
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
        } finally {
            setLoading(false)
        }
    }
    useEffect(() => {
        const params = {
            limit: 20
        }
        fetchData(params);
    }, [])

    const columns = [...modelsTableColumn]
    columns.push(
        {
            title: 'Actions',
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
        const params1 = {
            limit: limit || 20
        }
        await deleteModels(params.model_id as string)
        await fetchData(params1)
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
        setLoading(true)
        setFormShow(true)
        setResetButtonShow(true)
        form1.setFieldsValue({
            name: record.name
        })
        setSelectedSecondId(record.model_schema_id)
        setSecondModalNameValue(record.name)
        setModelId(record.model_id)
        setProviderId(record.provider_id)
        await fetchEditFormData(record.model_id, record.provider_id)
        setDrawerEditOpen(true)
        setLoading(false)
    }
    const fetchEditFormData = async (model_id: string, provider_id: string) => {
        const res = await getModelsForm(model_id)
        setType(res.data.type)
        setProerties(res.data.properties)
        const res1 = await getAiModelsForm(provider_id)
        setFormData(res1.data[0].credentials_schema)
        form.setFieldsValue(res.data.display_credentials)
    }

    const handleConfirm = async () => {
        await form1.validateFields().then(async () => {

            await form.validateFields().then(async () => {
                const params = {
                    name: form1.getFieldValue('name'),
                    credentials: resetButtonShow ? undefined : form.getFieldsValue()
                }
                try {
                    await updateModels(modelId, params)
                    // setConfirmLoading(false)
                    toast.success('Update successfully')
                    setDrawerEditOpen(false)
                    const params1 = {
                        limit: limit || 20
                    }
                    await fetchData(params1)
                } catch (error) {
                    toast.error(error.response.data.error.message)
                }


                setUpdatePrevButton(true)
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

    return (
        <div className={styles["models-page"]}>
            <Spin spinning={loading} wrapperClassName={styles.spinloading}>
                <ModalTable updatePrevButton={updatePrevButton} onChildEvent={handleChildEvent} name="model" hasMore={hasMore} id='model_id' columns={columns} ifSelect={false} onOpenDrawer={handleCreateModel} dataSource={modelList} />
            </Spin>
            <ModelModal getOptionsList={fetchData} ref={childRef} open={modelOne} handleSetModelOne={handleModalCancel} handleSetModelConfirmOne={handleSetModelConfirmOne}></ModelModal>

            <Drawer title="Edit Model" width={700} closeIcon={<img src={closeIcon} alt="closeIcon" />} footer={[
                <Button key="cancel" onClick={onClose} className='cancel-button'>
                    Cancel
                </Button>,
                <Button key="submit" loading={loading} onClick={handleConfirm} className={`next-button ${styles.button}`}>
                    Confirm
                </Button>
            ]} placement="right" onClose={onClose} open={drawerEditOpen} className={styles['edit-modal-header']}>
                <div className={styles['second-modal']}>
                    <div className={styles['label']}>Base model</div>
                    <div className={styles['frameParent']}>
                        <div className={styles['modelproviderParent']}>
                            <IconComponent providerId={providerId} />
                            <div className={styles['openai']}>{selectedSecondId}</div>
                        </div>
                    </div>
                    <div className={styles['label3']} style={{ marginTop: '24px' }}>Type</div>
                    <span className={styles['modeltypetag']}>
                        {typeReverse[type as keyof typeof typeReverse]}
                    </span>
                    <div className={styles['label3']} style={{ marginTop: '24px' }}>Properties</div>
                    <div className={styles['instanceParent']}>
                        {proerties && Object.entries(proerties).map(([key, property]) => (
                            property !== null ? (
                                <div className={styles['streamParent']} key={key}>
                                    <div className={styles['stream']}>{key}</div>
                                    <div className={styles['instanceChild']} />
                                    <div className={styles['on']}>{String(property)}</div>
                                </div>
                            ) : null
                        ))}
                    </div>

                    <Form layout="vertical" form={form1} autoComplete="off" className={styles['input-form']} >
                        <Form.Item rules={[
                            {
                                required: true,
                                message: 'Please input name.',
                            },
                        ]} label="Model name" name="name">
                            <Input className={styles['input-name']} placeholder='Enter model name' key={secondModalNameValue} />
                        </Form.Item>
                    </Form>
                    <div className={styles['hr']}></div>
                    <div className={styles['credentials']}>Credentials</div>
                    <div className={styles['label-desc']} style={{ marginBottom: '24px' }}>
                        Please enter your model credentials, and we will send one token to the model provider to verify the validity of your credentials. All credentials are encrypted at rest with AES-256 and in transit with TLS 1.2. Refer to <a className='href' href='https://docs.tasking.ai/docs/guide/model/overview#required-credentials-for-model-access' target='_blank' rel='noopener noreferrer'>documentation</a> for more information.
                    </div>
                    {resetButtonShow && <div className={styles['formbuttoncancel']} onClick={handleResetCredentials}>
                        <div className={styles['text1']}>Reset credentials</div>
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
            <Modal title='Delete Model'
                onCancel={handleDeleteCancel}
                open={openDeleteModal}
                centered
                className={styles['delete-model-modal']}
                closeIcon={<img src={closeIcon} alt="closeIcon" />}
                footer={[
                    <Button key="cancel" onClick={handleDeleteCancel} className='cancel-button'>
                        Cancel
                    </Button>,
                    <Button key="delete" onClick={handleDeleteConfrim} className={disabled ? 'disabled-button' : 'delete-button'} disabled={disabled} loading={deleteLoading}>
                        Delete
                    </Button>
                ]}
            >
                <p className={styles.desc}>Are you sure you want to delete<span className={styles.span}> {record.name}</span>? This action cannot be undone and all configurations associated with the model will be affected. </p>
                <Input value={deleteValue} onChange={handleDeleteValue} placeholder='Enter model name to confirm'></Input>
            </Modal>
        </div>

    )
}
export default ModelsPage