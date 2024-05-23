import {
    Button,
    Modal
} from 'antd';
import closeIcon from '../../assets/img/x-close.svg'
import { PlusOutlined } from '@ant-design/icons';
import { useTranslation } from "react-i18next";
import { useEffect, useState, useRef } from 'react'
import ModelModal from '../modelModal/index'
import { ChildRefType } from '../../constant/index.ts'
import ModalTable from '../modalTable/index'
import { getModelsList } from '../../axios/models.ts'
import { useDispatch } from 'react-redux';
import { fetchModelsData } from '../../Redux/actions.ts'
import { valueLimit, } from '@/constant/assistant.ts'
import CommonComponents from '../../contents/index'
import styles from './modelComponent.module.scss'
function ModelComponent(props: any) {
    const { t } = useTranslation();
    const dispatch = useDispatch();
    const { modelsTableColumn,  } = CommonComponents();
    const [recordsSelected, setRecordsSelected] = useState([])
    const [confirmLoading, setConfirmLoading] = useState(false)
    const [modelOne, setModelOne] = useState(false);
    const childRef = useRef<ChildRefType | null>(null);
    const [updateModelPrevButton, setUpdateModelPrevButton] = useState(false)
    const [options, setOptions] = useState([])
    const [hasModelMore, setHasModelMore] = useState(false)
    const [modelLimit, setModelLimit] = useState(20)
    const [selectedRows, setSelectedRows] = useState<any[]>([])
    const [detailSelectedRowInfo, setDetailSelectedRowInfo] = useState<any>({})
    useEffect(() => {
        fetchModelsList()
    }, [])
    useEffect(() => {
        setSelectedRows(props.defaultSelectedData || [])
    }, [props.defaultSelectedData])
    const handleCreateModelId = async () => {
        await setModelOne(true)
        childRef.current?.fetchAiModelsList()

    }
    const handleSetModelConfirmOne = () => {
        setModelOne(false)
        setUpdateModelPrevButton(true)
    }
    const handleModalCancel = () => {
        setModelOne(false)
    }
    const fetchModelsList = async (value?: any, type?: string) => {
        if (type) {
            dispatch(fetchModelsData(20) as any);
        }
        const params = {
            limit: modelLimit || 20,
            ...value
        }
        try {
            const res: any = await getModelsList(params, 'chat_completion')
            const data = res.data.map((item: any) => {
                return {
                    ...item,
                    key: item.model_id
                }
            })
            setOptions(data)
            setHasModelMore(res.has_more)
        } catch (error) {
            console.log(error)
        }
    }
    const handleModalClose = () => {
       props.handleCloseModal()
    }
    const handleChildModelEvent = async (value: valueLimit) => {
        setModelLimit(value.limit)
        setUpdateModelPrevButton(false)
        await fetchModelsList(value)
    }
    const handleRecordsSelected = (value: any, selectedRows: any[]) => {
        setRecordsSelected(value)
        setDetailSelectedRowInfo(selectedRows)
        const tag = selectedRows.map(item => (item.name + '-' + item.model_id))
        setSelectedRows(tag)
    }
    const handleModalConfirm =async () => {
        setConfirmLoading(true)
        await props.handleModalConfirm(...detailSelectedRowInfo)
        setConfirmLoading(false)
    }
    return (
        <>
            <Modal closeIcon={<img src={closeIcon} alt="closeIcon" className={styles['img-icon-close']} />} centered onCancel={handleModalClose} footer={[
                <div className='footer-group' key='footer1'>
                    <Button key="model" icon={<PlusOutlined />} onClick={handleCreateModelId} className='cancel-button'>
                        {t('projectNewModel')}
                    </Button>
                    <div>
                        <span className='select-record'>
                            {recordsSelected.length}  {recordsSelected.length > 1 ? `${t('projectItemsSelected')}` : `${t('projectItemSelected')}`}
                        </span>
                        <Button key="cancel" onClick={handleModalClose} className={`cancel-button ${styles.cancelButton}`}>
                            {t('cancel')}
                        </Button>
                        <Button key="submit" onClick={handleModalConfirm} className='next-button' loading={confirmLoading}>
                            {t('confirm')}
                        </Button>
                    </div>
                </div>
            ]} title={t('projectSelectModel')} open={props.modalTableOpen} width={1000} className={`modal-inner-table ${styles['retrieval-model']}`}>
                <ModalTable onOpenDrawer={handleCreateModelId} title='New model' name="model" updatePrevButton={updateModelPrevButton} defaultSelectedRowKeys={selectedRows} handleRecordsSelected={handleRecordsSelected} ifSelect={true} columns={modelsTableColumn} hasMore={hasModelMore} id='model_id' dataSource={options} onChildEvent={handleChildModelEvent}></ModalTable>
            </Modal>
            <ModelModal type='chat_completion' ref={childRef} open={modelOne} handleSetModelConfirmOne={handleSetModelConfirmOne} handleSetModelOne={handleModalCancel} getOptionsList={fetchModelsList} modelType='chat_completion'></ModelModal>
        </>


    );
}
export default ModelComponent;