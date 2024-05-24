import { useState, useEffect, useRef, ChangeEvent } from 'react';
import closeIcon from '../../assets/img/x-close.svg'
import ModalFooterEnd from '../modalFooterEnd/index'
import { RightOutlined, PlusOutlined } from '@ant-design/icons';
import { toast } from 'react-toastify';
import { getModelsList } from '../../axios/models'
import {  useDispatch } from 'react-redux';

import ModelModal from '../modelModal/index'
import { fetchModelsData } from '../../Redux/actions';

import {
    Input, Select, Modal, Button
} from 'antd';
import { createCollectionType } from '@/constant/createCollection.ts'
import { createRetrieval } from '../../axios/retrieval';
import ModalTable from '../modalTable/index';
import styles from './createCollection.module.scss'
import CommonComponents from '../../contents/index'
import ApiErrorResponse, { ChildRefType } from '../../constant/index.ts'
import { useTranslation } from "react-i18next";
function CreateCollection(props: createCollectionType) {
    const { t } = useTranslation();
    const dispatch = useDispatch();
    const { modelsTableColumn } = CommonComponents();
    const { OpenDrawer, handleModalCloseOrOpen, handleFetchData } = props
    const [drawerName, setDrawerName] = useState('')
    const [descriptionText, setDescriptionText] = useState('')
    const [selectedRows, setSelectedRows] = useState<string[]>([])
    const [selectModelName, setSelectModelName] = useState<string | undefined>(undefined)
    const [selectValue, setSelectValue] = useState(1000)
    const [modelOne, setModelOne] = useState(false);
    const [recordsSelected, setRecordsSelected] = useState<string[]>([])
    const [updatePrevButton, setUpdatePrevButton] = useState(false)
    const [defaultSelectedRowKeys, setDefaultSelectedRowKeys] = useState([])
    const [modelHasMore, setModelHasMore] = useState(false)
    const [options, setOptions] = useState([])
    const childRef = useRef<ChildRefType | null>(null);
    useEffect(() => {
        const params = {
            limit: 20,
        }
        fetchModelsList(params)
    }, []);
    const [modalTableOpen, setModalTableOpen] = useState(false)
    const fetchModelsList = async (params: Record<string, string | number>,type?: string) => {
        if(type) {
            dispatch(fetchModelsData(20) as any);
        }
        try {
            const res: any = await getModelsList(params, 'text_embedding')
            const data = res.data.map((item: any) => {
                return {
                    ...item,
                    key: item.model_id,
                }
            })
            setModelHasMore(res.has_more)
            setOptions(data)
        } catch (error) {
            console.log(error)
        }
    }
    const handleCancel = () => {
        handleModalCloseOrOpen(false)
        setDrawerName('')
        setDescriptionText('')
        setSelectedRows([])
        setSelectModelName(undefined)
        setSelectValue(1000)
        setRecordsSelected([])
        setDefaultSelectedRowKeys([])
        setUpdatePrevButton(false)
    }
    const handleNameChange = (e: ChangeEvent<HTMLInputElement>) => {
        setDrawerName(e.target.value)
    }
    const handleSelectModelId = () => {
        setRecordsSelected([])
        setModalTableOpen(true)
        setUpdatePrevButton(false)
    }
    const handleSelectValue = (value: number) => {
        setSelectValue(value)
    }
    const handleRequest = async () => {
        if (!selectedRows || !selectValue) {
            return toast.error(`${t('missingRequiredParameters')}`)
        }
        try {
            const params = {
                capacity: Number(selectValue),
                embedding_model_id: selectedRows[0].slice(-8),

                name: drawerName || '',
                description: descriptionText || '',
                metadata: {}
            }
            await createRetrieval(params)
            handleFetchData()
            setDrawerName('')
            setDescriptionText('')
            setSelectedRows([])
            setSelectModelName(undefined)
            setSelectValue(1000)
            setRecordsSelected([])
            setDefaultSelectedRowKeys([])
            handleModalCloseOrOpen(false)
            setUpdatePrevButton(true)

        } catch (error) {
            console.log(error)
            const apiError = error as ApiErrorResponse;
            const Response: string = apiError.response.data.error.message;
            toast.error(Response)
        }
    }
    const handleModalCancel = () => {
        setModelOne(false)
    }
    const handleSetModelConfirmOne = () => {
        setModelOne(false)
        setUpdatePrevButton(true)
    }
    const handleModalClose = () => {
        setModalTableOpen(false)
        setUpdatePrevButton(false)
        setDefaultSelectedRowKeys([])
        setSelectModelName(undefined)
        setSelectedRows([])
    }
    const handleModalCloseConfirm = () => {
        console.log(selectedRows)
        if (selectedRows.length) {
            let str = selectedRows[0];
            let index = str.lastIndexOf('-');
            if (index !== -1) {
                let result = str.substring(0, index);
                setSelectModelName(result)
            }
        }
        setModalTableOpen(false)

    }
    const handleRecordsSelected = (value: string[], selectedRows: any[]) => {
        setRecordsSelected(value)
        const tag = selectedRows.map(item => (item.name + '-' + item.model_id))
        if (value.length === 0) {
            setSelectedRows([])
            setSelectModelName(undefined)
        } else {
            setSelectedRows(tag)
            // setSelectModelName(selectedRows.map(item => (item.name))[0])
        }
    }
    const handleCreateModelId = async () => {
        setModelOne(true)
        childRef.current?.fetchAiModelsList()
    }
    const handleChildModelEvent = async (value: any) => {
        await fetchModelsList(value)
    }
    return (
        <>
            <Modal zIndex={10000}  onCancel={handleCancel} className={styles['create-collection']} width={1000} centered closeIcon={<img src={closeIcon} alt="closeIcon" className='img-icon-close' />} title='Create Collection' open={OpenDrawer} footer={<ModalFooterEnd handleOk={() => handleRequest()} onCancel={handleCancel} />}>
                <div className={styles['drawer-retrieval']}>
                    <div className={styles['name-prompt']}>
                        {t('projectModelColumnName')}
                    </div>
                    <Input value={drawerName} onChange={handleNameChange} className={styles['input']}></Input>
                    <div className={styles['desc-prompt']}>
                        {t('projectAssistantsColumnDescription')}
                    </div>
                    <div className={styles['label-desc']}>
                    {t('projectRetrievalCreateDesc')}
                    </div>
                    <Input.TextArea className={styles['input']} autoSize={{ minRows: 3, maxRows: 10 }} showCount
                         placeholder={t('projectRecordEnterDescription')}
                        value={descriptionText}
                        onChange={(e) => setDescriptionText(e.target.value)}
                        maxLength={200} />
                    <div className={styles['hr']}></div>
                    <div className={styles['label']}>
                        <span className={styles['span']}>*</span>
                        <span>{t('projectRetrievalEmbeddingModel')}</span>
                    </div>
                    <div className={styles['label-desc']}>{t('projectRetrievalEmbeddingModelDesc')}</div>
                    <Select
                       placeholder={t('projectSelectModel')}
                        open={false}
                        mode="multiple"
                        className={styles['input']}
                        style={{caretColor: 'transparent'}}
                        suffixIcon={<RightOutlined />}
                        maxTagCount={2} removeIcon={null}
                        value={selectModelName} onClick={handleSelectModelId}
                    >

                    </Select>
                    <div className={styles['hr']}></div>

                    <div className={styles['label']}>
                        <span className={styles['span']}>*</span>
                        <span>{t('projectRetrievalColumnCapacity')}</span>
                    </div>
                    <div className={styles['label-desc']}>
                    {t('projectRetrievalCapacityDesc')}
                    </div>
                    <Select
                       placeholder={t('projectRetrievalCapacityPlaceholder')}
                        onChange={handleSelectValue}
                        value={selectValue}
                        className={styles['input']}
                        options={[
                            {
                                value: '1000',
                                label: '1000 chunks',
                            },
                        ]} />
                </div>
            </Modal>
            <Modal zIndex={10001} closeIcon={<img src={closeIcon} alt="closeIcon" className={styles['img-icon-close']} />} onCancel={handleModalClose} centered footer={[
                <div className='footer-group' key='footer'>
                    <Button key="model" icon={<PlusOutlined />} onClick={handleCreateModelId} className='cancel-button'>
                        {t('projectNewModel')}
                    </Button>
                    <div>
                        <span className='select-record'>
                            {recordsSelected.length} {recordsSelected.length > 1 ? `${t('projectItemsSelected')}` : `${t('projectItemSelected')}`}
                        </span>
                        <Button key="cancel" onClick={handleModalClose} className={`cancel-button ${styles.cancelButton}`}>
                            {t('cancel')}
                        </Button>
                        <Button key="submit" onClick={handleModalCloseConfirm} className='next-button'>
                            {t('confirm')}
                        </Button>
                    </div>

                </div>

            ]} title={t('projectSelectModel')} open={modalTableOpen} width={1000} className={`modal-inner-table ${styles['retrieval-model']}`}>
                <ModalTable title='New model' name="model" onOpenDrawer={handleCreateModelId} updatePrevButton={updatePrevButton} defaultSelectedRowKeys={defaultSelectedRowKeys} handleRecordsSelected={handleRecordsSelected} ifSelect={true} columns={modelsTableColumn} hasMore={modelHasMore} id='model_id' dataSource={options} onChildEvent={handleChildModelEvent}></ModalTable>
            </Modal>
            <ModelModal type='text_embedding'  getOptionsList={fetchModelsList} ref={childRef} open={modelOne} handleSetModelOne={handleModalCancel} modelType='text_embedding' handleSetModelConfirmOne={handleSetModelConfirmOne}></ModelModal>
        </>
    );
}
export default CreateCollection;