<template>
    <div class="todo-app">
        <!-- 新增待办事项 -->
        <div class="add-todo">
            <span class="add-label" @mouseenter="showDropdown" @mouseleave="scheduleHideDropdown">
                新增待办事项
            </span>
            <div
                v-if="dropdownVisible"
                class="dropdown"
                @mouseenter="keepDropdownVisible"
                @mouseleave="scheduleHideDropdown"
            >
                <button @click="addFromBlank">从空白事项添加</button>
                <button @click="addFromMeeting">从会议记录提取</button>
            </div>
        </div>

        <!-- 选择标签 -->
        <div class="tabs">
            <button :class="{ active: selectedTab === 'check' }" @click="selectTab('check')"
                >要检查的</button
            >
            <button :class="{ active: selectedTab === 'execute' }" @click="selectTab('execute')"
                >要执行的</button
            >
        </div>

        <!-- 待办事项表格 -->
        <div class="todo-list">
            <table v-if="selectedTab === 'check'">
                <thead>
                    <tr>
                        <th>任务名称</th>
                        <th>截止时间</th>
                        <th>状态</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(todo, index) in checkTodos" :key="index">
                        <td>{{ todo.name }}</td>
                        <td>{{ todo.dueDate }}</td>
                        <td>{{ todo.status }}</td>
                    </tr>
                </tbody>
            </table>

            <table v-if="selectedTab === 'execute'">
                <thead>
                    <tr>
                        <th>任务名称</th>
                        <th>执行人</th>
                        <th>状态</th>
                        <th>操作</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(todo, index) in executeTodos" :key="index">
                        <td>{{ todo.name }}</td>
                        <td>{{ todo.executor }}</td>
                        <td>{{ todo.status }}</td>
                        <td>
                            <!-- 根据状态显示提交按钮或完成图标 -->
                            <button
                                v-if="todo.status === '待处理'"
                                @click="submitTask(todo)"
                                class="submit-btn"
                            >
                                提交
                            </button>
                            <span v-else-if="todo.status === '已完成'" class="completed-icon"
                                >✔</span
                            >
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script setup>
    import { ref, onMounted } from 'vue';
    import router from '../router';

    const dropdownVisible = ref(false); // 控制下拉框显示
    const selectedTab = ref('check'); // 当前选中的标签
    const checkTodos = ref([]); // 从服务器获取的待检查任务列表
    const executeTodos = ref([]); // 从服务器获取的待执行任务列表
    const dropdownTimeout = ref(null); // 定时器用于控制下拉按钮消失延时
    const showDropdown = () => {
        dropdownVisible.value = true;
        if (dropdownTimeout.value) {
            clearTimeout(dropdownTimeout.value); // 如果有定时器，清除它
        }
    };
    const scheduleHideDropdown = () => {
        dropdownTimeout.value = setTimeout(() => {
            dropdownVisible.value = false;
        }, 50); // 延时 50ms 后隐藏
    };
    const keepDropdownVisible = () => {
        // 保持下拉按钮可见，鼠标悬停时不消失
        if (dropdownTimeout.value) {
            clearTimeout(dropdownTimeout.value);
        }
    };
    const addFromBlank = () => {
        // 跳转到空白事项添加页面
        router.push('/new-tasks');
    };
    const addFromMeeting = () => {
        // 跳转到会议记录提取页面
        router.push('/extract-tasks-from-meetings');
    };
    const selectTab = tab => {
        selectedTab.value = tab;
    };
    const submitTask = todo => {
        // 提交任务处理逻辑
        todo.status = '已完成'; // 模拟任务提交后状态变更为已完成
        alert(`任务"${todo.name}"已提交！`);
    };
    onMounted(() => {
        // 模拟从服务器获取数据
        checkTodos.value = [
            { name: '检查日报', dueDate: '2024-01-01', status: '待处理' },
            { name: '审核项目进度', dueDate: '2024-01-02', status: '已完成' },
        ];
        executeTodos.value = [
            { name: '完成任务A', executor: '张三', status: '待处理' },
            { name: '处理任务B', executor: '李四', status: '已完成' },
        ];
    });
</script>

<style scoped>
    .todo-app {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        padding: 30px;
        min-height: 100vh;
    }

    /* 新增待办事项样式 */
    .add-todo {
        position: relative;
        background-color: #007bff;
        padding: 15px 20px;
        color: white;
        border-radius: 8px;
        display: inline-block;
        margin-bottom: 20px;
        font-size: 18px;
        font-weight: bold;
        cursor: pointer;
    }

    .add-label {
        display: inline-block;
    }

    .add-todo:hover {
        background-color: #0056b3;
    }

    .dropdown {
        position: absolute;
        top: 50px;
        left: 0;
        background-color: #ffffff;
        border: 1px solid #ddd;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        width: 200px;
        transition: opacity 0.3s ease;
        padding: 0; /* 保证按钮不会超出边界 */
    }

    .dropdown button {
        width: 100%;
        padding: 12px;
        border: none;
        background: none;
        text-align: left;
        cursor: pointer;
        font-size: 14px;
        color: #333;
        border-radius: 8px; /* 保证按钮与父容器圆角一致 */
        box-sizing: border-box; /* 确保内边距不会改变元素的大小 */
        box-sizing: border-box; /* 确保背景色不会超出边框 */
    }

    .dropdown button:hover {
        background-color: #f1f1f1;
    }

    /* 标签栏 */
    .tabs {
        display: flex;
        margin-bottom: 20px;
    }

    .tabs button {
        padding: 12px 25px;
        margin-right: 12px;
        border: 1px solid #ddd;
        background-color: #fff;
        font-weight: bold;
        cursor: pointer;
        border-radius: 8px;
        transition: background-color 0.3s ease;
    }

    /* 选中的按钮 */
    .tabs button.active {
        background-color: #007bff;
        color: white;
        border-color: #007bff;
    }

    /* 悬停时加深背景色 */
    .tabs button:hover {
        background-color: #f0f4f8;
    }

    /* 悬停时选中按钮加深 */
    .tabs button.active:hover {
        background-color: #0056b3;
    }

    /* 表格样式 */
    .todo-list table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .todo-list th,
    .todo-list td {
        padding: 14px;
        border: 1px solid #ddd;
        text-align: left;
        font-size: 16px;
    }

    .todo-list th {
        background-color: #f7f9fc;
        color: #555;
    }

    .todo-list td {
        background-color: #ffffff;
        color: #333;
    }

    .todo-list td:nth-child(odd) {
        background-color: #f9f9f9;
    }

    .todo-list tr:hover {
        background-color: #f1f1f1;
    }

    /* 提交按钮样式 */
    .submit-btn {
        padding: 6px 12px;
        font-size: 14px;
        color: white;
        background-color: #007bff;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }

    .submit-btn:hover {
        background-color: #0056b3;
    }

    /* 完成图标 */
    .completed-icon {
        color: #28a745;
        font-size: 18px;
        font-weight: bold;
    }
</style>
