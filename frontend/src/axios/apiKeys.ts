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
    if (params) {
        Object.keys(params).forEach(key => {
            str += `${key}=${params[key]}&`
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