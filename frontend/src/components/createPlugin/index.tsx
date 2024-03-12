import { Modal, Button, Spin, Form, Input } from 'antd';
import { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { LeftOutlined, RightOutlined } from '@ant-design/icons';
import styles from './createPlugin.module.scss';
import closeIcon from '../../assets/img/x-close.svg'
import { getPluginDetail, createPlugin, bundleList } from '@/axios/plugin.ts'
import ParameterTable from '../parameterTable/index.tsx'
import RightArrow from '../../assets/img/rightarrow.svg?react'
import ToolsNew from '../../assets/img/tools.svg?react'
import ApiErrorResponse from '@/constant/index'
import { toast } from 'react-toastify';

function CreatePlugin(props: any) {
    const { t } = useTranslation();
    const { open, handleCloseModal, handleConfirmRequest } = props
    const [openCreateModal2, setOpenCreateModal2] = useState(false);
    const [openCreateModal3, setOpenCreateModal3] = useState(false);
    const [confirmLoading, setConfirmLoading] = useState(false)
    const [form] = Form.useForm();
    const [bundleId, setBundleId] = useState('')
    const [bundilesList, setBundlesList] = useState([])

    const [pluginName, setPluginName] = useState('')
    const [credentialsSchema, setCredentialsSchema] = useState({})
    const [pluginInfoLoading, setPluginInfoLoading] = useState(false)
    const [bundleName, setBundleName] = useState('')
    const [pluginListData, setPluginListData] = useState([])
    const [pluginId, setPluginId] = useState('')
    const [pluginDesc, setPluginDesc] = useState('')
    const [inputSchema, setInputSchema] = useState({})
    const [cachedImages, setCachedImages] = useState({});

    useEffect(() => {

        const params1 = {
            limit: 100,
            offset: 0,
            lang: 'en'
        }
        getBundleList(params1)
    }, [])
    const getBundleList = async (params: object) => {
        const res: any = await bundleList(params)
        const selectedItem: any = res.data.find((item: any) => item.registered === false) || []
        setBundleId(selectedItem.bundle_id)
        setBundleName(selectedItem.name)
        setBundlesList(res.data)
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
        setCredentialsSchema(selectedItem.credentials_schema)
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

    const handleNext1 = () => {
        setOpenCreateModal3(true)
    }
    const handleCancel1 = () => {
        setOpenCreateModal2(false)
    }
    const handleCancel = () => {
        handleCloseModal()
    }
    const handleNext = () => {
        setOpenCreateModal2(true)
    }
    const handleCancel2 = () => {
        setOpenCreateModal3(false)
    }
    const handleConfirm = async () => {
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
                handleConfirmRequest()
                setOpenCreateModal3(false)
                setOpenCreateModal2(false)
                handleCloseModal()

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
    const handleValuesChange = (changedValues: object) => {
        form.validateFields(Object.keys(changedValues));
    };
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
    const handleClickBundle = async (bundleId: string, bundelName: string, item: any) => {
        setBundleId(bundleId)
        setPluginInfoLoading(true)
        setBundleName(bundelName)

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
        setPluginInfoLoading(false)
    }
    return <>
        <Modal footer={[
            <>
                {openCreateModal2 ? <>
                    <Button icon={<LeftOutlined />} key="cancel" onClick={handleCancel1} className='cancel-button'>
                        {t('back')}
                    </Button>
                    <Button key="submit" onClick={handleNext1} className='next-button' style={{ marginLeft: '10px' }}>
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
        ]} zIndex={10002} width={1280} onCancel={handleCancel} centered closeIcon={<img src={closeIcon} alt="closeIcon" className={styles['img-icon-close']} />} title={openCreateModal2 ? t('projectBundleSelection') : t('projectPluginCreate')} open={open} className={styles.drawerCreate}>
            {openCreateModal2 ? <div className={styles.componentsData}>
                <div className={styles.inputWithLabelParent}>
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
                        </div>
                    </div>
                </div>

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


                        </div>
                        <div className={styles.pluginDesc}>{pluginDesc}</div>
                        <div className={styles.inputParams}>{t('projectInputParameters')}</div>
                        <div style={{ marginLeft: '24px', marginTop: '12px' }}>
                            <ParameterTable parameters={inputSchema} />
                        </div>
                    </div>
                </div></div> : <div className={styles.modalContent}>
                <div className={styles.left}>
                    <div className={styles.selectBundleDesc}>{t('projectBundleDesc')}</div>
                    <div className={styles.content}>
                        {bundilesList.map((item: any, index: number) => (
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

                                <div className={styles.frameGroup}>
                                    <div className={styles.functionaliconsParent}>
                                        <ToolsNew />
                                        <div className={styles.webSearch}>{item.num_plugins} {item.num_plugins > 1 ? t('projectToolsTitle') : 'Tool'}</div>
                                    </div>
                                    <div className={styles.taskingaiWrapper}>
                                        <div className={styles.taskingai}>{item.developer}</div>
                                    </div>
                                </div>
                            </div>
                        ))}

                    </div>
                </div>
                <Spin spinning={pluginInfoLoading}>
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
                </Spin>
            </div>}
        </Modal>
        <Modal footer={[
            <Button key="cancel" onClick={handleCancel2} className='cancel-button'>
                {t('cancel')}
            </Button>,
            <Button key="submit" loading={confirmLoading} onClick={handleConfirm} className='next-button'>
                {t('confirm')}
            </Button>
        ]} width={720} zIndex={10003} onCancel={handleCancel2} open={openCreateModal3} centered closeIcon={<img src={closeIcon} alt="closeIcon" className={styles['img-icon-close']} />} title={t('projectPluginCreate')} className={styles.createModal3}>
            <div className={styles.editForm}>
                <div className={styles.bundleTitle}>
                    <div className={styles.label}>{t('projectBundleTitle')}</div>
                    <div className={styles.googleWeb}>
                        <img loading="lazy" src={(cachedImages as any)[bundleId]} alt="" style={{ width: '24px', height: '24px' }} />
                        <div className={styles.googleWebSearch}>{bundleName}</div>
                    </div>
                </div>
                <div className={styles['credentials']}>{t('projectModelCredentials')}</div>
                <div className={styles['label-desc']} style={{ marginBottom: '24px' }}>
                    All plugin credentials are encrypted at rest with AES-256 and in transit with TLS 1.2. Refer to <a className='href' href='https://docs.tasking.ai/docs/guide/tool/plugin/create-bundles-and-plugins' target='_blank' rel='noopener noreferrer'>documentation</a> for more information.
                </div>

                <Form
                    layout="vertical"
                    autoComplete="off"
                    form={form}
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
            </div>
        </Modal>
    </>;
}
export default CreatePlugin;