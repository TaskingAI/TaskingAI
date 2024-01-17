import { request } from '../utils/index'
const deletePluginFun = async (pluginFunId:string) => {
    return await request.delete(`api/v1/functions/${pluginFunId}`)
}
const createPluginFun = async (name:string, description:string, parameter_schema:object) => {
    const params = {
        name,
        description,
        parameters: parameter_schema
    }
    return await request.post(`api/v1/functions`, params)
}
const getPluginList = async (offset:number, limit:number) => {
    return await request.get(`api/v1/functions?offset=${offset}&limit=${limit}`)
}
const editPluginFun = async (name:string, description:string, parameter_schema:object,id:string) => {
    const params = {
        name,
        description,
        parameters: parameter_schema,
    }
    return await request.post(`api/v1/functions/${id}`, params)
}
export { deletePluginFun, createPluginFun, getPluginList, editPluginFun }