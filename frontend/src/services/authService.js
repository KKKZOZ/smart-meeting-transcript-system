import axios from '@/axios'; // 导入我们配置好的 axios 实例

export default {
    async login(credentials) {
        const { username, password } = credentials
        
        // 创建 FormData 对象，使用 OAuth2 password grant type 的标准格式
        const formData = new URLSearchParams()
        formData.append('username', username)
        formData.append('password', password)
        formData.append('grant_type', 'password')
        
        const response = await axios.post('/api/login', formData, {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        })
        return response.data
    },
}
