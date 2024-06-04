import styles from './apiKey.module.scss'
import ModalTable from '../modalTable/index'
import closeIcon from '../../assets/img/x-close.svg'
import { Button, Modal, Form, Input, Spin, Space, Tooltip } from 'antd'
import { useState, useEffect, ChangeEvent } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { toast } from 'react-toastify'
import { fetchApikeysData } from '../../Redux/actions';

import tooltipTitle from '../../contents/tooltipTitle.tsx'
import EditIcon from '../../assets/img/editIcon.svg?react'
import DeleteIcon from '../../assets/img/deleteIcon.svg?react'
import ShowEye from '../../assets/img/showEye.svg?react'
import HideEye from '../../assets/img/eyeClose.svg?react'
import CommonComponents from '../../contents/index'
import ApiErrorResponse from '../../constant/index.ts'
import { useTranslation, Trans } from 'react-i18next';
import { createApiKeys, getApiKeysList, getApiKeys, updateApiKeys, deleteApiKeys } from '../../axios/apiKeys.ts'
function ApiKeys() {
    const { apiKeyLists } = useSelector((state: any) => state.apikey);
    const dispatch = useDispatch()
    const { t } = useTranslation(['components/apiKey/index', 'common']);
    const { apikeysTableColumn } = CommonComponents();
    const { tooltipEditTitle, tooltipDeleteTitle, tooltipShowTitle, tooltipHideTitle } = tooltipTitle();

    useEffect(() => {
        if (apiKeyLists.data.length > 0) {
            const data = apiKeyLists.data.map((item: any) => {
                return {
                    ...item,
                    key: item.apikey_id
                }
            })
            setApiKeysList(data)
        }else {
            setApiKeysList([])
        }
    }, [apiKeyLists])
    const [form] = Form.useForm();
    const [form1] = Form.useForm();
    const [deleteForm] = Form.useForm();
    const [openEditAPIKey, setOpenEditAPIKey] = useState(false)
    const [openCreateAPIKey, setOpenCreateAPIKey] = useState(false)
    const [createNameValue, setCreateNameValue] = useState('')

    const [openDeleteModal, setOpenDeleteModal] = useState(false)
    const [apiKeysList, setApiKeysList] = useState<any[]>([])
    const [loading, setLoading] = useState(false);
    const [confirmLoading, setConfirmLoading] = useState(false)
    const [tableLoading, setTableLoading] = useState(false)
    const [deleteLoading, setDeleteLoading] = useState(false);
    const [record, setRecord] = useState<any>({});
    const [initialValues, setInitialValues] = useState({
        name: '',
    })
    const [id, setId] = useState('');
    const [disabled, setDisabled] = useState(true);
    const handleNewInstance = async () => {
        await form.setFieldValue('name', '')
        await setCreateNameValue('')
        setId('')
        setOpenCreateAPIKey(true)
        await form.resetFields()
    }

    const fetchData = async (params: Record<string, any>) => {
        try {
            setTableLoading(true)
            const res = await getApiKeysList(params)
            const data = res.data.map((item: any) => {
                return {
                    ...item,
                    key: item.apikey_id
                }
            })
            setApiKeysList(data)
        } catch (e) {
            console.log(e)
        } finally {
            setTableLoading(false)
        }
    }

    const columns = [...apikeysTableColumn]
    columns.push(
        {
            title: `${t('actions', {ns: 'common'})}`,
            key: 'action',
            fixed: 'right',
            width: 157,
            render: (__: string, record: any) => (
                <Space size="middle">
                    <div onClick={() => handleShow(record)} className='table-edit-icon1'>
                        <Tooltip placement='bottom' color='#fff' arrow={false} overlayClassName='table-tooltip' title={record.apikey.includes('***') ? tooltipShowTitle : tooltipHideTitle}>
                            {record.apikey.includes('***') ? <ShowEye /> : <HideEye />}
                        </Tooltip>
                    </div>
                    <div onClick={() => handleEdit(record)} className='table-edit-icon'>
                        <Tooltip placement='bottom' title={tooltipEditTitle} color='#fff' arrow={false} overlayClassName='table-tooltip'>
                            <EditIcon />
                        </Tooltip>
                    </div>
                    <div onClick={() => handleDelete(record)} className='table-edit-icon'>
                        <Tooltip placement='bottom' title={tooltipDeleteTitle} color='#fff' arrow={false} overlayClassName='table-tooltip'>
                            <DeleteIcon />
                        </Tooltip>

                    </div>
                </Space>
            ),
        }
    )
    const handleModalCancel = async () => {
        await form.resetFields()
        await form.setFieldsValue({ name: '' });
        setOpenEditAPIKey(false)
    }
    const handleCreateCancel = async () => {
        await form.resetFields()
        await form.setFieldsValue({ name: '' });
        setOpenCreateAPIKey(false)
    }
    const handleDeleteCancel = async () => {
        setOpenDeleteModal(false)
        await deleteForm.resetFields()
    }
    const handleShow = async (val: any) => {
        let res: any;
        if (val.apikey.includes('***')) {
            res = await getApiKeys(val.apikey_id, 'true')
        } else {
            res = await getApiKeys(val.apikey_id, 'false')
        }

        const updatedApiKeysList = apiKeysList.map((item: any) => {
            if (item.apikey_id === val.apikey_id) {
                return res.data;
            }
            return {
                ...item,
                key: item.apikey_id
            }
        });
        setApiKeysList(updatedApiKeysList);
    }
    const handleEdit = async (val: any) => {
        setInitialValues({
            name: val.name,
        })
        await setCreateNameValue(val.name)
        form1.setFieldsValue({ name: val.name });
        setId(val.apikey_id)
        setOpenEditAPIKey(true)
    }
    const handleDelete = async (record: any) => {
        await deleteForm.resetFields()
        setOpenDeleteModal(true)
        setDisabled(true)
        setRecord(record)
    }
    const handleDeleteValue = (e: ChangeEvent<HTMLInputElement>) => {
        if (e.target.value === record.name) {
            setDisabled(false)
        } else {
            setDisabled(true)
        }
    }
    const handleCreateConfirm = async () => {
        if (id) {
            form1.validateFields().then(async () => {
                setLoading(true);
                const params = {
                    name: createNameValue,
                }
                try {
                    await updateApiKeys(id, params)
                    setOpenEditAPIKey(false)
                    toast.success(`${t('updateSuccessful', {ns: 'common'})}`)

                } catch (e) {
                    console.log(e)
                    const errorResponse = e as ApiErrorResponse;
                    const errorMessage: string = errorResponse.response.data.error.message;
                    toast.error(errorMessage)
                }
                dispatch(fetchApikeysData(20) as any);
                setLoading(false);
                await form1.resetFields()
                await form1.setFieldsValue({ name: '' });
            }).catch((errorInfo) => {
                console.log(errorInfo)
            })
            return
        } else {
            form.validateFields().then(async () => {
                setConfirmLoading(true);
                const params = {
                    name: createNameValue,
                }
                try {
                    await createApiKeys(params)
                    setOpenCreateAPIKey(false)
                    toast.success(`${t('creationSuccessful', {ns: 'common'})}`)

                } catch (e) {
                    console.log(e)
                    const errorResponse = e as ApiErrorResponse;
                    const errorMessage: string = errorResponse.response.data.error.message;
                    toast.error(errorMessage)
                }

                dispatch(fetchApikeysData(20) as any);
                setConfirmLoading(false);
                await form.resetFields()
                await form.setFieldsValue({ name: '' });
            }).catch((errorInfo) => {
                console.log(errorInfo)
            })
            return
        }
    }
    const handleChildEvent = async (value: Record<string, any>) => {
        await fetchData(value);
    }
    const handleChangeNameValue = (e: ChangeEvent<HTMLInputElement>) => {
        setCreateNameValue(e.target.value)
    }
    const handleDeleteConfirm = async () => {
        setDeleteLoading(true)

        await deleteApiKeys(record.apikey_id)
        setApiKeysList(prevList => prevList.filter(item => record.apikey_id !== item.apikey_id));

        dispatch(fetchApikeysData(20) as any);

        setOpenDeleteModal(false)
        setDeleteLoading(false)
    }
    return (
        <div className={styles["api-keys"]}>

            <Spin spinning={tableLoading} wrapperClassName={styles.spinloading}>
                <ModalTable ifSelect={false} title={t('newApiKey')} loading={tableLoading} ifHideFooter={true} columns={columns} name="API Key" dataSource={apiKeysList} onChildEvent={handleChildEvent} onOpenDrawer={handleNewInstance} />
            </Spin>
            <Modal title={t('editApiKey')}
                onCancel={handleModalCancel}
                open={openEditAPIKey}
                centered
                className={styles['delete-apikey-modal']}
                closeIcon={<img src={closeIcon} alt="closeIcon" />}
                footer={[
                    <Button key="cancel" onClick={handleModalCancel} className='cancel-button'>
                        {t('cancel', {ns: 'common'})}
                    </Button>,
                    <Button key="submit" loading={loading} onClick={handleCreateConfirm} className='next-button'>
                        {t('confirm', {ns: 'common'})}
                    </Button>
                ]}
            >
                <Form layout='vertical' className={styles['edit-form']} initialValues={initialValues} form={form1}>
                    <Form.Item label={t('name', {ns: 'common'})} name="name" rules={[{ required: true, message: t('requiredApiKeyName') }]}>
                        <Input className={styles['edit-instance-modal']} onChange={handleChangeNameValue}></Input>
                    </Form.Item>
                </Form>
            </Modal>
            <Modal title={t('createApiKey')}
                onCancel={handleCreateCancel}
                open={openCreateAPIKey}
                className={styles['create-apikey-modal']}
                centered
                closeIcon={<img src={closeIcon} alt="closeIcon" />}
                footer={[
                    <Button key="cancel" onClick={handleCreateCancel} className='cancel-button'>
                        {t('cancel', {ns: 'common'})}
                    </Button>,
                    <Button key="submit" loading={confirmLoading} onClick={handleCreateConfirm} className='next-button'>
                        {t('confirm', {ns: 'common'})}
                    </Button>
                ]}
            >
                <Form layout='vertical' className={styles['edit-form']} form={form}>
                    <Form.Item label={t('name', {ns: 'common'})} name="name" rules={[{ required: true, message: `${t('nameRequired', {ns: 'common'})}` }]}>
                        <Input className={styles['edit-instance-modal']} onChange={handleChangeNameValue}></Input>
                    </Form.Item>
                </Form>
            </Modal>
            <Modal title={t('deleteApiKey')}
                onCancel={handleDeleteCancel}
                open={openDeleteModal}
                centered
                className={styles['delete-apikey-modal']}
                closeIcon={<img src={closeIcon} alt="closeIcon" />}
                footer={[
                    <Button key="cancel" onClick={handleDeleteCancel} className='cancel-button'>
                        {t('cancel', {ns: 'common'})}
                    </Button>,
                    <Button key="delete" onClick={handleDeleteConfirm} className={disabled ? 'disabled-button' : 'delete-button'} disabled={disabled} loading={deleteLoading}>
                        {t('delete', {ns: 'common'})}
                    </Button>
                ]}
            >
                <p className={styles['p']}><Trans i18nKey="components/apiKey/index:deleteItem" values={{ deleteValue: record.name}} components={[<span className={styles['span']}>{record.name}</span>]} /> {t('deleteDesc')} </p>
                <Form layout='vertical' className={styles['edit-form']} form={deleteForm}>
                    <Form.Item label={t('apiKeyName')} name="name" rules={[{ required: true, message: `${t('apiKeyNameRequired')}` }]}>
                        <Input onChange={handleDeleteValue} className={styles['edit-instance-modal']} placeholder={t('apiKeyNameDeletePlaceholder')}></Input>
                    </Form.Item>
                </Form>
            </Modal>
        </div>
    )

}

export default ApiKeys