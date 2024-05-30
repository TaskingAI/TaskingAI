import { request } from '../utils/index'

const getRecordsList = async <T extends Record<string, string>>(collectionId: string, params: T) => {
    const project_base_url = `api/v1`
    const data = params
    let str = ''
    if (data.hasOwnProperty('name_search')) {
        str += `prefix_filter={"name":"${data.name_search}"}&`
        delete data.name_search
    } else if (data.hasOwnProperty('id_search')) {
        str += `prefix_filter={"chunk_id":"${data.id_search}"}&`
        delete data.id_search
    }
    if (data) {
        Object.keys(data).forEach(key => {
            str += `${key}=${data[key]}&`
        })
        str = str.substring(0, str.length - 1)
    }
    return await request.get(`${project_base_url}/collections/${collectionId}/chunks?${str}`)
}
const createRecord = async (collectionId: string, params: object) => {
    const project_base_url = `api/v1`
    return await request.post(`${project_base_url}/collections/${collectionId}/chunks`, params)
}
const deleteRecord = async (collectionId: string, id: string) => {
    const project_base_url = `api/v1`
    return await request.delete(`${project_base_url}/collections/${collectionId}/chunks/${id}`)

}
const updateRecord = async (collectionId: string, id: string, params: object) => {
    const project_base_url = `api/v1`
    return await request.post(`${project_base_url}/collections/${collectionId}/chunks/${id}`, params)
}
const getRecord = async (collectionId: string, id: string) => {
    const project_base_url = `api/v1`
    return await request.get(`${project_base_url}/collections/${collectionId}/chunks/${id}`)
}
export { getRecordsList, createRecord, deleteRecord, updateRecord, getRecord }