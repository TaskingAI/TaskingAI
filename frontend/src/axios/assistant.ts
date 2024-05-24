import { request } from '../utils/index'

const getAssistantsList = async  <T extends Record<string, any>>(
    params: T,
) => {
    const project_base_url = `api/v1`
    let str = ''
    const data = params
    if (data.hasOwnProperty('name_search')) {
        str += `prefix_filter={"name":"${data.name_search}"}&`
        delete data.name_search
    } else if (data.hasOwnProperty('id_search')) {
        str += `prefix_filter={"assistant_id":"${data.id_search}"}&`
        delete data.id_search
    }
    if (data) {
        Object.keys(data).forEach(key => {
            str += `${key}=${data[key]}&`
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