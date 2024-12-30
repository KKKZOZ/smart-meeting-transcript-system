<template>
    <div class="container">
        <!-- 新增按钮 -->
        <div>
            <!-- 下拉按钮 -->
            <button @click="toggleDropdown" class="search-btn">
                新增待办事项
            </button>

            <!-- 下拉菜单 -->
            <div v-if="dropdownVisible" class="dropdown-menu">
                <button @click="addTask" class="dropdown-item">从空白事项添加</button>
                <button @click="addByExtract" class="dropdown-item">从会议记录提取</button>
            </div>
        </div>

        <!-- 两个切换按钮 -->
        <div class="button-group">
            <button @click="review" class="switch-btn">要检查的</button>
            <button @click="excution" class="switch-btn">要执行的</button>
        </div>

        <!-- 表格 -->
        <table class="data-table">
            <thead>
                <tr>
                    <th>编号</th>
                    <th>姓名</th>
                    <th>年龄</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(row, index) in tableData" :key="index">
                    <td>{{ row.id }}</td>
                    <td>{{ row.name }}</td>
                    <td>{{ row.age }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script setup>
    import { ref, onMounted } from 'vue';
    import axios from '@/axios';
    import router from '../router';

    // 表格数据
    var tableData = ref([]);

    // 用于保存搜索数据
    var searchData = ref(null);

    // 下拉菜单控制
    var dropdownVisible = ref(false);

    const toggleDropdown = () => {
        dropdownVisible.value = !dropdownVisible.value; // 切换下拉菜单显示
    };

    // 搜索按钮点击后获取数据
    const addTask = async () => {
        try {
            // 发起 GET 请求，从后端获取数据（假设后端接口为 /api/data）
            const response = await axios.post('/api/llm_extraction'); // 示例接口
            searchData.value = response.data; // 保存搜索结果，但不填充表格
            alert(response.data)
        } catch (error) {
            console.error('获取数据失败', error);
            alert('数据获取失败');
        }
    };

    const addByExtract = () => {
        router.push("/extract-tasks-from-meetings");
    };

    // 独立的函数用来填充表格内容 A
    const review = () => {
        const mockDataA = [
            { id: 1, name: '张三', age: 28 },
            { id: 2, name: '李四', age: 35 },
            { id: 3, name: '王五', age: 22 },
        ];
        fillTableData(mockDataA);
    };

    // 独立的函数用来填充表格内容 B
    const excution = () => {
        const mockDataB = [
            { id: 4, name: '赵六', age: 42 },
            { id: 5, name: '孙七', age: 26 },
            { id: 6, name: '周八', age: 30 },
        ];
        fillTableData(mockDataB);
    };

    // 填充表格内容的通用方法
    const fillTableData = data => {
        tableData.value = data;
    };

    onMounted(() => {
        // 页面加载时可以自动调用搜索获取数据
        review();
    });
</script>

<style scoped>
    /* 页面容器 */
    .container {
        width: 80%;
        margin: 0 auto;
        padding: 20px;
    }

    /* 搜索按钮样式 */
    .search-btn {
        padding: 10px 20px;
        font-size: 16px;
        background-color: #4caf50;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        margin-bottom: 20px;
        transition: background-color 0.3s;
    }

    .search-btn:hover {
        background-color: #45a049;
    }

    /* 切换按钮样式 */
    .button-group {
        margin: 20px 0;
    }

    .switch-btn {
        padding: 10px 20px;
        font-size: 16px;
        background-color: #2196f3;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        margin-right: 10px;
    }

    .switch-btn:hover {
        background-color: #1976d2;
    }

    /* 表格样式 */
    .data-table {
        width: 100%;
        border-collapse: collapse;
        background-color: #ffffff;
        /* 设置不透明的白色背景 */
        margin-top: 20px;
    }

    .data-table th,
    .data-table td {
        padding: 10px;
        border: 1px solid #ddd;
        text-align: center;
    }

    .data-table th {
        background-color: #f4f4f4;
    }

    .data-table tr:nth-child(even) {
        background-color: #f9f9f9;
    }

    .data-table tr:hover {
        background-color: #f1f1f1;
    }

    /* 加载中的文本 */
    p {
        font-size: 16px;
        color: #555;
    }


    .search-btn:hover {
        background-color: #45a049;
        /* 鼠标悬停时的背景色 */
    }

    .dropdown-menu {
        display: block;
        position: absolute;
        background-color: white;
        border: 1px solid #ddd;
        border-radius: 5px;
        margin-top: 5px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }

    .dropdown-item {
        padding: 10px 20px;
        background-color: white;
        border: none;
        width: 100%;
        text-align: left;
        cursor: pointer;
    }

    .dropdown-item:hover {
        background-color: #f1f1f1;
        /* 鼠标悬停时的背景色 */
    }
</style>
