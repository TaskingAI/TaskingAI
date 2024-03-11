import { request } from '../utils/index'

const getActionsList = async <T extends Record<string, any>>(
    params: T,
) => {
    const project_base_url = `api/v1`
    const data = params
    let str = ''
    if (data.hasOwnProperty('name_search')) {
        str += `prefix_filter={"name":"${data.name_search}"}&`
        delete data.name_search
    } else if (data.hasOwnProperty('id_search')) {
        str += `prefix_filter={"action_id":"${data.id_search}"}&`
        delete data.id_search
    }
    if (data) {
        Object.keys(data).forEach(key => {
            str += `${key}=${data[key]}&`
        })
        str = str.substring(0, str.length - 1)
    }
    return await request.get(`${project_base_url}/actions?${str}`)
}
const createActions = async (params: object) => {
    const project_base_url = `api/v1`
    return await request.post(`${project_base_url}/actions/bulk_create`, params)
}
const updateActions = async (id: string, params: object) => {
    const project_base_url = `api/v1`
    return await request.post(`${project_base_url}/actions/${id}`, params)
}
const deleteActions = async (id: string) => {
    const project_base_url = `api/v1`
    return await request.delete(`${project_base_url}/actions/${id}`)
}
const getActionsDetail = async (id: string) => {
    const project_base_url = `api/v1`
    return await request.get(`${project_base_url}/actions/${id}`)
}
export { getActionsList, createActions, updateActions, deleteActions, getActionsDetail }