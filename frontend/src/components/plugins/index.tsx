import {
    Space, Spin, Tooltip,  Button, Form, Input, Drawer
} from 'antd';
import { useSelector, useDispatch } from 'react-redux';
import { fetchPluginData } from '../../Redux/actions';
import CreatePlugin from '../createPlugin/index.tsx';
import styles from './plugins.module.scss'
import { useState, useEffect,useRef } from 'react';
import ClipboardJS from 'clipboard';
import { toast } from 'react-toastify';
import { deletePlugin, bundleList, getPluginList, editPlugin } from '@/axios/plugin.ts'
import closeIcon from '../../assets/img/x-close.svg'
import DeleteModal from '../deleteModal/index.tsx'
import ModalTable from '../modalTable/index'
import CopyOutlined from '@/assets/img/copyIcon.svg?react';
import ParameterTable from '../parameterTable/index.tsx'
import EditIcon from '../../assets/img/editIcon.svg?react'
import DeleteIcon from '../../assets/img/deleteIcon.svg?react'
import ToolsNew from '../../assets/img/tools.svg?react'
import tooltipTitle from '../../contents/tooltipTitle.tsx'
import CommonComponents from '../../contents/index.tsx'
import ApiErrorResponse from '@/constant/index'
import { useTranslation } from "react-i18next";

function Plugins() {
    const { t } = useTranslation();
    const createPluginRef = useRef<any>()
    const dispatch = useDispatch()
    const { pluginLists } = useSelector((state: any) => state.plugin);
    const { bundleTableColumn } = CommonComponents()
    const { tooltipEditTitle, tooltipDeleteTitle,tooltipPluginTitle } = tooltipTitle();
    const [loading, setLoading] = useState(false);
    const [form] = Form.useForm()
    const [pluginFunList, setPluginFunList] = useState([])
    const [deleteValue, setDeleteValue] = useState('')
    const [updatePrevButton, setUpdatePrevButton] = useState(false)
    const [OpenDeleteModal, setOpenDeleteModal] = useState(false)
    const [limit, setLimit] = useState(20)
    const [hasMore, setHasMore] = useState(false)
    const [formDisabled, setFormDisabled] = useState(false)
    const [openCreateModal1, setOpenDrawer] = useState(false)
    const [bundleId, setBundleId] = useState('')
    const [bundleName, setBundleName] = useState('')
    const [bundilesList, setBundlesList] = useState([])
    const [credentialsSchema, setCredentialsSchema] = useState({})
    const [inputSchema, setInputSchema] = useState({})
    const [resetButtonShow, setResetButtonShow] = useState(true)
    const [pluginListData, setPluginListData] = useState([])
    const [pluginId, setPluginId] = useState('')
    const [pluginName, setPluginName] = useState('')
    const [pluginDesc, setPluginDesc] = useState('')
    const [bundleDesc, setBundleDesc] = useState('')
    const [confirmLoading, setConfirmLoading] = useState(false)
    const [openEditDrawer, setOpenEditDrawer] = useState(false)
    const [openEditFormDrawer, setOpenEditFormDrawer] = useState(false)
    const [isShowBundle, setIsShowBundle] = useState(true)
    const [cachedImages, setCachedImages] = useState({});
    useEffect(() => {
        const params1 = {
            limit: 100,
            offset: 0,
            lang: 'en'
        }
        getBundleList(params1)
    }, [])
    useEffect(() => {
        if (pluginLists.data.length > 0) {
            const data = pluginLists.data.map((item: any) => {
                return {
                    ...item,
                }
            })
            setPluginFunList(data)
            setHasMore(pluginLists.has_more)
        } else {
            setPluginFunList([])
        }
    }, [pluginLists])
    const fetchData = async (params: any) => {
        setLoading(true);
        try {
            const res: any = await getPluginList(params)
            const data = res.data.map((item: any) => {
                return {
                    ...item,
                }
            })

            setPluginFunList(data)
            setHasMore(res.has_more)
        } catch (error) {
            console.log(error)
        }
        setLoading(false);
    };
    const handleCreatePrompt = async () => {
        setOpenDrawer(true)
    }
    const getBundleList = async (params: object) => {
        const res: any = await bundleList(params)
        const imagesData: any = {};
        res.data.forEach((image: any) => {
            fetch(image.icon_url)
                .then(response => response.blob())
                .then(blob => {
                    const reader = new FileReader();
                    reader.onload = function () {
                        imagesData[image.bundle_id] = reader.result;
                        setCachedImages(imagesData);
                    };
                    reader.readAsDataURL(blob);
                });
        });
        setBundlesList(res.data)
    }
    const columns = [...bundleTableColumn]
    columns.push({
        title: `${t('projectColumnActions')}`,
        key: 'action',
        fixed: 'right',
        width: 156,
        render: (_: any, record: any) => (
            <Space size="middle">
                <div onClick={() => handleTools(record)} className='table-edit-icon'>
                    <Tooltip placement='bottom' color='#fff' arrow={false} title={tooltipPluginTitle} overlayClassName='table-tooltip'>
                        <ToolsNew />
                    </Tooltip>
                </div>
                <div onClick={JSON.stringify(record.display_credentials) !== '{}' ? () => handleEdit(record) : undefined} className={`table-edit-icon ${JSON.stringify(record.display_credentials) === '{}' && styles.disabledButton}`}>
                    {JSON.stringify(record.display_credentials) !== '{}' ? <Tooltip placement='bottom' title={tooltipEditTitle} color='#fff' arrow={false} overlayClassName='table-tooltip'>
                        <EditIcon />
                    </Tooltip> : <EditIcon />}
                </div>
                <div onClick={() => handleDelete(record)} className='table-edit-icon'>
                    <Tooltip placement='bottom' title={tooltipDeleteTitle} color='#fff' arrow={false} overlayClassName='table-tooltip'>
                        <DeleteIcon />
                    </Tooltip>
                </div>
            </Space>
        ),
    },)
    const handleEdit = async (record: any) => {
        setFormDisabled(true)
        setBundleId(record.bundle_id)
        const data: any = (bundilesList.find((item: any) => item.bundle_id === record.bundle_id) as any)
        setBundleName(data.name)
        setBundleDesc(record.description)
        setCredentialsSchema(data.credentials_schema)
        form.setFieldsValue(record.display_credentials)
        setResetButtonShow(true)
        setOpenEditFormDrawer(true)

    }
    const handleTools = async (record: any) => {
        setLoading(true)
        try {
            setPluginListData(record.plugins)
            setPluginName(record.plugins[0].name)
            setPluginDesc(record.plugins[0].description)
            setBundleName(record.name)
            setPluginId(record.plugins[0].plugin_id)
            const inputSchematemp = record.plugins[0].input_schema
            const arr: any[] = []
            Object.values(inputSchematemp).forEach((item: any) => {
                arr.push(item)
            })
            setInputSchema(arr)
            setOpenEditDrawer(true)
            setBundleId(record.bundle_id)
            setIsShowBundle(false)
        } catch (e) {
            const error = e as ApiErrorResponse
            toast.error(error.response.data.error.message)
        } finally {
            setLoading(false)
        }

    }
    const handleCopy = (text: string) => {
        const clipboard = new ClipboardJS('.icon-copy', {
            text: () => text
        });
        clipboard.on('success', function () {
            toast.success(t('CopiedToClipboard'))
            clipboard.destroy()
        });
        clipboard.on('error', function (e) {
            console.log(e);
        });
    }
    const onDeleteCancel = () => {
        setOpenDeleteModal(false)
    }
    const handleDelete = (val: any) => {
        setOpenDeleteModal(true)
        setDeleteValue(val.name)
        setBundleId(val.bundle_id)
    }

    const handleChildEvent = async (value: Record<string, any>) => {
        setUpdatePrevButton(false)
        setLimit(value.limit)
        await fetchData(value);
    }
    const onDeleteConfirm = async () => {
        try {
            await deletePlugin(bundleId)
            const limit1: number = limit || 20
            dispatch(fetchPluginData(limit1) as any);
            if(createPluginRef.current) {
                createPluginRef.current.getBundleList({
                    limit: 100,
                    offset: 0,
                    lang: 'en'
                })
            }
            setUpdatePrevButton(true)
        } catch (error) {
            console.log(error)
        }
        setOpenDeleteModal(false)
    }
   
  
    const handleClickPlugin = (pluginId: string, pluginName: string) => {
        setPluginId(pluginId)
        setPluginName(pluginName)
        setPluginDesc((pluginListData as any[]).find((item: any) => item.plugin_id === pluginId).description)
        const inputSchematemp = (pluginListData as any[]).find(item => item.plugin_id === pluginId).input_schema
        const arr: any[] = []
        Object.values(inputSchematemp).forEach((item: any) => {
            arr.push(item)
        })
        setInputSchema(arr)
    }
    const handleValuesChange = (changedValues: object) => {
        form.validateFields(Object.keys(changedValues));
    };
 
    const handleConfirmRequest = async () => {
        dispatch(fetchPluginData(20) as any);
    }
    const handleClosePluginModal = () => {
        setOpenDrawer(false)
    }
 
    const handleResetCredentials = async () => {
        form.resetFields();
        setResetButtonShow(false)
        setFormDisabled(false)
    }
    const ComponentsData = () => {
        return (
            (
                <div className={styles.componentsData}>
                    {isShowBundle && <div className={styles.inputWithLabelParent}>
                        <div className={styles.inputWithLabel}>
                            <div className={styles.label}>{t('projectBundleTitle')}</div>
                            <div className={styles.inputWithLabelInner}>
                                <div className={styles.frameWrapper}>
                                    <div className={styles.frameContainer}>
                                        <div className={styles.logoParent}>
                                            <img loading="lazy" src={(cachedImages as any)[bundleId]} alt="" style={{ width: '24px', height: '24px' }} />
                                            <div className={styles.label}>{bundleName}</div>
                                        </div>
                                    </div>

                                </div>
                                <div className={styles.desc}>
                                    {bundleDesc}
                                </div>
                            </div>
                        </div>
                    </div>}

                    <div className={styles.content1}>
                        <div className={styles.left}>
                            {pluginListData.map((item: any, index) => (
                                <div key={index} onClick={() => { handleClickPlugin(item.plugin_id, item.name) }} className={`${styles.pluginName} ${pluginId === item.plugin_id && styles.pluginId}`}>
                                    {item.name}
                                </div>
                            ))}
                        </div>
                        <div className={styles.right}>
                            <div className={styles.topContent}>
                                <div className={styles.pluginTitle}>{pluginName}</div>
                                {!isShowBundle && <div className={styles.pluginId}>
                                    {bundleId}/{pluginId} <CopyOutlined className='icon-copy' onClick={() => handleCopy(`${bundleId}/${pluginId}`)} />
                                </div>}

                            </div>
                            <div className={styles.pluginDesc}>{pluginDesc}</div>
                            <div style={{ marginLeft: '24px' }}>
                                <ParameterTable parameters={inputSchema} />
                            </div>
                        </div>
                    </div></div>
            )
        )
    }
    const EditForm = () => {
        return (
            <div className={styles.editForm}>
                <div className={styles.bundleTitle}>
                    <div className={styles.label}>{t('projectBundleTitle')}</div>
                    <div className={styles.googleWeb}>
                        <img loading="lazy" src={(cachedImages as any)[bundleId]} alt="" style={{ width: '24px', height: '24px' }} />
                        <div className={styles.googleWebSearch}>{bundleName}</div>
                    </div>
                </div>
                {JSON.stringify(credentialsSchema) !== '{}' && <div>
                    <div className={styles['credentials']}>{t('projectModelCredentials')}</div>
                    <div className={styles['label-desc']} style={{ marginBottom: '24px' }}>
                        All plugin credentials are encrypted at rest with AES-256 and in transit with TLS 1.2.
                    </div>
                    {resetButtonShow && <div className={styles['formbuttoncancel']} onClick={handleResetCredentials}>
                        <div className={styles['text1']}>{t('projectModelResetCredentials')}</div>
                    </div>}
                    <Form
                        layout="vertical"
                        autoComplete="off"
                        form={form}
                        disabled={formDisabled}
                        onValuesChange={handleValuesChange}
                        className={styles['second-form']}
                    >
                        {credentialsSchema && Object.entries(credentialsSchema).map(([key, property]: [any, any]) => (
                            <Form.Item label={key} key={key} name={key} rules={[
                                {
                                    required: property.required,
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
                </div>}

            </div>
        )
    }
    const handleEditCancel = () => {
        setOpenEditDrawer(false)
    }
    const handleEditFormCancel = () => {
        setOpenEditFormDrawer(false)
    }
    const handleEditFormConfirm = async () => {

        form.validateFields().then(async () => {
            try {
                const credentials = form.getFieldsValue()
                const params = {
                    name: bundleName,
                    credentials,
                }
                setConfirmLoading(true)
                await editPlugin(bundleId, params)
                const limit1: number = limit || 20
                dispatch(fetchPluginData(limit1) as any);
                setUpdatePrevButton(true)
                setOpenEditFormDrawer(false)
                setOpenEditDrawer(false)
                toast.success(t('updateSuccessful'))
            } catch (error) {
                const apiError = error as ApiErrorResponse;
                const errorMessage: string = apiError.response.data.error.message;
                toast.error(errorMessage)
            } finally {
                setConfirmLoading(false)

            }

        })
    }
    return (
        <div className={styles["actions"]}>
            <Spin spinning={loading} wrapperClassName={styles.spinloading}>
                <ModalTable loading={loading} title='New plugin' updatePrevButton={updatePrevButton} name='plugin' id='bundle_id' hasMore={hasMore} ifSelect={false} columns={columns} dataSource={pluginFunList} onChildEvent={handleChildEvent} onOpenDrawer={handleCreatePrompt} />
            </Spin>
            <CreatePlugin ref={createPluginRef} handleConfirmRequest={handleConfirmRequest} open={openCreateModal1} handleCloseModal={handleClosePluginModal}></CreatePlugin>
   
            <Drawer footer={null} width={1280} closeIcon={<img src={closeIcon} alt="closeIcon" className={styles['img-icon-close']} />} onClose={handleEditCancel} open={openEditDrawer} title={bundleName + ' / ' + t('projectPluginsTitle')} className={styles.openLookDrawer}>
                <ComponentsData />
            </Drawer>
            <Drawer title={t('projectPluginEditPlugin')} footer={[
                <Button key="cancel" onClick={handleEditFormCancel} className='cancel-button'>
                    {t('cancel')}
                </Button>,
                <Button key="submit" loading={confirmLoading} onClick={handleEditFormConfirm} className={`next-button ${styles.button}`}>
                    {t('confirm')}
                </Button>
            ]} open={openEditFormDrawer} closeIcon={<img src={closeIcon} alt="closeIcon" className={styles['img-icon-close']} />} width={720} onClose={handleEditFormCancel} className={styles.openEditDrawer}>
                <EditForm />
            </Drawer>
            <DeleteModal open={OpenDeleteModal} describe={`${t('projectPluginDeleteDesc')} ${deleteValue}? ${t('projectDeleteProjectDesc')}`} title={t('projectPluginDeleteTitle')} projectName={deleteValue} onDeleteCancel={onDeleteCancel} onDeleteConfirm={onDeleteConfirm} />
        </div>

    )
}
export default Plugins