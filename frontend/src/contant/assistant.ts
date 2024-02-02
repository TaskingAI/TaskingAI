interface valueLimit {
    limit: number,
    [key: string]: string | number;
}
interface assistantListType {
    assistant_id: string,
    id: string,
    retrievals: any[],
    tools: any[],
    name: string,
    description: string,
    max_messages: number,
    max_tokens: number,
    memory: string,
    system_prompt_template: string[],
    model_id: string,
}
interface authenticationType {
    type: string
    content?: any
    secret?: string
}
interface commonDataType {
    openapi_schema: string,
    authentication?: authenticationType
}
interface modelModalProps {
    handleSetModelOne: (value: any) => void;
    modelType?: string;
    getOptionsList: (object: object, modelType: string) => void;
    handleSetModelConfirmOne: (value: boolean) => void;
    open: boolean;
}
interface DrawerAssistantProps {
    handleAddPromptInput: () => void;
    handleMemoryChange1: (value: string) => void;
    inputValue1: number;
    memoryValue: string;
    handleInputValueOne: (value: number) => void;
    handleInputValue2?: (value: string) => void;
    handleInputValueTwo: (value: number) => void;
    inputValue2: number;
    handleActionModalTable: (value: any) => void;
    selectedActionsRows: any[];
    drawerName: string;
    selectedRetrievalRows: any[];
    handleModalTable: (value: any) => void;
    systemPromptTemplate: string[];
    handleDeletePromptInput: (index: number) => void;
    handleInputPromptChange: (index: number, value: string) => void;
    selectedRows: any[];
    handleSelectModelId: (value: boolean) => void;
    handleChangeName: (value: string) => void;
    drawerDesc: string;
    handleDescriptionChange: (value: string) => void;
}
export type { valueLimit, DrawerAssistantProps, assistantListType, commonDataType, modelModalProps }