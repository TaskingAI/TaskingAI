import { request } from '../utils/index'

const createApiKeys = async (params: object) => {
    const project_base_url = `api/v1`
    return await request.post(`${project_base_url}/apikeys`, params)
}
const getApiKeysList = async  <T extends Record<string, string>>(
    params: T,
) => {
    const project_base_url = `api/v1`
    let str = ''
    const data = params

    if (data.hasOwnProperty('name_search')) {
        str += `prefix_filter={"name":"${data.name_search}"}&`
        delete data.name_search
    } else if (data.hasOwnProperty('id_search')) {
        str += `prefix_filter={"apikey_id":"${data.id_search}"}&`
        delete data.id_search
    }
    if (data) {
        Object.keys(data).forEach(key => {
            str += `${key}=${data[key]}&`
        })
        str = str.substring(0, str.length - 1)
    }
    return await request.get(`${project_base_url}/apikeys?${str}`)
}
const getApiKeys = async (id: string, plain: string) => {
    const project_base_url = `api/v1`
    return await request.get(`${project_base_url}/apikeys/${id}?plain=${plain}`)
}
const updateApiKeys = async (id, params: object) => {
    const project_base_url = `api/v1`
    return await request.post(`${project_base_url}/apikeys/${id}`, params)
}
const deleteApiKeys = async (id) => {
    const project_base_url = `api/v1`
    return await request.delete(`${project_base_url}/apikeys/${id}`)
}
export { createApiKeys, getApiKeysList, getApiKeys, updateApiKeys, deleteApiKeys }