import { useState } from 'react';
import { Button } from 'antd';
import './modalFooterEnd.scss'

function ModalFooterEnd({ onCancel, handleOk }) {
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
        <div className='button-footer'>
            <Button key="cancel" onClick={handleCancel} className='cancel-button'>
                Cancel
            </Button>
            <Button key="Confirm" onClick={handleSuccess} className='next-button' loading={confirmLoading}>
                Confirm
            </Button>
        </div>
    )
}
export default ModalFooterEnd