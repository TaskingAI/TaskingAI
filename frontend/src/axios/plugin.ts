import { request } from "../utils/index";
const deletePlugin = async (pluginFunId: string) => {
  return await request.delete(`api/v1/bundle_instances/${pluginFunId}`);
};
const bundleList = async (params) => {
  const str = Object.entries(params)
    .filter(([_key, value]) => value)
    .map(([key, value]) => `${key}=${value}`)
    .join("&");
  return await request.get(`api/v1/bundles?${str}`);
};
const getPluginDetail = async (pluginFunId: string) => {
  return await request.get(`api/v1/plugins?bundle_id=${pluginFunId}`);
};
const createPlugin = async (params: object) => {
  return await request.post(`api/v1/bundle_instances`, params);
};
const getPluginList = async (params) => {
  const data = params;
  let str = "";
  if (data.hasOwnProperty("name_search")) {
    str += `prefix_filter={"name":"${data.name_search}"}&`;
    delete data.name_search;
  } else if (data.hasOwnProperty("id_search")) {
    str += `prefix_filter={"bundle_instance_id":"${data.id_search}"}&`;
    delete data.id_search;
  }
  if (data) {
    Object.keys(data).forEach((key) => {
      str += `${key}=${data[key]}&`;
    });
    str = str.substring(0, str.length - 1);
  }
  return await request.get(`api/v1/bundle_instances?${str}`);
};
const editPlugin = async (id: string, params) => {
  return await request.post(`api/v1/bundle_instances/${id}`, params);
};
export {
  deletePlugin,
  bundleList,
  getPluginDetail,
  createPlugin,
  getPluginList,
  editPlugin,
};
