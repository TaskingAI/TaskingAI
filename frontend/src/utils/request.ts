import axios from "axios";
import { toast } from "react-toastify";
const request = axios.create({
  baseURL: "/",
  timeout: 60000,
});
request.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = "Bearer " + localStorage.getItem("token");
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  },
);

request.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    console.log(error);
    const location = window.location.href;
    if (!error.response) {
      toast.error("Connection failed. Please retry.");
    }
    if (
      error.response.status === 401 &&
      !location.includes("/auth/signin") &&
      error.response.data.error.code === "TOKEN_VALIDATION_FAILED"
    ) {
      localStorage.removeItem("token");
      window.location.href = "/auth/signin";
    }
    return Promise.reject(error);
  },
);

export { request };
