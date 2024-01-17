import { request } from '../utils/index'

const getActionsList = async <T extends Record<string, string>>(
    params: T,
  )=> {
const project_base_url = `api/v1`
    let str = ''
    if(params){
        Object.keys(params).forEach(key => {
            str+=`${key}=${params[key]}&`
         })
         str = str.substring(0,str.length-1)
    }
    return await request.get(`${project_base_url}/actions?${str}`)
}
const createActions = async (params:object) => {
const project_base_url = `api/v1`
    return await request.post(`${project_base_url}/actions/bulk_create`,params)
}
const updateActions = async (id:string,params:object) => {
const project_base_url = `api/v1`
    return await request.post(`${project_base_url}/actions/${id}`,params)
}
const deleteActions = async (id:string) => {
const project_base_url = `api/v1`
    return await request.delete(`${project_base_url}/actions/${id}`)
}
const getActionsDetail = async (id:string) => {
const project_base_url = `api/v1`
    return await request.get(`${project_base_url}/actions/${id}`)
}
export { getActionsList,createActions,updateActions,deleteActions,getActionsDetail }