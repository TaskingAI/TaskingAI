import React, { useState } from 'react';
import {
    Button,
    Modal
} from 'antd';
import './deleteMoal.module.scss'
import closeIcon from '../../assets/img/x-close.svg'

const DeleteModal = (props) => {
    const [deleteLoading, setDeleteLoading] = useState(false)
    const { title, projectName, open, onDeleteConfirm, onDeleteCancel, describe } = props
    const parts = describe.split(new RegExp(`(${projectName})`, 'i'))
    const handleOk = async () => {
        await setDeleteLoading(true)
        await onDeleteConfirm()
        await setDeleteLoading(false)
    };

    const handleCancel = () => {
        onDeleteCancel()
    };

    const customFooter = (
        <div>
            <Button key="back" onClick={handleCancel} className='cancel-button'>
                Cancel
            </Button>
            <Button key="submit" type="primary" onClick={handleOk} danger loading={deleteLoading} className='delete-button'>
                Delete
            </Button>
        </div>
    );

    return (
        <Modal
            title={title}
            open={open}
            onOk={handleOk}
            centered
            closeIcon={<img src={closeIcon} alt="closeIcon" />}
            className='delete-modals'
            onCancel={handleCancel}
            footer={customFooter}
        >
            <p className='p'>
                {parts.map((part, index) => (
                    <span key={index} style={part.toLowerCase() === projectName?.toLowerCase() ? { color: '#087443' } : {}}>
                        {part}
                    </span>
                ))}
            </p>
        </Modal>
    );
};

export default DeleteModal;
