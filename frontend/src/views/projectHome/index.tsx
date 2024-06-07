import { Layout, Menu, Button, Modal, Select } from 'antd';
import { useState, useEffect } from 'react'
import { Link, Outlet, useNavigate, useLocation } from 'react-router-dom'
import { projectHomeType } from '@/constant/index'
import CloseIcon from '@/assets/img/x-close.svg?react'
import { fetchAssistantsData, fetchPluginData, fetchActionData, fetchModelsData, fetchRetrievalData, fetchApikeysData } from '../../Redux/actions';
import TaskingCloud from '@/assets/img/taskingaiCloud.svg?react'
import {
    QuestionCircleOutlined,
    LogoutOutlined,
} from '@ant-design/icons';
import './projectHome.scss';
import { themeColorRedux } from '@/Redux/actions'

import LightIcon from '@/assets/img/lightIcon.svg?react'
import DarkIcon from '@/assets/img/darkIcon.svg?react'
import ThemeColorIcon from '@/assets/img/themeColorIcon.svg?react'
import Forum from '../../assets/img/Forum.svg?react'
import ApiReference from '../../assets/img/apiReferenceNew.svg?react'
import { setPlaygroundSelect } from '@/Redux/actions/playground'
import ModelIcon from '../../assets/img/modelIcon.svg?react'
import Assistant from '../../assets/img/assistantsNew.svg?react'
import Retrieval from '../../assets/img/retrievalNew.svg?react';
import Plugin from '../../assets/img/toolsNew.svg?react';
import Back from '../../assets/img/backHomeNew.svg?react';
import Apikeys from '../../assets/img/apikeysNew.svg?react';
import AiIcon from "../../assets/img/LOGO.svg?react";
import ArrowIcons from '../../assets/img/ArrowIcons.svg?react';
import RightArrow from '../../assets/img/rightarrow.svg?react';
import Playground from '../../assets/img/playgroundNew.svg?react';
import config from '../../../package.json'
import HomeIcon from '@/assets/img/homeIcon.svg?react'
import { useDispatch, useSelector } from 'react-redux';
const { Header, Content, Sider } = Layout;
const ProjectHome = () => {
    const { search, pathname } = useLocation();

    const navigate = useNavigate();
    const dispatch = useDispatch();
    const { playgroundType } = useSelector((state: any) => state.playgroundType)
    const { assistantPlaygroundId } = useSelector((state: any) => state.assistantId)
    const location = useLocation()
    const { modelName, modelId } = useSelector((state: any) => state.modelId)
    const keyReverseValue: Record<string, string> = {
        ['/project']: 'Home',
        ['/project/models']: 'Models',
        ['/project/home']: 'Home',
        ['/project/assistants']: 'Assistants',
        ['/project/collections']: 'Retrieval',
        ['/project/playground']: 'Playground',
        ['/project/tools']: 'Plugins',
        ['/project/tools/actions']: 'Actions',
        ['/project/tools/plugins']: 'Plugins',
        ['/project/apikeys']: 'API Keys',
    }
    const subMenuItems = [
        { key: '/project/tools/plugins', icon: <LogoutOutlined />, text: 'Plugins', path: `/project/tools/plugins` },
        { key: '/project/tools/actions', icon: <LogoutOutlined />, text: 'Actions', path: `/project/tools/actions` },
    ];
    const [key, setKey] = useState('')
    const filteredKeys = [location.pathname === `/project` || location.pathname === `/project/` ? `/project/home` : location.pathname, location.pathname.includes('tools') && `/project/tools`, !location.pathname.includes('tools/actions') && location.pathname.includes('tools') && `/project/tools/plugins`]

    const [selectedKey, setSelectedKey] = useState(filteredKeys.filter(item => Boolean(item)) as string[])
    const [isOpen, setOpen] = useState(selectedKey.filter(item => typeof item === 'string').some(item => (item as string).includes('tools')))
    const [collapsed, setCollapsed] = useState(false);
    const [showTaskingAi, setShowTaskingAi] = useState(true);
    const [logoutOpen, setLogoutOpen] = useState(false)
    const [assistantParams, setAssistantParams] = useState('')
    const [selectedTheme, setSelectedTheme] = useState(localStorage.getItem('themeColor') || 'light')

    useEffect(() => {
        const queryParams: any = new URLSearchParams(search);
        const assistantId = queryParams.get('assistant_id')

        if (location.pathname === `/project/playground` && assistantId && playgroundType === 'assistant') {
            setAssistantParams(`assistant_id=${assistantId}`)
        } else if (playgroundType === 'chat_completion' && modelId) {
            setAssistantParams(`model_id=${modelId}&model_name=${modelName}`)
        }
        const key = location.pathname
        setSelectedKey([key])
        setKey(key)
        if (key === `/project/tools`) {
            setSelectedKey([key, `/project/tools/plugins`])
            setOpen(true)
        } else {
            if (key === `/project/tools/plugins` || key === `/project/tools/actions`) {
                setOpen(true)
                setSelectedKey([key, `/project/tools`])
            } else {
                setOpen(false)
                setSelectedKey([key])
            }
        }
    }, [location.pathname, location.search])
    useEffect(() => {
        dispatch(fetchAssistantsData() as any);
        dispatch(fetchModelsData(20) as any);
        dispatch(fetchRetrievalData({
            limit: 20
        }) as any);
        dispatch(fetchApikeysData(20) as any)
        dispatch(fetchPluginData(20) as any)
        dispatch(fetchActionData(20) as any)
    }, []);
    const handleClickMenu = (e: projectHomeType) => {

        if (e.key !== '/' && e.key !== '/taskingCloud') {
            navigate(e.key)
        }
        if (e.key === `/project/playground`) {
            navigate(`${e.key}?${assistantParams}`)
        } else if (e.key !== '/' && e.key !== '/taskingCloud') {
            navigate(e.key)

        } else {
            navigate(null)
        }

    }
    const toggleCollapsed = () => {
        setCollapsed(!collapsed);
    };
    const handleSubMenuNew = ({ key }: { key: string }) => {
        setSelectedKey([`/project/tools`, key])
    }
    const handleChangePlaygroundModel = (value: string) => {
        if (value === 'chat_completion') {
            if (modelId && modelName) {
                navigate(`${pathname}?model_id=${modelId}&model_name=${modelName}`)
            } else {
                navigate(`${pathname}`)
            }

        } else if (value === 'assistant') {
            if (assistantPlaygroundId) {
                navigate(`${pathname}?assistant_id=${assistantPlaygroundId}`)
            } else {
                navigate(`${pathname}`)
            }
        }
        dispatch(setPlaygroundSelect(value))
    }
    const handleSubMenu = () => {
        setOpen(true)
    }
    const handleBack = () => {
        setLogoutOpen(true)
    }
    const handleModalCancel = () => {
        setLogoutOpen(false)
    }
    const handleCreateConfirm = () => {
        localStorage.removeItem('token')
        navigate('/auth/signin')
        setLogoutOpen(false)
    }
    const handleMouseEnter = () => {
        setShowTaskingAi(false);
    };

    const handleMouseLeave = () => {
        setShowTaskingAi(true);
    };
    const handleSubMenuClick = ({ key }: { key: string }) => {
        setKey(key)
    };
    const handleHref = () => {
        window.open('https://tasking.ai', '_blank')
    }
    const handleClickThemeColor = (value: string): React.MouseEventHandler<HTMLElement> => {
        return (): void => {
            setSelectedTheme(value)
            const root = document.documentElement;
            root.classList.remove('light-theme', 'dark-theme', 'systemColor-theme');
            if (value === 'light') {
                root.classList.add('light-theme');
                dispatch(themeColorRedux('light') as any)
            } else if (value === 'dark') {
                root.classList.add('dark-theme');
                dispatch(themeColorRedux('dark'))
            } else {
                localStorage.setItem('themeColor', 'systemColor')
                root.classList.add('systemColor-theme');
                dispatch(themeColorRedux('systemColor'))
            }
        };
    }
    return (
        <Layout style={{ minHeight: '100vh', maxHeight: '100vh' }}>
            <Header className="header">
                <div className={`left-header1 ${collapsed ? 'collapsed-header' : ''}`} onMouseEnter={handleMouseEnter} onMouseLeave={handleMouseLeave}>
                    {!collapsed && <div className="left-header-icon" onClick={handleHref}>
                        <AiIcon /> <span className='left-header-title'>Tasking.AI</span>
                    </div>}
                    {
                        !collapsed ? <div className='arrowiconsParent' onClick={toggleCollapsed}>
                            <ArrowIcons />
                        </div> : (
                            showTaskingAi ? <AiIcon onClick={toggleCollapsed} /> : <div className='arrowiconsParent' onClick={toggleCollapsed}> <RightArrow /> </div>
                        )
                    }

                </div>
                {isOpen && <div className='center-header' >
                    Tools
                </div>}
                <div className="right-header">
                    <div style={{ height: '100%', display: 'flex', alignItems: 'center' }}>
                        <span style={{ lineHeight: 1 }}>{keyReverseValue[key]}</span>
                        {keyReverseValue[key] === 'Playground' && <Select value={playgroundType} style={{ marginLeft: '10px', width: '155px' }} defaultValue='assistant' onChange={handleChangePlaygroundModel} options={[{ value: 'chat_completion', label: 'Chat Completion' }, { value: 'assistant', label: 'Assistant' }]}></Select>}
                    </div>

                    <div className='button-group-href'>
                        <Button
                            icon={<Forum />}
                            className='document-button cancel-button'
                            onClick={() => window.open('https://forum.tasking.ai/', '_blank')}
                        >
                            Forum
                        </Button>
                        <Button
                            icon={<ApiReference />}
                            className='document-button cancel-button'
                            onClick={() => window.open('https://docs.tasking.ai/api/', '_blank')}
                        >
                            API Reference
                        </Button>
                        <Button
                            icon={<QuestionCircleOutlined />}
                            className='document-button cancel-button'
                            onClick={() => window.open('https://docs.tasking.ai', '_blank')}
                        >
                            Documentation
                        </Button>
                    </div>

                </div>
            </Header>
            <Layout>
                <Sider width={collapsed ? 58 : 226} theme="light" >
                    <div className="menu-page">

                        <Menu onMouseEnter={handleMouseEnter}
                            onMouseLeave={handleMouseLeave} className={collapsed ? 'collapsed' : ''} inlineCollapsed={collapsed} mode="vertical" theme="light" selectedKeys={selectedKey} onClick={handleClickMenu} >
                            <Menu.Item key={`/project/home`} icon={<HomeIcon className="svg-icons" />}>
                                <Link to={`/project/home`}>Home</Link>
                            </Menu.Item>
                            <Menu.Item key={'/project/playground'} icon={<Playground className="svg-icons" />}>
                                <Link to={'/project/playground'}>Playground</Link>
                            </Menu.Item>

                            <Menu.Item key='/hr1' className='menu-hr'>
                            </Menu.Item>
                            <Menu.Item key={'/project/models'} icon={<ModelIcon className="svg-icons" />}>
                                <Link to={'/project/models'}>Models</Link>
                            </Menu.Item>
                            <Menu.Item key={'/project/collections'} icon={<Retrieval className="svg-icons" />}>
                                <Link to={'/project/collections'}>Retrieval</Link>
                            </Menu.Item>
                            <Menu.Item key={'/project/tools'} icon={<Plugin className="svg-icons" />} onClick={handleSubMenu}>
                                <Link to={'/project/tools'}>Tools</Link>
                            </Menu.Item>
                            <Menu.Item key='/hr2' className='menu-hr'>
                            </Menu.Item>
                            <Menu.Item key={`/project/assistants`} icon={<Assistant className="svg-icons" />}>
                                <Link to={'/project/assistants'}>Assistants</Link>
                            </Menu.Item>
                            <Menu.Item key='/hr3' className='menu-hr'>
                            </Menu.Item>
                            <Menu.Item key='/hr4' className='menu-hr border-hr'>
                            </Menu.Item>
                            <Menu.Item key={'/project/apikeys'} className='api-key-menu' icon={<Apikeys className="svg-icons" />}>
                                <Link to={'/project/apikeys'}>API Keys</Link>
                            </Menu.Item>

                            <Menu.Item icon={<Back className="svg-icons" />} onClick={handleBack} className='orgination' key='/'>
                                <a onClick={handleBack}>Logout</a>
                            </Menu.Item>

                            <Menu.Item icon={<TaskingCloud className="svg-icons-taskingai" />} className='taskingCloud' key='/taskingCloud'>
                                <a href='http://www.tasking.ai' target='blank'>Try TaskingAI Cloud</a>
                            </Menu.Item>
                            <div className='theme-color'>
                                <div className={`slider ${selectedTheme}`}></div>
                                {!collapsed && <div onClick={handleClickThemeColor('light')} className={`theme-item ${selectedTheme === 'light' && 'theme-selected'}`}>
                                    <LightIcon />
                                </div>}
                                {!collapsed && <div onClick={handleClickThemeColor('systemColor')} className={`theme-item ${selectedTheme === 'systemColor' && 'theme-selected'}`}>
                                    <ThemeColorIcon className='theme-item' />
                                </div>}
                                {!collapsed && <div onClick={handleClickThemeColor('dark')} className={`theme-item ${selectedTheme === 'dark' && 'theme-selected'}`}>
                                    <DarkIcon className='theme-item' />
                                </div>}
                                {
                                    collapsed && <div className={`theme-item-single theme-selected`}>
                                        {selectedTheme === 'light' && <LightIcon className='theme-item' />}
                                        {selectedTheme === 'dark' && <DarkIcon className='theme-item' />}
                                        {selectedTheme === 'systemColor' && <ThemeColorIcon className='theme-item' />}
                                    </div>
                                }
                            </div>
                            <Menu.Item className='version' disabled style={{ cursor: "default" }}>
                                <span>TaskingAI Community {config.version}</span>
                            </Menu.Item>
                        </Menu>

                    </div>
                </Sider>
                {isOpen && <Sider width={210} theme="light">
                    <div className="menu-page">

                        <Menu mode="vertical" theme="light" onClick={handleSubMenuClick} selectedKeys={selectedKey} onSelect={handleSubMenuNew}>
                            {subMenuItems.map(item => (
                                <Menu.Item key={item.key}>
                                    <Link to={item.path}>{item.text}</Link>
                                </Menu.Item>
                            ))}
                        </Menu>
                    </div>
                </Sider>}
                <Layout>
                    <Content
                        className="site-layout-background"
                        style={{
                            margin: 0,
                            minHeight: 280,
                            display: 'flex',
                            flexDirection: 'column',
                            background: 'white'
                        }}
                    >
                        <Outlet></Outlet>
                    </Content>
                </Layout>
                <Modal title='Logout' centered open={logoutOpen} closeIcon={<CloseIcon />}
                    onCancel={handleModalCancel}
                    footer={[
                        <Button key="cancel" onClick={handleModalCancel} className='cancel-button'>
                            Cancel
                        </Button>,
                        <Button key="submit" onClick={handleCreateConfirm} className='delete-button'>
                            Confirm
                        </Button>
                    ]}>
                    <span>Are you sure you want to log out of your TaskingAI account?</span>
                </Modal>
            </Layout>
        </Layout>

    );
};

export default ProjectHome;
