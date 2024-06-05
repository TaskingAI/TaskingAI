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
import { useTranslation } from 'react-i18next';
const DashBoard = () => {
    const { t } = useTranslation(['components/dashboard/index', 'common']);
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
                <div className={styles['second-title']}>{t('welcome')}</div>
                <div className={styles.desc}>{t('projectDeployed')}</div>
                <div className={styles.content}>
                    <div className={styles['son-content']}>
                        <div className={styles['second-title']}>
                            {t('getStarted')}
                        </div>
                        <div className={styles.desc} style={{ marginBottom: '24px' }}>{t('getStartedDesc')}</div>
                        <div className={styles['group-button']}>
                            <Button onClick={()=>window.open('https://www.tasking.ai/examples')} style={{ display: 'flex', alignItems: 'center' }} icon={<Examples />} className='cancel-button'><span style={{ fontSize: '12px', lineHeight: '15px' }} >{t('examples')}</span></Button>
                            <Button onClick={()=>window.open('https://docs.tasking.ai')} style={{ display: 'flex', alignItems: 'center' }} icon={<Documentation />} className='cancel-button'><span style={{ fontSize: '12px', lineHeight: '15px' }}>{t('documentation', {ns: 'common'})}</span></Button>
                            <Button onClick={()=>window.open('https://forum.tasking.ai')} style={{ display: 'flex', alignItems: 'center' }} icon={<Forum />} className='cancel-button'><span style={{ fontSize: '12px', lineHeight: '15px' }}>{t('forum')}</span></Button>
                        </div>
                    </div>
                    <img style={{width:'333px',height:'250px'}} src={DashBoardImg} alt="" />
                </div>
                <div className={styles['second-title']}>{t('exploreBasicModules')}</div>
                <div className={styles.desc} style={{ marginBottom: '24px' }}>{t('exploreBasicModulesDesc')}</div>
                <div className={styles['card-group']}>
                    <div className={styles['card-item']}>
                        <div className={styles['card-top']}>
                            <div className={styles['card-header']}>
                                <ModelGreenIcon />
                                <span className={styles['card-name']}>{t('model')}</span>
                            </div>
                            <div className={styles.desc}>{t('modelDesc')}</div>
                        </div>
                        <div className={styles['button-group']}>
                            <Button className='cancel-button' onClick={() => handleNavigate('model')}>{t('modelExplore')}</Button>
                            <Button onClick={()=>window.open('https://docs.tasking.ai/docs/guide/product_modules/model/overview')} icon={<ForwardIcon />} style={{ display: 'flex', alignItems: 'center' }} className='cancel-button'>{t('docs')}</Button>
                        </div>
                    </div>
                    <div className={styles['card-item']}>
                        <div className={styles['card-top']}>
                            <div className={styles['card-header']}>
                                <RetrievalGreenIcon />
                                <span className={styles['card-name']}>{t('retrieval', {ns: 'common'})}</span>
                            </div>
                            <div className={styles.desc}>{t('retrievalDesc')}</div>
                        </div>
                        <div className={styles['button-group']}>
                            <Button className='cancel-button' onClick={() => handleNavigate('retrieval')}>{t('retrievalExplore')}</Button>
                            <Button onClick={()=>window.open('https://docs.tasking.ai/docs/guide/product_modules/retrieval/overview/')} icon={<ForwardIcon />} style={{ display: 'flex', alignItems: 'center' }} className='cancel-button'>{t('docs')}</Button>
                        </div>
                    </div>
                    <div className={styles['card-item']}>
                        <div className={styles['card-top']}>
                            <div className={styles['card-header']}>
                                <ToolGreenIcon />
                                <span className={styles['card-name']}>{t('tool', {ns: 'cool'})}</span>
                            </div>
                            <div className={styles.desc}>{t('toolDesc')}</div>
                        </div>
                        <div className={styles['button-group']}>
                            <Button className='cancel-button' onClick={() => handleNavigate('tool')}>{t('toolExplore')}</Button>
                            <Button onClick={()=>window.open('https://docs.tasking.ai/docs/guide/product_modules/tool/overview/')} icon={<ForwardIcon />} style={{ display: 'flex', alignItems: 'center' }} className='cancel-button'>{t('docs')}</Button>
                        </div>
                    </div>
                    <div className={styles['card-item']}>
                        <div className={styles['card-top']}>
                            <div className={styles['card-header']}>
                                <AssistantGreenIcon />
                                <span className={styles['card-name']}>{t('assistant', {ns: 'cool'})}</span>
                            </div>
                            <div className={styles.desc}>{t('assistantDesc')}</div>
                        </div>
                        <div className={styles['button-group']}>
                            <Button className='cancel-button' onClick={() => handleNavigate('assistant')}>{t('assistantExplore')}</Button>
                            <Button onClick={()=>window.open('https://docs.tasking.ai/docs/guide/product_modules/assistant/overview/')} icon={<ForwardIcon />} style={{ display: 'flex', alignItems: 'center' }} className='cancel-button'>{t('docs')}</Button>
                        </div>
                    </div>
                </div>
                <div className='dashboard-markdown' style={{ height: '435px', display: 'flex', justifyContent: 'space-between',gap:'48px' }}>
                    <div className={styles['son-content']}>
                        <div className={styles['second-title']}>
                            {t('accessThroughCode')}
                        </div>
                        <div className={styles.desc} style={{ marginBottom: '12px' }}>{t('accessThroughCodeDesc')}</div>
                        <div className={styles['group-button']}>
                            <Button style={{ display: 'flex', alignItems: 'center' }} className='cancel-button'><span style={{ fontSize: '12px', lineHeight: '15px' }}  onClick={() => handleNavigate('apikey')}>{t('viewApiKeys')}</span></Button>
                            <Button onClick={()=>window.open('https://docs.tasking.ai/docs/guide/sdks/rest_api/authorization')} style={{ display: 'flex', alignItems: 'center' }} icon={<ForwardIcon />} className='cancel-button'><span style={{ fontSize: '12px', lineHeight: '15px' }}>{t('aboutAuth')}</span></Button>
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
                    {t('clientLibraries')}
                </div>
                <div className={styles.desc} style={{ marginBottom: '24px' }}>{t('clientLibrariesDesc')}</div>
                <div className={styles['card-bottom']}>
                    <div className={styles['card-bottom-item']}>
                        <div className={styles['card-header']}>
                            <ApiReference />
                            <span className={styles['card-bottom-title']}>REST APIs</span>
                        </div>
                        <div>
                            <Button onClick={()=>window.open('https://docs.tasking.ai/api/')} style={{ display: 'flex', alignItems: 'center' }} icon={<ForwardIcon />} className='cancel-button'><span style={{ fontSize: '12px', lineHeight: '15px' }}>{t('apiReference')}</span></Button>

                        </div>
                    </div>
                    <div className={styles['card-bottom-item']}>
                        <div className={styles['card-header']}>
                            <PythonIcon />
                            <span className={styles['card-bottom-title']}>Python SDK</span>
                        </div>
                        <div style={{ display: 'flex', gap: '12px' }}>
                            <Button onClick={()=>window.open('https://pypi.org/project/taskingai/')} className='cancel-button'>PyPI</Button>
                            <Button onClick={()=>window.open('https://docs.tasking.ai/docs/guide/sdks/python/quickstart')} style={{ display: 'flex', alignItems: 'center' }} icon={<ForwardIcon />} className='cancel-button'><span style={{ fontSize: '12px', lineHeight: '15px' }}>{t('documentation', {ns: 'common'})}</span></Button>
                        </div>
                    </div>
                    <div className={styles['card-bottom-item']}>
                        <div className={styles['card-header']}>
                            <OpenaiIcon />
                            <span className={styles['card-bottom-title']}>OpenAI compatible APIs</span>
                        </div>
                        <div style={{ display: 'flex', gap: '12px' }}>
                            <Button onClick={()=>window.open('https://platform.openai.com/docs/guides/text-generation/chat-completions-api')} className='cancel-button'>OpenAI</Button>
                            <Button onClick={()=>window.open('https://docs.tasking.ai/docs/guide/sdks/openai_compatible/overview')} style={{ display: 'flex', alignItems: 'center' }} icon={<ForwardIcon />} className='cancel-button'><span style={{ fontSize: '12px', lineHeight: '15px' }}>{t('documentation', {ns: 'common'})}</span></Button>
                        </div>
                    </div>
                    <div className={styles['card-bottom-item']}>
                        <div className={styles['card-header']}>
                            <NodeIcon />
                            <span className={styles['card-bottom-title']}>Node.js SDK</span>
                        </div>
                        <div>
                            <Button disabled type='primary'><span style={{ fontSize: '12px', lineHeight: '15px' }}>{t('comingSoon')}</span></Button>

                        </div>
                    </div>
                </div>
            </div>
        </div>

    );
}
export default DashBoard;