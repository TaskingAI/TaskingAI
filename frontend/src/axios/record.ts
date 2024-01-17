import { request } from '../utils/index'

const getRecordsList = async <T extends Record<string,string>>(params:T,collectionId:string)=> {
const project_base_url = `api/v1`
    let str = ''
    if(params){
        Object.keys(params).forEach(key => {
            str+=`${key}=${params[key]}&`
         })
         str = str.substring(0,str.length-1)
    }
    return await request.get(`${project_base_url}/collections/${collectionId}/records?${str}`)
}
const createRecord = async (collectionId:string,params:object) => {
const project_base_url = `api/v1`
    return await request.post(`${project_base_url}/collections/${collectionId}/records`, params)
}
const deleteRecord = async (collectionId:string,id:string) => {
const project_base_url = `api/v1`
    return await request.delete(`${project_base_url}/collections/${collectionId}/records/${id}`)

}
const updateRecord = async (collectionId:string,id:string,params:object) => {
const project_base_url = `api/v1`
    return await request.post(`${project_base_url}/collections/${collectionId}/records/${id}`,params)
}
const getRecord = async (collectionId:string,id:string) => {
const project_base_url = `api/v1`
    return await request.get(`${project_base_url}/collections/${collectionId}/records/${id}`)
}
export { getRecordsList,createRecord,deleteRecord,updateRecord,getRecord }