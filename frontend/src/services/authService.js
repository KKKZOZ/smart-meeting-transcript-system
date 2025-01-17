import axios from '@/axios'; // 导入我们配置好的 axios 实例

export default {
    async login(credentials) {
        const { username, password } = credentials;

        // 创建 FormData 对象，使用 OAuth2 password grant type 的标准格式
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);
        formData.append('grant_type', 'password');

        const response = await axios.post('/api/login', formData, {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
        });
        return response.data;
    },
    async register(userData) {
        console.log('userData:', userData);
        const response = await axios.post('/api/register', userData, {
            headers: {
                'Content-Type': 'application/json'
            }
        })
        return response.data
    },
    async getUserInfo() {
        const response = await axios.get('/api/me');
        return response.data;
    },
};
