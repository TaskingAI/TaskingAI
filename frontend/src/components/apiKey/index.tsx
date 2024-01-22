import styles from './apiKey.module.scss'
import ModalTable from '../modalTable/index'
import closeIcon from '../../assets/img/x-close.svg'
import { Button, Modal, Form, Input, Spin, Space, Tooltip } from 'antd'
import { useState, useEffect } from 'react';
import { toast } from 'react-toastify'
import { tooltipEditTitle, tooltipDeleteTitle, tooltipHideTitle, tooltipShowTitle } from '../../contents/index.tsx'
import EditIcon from '../../assets/img/editIcon.svg?react'
import DeleteIcon from '../../assets/img/deleteIcon.svg?react'
import ShowEye from '../../assets/img/showEye.svg?react'
import HideEye from '../../assets/img/eyeClose.svg?react'
import { apikeysTableColumn } from '../../contents/index'
import { createApiKeys, getApiKeysList, getApiKeys, updateApiKeys, deleteApiKeys } from '../../axios/apiKeys.ts'
function ApiKeys() {
    useEffect(() => {
        const params = {
            limit: 20,
        }
        fetchData(params)
    }, [])
    const [form] = Form.useForm();
    const [form1] = Form.useForm();
    const [deleteForm] = Form.useForm();
    const [openEditAPIKey, setOpenEditAPIKey] = useState(false)
    const [openCreateAPIKey, setOpenCreateAPIKey] = useState(false)
    const [createNameValue, setCreateNameValue] = useState('')
    const [openDeleteModal, setOpenDeleteModal] = useState(false)
    const [apiKeysList, setApiKeysList] = useState([])
    const [loading, setLoading] = useState(false);
    const [deleteLoading, setDeleteLoading] = useState(false);
    const [apiKeyName, setapiKeyName] = useState('');
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
    useEffect(() => {
        if (apiKeyName === 'Create API Key') {
            form.setFieldsValue({ name: '' });
        }
    }, [apiKeyName])
    const fetchData = async (params) => {
        try {
            const res = await getApiKeysList(params)
            const data = res.data.map((item) => {
                return {
                    ...item,
                    key: item.apikey_id
                }
            })
            setApiKeysList(data)
        } catch (e) {
            console.log(e)
        }
    }

   const columns = [...apikeysTableColumn]
   columns.push(
    {
        title: 'Actions',
        key: 'action',
        fixed: 'right',
        width: 157,
        render: (_, record) => (
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
    const handleShow = async (val) => {
        let res;
        if (val.apikey.includes('***')) {
            res = await getApiKeys(val.apikey_id, 'true')
        } else {
            res = await getApiKeys(val.apikey_id, 'false')
        }

        const updatedApiKeysList = apiKeysList.map((item) => {
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
    const handleEdit = async (val) => {
        setInitialValues({
            name: val.name,
        })
        await setCreateNameValue(val.name)
        form1.setFieldsValue({ name: val.name });
        setId(val.apikey_id)

        setapiKeyName('Edit API Key')
        setOpenEditAPIKey(true)
    }
    const handleDelete = async (record) => {
        await deleteForm.resetFields()
        setOpenDeleteModal(true)
        setDisabled(true)
        setRecord(record)
    }
    const handleDeleteValue = (e) => {
        if (e.target.value === record.name) {
            setDisabled(false)
        } else {
            setDisabled(true)
        }
    }
    const handleCreateConfrim = async () => {
        if (id) {
            form1.validateFields().then(async () => {
                setLoading(true);
                const params = {
                    name: createNameValue,
                }
                try {
                    await updateApiKeys(id,params)
                    setOpenEditAPIKey(false)
                    toast.success('Update successful')

                } catch (e) {
                    console.log(e)
                    toast.error(e.response.data.error.message)
                }
                const params1 = {
                    limit: 20,
                }
                await fetchData(params1)
                setLoading(false);
                await form1.resetFields()
                await form1.setFieldsValue({ name: '' });
            }).catch((errorInfo) => { 
                console.log(errorInfo)
            })
            return
        } else {
            form.validateFields().then(async () => {
                setLoading(true);
                const params = {
                    name: createNameValue,
                }
                try {
                    await createApiKeys(params)
                    setOpenCreateAPIKey(false)
                    toast.success('Creation successful')

                } catch (e) {
                    console.log(e)
                    toast.error(e.response.data.error.message)
                }
                const params1 = {
                    limit: 20,
                }
                await fetchData(params1)
                setLoading(false);
                await form.resetFields()
                await form.setFieldsValue({ name: '' });
            }).catch((errorInfo) => {
                console.log(errorInfo)
             })
            return
        }
    }
    const handleChildEvent = async (value) => {
        await fetchData(value);
    }
    const handleChangeNameValue = (e) => {
        setCreateNameValue(e.target.value)
    }
    const handleDeleteConfrim = async () => {
        setDeleteLoading(true)

        await deleteApiKeys(record.apikey_id)
        setApiKeysList(prevList => prevList.filter(item => record.apikey_id !== item.apikey_id));
        const params1 = {
            limit: 20,
        }
        await fetchData(params1)
        setOpenDeleteModal(false)
        setDeleteLoading(false)
    }
    return (
        <div className={styles["api-keys"]}>

            <Spin spinning={false} wrapperClassName={styles.spinloading}>
                <ModalTable ifSelect={false} ifHideFooter={true} columns={columns} name="API Key" dataSource={apiKeysList} onChildEvent={handleChildEvent} onOpenDrawer={handleNewInstance} />
            </Spin>
            <Modal title='Edit API Key'
                onCancel={handleModalCancel}
                open={openEditAPIKey}
                centered
                className={styles['delete-apikey-modal']}
                closeIcon={<img src={closeIcon} alt="closeIcon" />}
                footer={[
                    <Button key="cancel" onClick={handleModalCancel} className='cancel-button'>
                        Cancel
                    </Button>,
                    <Button key="submit" loading={loading} onClick={handleCreateConfrim} className='next-button'>
                        Confirm
                    </Button>
                ]}
            >
                <Form layout='vertical' className={styles['edit-form']} initialValues={initialValues} form={form1}>
                    <Form.Item label="Name" name="name" rules={[{ required: true, message: 'Please input Instance Name.' }]}>
                        <Input className={styles['edit-instance-modal']} onChange={handleChangeNameValue}></Input>
                    </Form.Item>
                </Form>
            </Modal>
            <Modal title='Create API Key'
                onCancel={handleCreateCancel}
                open={openCreateAPIKey}
                className={styles['create-apikey-modal']}
                centered
                closeIcon={<img src={closeIcon} alt="closeIcon" />}
                footer={[
                    <Button key="cancel" onClick={handleCreateCancel} className='cancel-button'>
                        Cancel
                    </Button>,
                    <Button key="submit" loading={loading} onClick={handleCreateConfrim} className='next-button'>
                        Confirm
                    </Button>
                ]}
            >
                <Form layout='vertical' className={styles['edit-form']} form={form}>
                    <Form.Item label="Name" name="name" rules={[{ required: true, message: 'Please input Instance Name.' }]}>
                        <Input className={styles['edit-instance-modal']} onChange={handleChangeNameValue}></Input>
                    </Form.Item>
                </Form>
            </Modal>
            <Modal title='Delete API Key'
                onCancel={handleDeleteCancel}
                open={openDeleteModal}
                centered
                className={styles['delete-apikey-modal']}
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
                <p className={styles['p']}>Are you sure you want to delete<span className={styles['span']}> {record.name}</span>? Please be aware that once the API Key is deleted,it will no longer have the access to your project. </p>

                <Form layout='vertical' className={styles['edit-form']} form={deleteForm}>
                    <Form.Item label="API Key Name" name="name" rules={[{ required: true, message: 'Please input API Key Name.' }]}>
                        <Input onChange={handleDeleteValue} className={styles['edit-instance-modal']} placeholder='Enter name to confirm'></Input>
                    </Form.Item>
                </Form>
            </Modal>
        </div>
    )

}

export default ApiKeys