import { useState } from 'react';
import {
    Button,
    Modal
} from 'antd';
import styles from './deleteMoal.module.scss'
import closeIcon from '../../assets/img/x-close.svg'
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
            <Button key="back" onClick={handleCancel} className='cancel-button'>
                {t('cancel')}
            </Button>
            <Button key="submit"  onClick={handleOk} loading={deleteLoading} className={`${buttonType} ${styles.button}`}>
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
            closeIcon={<img src={closeIcon} alt="closeIcon" />}
            className={styles['delete-modals']}
            onCancel={handleCancel}
            footer={customFooter}
        >
            <p className={styles['p']}>
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
