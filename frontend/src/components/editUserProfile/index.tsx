import React, { useState } from 'react';
import { Modal, Button, Input } from 'antd';
import ModalFooter from '../modalFooter/index';
import closeIcon from '../../assets/img/x-close.svg'
import './editUserProfile.scss'
const EditableModal = ({ open, onCancel, onOk }) => {
    const [content, setContent] = useState('');
    const [input, setInput] = useState('')
    const handleOk = async () => {
       await onOk(input, content)
        setContent('')
        setInput('')
    };
    const handleCancel = () => {
        onCancel(); 
        setContent('')
        setInput('')

    };

    return (
        <Modal
            title={
                <div className='title'>
                    Edit User Profile
                </div>
            }
            open={open}
            centered
            onCancel={handleCancel}
            closeIcon={<img src={closeIcon} alt="closeIcon" />}
            footer={<ModalFooter handleOk={handleOk} onCancel={handleCancel} />}
            width={600}
        >
            <div className='modal'>
                <div className='required-label'>
                <span className='required-span'>*</span>
                    <span>{`First name `}</span> 
                </div>
                <Input placeholder="Enter first name" className='input-top' onChange={(e) => setInput(e.target.value)} value={input} />
                <div className='required-label'>
                <span className='required-span'>*</span>
                    <span>{`Last name `}</span>
                  
                </div>
                <Input
                    placeholder="Enter last name"
                    value={content}
                    className='input'
                    onChange={(e) => setContent(e.target.value)}
                />
            </div>

        </Modal>
    );
};

export default EditableModal;
