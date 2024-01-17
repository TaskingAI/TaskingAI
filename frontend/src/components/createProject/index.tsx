import React, { useState } from 'react';
import { Modal, Button, Input } from 'antd';
import closeIcon from '../../assets/img/x-close.svg'
import './CreateProject.scss'
const EditableModal = ({ open, onCancel, onOk }) => {
    const [content, setContent] = useState('');
    const [input, setInput] = useState('')
    const [loading, setLoading] = useState(false)
    const handleOk = async () => {
        await setLoading(true)
        await onOk(input, content)
        setContent('')
        setInput('')
        await setLoading(false)
    };
    const handleCancel = () => {
        setContent('')
        setInput('')
        onCancel();
    };

    return (
        <Modal
            title={
                <div className='title'>
                    Create Project
                </div>
            }
            className='create-project'
            centered
            open={open}
            onCancel={handleCancel}
            closeIcon={<img src={closeIcon} alt="closeIcon" />}
            footer={[
                <Button key="cancel" onClick={handleCancel} className='cancel-button'>
                    Cancel
                </Button>,
                <Button key="submit" loading={loading} onClick={handleOk} className='next-button'>
                    Confirm
                </Button>
            ]}
            width={720}
        >
            <div className='required-label'>
            <span className='required-span'>*</span>
                <span>{`Project name `}</span>
               
            </div>
            <div className="project-indu-model project-indu">The name of your project. Every project in your organization should have a unique name.</div>
            <Input placeholder="Enter project name" onChange={(e) => setInput(e.target.value)} value={input} />

            <div className='required-label-two required-label'>
            <span className='required-span'>*</span>
                <span>{`Project description `}</span>
         
            </div>
            <div className="project-indu project-indu-model">A brief description of the purpose of your project</div>
            <Input.TextArea
                placeholder="Enter porject description"
                value={content}
                className='input'
                showCount
                maxLength={200}
                onChange={(e) => setContent(e.target.value)}
            />
        </Modal>

    );
};

export default EditableModal;
