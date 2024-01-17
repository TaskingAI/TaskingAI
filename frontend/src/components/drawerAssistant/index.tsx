import { Input, Button, Select, InputNumber } from 'antd';
import './drawerAssistant.scss'
import DeleteInputIcon from '../../assets/img/deleteInputIcon.svg?react'
import { PlusOutlined, RightOutlined } from '@ant-design/icons';
function DrawerAssistant({ handleAddPromptInput, handleMemoryChange1, inputValue1, memoryValue, handleInputValueOne, handleInputValueTwo, inputValue2, handleActionModalTable, selectedActionsRows, drawerName, selectedRetrievalRows, handleModalTable, systemPromptTemplate, handleDeletePromptInput, handleInputPromptChange, selectedRows, handleSelectModelId, handleChangeName, drawerDesc, handleDescriptionChange }) {

    const handleChangeNames = (e) => {
        handleChangeName(e.target.value)
    }
    const handleInputValue1 = (value) => {
        handleInputValueOne(value)
    }
    const handleInputValue2 = (value) => {
        handleInputValueTwo(value)
    }
    const handleDescriptionChanges = (e) => {
        handleDescriptionChange(e.target.value)
    }
    const handleSelectModelIds = () => {
        handleSelectModelId(true)
    }
    const handleInputPromptChanges = (index, newValue) => {
        handleInputPromptChange(index, newValue)
    }
    const handleDeletePromptInputs = (index) => {
        handleDeletePromptInput(index)
    }
    const handleModalTables = () => {
        handleModalTable(true)
    }
    const handleSelectActions = () => {
        handleActionModalTable(true)
    }
    const handleAddPrompt = () => {
        handleAddPromptInput()
    }
    const handleMemoryChange = (value) => {
        handleMemoryChange1(value)
    }
    return (
        <div className='drawer-assistant'>
            <div className='name-prompt'>
                Name
            </div>
            <Input value={drawerName} onChange={handleChangeNames} className='input'></Input>
            <div className='label'>
                Description
            </div>
            <div className='label-desc'>
                A description of the assistant.
            </div>
            <Input.TextArea className='input' type="text" autoSize={{ minRows: 3, maxRows: 10 }} showCount
                maxLength={200} value={drawerDesc} onChange={handleDescriptionChanges} />
            <hr className='hr'></hr>
            <div className='label'>
                <span className='span'>*</span>
                <span>{`Language model `}</span>

            </div>
            <div className='label-desc'>Enter a chat completion model ID.</div>
            <Select
                placeholder='Select a model'
                open={false}
                suffixIcon={<RightOutlined />}
                removeIcon={null}
                className='input'
                value={selectedRows} onClick={handleSelectModelIds}
            >
            </Select>
            <div className='label'>
                <span>{`System prompt template `}</span>

            </div>
            <div className='label-desc'>{`A system prompt for a chat completion model is the initial instruction that guides its response. This can incorporate a template with variable parameters, and any block without parameters is excluded from the final prompt. `}
                <a className='referToTheDocumentationFor href' href="https://docs.tasking.ai/docs/guide/assistant/components/system-prompt-template" target="_blank">
                    <span className='referToThe'>Refer to the documentation for a comprehensive understanding of the usage of the system prompt.</span>
                </a>
            </div>
            {systemPromptTemplate?.map((value, index) => (
                <div className='input-map' key={index}>
                    <Input.TextArea
                        type="text"
                        autoSize={{ minRows: 1, maxRows: 10 }}
                        value={value}
                        className='inputs'
                        placeholder='Enter system prompt'
                        onChange={(e) => handleInputPromptChanges(index, e.target.value)}
                    />
                    <DeleteInputIcon onClick={() => handleDeletePromptInputs(index)} style={{ marginTop: '8px' }} /></div>
            ))}
            <div className='add-bottom'>
                <Button onClick={handleAddPrompt} disabled={systemPromptTemplate.length === 10} icon={<PlusOutlined />}>Add</Button>
                <span>{systemPromptTemplate.length}/10</span>
            </div>
            <hr className='hr'></hr>
            <div className='label'>
                <span className='span'>*</span>
                <span>{`Memory`}</span>

            </div>
            <div className='label-desc'>{`The context memory is the assistant’s ability to retain and use information from previous interactions during a conversation to maintain continuity and relevance in responses. `}
                <a className='referToTheDocumentationFor href' href="https://docs.tasking.ai/docs/guide/assistant/components/memory" target="_blank">
                    <span className='referToThe'>Refer to the documentation to see the difference between various memory methods.</span>
                </a>
            </div>
            <Select
                onChange={handleMemoryChange}
                value={memoryValue}
                className='input'
                options={[
                    {
                        value: 'message_window',
                        label: 'Message Window',
                    },
                    {
                        value: 'zero',
                        label: 'Zero',
                    },
                    {
                        value: 'naive',
                        label: 'Naive',
                    }

                ]}>
            </Select>
            {
                memoryValue === 'message_window' && <div className='input-double'>
                    <InputNumber
                        parser={(value) => (isNaN(value) ? 1 : parseInt(value, 10))}
                        min={1}
                        max={1024}
                        placeholder='Enter max messages (from 1 to 1024)'
                        value={inputValue1}
                        onChange={(e) => handleInputValue1(e)}
                    />

                    <InputNumber parser={(value) => (isNaN(value) ? 1 : parseInt(value, 10))} min={1} max={8192} placeholder='Enter max token(from 1 to 8192)' value={inputValue2} onChange={(e) => handleInputValue2(e)}></InputNumber>
                </div>
            }

            <hr className='hr'></hr>
            <div className='desc-retrieval'>
                Retrieval
            </div>
            <div className='label-desc'>
                Enter the collection ID available in your project.
            </div>
            <Select className='input' placeholder="Select collections" onClick={handleModalTables} suffixIcon={<RightOutlined />} mode="multiple" open={false} value={selectedRetrievalRows} maxTagCount={2} removeIcon={null} />
            <hr className='hr'></hr>
            <div className='desc-retrieval'>
                Tools
            </div>
            <div className='label-desc'>
                Select the actions or tools you need from those available in your project.
            </div>
            <Select
                placeholder='Select actions'
                open={false}
                removeIcon={null}
                mode="multiple"
                className='input input-bottom'
                maxTagCount={2}
                suffixIcon={<RightOutlined />}
                value={selectedActionsRows} onClick={handleSelectActions}
            >

            </Select>
        </div>
    );
}
export default DrawerAssistant;