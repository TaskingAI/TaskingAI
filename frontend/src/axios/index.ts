import { request } from '../utils/index'
const auth_base_url = 'api/v1'

const verifyToken = async () => {
    return await request.post(`${auth_base_url}/admins/verify_token`)

}
const fetchLogin = async (data:object) => {
    return await request.post(`${auth_base_url}/admins/login`, data)
}
const  fetchIcon = async (providerId) => {
    return await request.get(`/images/providers/icons/${providerId}.svg`)
}
const getViewCode = async (module: string) => {
    return await request.get(`api/v1/ui/template_codes/get_code?module=${module}`)
}
export { verifyToken , fetchLogin, fetchIcon, getViewCode }
