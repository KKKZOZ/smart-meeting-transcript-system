// src/axios.js
import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://localhost:8000', // 本地后端接口的基础 URL
  timeout: 1000, // 请求超时时间
  headers: { 'Content-Type': 'application/json' }
});

export default instance;