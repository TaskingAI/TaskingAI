import { Input, Button, Select, InputNumber } from 'antd';
import './drawerAssistant.scss'
import ModalSelect from '../modalSelect/index'
import DeleteInputIcon from '../../assets/img/deleteInputIcon.svg?react'
import { PlusOutlined, RightOutlined } from '@ant-design/icons';
import { ChangeEvent, useImperativeHandle, forwardRef } from 'react';
import { useTranslation } from 'react-i18next';
import { useState, useEffect } from 'react';
import PluginComponent from '../pluginComponent/index'
const DrawerAssistant = forwardRef((props: any, ref: any) => {
    const { t } = useTranslation(['components/drawerAssistant/index', 'common'])
    const { handleAddPromptInput, handleNewBundle,modelName,drawerTitle,openDrawer,selectedPluginGroup,selectedActionsSelected, handleNewActionModal, topk, maxTokens, bundilesList, handleMaxToken, handleToks, handleNewCollection, selectedCollectionList, collectionHasMore, actionHasMore, retrievalList, actionList, handleMemoryChange1, handleRetrievalConfigChange1, retrievalConfig, inputValue1, memoryValue, handleInputValueOne, handleInputValueTwo, inputValue2, selectedActionsRows, drawerName, systemPromptTemplate, handleDeletePromptInput, handleInputPromptChange, handleSelectModelId, handleChangeName, drawerDesc, handleDescriptionChange } = props
    const [collectionModal, setCollectionModal] = useState(false)
    const [actionModal, setActionModal] = useState(false)
    const [pluginModal, setPluginModal] = useState(false)
   
    const [pluginIndex, setPluginIndex] = useState(0)
    const [collectionSelectedId, setCollectionSelectedId] = useState('')
    const [pluginSelectedId, setPluginSelectedId] = useState('')
    const [bundleSelectedItem, setBundleSelectedItem] = useState({})
    const [actionSelectedId, setActionSelectedid] = useState('')
    const [selectedPluginList, setSelectedPluginList] = useState(selectedPluginGroup)
    const [retrievalSelectedList, setRetrievalSelectedList] = useState<any[]>(selectedCollectionList)
    const [actionSelectedList, setActionSelectedList] = useState<any[]>(selectedActionsSelected)
    const [pluginActionList, setPluginActionList] = useState<any[]>(selectedActionsRows)
    const [isShowRetrievalConfig, setIsShowRetrievalConfig] = useState(false)
    const [retrievalFormList, setRetrievalFormList] = useState<any[]>(selectedCollectionList.map((item: any) => ({ collection_id: item.collection_id,name:item.name })) || [''])
    const [indexCollection, setIndexCollection] = useState(0)
    const [indexAction, setIndexAction] = useState(0)

    useEffect(() => {
        const data = retrievalFormList.filter((item: any) => Boolean(item.collection_id)).length
        if (data === 0) {
            setIsShowRetrievalConfig(false)
            handleToks(3)
            handleMaxToken(4096)
            handleRetrievalConfigChange1('user_message')
        } else {
            setIsShowRetrievalConfig(true)
        }
    }, [retrievalFormList])
    useEffect(() => {
        setSelectedPluginList(selectedPluginGroup)
    }, [selectedPluginGroup])
    useEffect(() => {
        if(drawerTitle === t('createAssistant', {ns: 'common'}) && openDrawer) {
            setSelectedPluginList([]) 
            setActionSelectedList([])
            setRetrievalSelectedList([])
            setPluginActionList([])
            setRetrievalFormList([''])
        } else if(drawerTitle === t('editAssistant', {ns: 'common'}) && openDrawer) {
            const retrievalFormList1 = selectedCollectionList.map((item: any) => ({ collection_id: item.collection_id,name: item.name })).length > 0 ? selectedCollectionList.map((item: any) => ({ collection_id: item.collection_id,name: item.name })) : ['']
            setRetrievalSelectedList(retrievalFormList1)
            setRetrievalFormList(retrievalFormList1)
            setSelectedPluginList(selectedPluginGroup)
            setActionSelectedList(selectedActionsSelected)
            setPluginActionList(selectedActionsRows)
        }
    }, [drawerTitle,openDrawer])
    useEffect(() => {
    
        setPluginActionList(selectedActionsRows.length ? selectedActionsRows : [{ type: 'plugin', value: '' }])

    }, [selectedActionsRows])
    useImperativeHandle(ref, () => ({
        getRetrievalSelectedList: () => retrievalSelectedList.map((item) => item?.collection_id),
        getActionSelectedList: () => pluginActionList,
    }));
    const handleChangeNames = (e: ChangeEvent<HTMLInputElement>) => {
        handleChangeName(e.target.value)
    }
    const handleSelectedItem = (value: any) => {
        const data = value
        if(!data.name) {
          data.name = t('untitledCollection', {ns: 'common'})
        }
        setRetrievalSelectedList((prev) => {
            const newRetrievalSelectedList = [...prev, data]
            return newRetrievalSelectedList
        })
        setRetrievalFormList((prev) => {
            const newRetrievalFormList = [...prev]
            newRetrievalFormList[indexCollection] = data
            return newRetrievalFormList
        })
    }
    const handleActionItem = (value: any) => {
        setActionSelectedList((prev) => {
            const newActionSelectedList = [...prev, value]
            return newActionSelectedList
        })
        setPluginActionList((prev) => {
            const item = { type: 'action', value: value.action_id,name: value.name }

            prev[indexAction] = item
            return prev
        })
    }
    const handleCancelCollectionModal = () => {
        setCollectionModal(false)
    }
    const handleCancelActionModal = () => {
        setActionModal(false)
    }
    const handleInputValue1 = (value: number) => {
        handleInputValueOne(value)
    }
    const handleInputValue2 = (value: number) => {
        handleInputValueTwo(value)
    }
    const handleDescriptionChanges = (e: ChangeEvent<HTMLInputElement>) => {
        handleDescriptionChange(e.target.value)
    }
    const handleSelectModelIds = () => {
        handleSelectModelId(true)
    }
    const handleInputPromptChanges = (index: number, newValue: any) => {
        handleInputPromptChange(index, newValue)
    }
    const handleDeletePromptInputs = (index: number) => {
        handleDeletePromptInput(index)
    }

    const handleSelectActions = (index: any, actionId: string) => {
        if (actionId) {
            setActionSelectedid(actionId)
            setActionSelectedList((prev) => {
                const newRetrievalSelectedList = prev.filter(item => item.action_id !== actionId)
                return newRetrievalSelectedList
            })
        } else {
            setActionSelectedid('')
        }
        setIndexAction(index)
        setActionModal(true)
    }
    const handleNewCollection1 = () => {
        handleNewCollection(true)
    }
    const handleNewAction = () => {
        handleNewActionModal(true)
    }
    const handleSelectPlugins = (index: any,value:string) => {
        if(value) {
            setPluginSelectedId(value.split('/')[1])
            setBundleSelectedItem({bundle_id: value.split('/')[0]})
            setSelectedPluginList((prev: any) => {
                const newActionFormList = prev.filter((item: any) => item !== value.split('/')[1])
                return newActionFormList
            })
        }else {
            setPluginSelectedId('')
        }
        setPluginIndex(index)
        setPluginModal(true)
    }
    const handleAddPrompt = () => {
        handleAddPromptInput()
    }
    const handleAddRetrieval = () => {
        setRetrievalFormList((prev) => {
            const newRetrievalFormList = [...prev, '']
            return newRetrievalFormList
        })
    }
    const handleDeleteRetrieval = (id: string,index:number) => {
        setRetrievalFormList((prev) => {
            if (!id) {
                prev.splice(index,1)
                return [...prev];
            } else {
                const newRetrievalFormList = prev.filter(item => item.collection_id !== id)
                return newRetrievalFormList
            }
        
        })
        setRetrievalSelectedList((prev) => {
            const newRetrievalSelectedList = prev.filter(item => item.collection_id !== id)
            return newRetrievalSelectedList
        })
    }
    const handleDeleteTool = (data: any,index:number) => {
        setPluginActionList((prev) => {
            if(!data.value) {
                 prev.splice(index,1)
                return [...prev];
            }else {
                const newPluginActionList = prev.filter(item => item.value !== data.value)
                return newPluginActionList
            }
         
        })
        if(data.type === 'action') {
            setActionSelectedList((prev) => {
                const newActionSelectedList = prev.filter(item => item.action_id !== data.value)
                return newActionSelectedList
            })
        }
        if(data.type === 'plugin') {
            setSelectedPluginList((prev: any) => {
                const newPluginSelectedList = prev.filter((item: any) => item !== data.value.split('/')[1])
                return newPluginSelectedList
            })
        }
      
    }
    const handleAddTool = () => {
        setPluginActionList((prev) => {
            const newRetrievalFormList = [...prev, { type: 'plugin', value: '' }]
            return newRetrievalFormList
        })
    }
    const handleClosePluginModal = () => {
        setPluginModal(false)
    }
    const handleCollectionModal = (index: number, collectionId: string) => {
        setIndexCollection(index)
        setCollectionModal(true)
        if (collectionId) {
            setCollectionSelectedId(collectionId)
            setRetrievalSelectedList((prev) => {
                const newRetrievalSelectedList = prev.filter(item => item.collection_id !== collectionId)
                return newRetrievalSelectedList
            })
        } else {
            setCollectionSelectedId('')

        }
    }
    const handleMemoryChange = (value: string) => {
        handleMemoryChange1(value)
    }
    const handleRetrievalConfigChange = (value: string) => {
        handleRetrievalConfigChange1(value)
    }
    const handlePluginConfirm = (pluginId: any, data: any) => {
        const pluginName = data.plugins.find((item:any)=>item.plugin_id === pluginId).name
        setSelectedPluginList((prev: any) => {
            const newActionFormList: any = [...prev, pluginId]
            return newActionFormList
        })
        setPluginActionList((prev) => {
            const newActionFormList = [...prev]
            const item = { type: 'plugin', value: `${data.bundle_id}/${pluginId}`,name: `${data.name}/${pluginName}` }
            newActionFormList[pluginIndex] = item
            return newActionFormList
        })
    }
    const handleMaxTokens = (value: number) => {
        handleMaxToken(value)
    }
    const handleTopk = (value: number) => {
        handleToks(value)
    }
    const handleToolsChange = (value: string = 'plugin', index: any, item1: any) => {
        setSelectedPluginList((prev: any) => {
            const data = prev.filter((item: any) => item !== item1.value)
            return data
        })
        setPluginActionList(prev => {
            const newActionFormList = [...prev]
            newActionFormList[index].type = value
            newActionFormList[index].value = ''
            return newActionFormList
        })
    }
    const handleCreateBundle = () => {
        handleNewBundle()
    }
    return (
        <div className='drawer-assistant'>
            <div className='left-assistant'>
                <div className='basic-information'>
                    {t('basicInformation')}
                </div>
                <div className='name-prompt'>
                    {t('name', {ns: 'common'})}
                </div>
                <Input value={drawerName} onChange={handleChangeNames} className='input' placeholder={t('enterName', {ns: 'common'})}></Input>
                <div className='label'>
                    {t('description', {ns: 'common'})}
                </div>
                <div className='label-desc'>
                    {t('descriptionDesc')}
                </div>
                <Input.TextArea placeholder={t('enterDescription', {ns: 'common'})} className='input' autoSize={{ minRows: 3, maxRows: 10 }} showCount
                    maxLength={200} value={drawerDesc} onChange={(e) => handleDescriptionChanges(e as any)} />
                <div className='hr'></div>
                <div className='label'>
                    <span className='span'>*</span>
                    <span>{t('langModel', {ns: 'common'})}</span>
                </div>
                <div className='label-desc'>{t('langModelSelect')}</div>
                <Select
                    placeholder={t('projectSelectModel')}
                    open={false}
                    mode="multiple"
                    suffixIcon={<RightOutlined />}
                    removeIcon={null}
                    style={{caretColor:'transparent'}}
                    className='input'
                    value={modelName} onClick={handleSelectModelIds}
                >
                </Select>
                <div className='label'>
                    <span>{t('systemPromptTemplate')}</span>
                </div>
                <div className='label-desc'>{t('systemPromptTemplateDescPart1')}{"{{language}}"}{t('systemPromptTemplateDescPart2')} 
                &nbsp;<a className='referToTheDocumentationFor href' href="https://docs.tasking.ai/docs/guide/product_modules/assistant/components/system-prompt-template" target="_blank">
                        <span className='referToThe'>{t('learnMore')}</span>
                    </a>
                </div>
                {systemPromptTemplate?.map((value: any, index: number) => (
                    <div className='input-map' key={index}>
                        <Input.TextArea
                            autoSize={{ minRows: 1, maxRows: 10 }}
                            value={value}
                            className='inputs'
                            placeholder={t('systemPromptPlaceholder')}
                            onChange={(e) => handleInputPromptChanges(index, e.target.value)}
                        />
                        <DeleteInputIcon onClick={() => handleDeletePromptInputs(index)} style={{ marginTop: '8px' }} /></div>
                ))}
                <div className='add-bottom'>
                    <Button onClick={handleAddPrompt} disabled={systemPromptTemplate.length === 10} icon={<PlusOutlined />}>{t('add', {ns: 'common'})}</Button>
                    <span>{systemPromptTemplate.length}/10</span>
                </div>
                <div className='hr'></div>
                <div className='label'>
                    <span className='span'>*</span>
                    <span>{t('memory', {ns: 'common'})}</span>

                </div>
                <div className='label-desc'>{t('contextMemoryDescription')} 
                &nbsp;<a className='referToTheDocumentationFor href'   href="https://docs.tasking.ai/docs/guide/product_modules/assistant/components/memory" target="_blank">
                         <span className='referToThe'>{t('learnMore')}</span>
                    </a>
                </div>
                <div className='memory-type'>
                    <Button className='button-type' >{t('type', {ns: 'common'})}</Button>
                    <Select
                        onChange={handleMemoryChange}
                        value={memoryValue}
                       
                        className='select-input'
                        options={[
                            {
                                value: 'message_window',
                                label: t('messageWindow', {ns: 'common'}),
                            },
                            {
                                value: 'zero',
                                label: t('zero', {ns: 'common'}),
                            },
                            {
                                value: 'naive',
                                label: t('naive', {ns: 'common'}),
                            }

                        ]}>
                    </Select>
                </div>
                {
                    memoryValue === 'message_window' && <div className='input-double'>
                        <div className='input-children'>
                            <Button className='button-type' >{t('maxMessages')}</Button>
                            <InputNumber
                                parser={(value: any) => (isNaN(value) ? 1 : parseInt(value, 10))}
                                min={1}
                                max={128}
                                placeholder={t('messagesPlaceholder')}
                                value={inputValue1}
                                onChange={(value) => handleInputValue1(value as number)}
                            />
                        </div>
                        <div className='input-children1'>
                            <Button className='button-type' >{t('maxTokens', {ns: 'common'})}</Button>
                            <InputNumber parser={(value: any) => (isNaN(value) ? 1 : parseInt(value, 10))} min={1} max={8192} placeholder={t('maxTokensPlaceholder')} value={inputValue2} onChange={(e) => handleInputValue2(e as number)}></InputNumber>
                        </div>

                    </div>
                }
            </div>
            <div className='right-assistant'>
                <div className='basic-information'>
                    {t('integrations')}
                </div>
                <div className='desc-retrieval'>
                    {t('retrieval', {ns: 'common'})}
                </div>
                <div className='label-desc'>
                    {t('retrievalDescription')} <a href="https://docs.tasking.ai/docs/guide/product_modules/retrieval/overview" target='_blank'  className='referToTheDocumentationFor'>{t('learnMore')}</a>
                </div>
                {retrievalFormList.map((item: any, index: number) => (
                    <div className='retrieval-list' key={item.collection_id}>
                        <Select options={[
                            { value: 'Collection', label: t('collection', {ns: 'common'}) }
                        ]} defaultValue='Collection'   className='retrieval-type'></Select>
                        <Select className='input' mode="multiple" placeholder={!item.name && t('retrievalPlaceHolder', {ns: 'common'})} style={{caretColor:'transparent'}} onClick={() => handleCollectionModal(index, item.collection_id)} suffixIcon={<RightOutlined />} open={false} value={item.name ? item.name : undefined} removeIcon={null} />
                        <div> <DeleteInputIcon onClick={() => handleDeleteRetrieval(item.collection_id,index)} style={{ marginTop: '8px' }} /></div>
                    </div>
                ))}
                <div className={`add-bottom ${retrievalFormList.length === 10 && 'disabled-button'}`} >
                    <Button onClick={handleAddRetrieval} disabled={retrievalFormList.length === 10} icon={<PlusOutlined />}>{t('add', {ns: 'common'})}</Button>
                    <span>{retrievalFormList.length}/10</span>
                </div>
                {isShowRetrievalConfig && <>
                    <div className='desc-retrieval' style={{ marginBottom: '12px' }}>
                        {t('retrievalConfigs')}
                    </div>
                    <div className='memory-type'>
                        <Button className='button-type' >{t('method', {ns: 'common'})}</Button>
                        <Select
                            onChange={handleRetrievalConfigChange}
                            value={retrievalConfig}
                            className='select-input'
                            options={[
                                {
                                    value: 'function_call',
                                    label: t('functionCall', {ns: 'common'}),
                                },
                                {
                                    value: 'user_message',
                                    label: t('userMessage'),
                                },
                                {
                                    value: 'memory',
                                    label: t('memory', {ns: 'common'}),
                                }
                            ]}>
                        </Select>
                    </div>
                    <div className='input-double'>
                        <div className='input-children'>
                            <Button className='button-type' >Top K</Button>
                            <InputNumber
                                parser={(value: any) => (isNaN(value) ? 1 : parseInt(value, 10))}
                                min={1}
                                max={128}
                                placeholder={t('topKPlaceholder')}
                                value={topk}
                                onChange={(value) => handleTopk(value as number)}
                            />
                        </div>
                        <div className='input-children1'>
                            <Button className='button-type' >{t('maxTokens', {ns: 'common'})}</Button>
                            <InputNumber parser={(value: any) => (isNaN(value) ? 1 : parseInt(value, 10))} min={1} max={8192} placeholder={t('maxTokensPlaceholder')} value={maxTokens} onChange={(e) => handleMaxTokens(e as number)}></InputNumber>
                        </div>

                    </div>
                </>}

                <div className='hr'></div>
                <div className='desc-retrieval'>
                    {t('tools', {ns: 'common'})}
                </div>
                <div className='label-desc'>
                    {t('toolsDesc')} <a href="https://docs.tasking.ai/docs/guide/product_modules/tool/overview" target='_blank' className='referToTheDocumentationFor'>{t('learnMore')}</a>
                </div>
                {pluginActionList.map((item: any, index: number) => {
                    return (
                        <div className='retrieval-list'>
                            <Select options={[
                                { value: 'plugin', label: t('plugin', {ns: 'common'}) },
                                { value: 'action', label: t('action', {ns: 'common'}) }
                            ]} defaultValue='plugin' className='retrieval-type' onChange={(value) => handleToolsChange(value, index, item)} value={item.type}></Select>
                            <Select
                                placeholder={item.type === 'plugin' ? t('selectPlugin') : t('selectAction')}
                                open={false}
                                removeIcon={null}
                                mode="multiple"
                                style={{caretColor:'transparent'}}
                                className='input'
                                suffixIcon={<RightOutlined />}
                                value={item.name ? item.name : undefined} onClick={item.type === 'action' ? () => handleSelectActions(index, item.value) : () => handleSelectPlugins(index,item.value)}
                            >
                            </Select>
                            <div> <DeleteInputIcon onClick={() => handleDeleteTool(item,index)} style={{ marginTop: '8px' }} /></div>
                        </div>
                    )
                })}
                <div style={{ marginBottom: '24px' }} className={`add-bottom ${pluginActionList.length === 10 && 'disabled-button'}`} >
                    <Button onClick={handleAddTool} disabled={pluginActionList.length === 10} icon={<PlusOutlined />}>{t('add', {ns: 'common'})}</Button>
                    <span>{pluginActionList.length}/10</span>
                </div>
            </div>
            {collectionModal && <ModalSelect collectionSelectedId={collectionSelectedId} id='collection_id' handleNewModal={handleNewCollection1} title={t('collection', {ns: 'common'})} nameTitle={t('selectCollection')} newTitle={t('newCollection', {ns: 'common'})} hasMore={collectionHasMore} handleSelectedItem={handleSelectedItem} retrievalModal={collectionModal} retrievalSelectedList={retrievalSelectedList} retrievalList={retrievalList} handleClose={handleCancelCollectionModal}></ModalSelect>}
            {actionModal && <ModalSelect id='action_id' collectionSelectedId={actionSelectedId} nameTitle={t('selectActionTitle')} handleNewModal={handleNewAction} title={t('action', {ns: 'common'})} newTitle={t('newAction', {ns: 'common'})} hasMore={actionHasMore} handleSelectedItem={handleActionItem} retrievalModal={actionModal} retrievalSelectedList={actionSelectedList} retrievalList={actionList} handleClose={handleCancelActionModal}></ModalSelect>}
            {pluginModal && <PluginComponent bundleSelectedItem={bundleSelectedItem} pluginSelectedId={pluginSelectedId}  selectedData={selectedPluginList} handleSelectedItem={handlePluginConfirm} open={pluginModal} handleCreateBundle={handleCreateBundle} bundleList={bundilesList} handleClose={handleClosePluginModal}></PluginComponent>}
        </div >
    );
})
export default DrawerAssistant;