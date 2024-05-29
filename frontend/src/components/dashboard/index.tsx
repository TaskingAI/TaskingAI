import styles from './dashboard.module.scss'
import DashBoardImg from '@/assets/img/projectHomeResource.png'
import Forum from '@/assets/img/Forum.svg?react'
import Documentation from '@/assets/img/documentIcon.svg?react'
import Examples from '@/assets/img/exampleIcon.svg?react'
import ModelGreenIcon from '@/assets/img/modelGreen.svg?react'
import ToolGreenIcon from '@/assets/img/toolGreenIcon.svg?react'
import AssistantGreenIcon from '@/assets/img/assistantGreenIcon.svg?react'
import RetrievalGreenIcon from '@/assets/img/retrievalGreenIcon.svg?react'
import ForwardIcon from '@/assets/img/forwardIcon.svg?react'
import ApiReference from '../../assets/img/restApisIcon.svg?react'
import PythonIcon from '@/assets/img/pythonIcon.svg?react'
import NodeIcon from '@/assets/img/jsIcon.svg?react'
import OpenaiIcon from '@/assets/img/openaiIcon.svg?react'
import { Button } from 'antd'
import './index.css'

import { useNavigate } from 'react-router-dom'
import MarkdownMessageBlock from '@taskingai/taskingai-markdown'
const DashBoard = () => {
    const projectname = localStorage.getItem('projectName')
    const navigate = useNavigate()
    const handleNavigate = (value: string) => {
        switch (value) {
            case 'model':
                navigate(`/project/models`)
                break;
            case 'retrieval':
                navigate(`/project/collections`)
                break;
            case 'tool':
                navigate(`/project/tools`)
                break;
            case 'assistant':
                navigate(`/project/assistants`)
                break;
            case 'apikey':
                navigate(`/project/apikeys`)
                break;
            default:
                break;
        }
    }
    return (
        <div className={styles.dashboardContent}>
            <div className={styles.dashboard}>
                <div className={styles.title}>{projectname}</div>
                <div className={styles['second-title']}>Welcome to your project</div>
                <div className={styles.desc}>Your project has been deployed on TaskingAI serverless computing cluster, with vector storage and agent runtime all setup and ready to use.</div>
                <div className={styles.content}>
                    <div className={styles['son-content']}>
                        <div className={styles['second-title']}>
                            Get started
                        </div>
                        <div className={styles.desc} style={{ marginBottom: '24px' }}>Embark on your AI-native adventure with TaskingAI, where Forums, API Reference, and Official Documentation are your treasure map to innovation.</div>
                        <div className={styles['group-button']}>
                            <Button onClick={()=>window.open('https://www.tasking.ai/examples')} style={{ display: 'flex', alignItems: 'center' }} icon={<Examples />} className='cancel-button'><span style={{ fontSize: '12px', lineHeight: '15px' }} >Examples</span></Button>
                            <Button onClick={()=>window.open('https://docs.tasking.ai')} style={{ display: 'flex', alignItems: 'center' }} icon={<Documentation />} className='cancel-button'><span style={{ fontSize: '12px', lineHeight: '15px' }}>Documentation</span></Button>
                            <Button onClick={()=>window.open('https://forum.tasking.ai')} style={{ display: 'flex', alignItems: 'center' }} icon={<Forum />} className='cancel-button'><span style={{ fontSize: '12px', lineHeight: '15px' }}>Forum</span></Button>
                        </div>
                    </div>
                    <img style={{width:'333px',height:'250px'}} src={DashBoardImg} alt="" />
                </div>
                <div className={styles['second-title']}>Explore basic modules</div>
                <div className={styles.desc} style={{ marginBottom: '24px' }}>Dive into the foundational trio of Model, Retrieval, and Tool with TaskingAI to build and integrate versatile, agent-driven applications. Seamlessly integrate with cloud resources or giants like OpenAI, Anthropic, and many else model providers, ensuring rapid incorporation into your project's code for immediate impact.</div>
                <div className={styles['card-group']}>
                    <div className={styles['card-item']}>
                        <div className={styles['card-top']}>
                            <div className={styles['card-header']}>
                                <ModelGreenIcon />
                                <span className={styles['card-name']}>Model</span>
                            </div>
                            <div className={styles.desc}>Connect various LLM providers, granting a spectrum of advanced AI models to craft your application.</div>
                        </div>
                        <div className={styles['button-group']}>
                            <Button className='cancel-button' onClick={() => handleNavigate('model')}>Explore model</Button>
                            <Button onClick={()=>window.open('https://docs.tasking.ai/docs/guide/product_modules/model/overview')} icon={<ForwardIcon />} style={{ display: 'flex', alignItems: 'center' }} className='cancel-button'>Docs</Button>
                        </div>
                    </div>
                    <div className={styles['card-item']}>
                        <div className={styles['card-top']}>
                            <div className={styles['card-header']}>
                                <RetrievalGreenIcon />
                                <span className={styles['card-name']}>Retrieval</span>
                            </div>
                            <div className={styles.desc}>Uses external data to enhance LLM inferences, enabling dynamic, context-aware interactions through record management and text queries.</div>
                        </div>
                        <div className={styles['button-group']}>
                            <Button className='cancel-button' onClick={() => handleNavigate('retrieval')}>Explore retrieval</Button>
                            <Button onClick={()=>window.open('https://docs.tasking.ai/docs/guide/product_modules/retrieval/overview/')} icon={<ForwardIcon />} style={{ display: 'flex', alignItems: 'center' }} className='cancel-button'>Docs</Button>
                        </div>
                    </div>
                    <div className={styles['card-item']}>
                        <div className={styles['card-top']}>
                            <div className={styles['card-header']}>
                                <ToolGreenIcon />
                                <span className={styles['card-name']}>Tool</span>
                            </div>
                            <div className={styles.desc}>Featuring Plugins and Actions, enhances Assistant functionalities, enabling integration with external APIs and tailored function executions.</div>
                        </div>
                        <div className={styles['button-group']}>
                            <Button className='cancel-button' onClick={() => handleNavigate('tool')}>Explore tool</Button>
                            <Button onClick={()=>window.open('https://docs.tasking.ai/docs/guide/product_modules/tool/overview/')} icon={<ForwardIcon />} style={{ display: 'flex', alignItems: 'center' }} className='cancel-button'>Docs</Button>
                        </div>
                    </div>
                    <div className={styles['card-item']}>
                        <div className={styles['card-top']}>
                            <div className={styles['card-header']}>
                                <AssistantGreenIcon />
                                <span className={styles['card-name']}>Assistant</span>
                            </div>
                            <div className={styles.desc}>A flexible framework for building customizable AI agents, supporting diverse applications with integrated models, memory, retrieval, and tools.</div>
                        </div>
                        <div className={styles['button-group']}>
                            <Button className='cancel-button' onClick={() => handleNavigate('assistant')}>Explore assistant</Button>
                            <Button onClick={()=>window.open('https://docs.tasking.ai/docs/guide/product_modules/assistant/overview/')} icon={<ForwardIcon />} style={{ display: 'flex', alignItems: 'center' }} className='cancel-button'>Docs</Button>
                        </div>
                    </div>
                </div>
                <div className='dashboard-markdown' style={{ height: '435px', display: 'flex', justifyContent: 'space-between',gap:'48px' }}>
                    <div className={styles['son-content']}>
                        <div className={styles['second-title']}>
                            Access the project through code
                        </div>
                        <div className={styles.desc} style={{ marginBottom: '12px' }}>Interact with the project through the TaskingAI client SDKs with your API keys.</div>
                        <div className={styles['group-button']}>
                            <Button style={{ display: 'flex', alignItems: 'center' }} className='cancel-button'><span style={{ fontSize: '12px', lineHeight: '15px' }}  onClick={() => handleNavigate('apikey')}>View API Keys</span></Button>
                            <Button onClick={()=>window.open('https://docs.tasking.ai/docs/guide/sdks/rest_api/authorization')} style={{ display: 'flex', alignItems: 'center' }} icon={<ForwardIcon />} className='cancel-button'><span style={{ fontSize: '12px', lineHeight: '15px' }}>About Authentication</span></Button>
                        </div>
                    </div>
                    <MarkdownMessageBlock styles={{flex:1}} message='```python
# authentication with TaskingAI python SDK
import taskingai
taskingai.init(api_key="YOUR_API_KEY")


# authentication with OpenAI-compatible APIs
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_TASKINGAI_API_KEY",
    base_url="https://oapi.tasking.ai/v1",
)


```'/>
                </div>

                <div className={styles['second-title']} style={{ marginTop: '72px' }}>
                    Client libraries
                </div>
                <div className={styles.desc} style={{ marginBottom: '24px' }}>Choose your preferred client library to start your project.</div>
                <div className={styles['card-bottom']}>
                    <div className={styles['card-bottom-item']}>
                        <div className={styles['card-header']}>
                            <ApiReference />
                            <span className={styles['card-bottom-title']}>REST APIs</span>
                        </div>
                        <div>
                            <Button onClick={()=>window.open('https://docs.tasking.ai/api/')} style={{ display: 'flex', alignItems: 'center' }} icon={<ForwardIcon />} className='cancel-button'><span style={{ fontSize: '12px', lineHeight: '15px' }}>API Reference</span></Button>

                        </div>
                    </div>
                    <div className={styles['card-bottom-item']}>
                        <div className={styles['card-header']}>
                            <PythonIcon />
                            <span className={styles['card-bottom-title']}>Python SDK</span>
                        </div>
                        <div style={{ display: 'flex', gap: '12px' }}>
                            <Button onClick={()=>window.open('https://pypi.org/project/taskingai/')} className='cancel-button'>PyPI</Button>
                            <Button onClick={()=>window.open('https://docs.tasking.ai/docs/guide/sdks/python/quickstart')} style={{ display: 'flex', alignItems: 'center' }} icon={<ForwardIcon />} className='cancel-button'><span style={{ fontSize: '12px', lineHeight: '15px' }}>Documentation</span></Button>
                        </div>
                    </div>
                    <div className={styles['card-bottom-item']}>
                        <div className={styles['card-header']}>
                            <OpenaiIcon />
                            <span className={styles['card-bottom-title']}>OpenAI compatible APIs</span>
                        </div>
                        <div style={{ display: 'flex', gap: '12px' }}>
                            <Button onClick={()=>window.open('https://platform.openai.com/docs/guides/text-generation/chat-completions-api')} className='cancel-button'>OpenAI</Button>
                            <Button onClick={()=>window.open('https://docs.tasking.ai/docs/guide/sdks/openai_compatible/overview')} style={{ display: 'flex', alignItems: 'center' }} icon={<ForwardIcon />} className='cancel-button'><span style={{ fontSize: '12px', lineHeight: '15px' }}>Documentation</span></Button>
                        </div>
                    </div>
                    <div className={styles['card-bottom-item']}>
                        <div className={styles['card-header']}>
                            <NodeIcon />
                            <span className={styles['card-bottom-title']}>Node.js SDK</span>
                        </div>
                        <div>
                            <Button disabled type='primary'><span style={{ fontSize: '12px', lineHeight: '15px' }}>Coming Soon</span></Button>

                        </div>
                    </div>
                </div>
            </div>
        </div>

    );
}
export default DashBoard;