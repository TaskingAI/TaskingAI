import { request } from '../utils/index'

const getProjectSettingsInfo = async () => {
    return await request.get(`api/v1/get`)
}
const updateProjectSettingInfo = async (params:object) => {
    return await request.post(`api/v1/update`,params)
}
const deleteProjectSetting = async ()=> {
    return await request.post(`api/v1/delete`)
}
export { getProjectSettingsInfo, updateProjectSettingInfo,deleteProjectSetting }