import { useState, useEffect, ChangeEvent } from 'react';
import closeIcon from '../../assets/img/x-close.svg'
import NoCollection from '../../assets/img/NO_COLLECTION.svg?react'
import NoTool from '../../assets/img/NO_TOOL.svg?react'
import { formatTime } from '../../utils/util'
import Paginations from '../../commonComponent/pagination/index'
import { Button, Modal, Radio, Select, Input, Spin } from 'antd';
import { PlusOutlined } from '@ant-design/icons';
import './modalSelect.scss'
import { useTranslation } from 'react-i18next';
import { getRetrievalList } from '../../axios/retrieval.ts'
import { getActionsList } from '../../axios/actions.ts'
function ModalSelect(prop: any) {
    const { t } = useTranslation()
    const { retrievalList, collectionSelectedId, hasMore, handleNewModal, id, nameTitle, title, newTitle, handleSelectedItem, retrievalSelectedList, retrievalModal, handleClose } = prop
    const [collectionId, setCollectionId] = useState(collectionSelectedId !== undefined ? collectionSelectedId : '')
    const [collectionItem, setCollectionItem] = useState('')
    const [inputValue, setInputValue] = useState('')
    const [contentLoading, setContentLoading] = useState(false)
    const [contentList, setContentList] = useState(retrievalList)
    const optionsEnd = [

        {
            value: 'All Records',
            label: 'All Records',
        },
        {
            value: 'Selected Records',
            label: 'Selected Records',
        }
    ]
    const empty: Record<string, any> = {
        collection_id: <NoCollection style={{ width: '158px', height: '100px' }} />,
        action_id: <NoTool style={{ width: '158px', height: '100px' }} />
    }
    useEffect(() => {
        setCollectionId(collectionSelectedId)
    }, [])
    useEffect(()=> {
        setContentList(retrievalList)
    },[retrievalList])
    const handleRetrievlCancel = () => {
        if (!collectionSelectedId) {
            setCollectionId('')
        } else {
            const collectionItems = retrievalList.find((item: any) => item[id] === collectionSelectedId)
            if (collectionItems) {
                handleSelectedItem(collectionItems)
            }
            setCollectionId('')

        }
        handleClose()
    }
    const handleNewRetrieval = () => {
        handleNewModal()
    }
    const handleRetrievlConfirm = () => {
        const collectionItems = retrievalList.find((item: any) => item[id] === collectionId)
        if (collectionItem || collectionItems) {
            handleSelectedItem(collectionItem || collectionItems)
        }
        setCollectionId('')
        handleClose()
    }
    const handleSelectCollection = (value: any) => {
        setCollectionItem(value)
        setCollectionId(value[id])
    }
  
    const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
        setInputValue(e.target.value)
    }
    const handleSearch = () => {
        const params = {
            limit: 20,
            offset: 0,
            id_search: inputValue
        }
        if (id === 'collection_id') {
            fetchSearchData(params)
        } else {
            fetchActionData(params)
        }
    }
    const handleSelectEndChange = (value: string) => {
        if (value === 'All Records') {
            setContentList(retrievalList)
        } else {
            const data = retrievalList.filter((item: any) => retrievalSelectedList.map((item1: any) => item1[id]).includes(item[id]))
            setContentList(data)
        }
    }
    const fetchSearchData = async (value: any) => {
        setContentLoading(true)
        const res: any = await getRetrievalList(value)
        const data = res.data.map((item: any) => {
            return {
                ...item,
                capacity1: item.num_chunks + '/' + item.capacity,
                key: item.collection_id
            }
        })
        setContentList(data);
        setContentLoading(false)
    }
    const fetchActionData = async (params: any) => {
        setContentLoading(true)
        const res: any = await getActionsList(params)
        const data = res.data.map((item: any) => {
            return {
                ...item,
                key: item.action_id,
            }
        })
        setContentList(data)
        setContentLoading(false)
    }
    return (
        <Modal onCancel={handleRetrievlCancel} centered className='collection-modal' width={1325} open={retrievalModal} closeIcon={<img src={closeIcon} alt="closeIcon" />} title={nameTitle} footer={[
            <div className='footer-group' style={{ display: 'flex', justifyContent: 'space-between' }} key='footer2'>
                <Button key="model" icon={<PlusOutlined />} onClick={handleNewRetrieval} className='cancel-button'>
                    {newTitle}
                </Button>
                <div>
                    <span className='select-record'>
                        {collectionId ? 1 : 0}   {t('projectItemSelected')}
                    </span>
                    <Button key="cancel" onClick={handleRetrievlCancel} className='cancel-button' style={{ marginRight: '8px' }}>
                        {t('cancel')}
                    </Button>
                    <Button key="submit" onClick={handleRetrievlConfirm} className='next-button'>
                        {t('confirm')}
                    </Button>
                </div>
            </div>
        ]
        }>
            <div className='retrieval-modal-content' >
                <div className={'header-table'}>
                    <Select defaultValue={'ID'} options={[
                        {
                            value: 'id',
                            label: 'ID',
                        }
                    ]} className={'select-name'} />
                    <Input placeholder='Enter ID' className={'input-name'} onChange={handleInputChange} value={inputValue} />
                    <Button className='cancel-button' onClick={handleSearch}>Search</Button>
                    <Select defaultValue="All Records" onChange={handleSelectEndChange} options={optionsEnd} className={'select-data'} />

                </div>
                {contentList.length === 0 ? <div className='no-data'>
                    {empty[id]}
                    <div className='desc'>{newTitle}</div>
                    <Button icon={<PlusOutlined />} className='prompt-button' onClick={handleNewRetrieval}>{newTitle.split(' ').map((word: any) => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}</Button>
                </div> :
                    <Spin spinning={contentLoading}>
                        <div className='content'>
                            {contentList.map((item: any, index: number) => (
                                <div className={`retrieval-single ${retrievalSelectedList.map((item1: any) => item1[id]).includes(item[id]) && 'selected-retrieval'} ${item[id] === collectionId && 'retrieval-selected-single'}`} key={index} onClick={retrievalSelectedList.map((item1: any) => item1[id]).includes(item[id]) ? undefined : () => handleSelectCollection(item)}>
                                    <div className='top'>
                                        <span className='name'>{item.name || `Untitled ${title}`}</span>
                                        {retrievalSelectedList.map((item1: any) => item1[id]).includes(item[id]) && item[id] !== collectionId ? <span className='text'>Selected</span> : <Radio checked={item[id] === collectionId}></Radio>}
                                    </div>
                                    <div className='desc'>
                                        {item.description}
                                    </div>
                                    <div className='bottom'>
                                        <span>{item[id]}</span>
                                        <span>{formatTime(item.created_timestamp)}</span>
                                    </div>
                                </div>
                            ))}
                        </div>
                        <Paginations hasMore={hasMore} />
                    </Spin>
                }

            </div>
        </Modal >
    );
}
export default ModalSelect;