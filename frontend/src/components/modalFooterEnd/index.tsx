import { useState } from 'react';
import { Button } from 'antd';
import styles from './modalFooterEnd.module.scss'
import { ModalFooterEndProps } from '@/constant/index'
import { useTranslation } from "react-i18next";
function ModalFooterEnd({ onCancel, handleOk }:ModalFooterEndProps) {
    const { t } = useTranslation(['common']);
    const [confirmLoading, setConfirmLoading] = useState(false)
    const handleCancel = () => {
        onCancel()
    }
    const handleSuccess = async () => {
        try {
            setConfirmLoading(true);
            await handleOk();
        } finally {
            setConfirmLoading(false);
        }
    }
    return (
        <div className={styles['button-footer']}>
            <Button key="cancel" onClick={handleCancel} className='cancel-button'>
                {t('cancel', {ns: 'common'})}
            </Button>
            <Button key="Confirm" onClick={handleSuccess} className={`next-button ${styles['button']}`} loading={confirmLoading}>
                {t('confirm', {ns: 'common'})}
            </Button>
        </div>
    )
}
export default ModalFooterEnd