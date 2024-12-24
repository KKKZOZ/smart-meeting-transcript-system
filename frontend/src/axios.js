// src/axios.js
import axios from 'axios';

const instance = axios.create({
    baseURL: 'http://localhost:8000', // 本地后端接口的基础 URL
    timeout: 5000, // 将超时时间改为 5000 毫秒（5秒）
    headers: { 'Content-Type': 'application/json' },
});

// 请求拦截器
instance.interceptors.request.use(
    config => {
        // 在发送请求之前做一些处理
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    error => {
        return Promise.reject(error);
    },
);

// 响应拦截器
instance.interceptors.response.use(
    response => {
        // 对响应数据做处理
        return response;
    },
    error => {
        // 对响应错误做处理
        if (error.response?.status === 401) {
            // token 过期或无效时的处理
            localStorage.removeItem('token');
            window.location.href = '/signin';
        }
        console.log('Error:', error.response.data);
        return Promise.reject(error);
    },
);

export default instance;
