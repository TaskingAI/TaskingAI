export const setPlaygroundSelect = (type:string)=>({
    type:'PLAYGROUND_TYPE',
    payload: type
})
export const setPlaygroundAssistantId = (type:string)=>({
    type:'ASSISTANT_ID',
    payload: type
})
export const setPlaygroundModelId = (type:string)=>({
    type:'MODEL_ID',
    payload: type
})
export const setPlaygroundModelName = (type:string)=>({
    type:'MODEL_NAME',
    payload: type
})
export const setTemperatureData = (temperatureData: any) => ({
    type: 'TEMPERATURE_DATA',
    payload: temperatureData,
})
export const setStopSequencesData = (stopSequencesData: any) => ({
    type: 'STOP_SEQUENCES_DATA',
    payload: stopSequencesData,
})
export const setMaxTokenData = (maxTokenData: any) => ({
    type: 'MAX_TOKEN_DATA',
    payload: maxTokenData,
})
export const setTopKData = (topKData: any) => ({
    type: 'TOP_K_DATA',
    payload: topKData,
})
export const setTopPData = (topPData: any) => ({
    type: 'TOP_P_DATA',
    payload: topPData,
})