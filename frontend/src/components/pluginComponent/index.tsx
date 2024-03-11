import { useState } from 'react';
import closeIcon from '../../assets/img/x-close.svg'
import Paginations from '../pagination/index'
import { Modal, Button, Collapse, Radio } from 'antd';
import { PlusOutlined } from '@ant-design/icons';
import { useTranslation } from 'react-i18next';
import { formatTime } from '@/utils/util.ts'
import NoTool from '../../assets/img/NO_TOOL.svg?react'

import RightArrow from '../../assets/img/rightarrow.svg?react'
import styles from './pluginComponent.module.scss'
function PluginComponent(props: any) {
    const [pluginId, setPluginId] = useState('')
    const { bundleList, handleSelectedItem, open, handleClose, selectedData, handleCreateBundle } = props
    const [selectedPluginList, setSelectedPluginList] = useState(selectedData)
    const [bundleItem, setBundleItem] = useState({} as any)
    const { t } = useTranslation()
    const handleCancel = () => {
        setPluginId('')
        handleClose()
    }
    const handleClickPlugin = (plugin: any, item: any) => {
        setPluginId(plugin.plugin_id)
        setBundleItem(item)
    }
    const handleNewBundle = () => {
        handleCreateBundle()
    }
    const handleRetrievlConfirm = () => {
        setSelectedPluginList((prev: any) => {
            const newData = [...prev, pluginId]
            handleSelectedItem(pluginId, newData, bundleItem)
            return newData
        })
        handleClose()
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
            {bundleList.length === 0 ? <div className={styles['no-data']}>
                <NoTool />
                <div className={styles['desc']}>New Bundle</div>
                <Button icon={<PlusOutlined />} className={styles['prompt-button']} onClick={handleNewBundle}>New Bundle</Button>
            </div> : bundleList.map((item: any) => {
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
                                <div className={`${styles['pluginSingle']} ${plugin.plugin_id === pluginId && styles['selectItem']} ${selectedPluginList.includes(plugin.plugin_id) && styles['selectedItem']}`} onClick={selectedPluginList.includes(plugin.plugin_id) ? undefined : () => handleClickPlugin(plugin, item)}>
                                    <div className={styles.pluginName}>
                                        {plugin.name}
                                        {selectedPluginList.includes(plugin.plugin_id) ? <span className={styles.selectedName}>Selected</span> : <Radio checked={plugin.plugin_id === pluginId} />}
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
            {/* {bundleList.map((item: any) => {
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
                                <div className={`${styles['pluginSingle']} ${plugin.plugin_id === pluginId && styles['selectItem']} ${selectedPluginList.includes(plugin.plugin_id) && styles['selectedItem']}`} onClick={selectedPluginList.includes(plugin.plugin_id) ? undefined : () => handleClickPlugin(plugin,item)}>
                                    <div className={styles.pluginName}>
                                        {plugin.name}
                                        {selectedPluginList.includes(plugin.plugin_id) ? <span className={styles.selectedName}>Selected</span> : <Radio checked={plugin.plugin_id === pluginId} />}
                                    </div>
                                    <div className={styles.pluginDesc}>
                                        {plugin.description}
                                    </div>
                                </div>
                            ))}
                        </div>
                    </Collapse.Panel>

                </Collapse>
            })} */}

        </div>

        <Paginations />
    </Modal >;
}
export default PluginComponent;