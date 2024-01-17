import { request } from '../utils/index'

const getAssistantsList = async  <T extends Record<string, string>>(
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
    return await request.get(`${project_base_url}/assistants?${str}`)
}
const createAssistant = async (params:object) => {
    const project_base_url = `api/v1`
    return await request.post(`${project_base_url}/assistants`, params)
}
const deleteAssistant = async (id:string) => {
    const project_base_url = `api/v1`
    return await request.delete(`${project_base_url}/assistants/${id}`)

}
const updateAssistant = async (id:string, params:object) => {
    const project_base_url = `api/v1`
    return await request.post(`${project_base_url}/assistants/${id}`, params)
}
const getAssistantDetail = async (id:string) => {
    const project_base_url = `api/v1`
    return await request.get(`${project_base_url}/assistants/${id}`)
}
export { getAssistantsList, createAssistant, deleteAssistant, updateAssistant, getAssistantDetail }