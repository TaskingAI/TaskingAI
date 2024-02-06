
import { Layout, Menu, ConfigProvider, Button,Modal } from 'antd';
import { useState, useEffect } from 'react'
import { Link, Outlet, useNavigate, useLocation } from 'react-router-dom'
import { projectHomeType } from '@/contant/index'
import CloseIcon from '@/assets/img/x-close.svg?react'

import {
    QuestionCircleOutlined,
    LogoutOutlined,
} from '@ant-design/icons';
import './projectHome.scss';
import IconData from '../../assets/img/modelNew.svg?react'
import Assistant from '../../assets/img/assistantsNew.svg?react'
import aiIcon from "../../assets/img/LOGO+TEXT.svg";
import Retrieval from '../../assets/img/retrievalNew.svg?react';
import Plugin from '../../assets/img/toolsNew.svg?react';
// import Setting from '../../assets/img/settingNew.svg?react';
import Back from '../../assets/img/backHomeNew.svg?react';
import Apikeys from '../../assets/img/apikeysNew.svg?react';
import TaskingAi from '../../assets/img/taskingAi.svg?react';
import ArrowIcons from '../../assets/img/ArrowIcons.svg?react';
import RightArrow from '../../assets/img/rightarrow.svg?react';
import Playground from '../../assets/img/playgroundNew.svg?react';
import config from '../../../package.json'
const { Header, Content, Sider } = Layout;


const ProjectHome = () => {
    const navigate = useNavigate();
    const location = useLocation()
    const keyReverseValue: Record<string, string> = {
        ['/project']: 'Models',
        ['/project/models']: 'Models',
        ['/project/assistants']: 'Assistants',
        ['/project/collections']: 'Retrieval',
        ['/project/playground']: 'Playground',
        ['/project/tools']: 'Actions',
        ['/project/tools/actions']: 'Actions',
        ['/project/apikeys']: 'API Keys',
    }
    const subMenuItems = [
        { key: '/project/tools', icon: <LogoutOutlined />, text: 'Actions', path: `/project/tools/actions` },
    ];
    const [key, setKey] = useState('')

    const selectedKey = location.pathname === '/project' || location.pathname === '/project/' ? '/project/models' : location.pathname
    const [isOpen, setOpen] = useState(selectedKey.includes('tools') || false)
    const [collapsed, setCollapsed] = useState(false);
    const [showTaskingAi, setShowTaskingAi] = useState(true);
    const [logoutOpen, setLogoutOpen] = useState(false)

    useEffect(() => {
        const key = location.pathname
        setKey(key)
    }, [location.pathname])
    const handleClickMenu = (e: projectHomeType) => {
        setKey(e.key)
        if (e.key.includes('tools')) {
            setOpen(true)
        } else {
            setOpen(false)
        }
        if(e.key !=='/') {
            navigate(e.key)

        }
    }
    const toggleCollapsed = () => {
        setCollapsed(!collapsed);
    };
    const handleSubMenu = () => {
        setOpen(true)
    }
    const handleBack = () => {
        setLogoutOpen(true)
    }
    const handleModalCancel = () => {
        setLogoutOpen(false)
    }
    const handleCreateConfrim = () => {
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
    const handleHref = ()=>{
        window.open('https://tasking.ai', '_blank')
    }
    return (
        <Layout style={{ minHeight: '100vh', maxHeight: '100vh' }}>
            <Header className="header">
                <div className={`left-header1 ${collapsed ? 'collapsed-header' : ''}`} onMouseEnter={handleMouseEnter} onMouseLeave={handleMouseLeave}>
                    {!collapsed && <img src={aiIcon} alt="" style={{ cursor: 'pointer' }} onClick={handleHref} />}
                    {
                        !collapsed ? <div className='arrowiconsParent' onClick={toggleCollapsed}>
                            <ArrowIcons />
                        </div> : (
                            showTaskingAi ? <TaskingAi onClick={toggleCollapsed} /> : <div className='arrowiconsParent' onClick={toggleCollapsed}> <RightArrow /> </div>
                        )
                    }

                </div>
                {isOpen && <div className='center-header' >
                    Tools
                </div>}
                <div className="right-header">
                    <span>{keyReverseValue[key]}</span>
                    <Button
                        icon={<QuestionCircleOutlined />}
                        className='document-button cancel-button'
                        onClick={() => window.open('https://docs.tasking.ai', '_blank')}
                    >
                        Documentation
                    </Button>
                </div>
            </Header>
            <Layout>
                <Sider width={collapsed ? 58 : 226} theme="light" >
                    <div className="menu-page">
                        <ConfigProvider theme={{
                            components: {
                                Menu: {
                                    itemSelectedBg: '#f3f8f6',
                                    itemSelectedColor: '#087443',
                                    itemActiveBg: '#f3f8f6'
                                }
                            }
                        }}>
                            <Menu onMouseEnter={handleMouseEnter}
                                onMouseLeave={handleMouseLeave} className={collapsed ? 'collapsed' : ''} inlineCollapsed={collapsed} mode="vertical" theme="light" selectedKeys={[selectedKey]} onClick={handleClickMenu} >


                                <Menu.Item key={'/project/models'} icon={<IconData className="svg-icons" />}>
                                    <Link to={'/project/models'}>Models</Link>
                                </Menu.Item>

                                <Menu.Item key={`/project/assistants`} icon={<Assistant className="svg-icons" />}>
                                    <Link to={'/project/assistants'}>Assistants</Link>
                                </Menu.Item>
                                <Menu.Item key={'/project/collections'} icon={<Retrieval className="svg-icons" />}>
                                    <Link to={'/project/collections'}>Retrieval</Link>
                                </Menu.Item>
                                <Menu.Item key={'/project/tools'} icon={<Plugin className="svg-icons" />} onClick={handleSubMenu}>
                                    <Link to={'/project/tools'}>Tools</Link>
                                </Menu.Item>

                                <Menu.Item key={'/project/playground'} icon={<Playground className="svg-icons" />}>
                                    <Link to={'/project/playground'}>Playground</Link>

                                </Menu.Item>
                                <Menu.Item key={'/project/apikeys'} icon={<Apikeys className="svg-icons" />}>
                                    <Link to={'/project/apikeys'}>API Keys</Link>
                                </Menu.Item>

                                <Menu.Item icon={<Back className="svg-icons" />} onClick={handleBack} className='orgination' key='/'>
                                    <span onClick={handleBack}>Logout</span>
                                </Menu.Item>
                                <Menu.Item  className='version' disabled style={{cursor:"default"}}>
                                    <span>TaskingAI Community {config.version}</span>
                                </Menu.Item>
                            </Menu>
                        </ConfigProvider>
                    </div>
                </Sider>
                {isOpen && <Sider width={210} theme="light">
                    <div className="menu-page">
                        <ConfigProvider theme={{
                            components: {
                                Menu: {
                                    itemSelectedBg: '#f3f8f6',
                                    itemSelectedColor: '#087443',
                                    itemActiveBg: '#f3f8f6'
                                }
                            }
                        }}>
                            <Menu mode="vertical" theme="light" onClick={handleSubMenuClick} selectedKeys={[selectedKey]}>
                                {subMenuItems.map(item => (
                                    <Menu.Item key={item.key}>
                                        <Link to={item.path}>{item.text}</Link>
                                    </Menu.Item>
                                ))}
                            </Menu>
                        </ConfigProvider>
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
                        <Button key="submit" onClick={handleCreateConfrim} className='delete-button'>
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
