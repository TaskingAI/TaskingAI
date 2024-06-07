import { useState } from 'react';
import {
    Button,
    Modal
} from 'antd';
import styles from './deleteMoal.module.scss'
import CloseIcon from '../../assets/img/x-close.svg?react'
import { deleteProjectType } from '@/constant/index'
import { useTranslation } from "react-i18next";
const DeleteModal = (props: deleteProjectType) => {
    const { t } = useTranslation();
    const [deleteLoading, setDeleteLoading] = useState(false)
    const { title, projectName, open, onDeleteConfirm, onDeleteCancel, describe, buttonType = 'delete-button' } = props
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
            <Button key="back" onClick={handleCancel}>
                {t('cancel')}
            </Button>
            <Button key="submit" type='primary'  onClick={handleOk} loading={deleteLoading} className={`${buttonType} ${styles.button}`}>
                {buttonType === 'delete-button' ? t('delete') : 'Confirm'}
            </Button>
        </div>
    );

    return (
        <Modal
            title={title}
            open={open}
            onOk={handleOk}
            centered
            closeIcon={<CloseIcon className={styles['img-icon-close']}/>}
            className={styles['delete-modals']}
            onCancel={handleCancel}
            footer={customFooter}
        >
            <p className={styles['p']}>
                {parts.map((part, index) => (
                    <span key={index} className={`${part.toLowerCase() === projectName?.toLowerCase() && styles['span']}`}>
                        {part}
                    </span>
                ))}
            </p>
        </Modal>
    );
};

export default DeleteModal;
