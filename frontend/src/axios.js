// src/axios.js
import axios from 'axios';
import store from '@/store'; 
import { useRouter } from 'vue-router';

const router = useRouter();

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
        return response;
    },
    error => {
        if (error.response?.status === 401 ) {
            localStorage.removeItem('token');
            store.dispatch('auth/logout');
            if (router.currentRoute.value.path !== '/signin') {
                router.push('/signin');
            }
        }
        return Promise.reject(error);
    }
);

export default instance;
