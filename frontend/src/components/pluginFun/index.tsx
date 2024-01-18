import './pluginFun.scss'
import { PlusOutlined, SyncOutlined, CopyOutlined, CloseCircleOutlined } from '@ant-design/icons';
import { useEffect, useState } from 'react'
import ModalFooterEnd from '../modalFooterEnd/index'
import {
    Button,
    Space, Table, Tag,  Drawer, Input, Select, Checkbox, Spin
} from 'antd';
import { toast } from 'react-toastify'
import ClipboardJS from 'clipboard';
import DeleteModal from '../deleteModal'
import {formatTimestamp} from '@/utils/util'
import { deletePluginFun, createPluginFun, getPluginList, editPluginFun } from '../../axios/pluginFun'
import closeIcon from '../../assets/img/x-close.svg'
const handleCopy = (text) => {
    const clipboard = new ClipboardJS('.icon-copy', {
        text: () => text
    });
    clipboard.on('success', function () {
        toast.success('Copied to clipboard')
        clipboard.destroy()
    });
    clipboard.on('error', function (e) {
        console.log(e);
    });
}
function convertToParameterSchema(data) {
    const parameterSchema = {
        type: 'object',
        properties: {},
        required: [],
    };

    data.forEach((item) => {
        const {  name, type, required, description } = item;

        parameterSchema.properties[name] = {
            type,
            description,
        };

        if (required) {
            parameterSchema.required.push(name);
        }
    });

    return { parameter_schema: parameterSchema };
}
function convertToNewFormat(data) {
    return data.map((item, index) => {
        const properties = item.parameters.properties;
        const parameters = Object.keys(properties);

        return {
            key: (index + 1).toString(),
            name: item.name,
            description: item.description,
            parameters: parameters,
            created_timestamp: item.created_timestamp,
            item
        };
    });
}
const transformObject = (jsonObject) => {
    const result = [];
    const properties = jsonObject.properties || {};
    const requiredFields = jsonObject.required || [];

    Object.keys(properties).forEach((key, index) => {
        const property = properties[key];
        const isRequired = requiredFields.includes(key);

        const transformedItem = {
            key: index + 1,
            name: key,
            type: property.type || '',
            required: isRequired,
            description: property.description || '',
        };

        result.push(transformedItem);
    });

    return result;
};
const { TextArea } = Input
function PluginFun() {
    const [pluginFunList, setPluginFunList] = useState([])
    const [OpenDeleteModal, setOpenDeleteModal] = useState(false)
    const [deleteValue, setDeleteValue] = useState('')
    const [OpenDrawer, setOpenDrawer] = useState(false)
    const [PluginId, setPluginId] = useState('')
    const [drawerName, setDrawerName] = useState('')
    const [loading, setLoading] = useState(false);
    const [drawerDescription, setDrawerDescription] = useState('')
    const [drawerTitle, setDrawerTitle] = useState('Create Function')
    const [dataDrawer, setDataSource] = useState([]);
    const [pagination, setPagination] = useState({
        current: 1,
        pageSize: 20,
        total: 0,
        showSizeChanger: true,
    });
    const [tipErrorShow, setTipErrorShow] = useState(false)
    useEffect(() => {
        fetchData(0, 20);
    }, []);

    const fetchData = async (offset, limit) => {
        setLoading(true);
        try {
            const res:any = await getPluginList(offset, limit)
            setPluginFunList(convertToNewFormat(res.data));
            setPagination({
                ...pagination,
                current: offset / limit + 1,
                pageSize: limit,
                total: res.total_count,
            })
        } catch (error) {
            console.log(error)
        }
        setLoading(false);
    };
    const handleReset = async () => {
        await fetchData(0, 20)
    }
    const handleCreatePrompt = async () => {
        setDrawerTitle('Create Function')
        setOpenDrawer(true)
        setDrawerName('')
        setPluginId('')
        setDrawerDescription('')
        setDataSource([])
    }
    const columns = [
        {
            title: 'Name',
            dataIndex: 'name',
            key: 'name',
            render: (text,record) =>
                <div>
                    <p className='table-text'>{text}</p>
                    <span>{record.item.function_id}</span><CopyOutlined className='icon-copy' onClick={() => handleCopy(record.item.function_id)} />
                </div>
            ,
        },
        {
            title: 'Description',
            dataIndex: 'description',
            key: 'description',
            render: (text) => (
                <>
                    <div>{text}</div>
                </>
            ),
        },
        {
            title: 'Parameters',
            dataIndex: 'parameters',
            key: 'parameters',
            render: (_) => (
                <>
                    {_.map((item, index) => (
                        <Tag color='green' key={index}>
                            {item}
                        </Tag>
                    ))}
                </>
            ),
        },
        {
            title: 'Created at',
            dataIndex: 'created_timestamp',
            key: 'created_timestamp',
            render: (time) => <div>{formatTimestamp(time)}</div>
        },
        {
            title: 'Actions',
            key: 'action',
            render: (_, record) => (
                <Space size="middle">
                    <Button onClick={() => handleEdit(record)} className='cancel-button'>Edit</Button>
                    <Button onClick={() => handleDelete(record)} className='cancel-button'>Delete</Button>
                </Space>
            ),
        },
    ];
    const handleDropdownChange = (key, value) => {
        setDataSource((prevDataSource) =>
            prevDataSource.map((record) =>
                record.key === key ? { ...record, type: value } : record
            )
        );
    };
    const handleCheckboxChange = (key, checked) => {
        setDataSource((prevDataSource) =>
            prevDataSource.map((record) =>
                record.key === key ? { ...record, required: checked } : record
            )
        );
    };
    const handleDeleteDrawer = (key) => {
        const newData = dataDrawer.filter(item => item.key !== key);
        setDataSource(newData)
    }
    const handleInputChange = (key, inputValue) => {
        setDataSource((prevDataSource) =>
            prevDataSource.map((record) =>
                record.key === key ? { ...record, description: inputValue } : record
            )
        );
    };
    const handleInputNameChange = (key, inputValue) => {
        setDataSource((prevDataSource) =>
            prevDataSource.map((record) =>
                record.key === key ? { ...record, name: inputValue } : record
            )
        );
    }
    const columnsDrawer = [
        {
            title: 'Name',
            dataIndex: 'name',
            key: 'name',
            render: (text, record) => (
                <Input.TextArea
                    autoSize={{ minRows: 1, maxRows: 10 }}
                    value={text}
                    onChange={(e) => handleInputNameChange(record.key, e.target.value)}
                />
            ),
        },
        {
            title: 'Type',
            dataIndex: 'type',
            key: 'type',
            render: (text, record) => (
                <Select
                    value={text}
                    style={{ width: 120 }}
                    onChange={(value) => handleDropdownChange(record.key, value)}
                >
                    <Select.Option value="string">String</Select.Option>
                    <Select.Option value="number">Number</Select.Option>
                    <Select.Option value="boolean">Boolean</Select.Option>
                    <Select.Option value="integer">Integer</Select.Option>
                </Select>
            )
        },
        {
            title: 'Required',
            dataIndex: 'required',
            key: 'required',
            render: (text, record) => (
                <Checkbox
                    checked={text}
                    onChange={(e) => handleCheckboxChange(record.key, e.target.checked)}
                />
            ),
        },
        {
            title: 'Description',
            dataIndex: 'description',
            key: 'description',
            render: (text, record) => (
                <Input.TextArea
                    autoSize={{ minRows: 1, maxRows: 10 }}
                    value={text}
                    onChange={(e) => handleInputChange(record.key, e.target.value)}
                />
            ),
        },
        {
            title: ' ',
            key: 'action',
            render: (_, record) => (
                <CloseCircleOutlined onClick={() => handleDeleteDrawer(record.key)} />
            ),
        }
    ];

    const handleEdit = (val) => {
        setDrawerTitle('Edit Function')
        setOpenDrawer(true)
        setDrawerName(val.name)
        setDrawerDescription(val.description)
        setPluginId(val.item.plugin_function_id)
        setDataSource(transformObject(val.item.parameter_schema))
    }
    const handleCancel = () => {
        setOpenDrawer(false)
    }
    const handleDelete = (val) => {
        setOpenDeleteModal(true)
        setDeleteValue(val.name)
        setPluginId(val.item.plugin_function_id)
    }
    const onDeleteCancel = () => {
        setOpenDeleteModal(false)
    }
    const handleAdd = () => {
        setDataSource((prevDataSource) =>
            prevDataSource.concat({
                name: '',
                type: 'string',
                required: false,
                description: '',
            })
        );

    }
    const handleRequest = async (name, desc, table) => {
        if (!name || !name.trim() || !desc || !desc.trim()) {
            toast.error('Missing required parameters')
            return
        }
        try {
            if (PluginId) {
                await editPluginFun(name, desc, convertToParameterSchema(table).parameter_schema, PluginId)
            } else {
                await createPluginFun(name, desc, convertToParameterSchema(table).parameter_schema)
            }
            await fetchData(0, 20)
            setOpenDrawer(false)

        } catch (e) {
            toast.error(e.response.data.error.code)
        }

    }
    // Function name
    const handleNameChange = (e) => {
        // must start with a letter and can include lowercase words, digits, and the underscore '_', and it is unique within the same self-hosted function collection.
        const regex = /^[a-zA-Z][a-zA-Z0-9_]*$/;
        if (!regex.test(e.target.value)) {
            setTipErrorShow(true)
        }else {
            setTipErrorShow(false)
        }
        setDrawerName(e.target.value)
    }
    // Function description
    const handleDescriptionChange = (e) => {
        setDrawerDescription(e.target.value)
    }
    const handleTableChange = async (pagination) => {
        await fetchData((pagination.current - 1)*pagination.pageSize, pagination.pageSize)
    }
    const onDeleteConfirm = async () => {
        try {
            await deletePluginFun(PluginId)
            await fetchData(0, 20)
        } catch (error) {
            console.log(error)
        }
        setOpenDeleteModal(false)
    }
    return (
        <div className="plugin-fun">
   
            <div className='header-prompts'>
                <div className='plusParent'>
                    <div className='arrowSyncParent' onClick={handleReset}>
                        <SyncOutlined />
                    </div>
                    <Button icon={<PlusOutlined />} className='prompt-button' onClick={handleCreatePrompt}>New function</Button>
                </div>
            </div>
            <Spin spinning={loading}>
                <Table columns={columns} dataSource={pluginFunList} pagination={pagination} onChange={handleTableChange} className={pluginFunList.length && 'table-custom'} />
            </Spin>

            <DeleteModal open={OpenDeleteModal} title='Delete Function' projectName={deleteValue} onDeleteCancel={onDeleteCancel} onDeleteConfirm={onDeleteConfirm} />
            <Drawer closeIcon={<img src={closeIcon} alt="closeIcon" className='img-icon-close' />} onClose={handleCancel} title={drawerTitle} placement="right" open={OpenDrawer} size='large' footer={<ModalFooterEnd handleOk={() => handleRequest(drawerName, drawerDescription, dataDrawer)} onCancel={handleCancel} />}>
                <div className='plugin-drawer'>
                    <div className='label-name'>
                    <span className='span'> *</span>
                        <span>Name</span>
                  
                    </div>
                    <div className='label-description'>The function name is a meaningful text string that must start with a letter and can include lowercase words, digits, and the underscore '_', and it is unique within the same self-hosted function collection.</div>
                    <Input className='input-drawer' value={drawerName} onChange={handleNameChange}></Input>
                    <span className={`tip-error ${tipErrorShow ? 'show' : ''}`}>Incorrect input format.</span>
                    <div className='label'>
                    <span className='span'> *</span>
                        <span>Description</span>
                      
                    </div>
                    <div className='label-description'>Briefly and accurately describe what the function does. The language model will learn to choose when and how to call this function.</div>
                    <TextArea className='input-drawer' value={drawerDescription} onChange={handleDescriptionChange} showCount maxLength={200}></TextArea>
                    <div className='label'>
                    <span className='span'> *</span>
                        <span>Variable schema</span>
                   
                    </div>
                    <div className='label-description'>
                        Define the parameters your function accepts.
                    </div>
                    <Table columns={columnsDrawer} dataSource={dataDrawer} className='table-drawer' pagination={false} />
                    <div className='add-bottom'>
                        <Button onClick={handleAdd} disabled={dataDrawer.length === 5} icon={<PlusOutlined />}>Add</Button>
                        <span>{dataDrawer.length}/5</span>
                    </div>
                </div>
            </Drawer>
        </div>
    )
}
export default PluginFun