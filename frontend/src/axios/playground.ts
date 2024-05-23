import { request } from '../utils/index'

const openChat = async (id:string, params:object) => {
    const project_base_url = `api/v1`
    return await request.post(`${project_base_url}/assistants/${id}/chats`, params)
}
const sendMessage = async (assistantsId:string, chatId:string, params:object) => {
    const project_base_url = `api/v1`
    return await request.post(`${project_base_url}/assistants/${assistantsId}/chats/${chatId}/messages`, params)
}
const getChatItem = async (assistantsId:string, chatId:string) => {
    const project_base_url = `api/v1`
    return await request.get(`${project_base_url}/assistants/${assistantsId}/chats/${chatId}`)

}
const getListChats = async  <T extends Record<string, any>>(
    assistantsId:string,
    params: T

  ) => {
    const project_base_url = `api/v1`
    let str = ''
    if (params) {
        Object.keys(params).forEach(key => {
            str += `${key}=${params[key]}&`
        })
        str = str.substring(0, str.length - 1)
    }
    return await request.get(`${project_base_url}/assistants/${assistantsId}/chats?${str}`)
}
const generateMessage = async (assistantsId:string, chatId:string, params:object) => {
    const project_base_url = `api/v1`
    return await request.post(`${project_base_url}/assistants/${assistantsId}/chats/${chatId}/generate`, params)
}
const deleteChatItem = async (assistantsId:string, chatId:string) => {
    const project_base_url = `api/v1`
    return await request.delete(`${project_base_url}/assistants/${assistantsId}/chats/${chatId}`)
}
const getHistoryMessage = async  <T extends Record<string, string>>(
    assistantsId:string,
    chatId:string,
    params: T,

  ) => {
    const project_base_url = `api/v1`
    let str = ''

    if (params) {
        Object.keys(params).forEach(key => {
            str += `${key}=${params[key]}&`
        })
        str = str.substring(0, str.length - 1)
    }
    return await request.get(`${project_base_url}/assistants/${assistantsId}/chats/${chatId}/messages?${str}`)

}
const modalGenerate = async (params:object) => {
    const project_base_url =`api/v1`
    return await request.post(`${project_base_url}/inference/chat_completion`, params)
}
export { openChat,getChatItem, sendMessage,modalGenerate, generateMessage, getListChats, getHistoryMessage,deleteChatItem }