import axios from '@/axios'; // 导入我们配置好的 axios 实例

export const authService = {
    async login(credentials) {
        try {
            // 将数据转换为 URLSearchParams 格式
            const formData = new URLSearchParams();
            formData.append('username', credentials.username);
            formData.append('password', credentials.password);

            const response = await axios.post('/api/login', formData, {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded', // 只在登录请求中修改 Content-Type
                },
            });

            console.log('API Response:', response.data);
            if (response.data.access_token) {
                console.log('Token:', response.data.access_token);
                localStorage.setItem('token', response.data.access_token);
            }
            return response.data;
        } catch (error) {
            throw error.response?.data || { message: '登录失败' };
        }
    },
    async register(credentials) {
        try {
            const response = await axios.post('/api/register', credentials);

            console.log('API Response:', response.data);
            if (response.data.access_token) {
                console.log('Token:', response.data.access_token);
                localStorage.setItem('token', response.data.access_token);
            }
            return response.data;
        } catch (error) {
            throw error.response?.data || { message: '登录失败' };
        }
    },
};
