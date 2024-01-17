import { useState } from 'react';
import { Button } from 'antd';
import './modalFooter.scss'

function ModalFooter({onCancel,handleOk}) {
    const [loading, setLoading] = useState(false)
    const handleCancel=()=>{
        onCancel()
    }
    const handleSuccess=async ()=>{
        await setLoading(true)
        await handleOk()
       await setLoading(false)
    }
    return (
        <div className='button'>
            <Button key="cancel" onClick={handleCancel} className='cancel-button'>
                Cancel
            </Button>
            <Button key="Confirm" onClick={handleSuccess} className='next-button' loading={loading}>
                Confirm
            </Button>
        </div>
    )
}
export default ModalFooter