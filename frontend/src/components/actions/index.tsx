import {
    Space, Drawer, Spin, Tooltip
} from 'antd';
import styles from './action.module.scss'
import { useState, useEffect,useRef } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchActionData } from '../../Redux/actions';
import { getFirstMethodAndEndpoint } from '../../utils/util.ts'
import { getActionsList, updateActions, deleteActions, createActions, getActionsDetail } from '../../axios/actions.ts'
import closeIcon from '../../assets/img/x-close.svg'
import DeleteModal from '../deleteModal/index.tsx'
import ModalTable from '../modalTable/index'
import ModalFooterEnd from '../modalFooterEnd/index'
import EditIcon from '../../assets/img/editIcon.svg?react'
import DeleteIcon from '../../assets/img/deleteIcon.svg?react'
import tooltipTitle from '../../contents/tooltipTitle.tsx'
import CommonComponents from '../../contents/index.tsx'
import ApiErrorResponse from '@/constant/index'
import { commonDataType } from '@/constant/assistant.ts'
import ActionDrawer from '../actionDrawer/index.tsx';
import { toast } from 'react-toastify';
import { useTranslation } from "react-i18next";
function Actions() {
    const { t } = useTranslation();
    const { actionLists } = useSelector((state: any) => state.action);
    const dispatch = useDispatch()
    const actionDrawerRef = useRef(null)
    const { actionsTableColumn } = CommonComponents();
    const { tooltipEditTitle, tooltipDeleteTitle } = tooltipTitle();
    const [loading, setLoading] = useState(false);
    const [pluginFunList, setPluginFunList] = useState([])
    const [deleteValue, setDeleteValue] = useState('')
    const [updatePrevButton, setUpdatePrevButton] = useState(false)
    const [OpenDrawer, setOpenDrawer] = useState(false)
    const [drawerTitle, setDrawerTitle] = useState('')
    const [OpenDeleteModal, setOpenDeleteModal] = useState(false)
    const [radioValue, setRadioValue] = useState('none')
    const [Authentication, setAuthentication] = useState<string>('')
    const [schema, setSchema] = useState('')
    const [custom, setCustom] = useState('')
    const [limit, setLimit] = useState(20)
    const [hasMore, setHasMore] = useState(false)
    const [actionId, setActionId] = useState('')
    const [tipSchema, setTipSchema] = useState(false)
    useEffect(() => {
        if (actionLists.data.length > 0) {
            const data = actionLists.data.map((item: any) => {
                return {
                    ...item,
                    key: item.action_id,
                    method: getFirstMethodAndEndpoint(item.openapi_schema)?.method,
                    endpoint: getFirstMethodAndEndpoint(item.openapi_schema)?.endpoint
                }
            })
            setPluginFunList(data)
            setHasMore(actionLists.has_more)
        } else {
            setPluginFunList([])
        }
    }, [actionLists])
    const onhandleTipError = (value: boolean) => {
        setTipSchema(value)
    }
    const fetchData = async (params: any) => {
        setLoading(true);
        try {
            const res: any = await getActionsList(params)
            const data = res.data.map((item: any) => {
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
    const handleCreatePrompt = async (value: boolean) => {
        setSchema('')
        setActionId('')
        setRadioValue('none')
        setAuthentication('')
        setDrawerTitle(`${t('projectActionEditTitle')}`)
        setOpenDrawer(value)
        setTipSchema(false)
    }
    const columns = [...actionsTableColumn]
    columns.push({
        title: `${t('projectColumnActions')}`,
        key: 'action',
        fixed: 'right',
        width: 118,
        render: (__: string, record: any) => (
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
    const handleEdit = async (val: any) => {
        setLoading(true)
        setTipSchema(false)
        const res = await getActionsDetail(val.action_id)
        const formattedData = JSON.stringify(res.data.openapi_schema, null, 4);
        setDrawerTitle(`${t('projectToolsEditAction')}`)
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
            toast.error(`${t('projectToolsActionInvalidSchema')}`)
            return
        }
        const commonData: commonDataType = {
            openapi_schema: JSON.parse(schemaStr),
            authentication: {
                type: radioValue,
                content: undefined,
                secret: undefined
            }
        };
        if (radioValue === 'custom') {
            if (commonData.authentication) {
                commonData.authentication.content = { [custom]: Authentication };
            }
        } else {
            if (radioValue === 'none') {
                (commonData.authentication as any).type = 'none'
            } else {
                if (commonData.authentication) {
                    commonData.authentication.secret = Authentication;
                }
            }
        }
        try {
            if (actionId) {
                (actionDrawerRef.current as any).getResetButtonState() && (commonData.authentication = undefined) 
                await updateActions(actionId, commonData);
            } else {
                await createActions(commonData);
            }
            const limit1: number = limit || 20
            dispatch(fetchActionData(limit1) as any);
            setUpdatePrevButton(true)
        } catch (error) {
            console.error(error);
            const apiError = error as ApiErrorResponse;
            const messageError: string = apiError.response.data.error.message;
            toast.error(messageError)
        }

        setOpenDrawer(false)
    }
    const onDeleteCancel = () => {
        setOpenDeleteModal(false)
    }

    const handleDelete = (val: any) => {
        setOpenDeleteModal(true)
        setDeleteValue(val.name)
        setActionId(val.action_id)
    }

    const handleCancel = () => {
        setOpenDrawer(false)
    }
    const handleSchemaChange = (value: string) => {
        setSchema(value)
    }
    const handleChildEvent = async (value: Record<string, any>) => {
        setUpdatePrevButton(false)
        setLimit(value.limit)
        await fetchData(value);
    }
    const onRadioChange = (value: string) => {
        setRadioValue(value)
    }

    const hangleChangeAuthorization = (value: string) => {
        setAuthentication(value)
    }
    const handleCustom = (value: string) => {
        setCustom(value)
    }
    const onDeleteConfirm = async () => {
        try {
            await deleteActions(actionId)
            const limit1: number = limit || 20
            dispatch(fetchActionData(limit1) as any);
            setUpdatePrevButton(true)
        } catch (error) {
            console.log(error)
        }
        setOpenDeleteModal(false)
    }
    return (
        <div className={styles["actions"]}>

            <Spin spinning={loading} wrapperClassName={styles.spinloading}>
                <ModalTable title='New action' loading={loading} updatePrevButton={updatePrevButton} name='action' id='action_id' hasMore={hasMore} ifSelect={false} columns={columns} dataSource={pluginFunList} onChildEvent={handleChildEvent} onOpenDrawer={handleCreatePrompt} />
            </Spin>
            <DeleteModal open={OpenDeleteModal} describe={`${t('deleteItem')} ${deleteValue}? ${t('projectActionDeleteDesc')}`} title='Delete Action' projectName={deleteValue} onDeleteCancel={onDeleteCancel} onDeleteConfirm={onDeleteConfirm} />
            <Drawer className={styles.drawerCreate} closeIcon={<img src={closeIcon} alt="closeIcon" className={styles['img-icon-close']} />} onClose={handleCancel} title={drawerTitle} placement="right" open={OpenDrawer} size='large' footer={<ModalFooterEnd handleOk={() => handleRequest()} onCancel={handleCancel} />}>
                <ActionDrawer ref={actionDrawerRef} actionId={actionId} showTipError={tipSchema} onhandleTipError={onhandleTipError} schema={schema} onSchemaChange={handleSchemaChange} open={OpenDrawer} onRadioChange={onRadioChange} onChangeCustom={handleCustom} onChangeAuthentication={hangleChangeAuthorization} radioValue={radioValue} custom={custom} Authentication={Authentication} />
            </Drawer>
        </div>

    )
}
export default Actions