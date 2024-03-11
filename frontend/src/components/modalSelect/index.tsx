import { useState, useEffect } from 'react';
import closeIcon from '../../assets/img/x-close.svg'
import NoCollection from '../../assets/img/NO_COLLECTION.svg?react'
import NoTool from '../../assets/img/NO_TOOL.svg?react'
import { formatTime } from '../../utils/util'
import Paginations from '../pagination/index'
import { Button, Modal, Radio } from 'antd';
import { PlusOutlined } from '@ant-design/icons';
import './modalSelect.scss'
import { useTranslation } from 'react-i18next';
function ModalSelect(prop: any) {
    const { t } = useTranslation()
    const { retrievalList, collectionSelectedId, hasMore, handleNewModal, id, nameTitle, newTitle, handleSelectedItem, retrievalSelectedList, retrievalModal, handleClose } = prop
    const [collectionId, setCollectionId] = useState(collectionSelectedId !== undefined ? collectionSelectedId : '')
    const [collectionItem, setCollectionItem] = useState('')
    const empty: Record<string, any> = {
        collection_id: <NoCollection style={{ width: '158px', height: '100px' }} />,
        action_id: <NoTool style={{ width: '158px', height: '100px' }} />
    }
    useEffect(() => {
        setCollectionId(collectionSelectedId)
    }, [])
    const handleRetrievlCancel = () => {
        setCollectionId('')
        handleClose()
    }
    const handleNewRetrieval = () => {
        handleNewModal()
    }
    const handleRetrievlConfirm = () => {
        const collectionItems = retrievalList.find((item: any) => item[id] === collectionId)
        handleSelectedItem(collectionItem || collectionItems)
        setCollectionId('')
        handleClose()
    }
    const handleSelectCollection = (value: any) => {
        setCollectionItem(value)
        setCollectionId(value[id])
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
            {retrievalList.length === 0 ? <div className='no-data'>
                {empty[id]}
                <div className='desc'>{newTitle}</div>
                <Button icon={<PlusOutlined />} className='prompt-button' onClick={handleNewRetrieval}>{newTitle.split(' ').map((word:any)=>word.charAt(0).toUpperCase()+ word.slice(1)).join(' ')}</Button>
            </div> : <div className='retrieval-modal-content' >
                <div className='content'>
                    {retrievalList.map((item: any, index: number) => (
                        <div className={`retrieval-single ${retrievalSelectedList.map((item1: any) => item1[id]).includes(item[id]) && 'selected-retrieval'} ${item[id] === collectionId && 'retrieval-selected-single'}`} key={index} onClick={retrievalSelectedList.map((item1: any) => item1[id]).includes(item[id]) ? undefined : () => handleSelectCollection(item)}>
                            <div className='top'>
                                <span className='name'>{item.name}</span>
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
            </div>}
        </Modal >
    );
}
export default ModalSelect;