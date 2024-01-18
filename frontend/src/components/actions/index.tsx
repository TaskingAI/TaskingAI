import {
    Space, Drawer, Input, Spin, Radio, Tooltip
} from 'antd';
import styles from './action.module.scss'
import { useState, useEffect } from 'react';
import { getFirstMethodAndEndpoint } from '../../utils/util.ts'
import { getActionsList, updateActions, deleteActions, createActions, getActionsDetail } from '../../axios/actions.ts'
import closeIcon from '../../assets/img/x-close.svg'
import DeleteModal from '../deleteModal/index.tsx'
import ModalTable from '../modalTable/index'
import ModalFooterEnd from '../modalFooterEnd/index'
import EditIcon from '../../assets/img/editIcon.svg?react'
import DeleteIcon from '../../assets/img/deleteIcon.svg?react'
import { tooltipEditTitle, tooltipDeleteTitle } from '../../contents/index.tsx'
import { toast } from 'react-toastify';
import {actionsTableColumn} from '../../contents/index.tsx'
function Actions() {
    const [loading, setLoading] = useState(false);
    const [pluginFunList, setPluginFunList] = useState([])
    const [deleteValue, setDeleteValue] = useState('')
    const [updatePrevButton, setUpdatePrevButton] = useState(false)
    const [OpenDrawer, setOpenDrawer] = useState(false)
    const [tipSchema, setTipSchema] = useState(false)
    const [drawerTitle, setDrawerTitle] = useState('Bulk Create Action')
    const [OpenDeleteModal, setOpenDeleteModal] = useState(false)
    const [radioValue, setRadioValue] = useState('none')
    const [Authentication, setAuthentication] = useState<string>('')
    const [schema, setSchema] = useState('')
    const [custom, setCustom] = useState('')
    const [limit, setLimit] = useState(20)
    const [hasMore, setHasMore] = useState(false)
    const [actionId, setActionId] = useState('')
    const { TextArea } = Input

    useEffect(() => {
        const params = {
            limit: 20,
        }
        fetchData(params)
    }, [])

    const fetchData = async (params) => {
        setLoading(true);
        try {
            const res:any = await getActionsList(params)
            const data = res.data.map((item) => {
                return {
                    ...item,
                    key: item.action_id,
                    method: getFirstMethodAndEndpoint(item.openapi_schema)?.method,
                    endpoint: getFirstMethodAndEndpoint(item.openapi_schema)?.endpoint
                }
            })
   
            setPluginFunList(data)
            setHasMore(res.has_more)
        } catch (error) {
            console.log(error)
        }
        setLoading(false);
    };
    const handleCreatePrompt = async (value) => {
        setSchema('')
        setActionId('')
        setRadioValue('none')
        setAuthentication('')

        setDrawerTitle('Bulk Create Action')
        setOpenDrawer(value)
    }
 
    const columns= [...actionsTableColumn]
    columns.push({
        title: 'Actions',
        key: 'action',
        fixed: 'right',
        width: 118,
        render: (_, record) => (
            <Space size="middle">
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
    },)
    
 

    const handleEdit = async (val) => {
        setLoading(true)
        const res = await getActionsDetail(val.action_id)
        const formattedData = JSON.stringify(res.data.schema, null, 4);
        setDrawerTitle('Edit Action')
        setTipSchema(false)
        setActionId(val.action_id)
        setSchema(formattedData)
        if (res.data.authentication) {
            if (res.data.authentication.content) {
                setRadioValue('custom')
                setCustom(Object.keys(res.data.authentication.content)[0])
                setAuthentication(Object.values(res.data.authentication.content)[0] as string)
            } else {
                setRadioValue(res.data.authentication.type)
                setAuthentication(res.data.authentication.secret)
            }
        } else {
            setRadioValue('none')
            setAuthentication('')
        }
        setLoading(false)
        setOpenDrawer(true)
    }
    const handleRequest = async () => {

        if (!schema) {
            setTipSchema(true)
            return
        }
        let schemaStr = schema
        try {
            if (schema.endsWith(',')) {
                schemaStr = schema.slice(0, -1)
            } else {
                schemaStr = schema
            }
            JSON.parse(schemaStr)
        } catch (e) {
            toast.error('Invalid schema')
            return
        }
        setTipSchema(false)
        const commonData = {
            schema: JSON.parse(schemaStr),
            authentication: {
                type: radioValue,
                content:undefined,
                secret: undefined
            }
        };
        if (radioValue === 'custom') {
            commonData.authentication.content = { [custom]: Authentication };
        } else {
            if (radioValue === 'none') {
                commonData.authentication = undefined
            } else {
                commonData.authentication.secret = Authentication;
            }
        }
        try {
            if (actionId) {
                await updateActions(actionId, commonData);
            } else {
                await createActions(commonData);
            }
            const params = {
                limit: limit || 20
            }
            await fetchData(params);
            setUpdatePrevButton(true)
        } catch (error) {
            console.error(error);
            toast.error(error.response.data.error.message)
        }

        setOpenDrawer(false)
    }
    const onDeleteCancel = () => {
        setOpenDeleteModal(false)
    }
    const titleCase = (str) => {
        const newStr = str.slice(0, 1).toUpperCase() + str.slice(1).toLowerCase();
        return newStr;
    }
    const handleDelete = (val) => {
        setOpenDeleteModal(true)
        setDeleteValue(val.name)
        setActionId(val.action_id)
    }

    const handleCancel = () => {
        setOpenDrawer(false)
    }
    const handleSchemaChange = (e) => {
        setSchema(e.target.value)
        if (!e.target.value) {
            setTipSchema(true)
        } else {
            setTipSchema(false)
        }
    }
    const handleChildEvent = async (value) => {
        setUpdatePrevButton(false)
        setLimit(value.limit)
        await fetchData(value);
    }
    const onRadioChange = (e) => {
        setRadioValue(e.target.value)
    }

    const hangleChangeAuthorization = (e) => {
        setAuthentication(e.target.value)
    }
    const handleCustom = (e) => {
        setCustom(e.target.value)
    }
    const onDeleteConfirm = async () => {
        try {
            await deleteActions(actionId)
            const params = {
                limit: limit || 20,
            }
            await fetchData(params)
            setUpdatePrevButton(true)
        } catch (error) {
            console.log(error)
        }
        setOpenDeleteModal(false)
    }
    return (
        <div className={styles["actions"]}>
        
            <Spin spinning={loading} wrapperClassName={styles.spinloading}>
                <ModalTable updatePrevButton={updatePrevButton} name='action' id='action_id' hasMore={hasMore} ifSelect={false} columns={columns} dataSource={pluginFunList} onChildEvent={handleChildEvent} onOpenDrawer={handleCreatePrompt} />
            </Spin>
            <DeleteModal open={OpenDeleteModal} describe={`Are you sure you want to delete ${deleteValue}? This action cannot be undone and all integrations associated with the action will be affected.`} title='Delete Action' projectName={deleteValue} onDeleteCancel={onDeleteCancel} onDeleteConfirm={onDeleteConfirm} />
            <Drawer closeIcon={<img src={closeIcon} alt="closeIcon" className={styles['img-icon-close']} />} onClose={handleCancel} title={drawerTitle} placement="right" open={OpenDrawer} size='large' footer={<ModalFooterEnd handleOk={() => handleRequest()} onCancel={handleCancel} />}>
                <div className={styles['action-drawer']}>
                    <div className={styles['top']}>
                        <div className={styles['label']} style={{ marginTop: 0 }}>
                            <span className={styles['span']}> * </span>
                            <span>Schema</span>

                        </div>
                        {drawerTitle === 'Bulk Create Action' ?
                            <div className={styles['label-description']}>
                                The action JSON schema is compliant with
                                <a href="https://www.openapis.org/what-is-openapi" target="_blank" rel="noopener noreferrer" className={styles['href']}> the OpenAPI Specification</a>.
                                If there are multiple paths and methods in the schema, the service will create multiple
                                actions whose schema only has exactly one path and one method. We’ll use "operationId" and
                                "description" fields of each endpoint method as the name and description of the tool. Check
                                <a href="https://docs.tasking.ai/docs/guide/tool/action" target="_blank" rel="noopener noreferrer" className={styles['href']}> the documentation </a>
                                to learn more.
                            </div> :
                            <div className={styles['label-description']}> The action schema, Which is compliant with the OpenAPI
                                Specification. It should only have exactly one path and one method.</div>}

                        <TextArea className={styles['input-drawer']} value={schema}
                            onChange={handleSchemaChange} showCount maxLength={32768}></TextArea>
                        <div className={`desc-action-error ${tipSchema ? 'show' : ''}`}>Schema is required</div>

                    </div>
                    <div className={styles['bottom']}>
                        <div className={styles['label']}>
                            <span className={styles['span']}> * </span>
                            <span>Authentication</span>

                        </div>
                        <div className={styles['label-description']}>Authentication Type</div>
                        <Radio.Group onChange={onRadioChange} value={radioValue}>
                            <Radio value='none'>None</Radio>
                            <Radio value='basic'>Basic</Radio>
                            <Radio value='bearer'>Bearer</Radio>
                            <Radio value='custom'>Custom</Radio>
                        </Radio.Group>
                        {radioValue !== 'none' && <div style={{ display: 'flex', justifyContent: 'space-around', alignItems: 'center', margin: '15px 0' }}>
                            {radioValue !== 'custom' ? <span className={styles['desc-description']}>Authorization </span> : <Input placeholder='X-Custom' onChange={handleCustom} value={custom} style={{ width: '14%' }} />} <span className={styles['desc-description']}>:</span>  <Input prefix={<span style={{ color: '#999' }} >{radioValue !== 'custom' && titleCase(radioValue)}</span>} value={Authentication} placeholder='<Secret>' onChange={hangleChangeAuthorization} style={{ width: '83%' }}></Input>
                        </div>
                        }
                    </div>

                </div>
            </Drawer>
        </div>

    )
}
export default Actions