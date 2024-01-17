import {router_item} from './index'
import { useRoutes } from "react-router-dom"

const GetRouters = () => {

    const routes = useRoutes(router_item)
    return routes
}
export default GetRouters