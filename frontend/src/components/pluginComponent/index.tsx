import { useState, ChangeEvent, useEffect } from 'react';
import closeIcon from '../../assets/img/x-close.svg'
import Paginations from '@/commonComponent/pagination'
import { Modal, Button, Collapse, Radio, Select, Input } from 'antd';
import { PlusOutlined } from '@ant-design/icons';
import { useTranslation } from 'react-i18next';
import { formatTime } from '@/utils/util.ts'
import NoTool from '../../assets/img/NO_TOOL.svg?react'

import RightArrow from '../../assets/img/rightarrow.svg?react'
import styles from './pluginComponent.module.scss'
function PluginComponent(props: any) {
    const { bundleList, handleSelectedItem, bundleSelectedItem, open, pluginSelectedId, handleClose, selectedData, handleCreateBundle } = props
    const [pluginId, setPluginId] = useState(pluginSelectedId !== undefined ? pluginSelectedId : '')
    const [inputValue, setInputValue] = useState('')
    const [bundleItem, setBundleItem] = useState(bundleSelectedItem !== undefined ? bundleSelectedItem : {})
    const { t } = useTranslation()
    const [bundleListData, setBundleListData] = useState(bundleList)
    useEffect(() => {
        setBundleListData(bundleList)
    }, [bundleList])
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
    const handleCancel = () => {
        setPluginId('')

        // handleSelectedItem('', [], {})
        handleClose()
    }
    const handleClickPlugin = (plugin: any, item: any) => {
        setPluginId(plugin.plugin_id)
        setBundleItem(item)
    }
    const handleNewBundle = () => {
        handleCreateBundle()
    }
    const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
        setInputValue(e.target.value)
    }
    const handleRetrievlConfirm = () => {
        if (typeof bundleItem === 'object' && Object.keys(bundleItem).length > 0 && pluginId) {
            handleSelectedItem(pluginId, bundleItem)
        }
        handleClose()
    }
    const handleSearch = () => {

    }
    const handleSelectEndChange = (value: string) => {
        if (value === 'All Records') {
            setBundleListData(bundleList)
        } else {
            const data = bundleList.map((item:any)=> {
                const newDataList = item.plugins.filter((plugin:any)=>selectedData.includes(plugin.plugin_id))
                return {
                    ...item,
                    plugins:newDataList
                }
            }).filter((item:any) => item.plugins.length > 0); 
            setBundleListData(data)
        }


    }
    return <Modal open={open} onCancel={handleCancel} centered className={styles['plugin-modal']} width={1325} closeIcon={<img src={closeIcon} alt="closeIcon" />} title='Select Plugin' footer={[
        <div className='footer-group' style={{ display: 'flex', justifyContent: 'space-between' }} key='footer2'>
            <Button key="model" icon={<PlusOutlined />} onClick={handleNewBundle} className='cancel-button'>
                New bundle
            </Button>
            <div>
                <span className='select-record'>
                    {pluginId ? 1 : 0}  {t('projectItemSelected')}
                </span>
                <Button key="cancel" onClick={handleCancel} className='cancel-button' style={{ marginRight: '8px' }}>
                    {t('cancel')}
                </Button>
                <Button key="submit" onClick={handleRetrievlConfirm} className='next-button'>
                    {t('confirm')}
                </Button>
            </div>
        </div>
    ]
    }>
        <div className={styles.content}>
            <div className={styles['header-table']}>
                <Select defaultValue={'ID'} options={[
                    {
                        value: 'id',
                        label: 'ID',
                    }
                ]} className={styles['select-name']} />
                <Input placeholder='Enter ID' className={styles['input-name']} onChange={handleInputChange} value={inputValue} />
                <Button className='cancel-button' onClick={handleSearch}>Search</Button>
                <Select defaultValue="All Records" onChange={handleSelectEndChange} options={optionsEnd} className={styles['select-data']} />

            </div>
            {bundleListData.length === 0 ? <div className={styles['no-data']}>
                <NoTool />
                <div className={styles['desc']}>New Bundle</div>
                <Button icon={<PlusOutlined />} type='primary' className={`${styles['prompt-button']} next-button`} onClick={handleNewBundle}>New Bundle</Button>
            </div> : bundleListData.map((item: any) => {
                return <Collapse key={item.bundle_instance_id} collapsible="header" className={styles.pluginCollapse}>
                    <Collapse.Panel showArrow={false} header={<div className={styles.bundle} >
                        <img className={styles.img} loading="lazy" src={item.icon_url} alt="" />
                        <div className={styles.right}>
                            <div className={styles.name}><span>
                                {item.name}
                            </span> <RightArrow /></div>
                            <div className={styles.desc}>{item.description}</div>
                            <div className={styles.time}>{formatTime(item.created_timestamp)}</div>
                        </div>
                    </div>} key={item.bundle_id}>
                        <div className={styles['plugin-list']}>
                            {item.plugins.map((plugin: any) => (
                                <div className={`${styles['pluginSingle']} ${plugin.plugin_id === pluginId && styles['selectItem']} ${selectedData.includes(plugin.plugin_id) && styles['selectedItem']}`} onClick={selectedData.includes(plugin.plugin_id) ? undefined : () => handleClickPlugin(plugin, item)}>
                                    <div className={styles.pluginName}>
                                        {plugin.name}
                                        {selectedData.includes(plugin.plugin_id) ? <span className={styles.selectedName}>Selected</span> : <Radio checked={plugin.plugin_id === pluginId} />}
                                    </div>
                                    <div className={styles.pluginDesc}>
                                        {plugin.description}
                                    </div>
                                </div>
                            ))}
                        </div>
                    </Collapse.Panel>

                </Collapse>
            })}
        </div>

        <Paginations />
    </Modal >;
}
export default PluginComponent;