import { request } from '../utils/index'

const getRetrievalList = async <T extends Record<string,string | number>>(
     params:T
    )=> {

    const project_base_url = `api/v1`
    const data = params
    let str = ''
    if (data.hasOwnProperty('name_search')) {
        str += `prefix_filter={"name":"${data.name_search}"}&`
        delete data.name_search
    } else if (data.hasOwnProperty('id_search')) {
        str += `prefix_filter={"collection_id":"${data.id_search}"}&`
        delete data.id_search
    }
    if (data) {
        Object.keys(data).forEach(key => {
            str += `${key}=${data[key]}&`
        })
        str = str.substring(0, str.length - 1)
    }
    return await request.get(`${project_base_url}/ui/collections?${str}`)
}
const createRetrieval = async (params:object) => {

    const project_base_url = `api/v1`
    return await request.post(`${project_base_url}/collections`, params)
}
const deleteRetrieval = async (id:string) => {

    const project_base_url = `api/v1`
    return await request.delete(`${project_base_url}/collections/${id}`)

}
const updateRetrieval = async (id:string, params:object) => {

    const project_base_url = `api/v1`
    return await request.post(`${project_base_url}/collections/${id}`, params)
}
export { getRetrievalList, createRetrieval, deleteRetrieval, updateRetrieval }