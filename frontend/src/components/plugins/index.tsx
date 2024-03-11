import {
    Space, Spin, Tooltip, Modal, Button, Form, Input, Drawer
} from 'antd';
import { RightOutlined } from '@ant-design/icons'
import { useSelector, useDispatch } from 'react-redux';
import { fetchPluginData } from '../../Redux/actions';

import styles from './plugins.module.scss'
import { useState, useEffect } from 'react';
import { LeftOutlined } from '@ant-design/icons';
import ClipboardJS from 'clipboard';
import { toast } from 'react-toastify';
import { deletePlugin, bundleList, getPluginDetail, createPlugin, getPluginList, editPlugin } from '@/axios/plugin.ts'
import closeIcon from '../../assets/img/x-close.svg'
import DeleteModal from '../deleteModal/index.tsx'
import ModalTable from '../modalTable/index'
import CopyOutlined from '@/assets/img/copyIcon.svg?react';
import ParameterTable from '../parameterTable/index.tsx'
import RightArrow from '../../assets/img/rightarrow.svg?react'
import EditIcon from '../../assets/img/editIcon.svg?react'
import DeleteIcon from '../../assets/img/deleteIcon.svg?react'
import ToolsNew from '../../assets/img/tools.svg?react'
import tooltipTitle from '../../contents/tooltipTitle.tsx'
import CommonComponents from '../../contents/index.tsx'
import ApiErrorResponse from '@/constant/index'
import { useTranslation } from "react-i18next";

function Plugins() {
    const { t } = useTranslation();
    const dispatch = useDispatch()

    const { pluginLists } = useSelector((state: any) => state.plugin);

    const { bundleTableColumn } = CommonComponents()
    const { tooltipEditTitle, tooltipDeleteTitle } = tooltipTitle();
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
    const [openCreateModal2, setOpenCreateModal2] = useState(false)
    const [openCreateModal3, setOpenCreateModal3] = useState(false)
    const [resetButtonShow, setResetButtonShow] = useState(true)
    const [pluginListData, setPluginListData] = useState([])
    const [pluginInfoLoading, setPluginInfoLoading] = useState(false)
    const [pluginId, setPluginId] = useState('')
    const [pluginName, setPluginName] = useState('')
    const [pluginDesc, setPluginDesc] = useState('')
    const [bundleDesc, setBundleDesc] = useState('')
    const [nextloading1, setNextLoading1] = useState(false)
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
        const selectedItem: any = bundilesList.find((item: any) => item.registered === false) || []
        setBundleId(selectedItem.bundle_id)
        setBundleName(selectedItem.name)
        try {
            setPluginInfoLoading(true)
            const res = await getPluginDetail(selectedItem.bundle_id)
            setPluginListData(res.data)
            setPluginId(res.data[0].plugin_id)
            setCredentialsSchema(selectedItem.credentials_schema)
            setPluginName(res.data[0].name)
            setPluginDesc(res.data[0].description)
            const inputSchematemp = res.data[0].input_schema
            const arr: any[] = []
            Object.values(inputSchematemp).forEach((item: any) => {
                arr.push(item)
            })
            setInputSchema(arr)
        } catch (error) {
            console.log(error)
        } finally {
            setPluginInfoLoading(false)
        }

    }
    const getBundleList = async (params: object) => {
        const res: any = await bundleList(params)
        setBundleId(res.data[0].bundle_id)
        setBundleName(res.data[0].name)
        setBundleDesc(res.data[0].description)
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

        setCredentialsSchema(res.data[0].credentials_schema)
        const res1 = await getPluginDetail(res.data[0].bundle_id)
        setPluginListData(res1.data)
        setPluginId(res1.data[0].plugin_id)
        setPluginName(res1.data[0].name)
        setPluginDesc(res1.data[0].description)
        const inputSchematemp = res1.data[0].input_schema
        const arr: any[] = []
        Object.values(inputSchematemp).forEach((item: any) => {
            arr.push(item)
        })
        setInputSchema(arr)
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
                    <Tooltip placement='bottom' color='#fff' arrow={false} overlayClassName='table-tooltip'>
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
        setCredentialsSchema(data.credentials_schema)
        form.setFieldsValue(record.display_credentials)
        setResetButtonShow(true)
        setOpenEditFormDrawer(true)

    }
    const handleTools = async (record: any) => {
        setLoading(true)
        try {
            setPluginListData(record.plugins)
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
            setUpdatePrevButton(true)
        } catch (error) {
            console.log(error)
        }
        setOpenDeleteModal(false)
    }
    const handleCancel = () => {
        setOpenDrawer(false)
        setOpenCreateModal2(false)
    }
    const handleCancel1 = () => {
        setOpenCreateModal2(false)
    }
    const handleCancel2 = () => {
        setOpenCreateModal3(false)
    }
    const handleNext = () => {
        setOpenCreateModal2(true)
        setIsShowBundle(true)
        setFormDisabled(false)

    }
    const handleClickBundle = async (bundleId: string, bundelName: string, item: any) => {
        setBundleId(bundleId)
        setBundleName(bundelName)
        setBundleDesc(item.description)
        setPluginListData(item.plugins)
        setPluginId(item.plugins[0].plugin_id)
        setCredentialsSchema(item.credentials_schema)
        setPluginName(item.plugins[0].name)
        setPluginDesc(item.plugins[0].description)
        const inputSchematemp = item.plugins[0].input_schema
        const arr: any[] = []
        Object.values(inputSchematemp).forEach((item: any) => {
            arr.push(item)
        })
        setInputSchema(arr)
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
    const handleNext1 = async () => {

        if (JSON.stringify(credentialsSchema) === '{}') {
            const params = {
                name: bundleName,
                bundle_id: bundleId,
            }
            try {
                setNextLoading1(true)
                await createPlugin(params)
                const limit1: number = limit || 20
                dispatch(fetchPluginData(limit1) as any);
                setOpenCreateModal3(false)
                setOpenCreateModal2(false)
                setOpenDrawer(false)
                setUpdatePrevButton(true)
                toast.success('Creation successful!')
            } catch (e) {
                const apiError = e as ApiErrorResponse;
                const errorMessage: string = apiError.response.data.error.message;
                toast.error(errorMessage)
            } finally {
                setNextLoading1(false)
            }
        } else {
            setResetButtonShow(false)
            form.resetFields()
            setOpenCreateModal3(true)
        }
    }
    const handleConfirm = () => {
        form.validateFields().then(async () => {
            try {
                const credentials = form.getFieldsValue()
                const params = {
                    name: bundleName,
                    credentials,
                    bundle_id: bundleId,
                }
                setConfirmLoading(true)
                await createPlugin(params)
                const limit1: number = limit || 20
                dispatch(fetchPluginData(limit1) as any);
                setOpenCreateModal3(false)
                setOpenCreateModal2(false)
                setOpenDrawer(false)
                setUpdatePrevButton(true)
                toast.success('Creation successful!')
            } catch (error) {
                const apiError = error as ApiErrorResponse;
                const errorMessage: string = apiError.response.data.error.message;
                toast.error(errorMessage)
            } finally {
                setConfirmLoading(false)
            }
        })
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
                            {/* <div className={styles.inputParams}>{t('projectInputParameters')}</div> */}
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
                        All plugin credentials are encrypted at rest with AES-256 and in transit with TLS 1.2. Refer to <a className='href' href='https://docs.tasking.ai/docs/guide/tool/plugin/create-bundles-and-plugins' target='_blank' rel='noopener noreferrer'>documentation</a> for more information.
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
                <ModalTable loading={loading} updatePrevButton={updatePrevButton} name='plugins' id='bundle_id' hasMore={hasMore} ifSelect={false} columns={columns} dataSource={pluginFunList} onChildEvent={handleChildEvent} onOpenDrawer={handleCreatePrompt} />
            </Spin>
            <Modal footer={[
                <>
                    {openCreateModal2 ? <>
                        <Button icon={<LeftOutlined />} key="cancel" onClick={handleCancel1} className='cancel-button'>
                            {t('back')}
                        </Button>
                        <Button key="submit" loading={nextloading1} onClick={handleNext1} className='next-button' style={{ marginLeft: '10px' }}>
                            {t('confirm')}
                        </Button>
                    </> : <><Button key="cancel" onClick={handleCancel} className='cancel-button'>
                        {t('cancel')}
                    </Button>
                        <Button key="submit" onClick={handleNext} className='next-button' style={{ marginLeft: '10px' }}>
                            {t('next')}
                            <RightOutlined />
                        </Button></>}
                </>
            ]} width={1280} onCancel={handleCancel} centered closeIcon={<img src={closeIcon} alt="closeIcon" className={styles['img-icon-close']} />} title={openCreateModal2 ? t('projectBundleSelection') : t('projectPluginCreate')} open={openCreateModal1} className={styles.drawerCreate}>
                {openCreateModal2 ? <ComponentsData /> : <Spin spinning={pluginInfoLoading}>
                    <div className={styles.modalContent}>
                        <div className={styles.left}>
                            <div className={styles.selectBundleDesc}>{t('projectBundleDesc')}</div>
                            <div className={styles.content}>
                                {bundilesList.map((item: any, index) => (
                                    <div key={index} className={`${styles.frameParent} ${item.bundle_id === bundleId && styles.activeframeParent} ${item.registered && styles.registeredItem}`} onClick={item.registered ? undefined : () => { handleClickBundle(item.bundle_id, item.name, item) }}>
                                        <div className={styles.logoParent}>
                                            <img src={(cachedImages as any)[item.bundle_id]} alt="" className={styles.img} />
                                            <div className={styles.frameWrapper}>
                                                <div className={styles.frameWrapper}>
                                                    <div className={styles.frameDiv}>
                                                        <div className={styles.frameChild} />
                                                    </div>
                                                </div>
                                            </div>
                                            {item.registered ? <div className={styles.registered}>Registered</div> : <RightArrow />}

                                        </div>
                                        <div className={styles.googleWebSearch}>{item.name}</div>
                                        <div className={styles.label}>{item.description}</div>
                                        {/* <div className={styles.webSearchWrapper}>
                                        <div className={styles.webSearch}>Web Search</div>
                                    </div> */}
                                        <div className={styles.frameGroup}>
                                            <div className={styles.functionaliconsParent}>
                                                <ToolsNew />
                                                <div className={styles.webSearch}>{item.num_plugins}  {item.num_plugins > 1 ? t('projectToolsTitle') : 'Tool'}</div>
                                            </div>
                                            <div className={styles.taskingaiWrapper}>
                                                <div className={styles.taskingai}>{item.developer}</div>
                                            </div>
                                        </div>
                                    </div>
                                ))}

                            </div>
                            {/* <Paginations hasMore={bundlesHasMore} onFetchData={getBundleList}></Paginations> */}
                        </div>
                        <>
                            <div className={styles.popupbodynormal}>
                                <div className={styles.googleWeb}>
                                    <img loading="lazy" src={(cachedImages as any)[bundleId]} alt="" style={{ width: '36px', height: '36px' }} />
                                    <div className={styles.googleWebSearch1}>{bundleName}</div>
                                </div>
                                {
                                    pluginListData.map((item: any, index) => (
                                        <div className={styles.pluginContent} key={index}>
                                            <div className={styles.pluginTitle}>{item.name}</div>
                                            <div className={styles.pluginDesc}>
                                                {item.description}
                                            </div>
                                        </div>
                                    ))
                                }
                            </div>
                        </>
                    </div>
                </Spin>
                }
            </Modal>
            {/* <Modal footer={[
                <Button icon={<LeftOutlined />} key="cancel" onClick={handleCancel1} className='cancel-button'>
                    {t('back')}
                </Button>,
                <Button key="submit" onClick={handleNext1} className='next-button'>
                    {t('confirm')}
                </Button>
            ]} width={1280} onCancel={handleCancel1} className={styles.createModal2} open={openCreateModal2} centered title={t('projectPluginCreate')} closeIcon={<img src={closeIcon} alt="closeIcon" className={styles['img-icon-close']} />} >
                <ComponentsData />
            </Modal> */}
            <Modal footer={[
                <Button key="cancel" onClick={handleCancel2} className='cancel-button'>
                    {t('cancel')}
                </Button>,
                <Button key="submit" loading={confirmLoading} onClick={handleConfirm} className='next-button'>
                    {t('confirm')}
                </Button>
            ]} width={720} onCancel={handleCancel2} open={openCreateModal3} centered closeIcon={<img src={closeIcon} alt="closeIcon" className={styles['img-icon-close']} />} title={t('projectPluginCreate')} className={styles.createModal3}>
                <EditForm />
            </Modal>
            <Drawer footer={[
                <Button key="cancel" onClick={handleEditCancel} className='cancel-button'>
                    {t('cancel')}
                </Button>,
                <Button key="submit" loading={confirmLoading} onClick={handleEditCancel} className={`next-button ${styles.button}`}>
                    {t('confirm')}
                </Button>
            ]} width={1280} closeIcon={<img src={closeIcon} alt="closeIcon" className={styles['img-icon-close']} />} onClose={handleEditCancel} open={openEditDrawer} title={`${t('projectBundleTitle')} ${t('projectModelColumnName')}/${t('projectPluginsTitle')}`} className={styles.openEditDrawer}>
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