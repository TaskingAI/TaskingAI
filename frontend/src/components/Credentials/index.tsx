import './credentials.scss'
import { Collapse, Form, Input, Space, Button } from 'antd'
import { useLocation } from 'react-router-dom';
import queryString from 'query-string';

import ModelProvider from '../../assets/img/ModelProvider.svg'
import Frame from '../../assets/img/Frame.svg'
import Anthropic from '../../assets/img/Anthropic.svg'
import { getCredentialList, createCredential } from '../../axios/credential'
import { useEffect, useState } from 'react'
const { Panel } = Collapse;
function Credentials() {
    const location = useLocation();
    
    const [credentialList, setCredentialList] = useState([])
    const [form1] = Form.useForm();
    const [form2] = Form.useForm();
    const [formMap, setFormMap] = useState({
        'openai': form1,
        'azure_openai': form2,
    });
    const { provider_id } = queryString.parse(location.search);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const res = await getCredentialList()

                setCredentialList(res.data)
            } catch (error) {
                console.log(error)
            }
        };

        fetchData();
    }, []);

    const onFinish = async (val, id) => {
        const params = {
            provider_id: id,
            credentials: val
        }
        await createCredential(params)
    }

    const onCancel = (providerId) => {
        formMap[providerId].resetFields();
    };

    return (
        <div className='credential'>
            <div className='youreAStep1'>You're a step closer to harnessing the power of your chosen Large Language Model (LLM). On the Credentials Configuration Page, ensure secure and seamless integration by inputting your subscribed API key. Your privacy is paramount to us; rest assured that any information you provide is treated with utmost confidentiality. We employ advanced encryption methods to safeguard your credentials, ensuring they remain solely for platform-LLM interactions. Prioritize security, privacy, and efficiency as you pave the way for enhanced AI functionalities.</div>
            <Collapse defaultActiveKey={[provider_id]} accordion>
                {credentialList.map((item) => (

                    <Panel header={<CustomHeader register={item.registered} providerId={item.provider_id} />} key={item.provider_id}>
                        <Form
                            layout="vertical"
                            autoComplete="off"
                            form={formMap[item.provider_id]}
                            name={item.provider_id}
                            onFinish={(val) => onFinish(val, item.provider_id)}
                        >
                            {Object.entries(item.credentials_schema.properties).map(([key, property]) => (
                                <Form.Item
                                    key={key}
                                    name={key}
                                    label={key}
                                    className='form-item'
                                    rules={[
                                        {
                                            required: true,
                                            message: `Please input ${key}!`,
                                        },
                                    ]}
                                >
                                    <div>
                                        <div className='description'>{property.description}</div>
                                        <Input placeholder={`Enter ${key}`} className='input' />
                                    </div>
                                </Form.Item>
                            ))}
                            <Form.Item className='button-bottom'>
                                <Button htmlType="button" onClick={() => onCancel(item.provider_id)}>
                                    Cancel
                                </Button>
                                <Button className='sub-button' htmlType='submit'>
                                    Confirm
                                </Button>
                            </Form.Item>
                            </Form>
                    </Panel>
                      
                ))}
        </Collapse>
        </div >
    )
}
const CustomHeader = (props) => {
    const renderItem = (providerId) => {
        if (providerId === 'openai') {
            return <div className='left-header'>
                <img src={ModelProvider} className='img' />
                <span>OpenAI</span>
            </div>
        } else if (providerId === 'azure_openai') {
            return <div className='left-header'>
                <img src={Frame} className='img' />
                <span>Azure OpenAI</span>
            </div>
        } else if (providerId === 'anthropic') {
            return <div className='left-header'>
                <img src={Anthropic} className='img' />
                <span>Anthropic</span>
            </div>
        }
    }
    return (
        <div className='custom-header'>
            {renderItem(props.providerId)}
            {!props.registered ? <div className='divroundedMd'>
                <div className='disabled'>Disabled</div>
            </div> : <div className='divroundedMdEnabled'>
                <div className='disabled'>Enabled</div>
            </div>}

        </div>
    );
};
export default Credentials