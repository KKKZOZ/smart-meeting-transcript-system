// src/axios.js
import axios from 'axios';
import store from '@/store';
import router from '@/router';

const instance = axios.create({
    baseURL: 'http://39.104.62.233:8000', // 本地后端接口的基础 URL
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
        return response;
    },
    error => {
        if (error.response?.status === 401) {
            console.log('401 错误，当前路由：', router.currentRoute.value.path);
            localStorage.removeItem('token');
            store.dispatch('auth/logout');
            if (router.currentRoute.value.path !== '/signin') {
                console.log('准备跳转到登录页');
                router.push('/signin');
            }
        }
        return Promise.reject(error);
    },
);

export default instance;
