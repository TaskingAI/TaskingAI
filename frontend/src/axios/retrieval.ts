import { request } from '../utils/index'

const getRetrievalList = async <T extends Record<string,string | number>>(
     params:T
    )=> {

    const project_base_url = `api/v1`
    let str = ''
    if (params) {
        Object.keys(params).forEach(key => {
            str += `${key}=${params[key]}&`
        })
        str = str.substring(0, str.length - 1)
    }

    return await request.get(`${project_base_url}/collections?${str}`)
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