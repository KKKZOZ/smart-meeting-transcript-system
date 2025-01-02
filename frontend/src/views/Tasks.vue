<template>
    <div class="task-app">
        <!-- 新增待办事项 -->
        <div class="add-task">
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
        <div class="task-list">
            <!-- 要检查的任务列表 -->
            <table v-if="selectedTab === 'check'">
                <thead>
                    <tr>
                        <th>任务描述</th>
                        <th>执行人</th>
                        <th>截止时间</th>
                        <th>状态</th>
                        <th>操作</th> <!-- 新增操作列 -->
                    </tr>
                </thead>
                <tbody>
                    <template v-for="(group, meeting_id) in groupedCheckTasks" :key="meeting_id">
                        <tr class="group-header">
                            <td colspan="5">会议名称: {{ group[0].meeting_title }}</td>
                        </tr>
                        <tr v-for="task in group" :key="task.meeting_id">
                            <td>{{ task.description }}</td>
                            <td>{{ task.executor_nickname }}({{ task.executor_name }})</td>
                            <td>{{ new Date(task.due_date).toLocaleString() }}</td>
                            <td>
                                <!-- 状态列，待处理和已完成后面加图标 -->
                                <span :class="{ 'pending': task.status === '待处理', 'completed': task.status === '已完成' }">
                                    {{ task.status }}
                                </span>
                            </td>
                            <td>
                                <!-- 只有待处理状态时显示提醒按钮 -->
                                <button v-if="task.status === '待处理'" @click="remind(task)" class="remind-btn">
                                    提醒
                                </button>
                            </td>
                        </tr>
                    </template>
                </tbody>
            </table>

            <!-- 要执行的任务列表 -->
            <table v-if="selectedTab === 'execute'">
                <thead>
                    <tr>
                        <th>任务描述</th>
                        <th>检查人</th>
                        <th>截止时间</th>
                        <th>状态</th>
                        <th>操作</th>
                    </tr>
                </thead>
                <tbody>
                    <template v-for="(group, meeting_id) in groupedExecuteTasks" :key="meeting_id">
                        <tr class="group-header">
                            <td colspan="5">会议名称: {{ group[0].meeting_title }}</td>
                        </tr>
                        <tr v-for="task in group" :key="task.meeting_id">
                            <td>{{ task.description }}</td>
                            <td>{{ task.inspector_nickname }}({{ task.inspector_name }})</td>
                            <td>{{ new Date(task.due_date).toLocaleString() }}</td>
                            <td>{{ task.status }}</td>
                            <td>
                                <button v-if="task.status === '待处理'" @click="submitTask(task)" class="submit-btn">
                                    提交
                                </button>
                                <span v-else-if="task.status === '已完成'" class="completed-icon">✔</span>
                            </td>
                        </tr>
                    </template>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script setup>
    import { ref, computed, onMounted } from 'vue';
    import axios from '@/axios';
    import router from '../router';

    const dropdownVisible = ref(false); // 控制下拉框显示
    const selectedTab = ref('check'); // 当前选中的标签
    const checkTasks = ref([]); // 从服务器获取的待检查任务列表
    const executeTasks = ref([]); // 从服务器获取的待执行任务列表
    const dropdownTimeout = ref(null); // 定时器用于控制下拉按钮消失延时


    // 将待检查任务按 ID 分组
    const groupedCheckTasks = computed(() => {
        const groups = {};
        checkTasks.value.forEach(task => {
            if (!groups[task.meeting_id]) {
                groups[task.meeting_id] = [];
            }
            groups[task.meeting_id].push(task);
        });
        return groups;
    });
    // 将待执行任务按 ID 分组
    const groupedExecuteTasks = computed(() => {
        const groups = {};
        executeTasks.value.forEach(task => {
            if (!groups[task.meeting_id]) {
                groups[task.meeting_id] = [];
            }
            groups[task.meeting_id].push(task);
        });
        return groups;
    });
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
    const submitTask = async (task) => {
        // 提交任务处理逻辑
        const response = await axios.post('/api/submit-tasks', {
            task_id: task.task_id
        });
        if (response.data.message == "success") {
            alert(`任务已提交！`);
            router.go(0);
        } else {
            alert(`任务提交失败`);
        }
    };

    // 提醒逻辑，提醒按钮点击时执行
    const remind = async (task) => {
        const response = await axios.post('/api/remind-tasks', {
            task_id: task.task_id
        });
        if (response.data.message == "success") {
            alert(`任务已提醒！`);
        } else {
            alert(`任务提醒失败`);
        }
    };

    const getTasksToReview = async () => {
        const response = await axios.post('/api/get-tasks-to-review');
        checkTasks.value = response.data;
    };

    const getTasksToExecute = async () => {
        const response = await axios.post('/api/get-tasks-to-execute');
        executeTasks.value = response.data;
    };

    onMounted(() => {
        // 从服务器获取数据
        getTasksToReview();
        getTasksToExecute();
    });
</script>

<style scoped>
    .task-app {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        padding: 30px;
        min-height: 100vh;
    }

    /* 新增待办事项样式 */
    .add-task {
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

    .add-task:hover {
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
        padding: 0;
        /* 保证按钮不会超出边界 */
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
        border-radius: 8px;
        transition: background-color 0.3s ease;
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
    .task-list table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .task-list th,
    .task-list td {
        padding: 14px;
        border: 1px solid #ddd;
        text-align: left;
        font-size: 16px;
    }

    .task-list th {
        background-color: #f7f9fc;
        color: #555;
    }

    .task-list td {
        background-color: #ffffff;
        color: #333;
    }

    .task-list td:nth-child(odd) {
        background-color: #f9f9f9;
    }

    .task-list tr:hover {
        background-color: #f1f1f1;
    }

    /* 状态列中的待处理和已完成图标 */
    .pending::after {
        content: ' ⏳';
        font-size: 18px;
    }

    .completed::after {
        content: ' ✔';
        font-size: 18px;
        color: #28a745;
    }

    /* 提醒按钮样式 */
    .remind-btn {
        padding: 6px 12px;
        font-size: 14px;
        color: white;
        background-color: #f39c12;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }

    .remind-btn:hover {
        background-color: #e67e22;
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

