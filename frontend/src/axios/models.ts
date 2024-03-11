import { request } from '../utils/index'

const getAiModelsList = async (offset: number, limit: number, type: string, providerId: string) => {
    const project_base_url = `api/v1`
    if (type) {
        return await request.get(`${project_base_url}/model_schemas?offset=${offset}&limit=${limit}&type=${type}&provider_id=${providerId}`)
    } else {
        return await request.get(`${project_base_url}/model_schemas?offset=${offset}&limit=${limit}&provider_id=${providerId}`)
    }
}

const getAiModelsForm = async (id: string) => {
    const project_base_url = `api/v1`
    return await request.get(`${project_base_url}/providers/get?provider_id=${id}`)
}
const getModelsList = async <T extends Record<string, string | number>>(
    params: T,
    type?: string
) => {
    const project_base_url = `api/v1`
    let str = ''
    const data = params
    if (data.hasOwnProperty('name_search')) {
        str += `prefix_filter={"name":"${data.name_search}"}&`
        delete data.name_search
    } else if (data.hasOwnProperty('id_search')) {
        str += `prefix_filter={"model_id":"${data.id_search}"}&`
        delete data.id_search
    }
    if (data) {
        Object.keys(data).forEach(key => {
            str += `${key}=${data[key]}&`
        })
        str = str.substring(0, str.length - 1)
    }

    if (type) {
        return await request.get(`${project_base_url}/models?${str}&equal_filter={"type": "${type}"}`)
    } else {
        return await request.get(`${project_base_url}/models?${str}`)
    }
}
const updateModels = async (model_id: string, params: object) => {
    const project_base_url = `api/v1`
    return await request.post(`${project_base_url}/models/${model_id}`, params)
}
const deleteModels = async (model_id: string) => {
    const project_base_url = `api/v1`
    return await request.delete(`${project_base_url}/models/${model_id}`)
}
const createModels = async (params: object) => {
    const project_base_url = `api/v1`
    return await request.post(`${project_base_url}/models`, params)
}
const getModelsForm = async (id: string) => {
    const project_base_url = `api/v1`
    return await request.get(`${project_base_url}/models/${id}?include_credentials_schema=true&include_display_credentials=true`)
}
const getModelProviderList = async (type: string) => {
    const project_base_url = `api/v1`
    if (type) {
        return await request.get(`${project_base_url}/providers?type=${type}&limit=100`)
    } else {
        return await request.get(`${project_base_url}/providers?limit=100`)
    }
}
export { getAiModelsList, getModelsList, updateModels, deleteModels, createModels, getAiModelsForm, getModelsForm, getModelProviderList }