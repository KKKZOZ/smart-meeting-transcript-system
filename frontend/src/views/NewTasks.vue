<template>
    <div class="task-app">
        <h1>新增待办事项</h1>
        <!-- 检查人下拉菜单和添加待办事项按钮 -->
        <div class="header">
            <div class="form-group">
                <label>选择检查人:</label>
                <!-- 下拉框内嵌搜索框 -->
                <div class="dropdown">
                    <input type="text" v-model="searchReviewer" placeholder="搜索检查人" class="search-input"
                        @focus="showDropdownReviewer = false" @blur="hideDropdownReviewer"
                        @input="clearSelectedReviewer" />
                    <select v-model="selectedReviewer">
                        <option value="" disabled>请选择检查人</option>
                        <option v-for="(user, idx) in filteredUsersReviewer" :key="idx" :value="user.id">
                            {{ user.nickname }} ({{ user.name }})
                        </option>
                    </select>
                    <div v-if="showDropdownReviewer" class="dropdown-list">
                        <ul>
                            <li v-for="(user, idx) in filteredUsersReviewer" :key="idx"
                                @click="selectReviewer(user.id)">
                                {{ user.nickname }} ({{ user.name }})
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
            <button class="add-btn" @click="addTaskItem">增加待办事项</button>
            <button v-if="meetingId && waiting" class="reload-btn">
                待办事项提取中，请稍候
            </button>
            <button v-if="meetingId && !waiting" class="reload-btn" @click="reextract">
                提取结果不满意？重试
            </button>
        </div>

        <!-- 待办事项列表 -->
        <div class="task-items">
            <div v-for="(task, index) in taskList" :key="index" class="task-item">
                <div class="task-header">
                    <span class="task-index">#{{ index + 1 }}</span>
                </div>
                <div class="form-group task-content">
                    <label>待办事项内容:</label>
                    <input type="text" v-model="task.content" placeholder="请输入待办事项内容" />
                </div>
                <div class="form-group task-executor">
                    <label>执行人:</label>
                    <!-- 每个待办事项的执行人搜索框是独立的 -->
                    <div class="dropdown">
                        <input type="text" v-model="task.searchExecutor" placeholder="搜索执行人" class="search-input"
                            @focus="showDropdownExecutor = false" @blur="hideDropdownExecutor"
                            @input="clearSelectedExecutor(task)" />
                        <select v-model="task.executor">
                            <option value="" disabled>请选择执行人</option>
                            <option v-for="(user, idx) in filteredUsersExecutor(task.searchExecutor)" :key="idx"
                                :value="user.id">
                                {{ user.nickname }} ({{ user.name }})
                            </option>
                        </select>
                        <div v-if="showDropdownExecutor" class="dropdown-list">
                            <ul>
                                <li v-for="(user, idx) in filteredUsersExecutor(task.searchExecutor)" :key="idx"
                                    @click="selectExecutor(task, user.id)">
                                    {{ user.nickname }} ({{ user.name }})
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>

                <!-- 截止时间选择 -->
                <div class="form-group datetime-group">
                    <label>截止时间:</label>
                    <div class="time-input">
                        <input type="date" v-model="task.dueDate" />
                        <select v-model="task.dueTime.hours">
                            <option value="" disabled>小时</option>
                            <option v-for="h in hours" :key="h" :value="h">{{ h }}</option>
                        </select>
                        <span>:</span>
                        <select v-model="task.dueTime.minutes">
                            <option value="" disabled>分钟</option>
                            <option v-for="m in minutes" :key="m" :value="m">{{ m }}</option>
                        </select>
                    </div>
                </div>

                <!-- 删除按钮 -->
                <button class="delete-btn" @click="deleteTaskItem(index)">删除</button>
            </div>
        </div>

        <!-- 提交按钮 -->
        <button :disabled="taskList.length === 0" class="submit-btn" @click="submitTaskList">
            创建待办事项
        </button>
    </div>
</template>

<script setup>
    import { ref, computed, onMounted } from 'vue';
    import axios from '@/axios';
    import router from '../router';
    import { useRoute } from 'vue-router';

    const route = useRoute();
    const meetingId = ref(null);
    const waiting = ref(true);
    const taskList = ref([]); // 存储待办事项列表
    const users = ref([]); // 执行人和检查人的候选列表，包含id、name和nickname
    const selectedReviewer = ref(''); // 当前选中的检查人id
    const searchReviewer = ref(''); // 搜索框绑定的值，用于检查人搜索
    const showDropdownReviewer = ref(false); // 控制检查人下拉框显示
    const showDropdownExecutor = ref(false); // 控制执行人下拉框显示
    const hours = ref(Array.from({ length: 24 }, (_, i) => String(i).padStart(2, '0'))); // 小时列表
    const minutes = ref(Array.from({ length: 60 }, (_, i) => String(i).padStart(2, '0'))); // 分钟列表

    onMounted(() => {
        getUserInfo();
        meetingId.value = route.query.meeting_id;
        if (meetingId.value) {
            getInitialTasks(); // 获取待办事项的初始数据
        }
    });

    const reextract = () => {
        taskList.value = [];
        router.go(0);
    };

    const getUserInfo = async () => {
        try {
            const response = await axios.post('/api/get-user-info');
            users.value = response.data;
            console.log(users.value);
        } catch (error) {
            console.error(error.message);
        }
    };

    // 模拟获取初始传入的待办事项（例如，来自 URL 或 API）
    const getInitialTasks = async () => {
        const response = await axios.post('/api/llm-extraction', {
            meeting_id: meetingId.value
        });
        var msg = response.data.message;
        if (msg === "fail") {
            alert("提取待办事项失败");
            return;
        }
        const initialTasks = response.data.data;

        // 根据executor的用户名来匹配对应的id或nickname
        taskList.value = initialTasks.map(task => {
            const executorUser = users.value.find(user => user.name === task.executor || user.nickname === task.executor);
            if (executorUser) {
                task.executor = executorUser.id; // 如果有匹配的用户，则使用id
            } else {
                task.executor = ''; // 如果没有匹配的用户，则清空
            }

            // 转换日期时间格式
            if (task.dueDate === '') {
                task.dueTime = { hours: '', minutes: '' };
            } else {
                try {
                    const [date, time] = task.dueDate.split(' ');
                    const [year, month, day] = date.split('-');
                    const [hour, minute] = time.split(':');
                    task.dueDate = `${year}-${month}-${day}`;
                    task.dueTime = { hours: hour, minutes: minute };
                } catch (error) {
                    task.dueDate = '';
                    task.dueTime = { hours: '', minutes: '' };
                }

            }

            return task;
        });
        waiting.value = false;
    };

    // 根据每个待办事项的searchExecutor来过滤用户列表 - 执行人
    const filteredUsersExecutor = (searchText) => {
        const searchQuery = searchText.toLowerCase();
        return users.value.filter(user => user.name.toLowerCase().includes(searchQuery) || user.nickname.toLowerCase().includes(searchQuery));
    };

    // 根据搜索值过滤用户列表 - 检查人
    const filteredUsersReviewer = computed(() => {
        const searchText = searchReviewer.value.toLowerCase();
        return users.value.filter(user => user.name.toLowerCase().includes(searchText) || user.nickname.toLowerCase().includes(searchText));
    });

    // 选择检查人
    const selectReviewer = (id) => {
        selectedReviewer.value = id;
        searchReviewer.value = ''; // 清空搜索框
        showDropdownReviewer.value = false; // 隐藏下拉框
    };

    // 选择执行人
    const selectExecutor = (task, id) => {
        task.executor = id;
        task.searchExecutor = ''; // 清空搜索框
        showDropdownExecutor.value = false; // 隐藏下拉框
    };

    // 添加新的待办事项
    const addTaskItem = () => {
        taskList.value.push({
            content: '',
            executor: '',
            dueDate: '',
            dueTime: { hours: '', minutes: '' },
            searchExecutor: '' // 每个待办事项有独立的执行人搜索框
        });
    };

    // 删除待办事项
    const deleteTaskItem = (index) => {
        taskList.value.splice(index, 1);
    };

    // 提交待办事项
    const submitTaskList = async () => {
        // 检查待办事项是否填写完整
        for (let task of taskList.value) {
            if (!task.content || !task.executor || !task.dueDate || !task.dueTime.hours || !task.dueTime.minutes) {
                alert('请填写所有待办事项的内容、执行人和截止时间');
                return;
            }
        }

        // 检查是否选择了检查人
        if (!selectedReviewer.value) {
            alert('请选择检查人');
            return;
        }

        var tasksToStore = JSON.parse(JSON.stringify(taskList.value));

        for (let task of tasksToStore) {
            delete task.searchExecutor;
            var dueDate = task.dueDate;
            var dueTime = task.dueTime;

            // 将dueDate和dueTime拼接为ISO 8601格式
            task.dueDate = `${dueDate}T${dueTime.hours}:${dueTime.minutes}:00`;

            delete task.dueTime;
        }

        const response = await axios.post('/api/create-tasks', {
            inspector: selectedReviewer.value,
            meeting_id: meetingId.value,
            tasks: tasksToStore
        });

        if (response.data.message === "success") {
            alert('待办事项创建成功！');
            router.push("/tasks");
        } else {
            alert('待办事项创建失败');
        }
    };

    // 清除检查人
    const clearSelectedReviewer = () => {
        if (!searchReviewer.value) {
            selectedReviewer.value = '';
        }
    };

    // 清除执行人
    const clearSelectedExecutor = (task) => {
        if (!task.searchExecutor) {
            task.executor = '';
        }
    };
</script>

<style scoped>
    .task-app {
        width: 80%;
        margin: 0 auto;
        padding: 20px;
        font-family: Arial, sans-serif;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
    }

    h1 {
        text-align: center;
        margin-bottom: 20px;
        font-size: 24px;
    }

    .header {
        display: flex;
        justify-content: space-between;
        margin-bottom: 20px;
        align-items: center;
    }

    .form-group {
        margin-bottom: 15px;
        width: 48%;
    }

    label {
        display: block;
        font-size: 14px;
        margin-bottom: 5px;
        color: #555;
    }

    select,
    input[type='text'],
    input[type='date'] {
        width: 100%;
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 4px;
        font-size: 14px;
    }

    input[type='text']:focus,
    select:focus,
    input[type='date']:focus {
        border-color: #4caf50;
        outline: none;
    }

    .add-btn {
        width: 10vw;
        /* 按钮宽度相对页面宽度的10% */
        height: 7vh;
        /* 按钮高度相对页面高度的5% */
        background-color: #4caf50;
        color: white;
        border: none;
        cursor: pointer;
        font-size: 16px;
        border-radius: 5px;
    }

    .add-btn:hover {
        background-color: #45a049;
    }

    .reload-btn {
        width: 15vw;
        height: 7vh;
        background-color: #ffa500;
        color: white;
        border: none;
        cursor: pointer;
        font-size: 16px;
        border-radius: 5px;
        margin-left: 10px;
    }

    .reload-btn:hover {
        background-color: #e69500;
    }

    .task-items {
        flex-grow: 1;
        margin-bottom: 20px;
        overflow-y: auto;
    }

    .task-item {
        display: flex;
        flex-direction: column;
        margin-bottom: 15px;
        padding: 15px;
        border: 1px solid #ddd;
        border-radius: 8px;
        background-color: #ffffff;
        position: relative;
    }

    .task-header {
        font-size: 16px;
        color: #333;
        margin-bottom: 10px;
    }

    .task-index {
        font-weight: bold;
    }

    .task-content,
    .task-executor,
    .datetime-group {
        margin-bottom: 10px;
    }

    .time-input {
        display: flex;
        align-items: center;
    }

    .time-input select {
        width: 60px;
        margin-left: 5px;
    }

    .time-input span {
        margin: 0 10px;
        font-size: 18px;
    }

    .delete-btn {
        background-color: #f44336;
        color: white;
        border: none;
        padding: 6px 12px;
        font-size: 14px;
        border-radius: 5px;
        cursor: pointer;
        position: absolute;
        right: 15px;
        top: 15px;
    }

    .delete-btn:hover {
        background-color: #e53935;
    }

    .submit-btn {
        display: block;
        width: 50%;
        padding: 12px;
        background-color: #2196f3;
        color: white;
        border: none;
        cursor: pointer;
        font-size: 16px;
        border-radius: 5px;
        margin-top: 20px;
        margin-left: auto;
        margin-right: auto;
    }

    .submit-btn:disabled {
        background-color: #b0bec5;
        cursor: not-allowed;
    }

    .submit-btn:disabled:hover {
        background-color: #b0bec5;
    }

    .submit-btn:hover {
        background-color: #1976d2;
    }

    .search-input {
        margin-bottom: 10px;
        padding: 8px;
        border-radius: 4px;
        border: 1px solid #ccc;
        font-size: 14px;
        width: 100%;
    }

    .dropdown-list {
        position: absolute;
        top: 35px;
        left: 0;
        right: 0;
        background-color: white;
        border: 1px solid #ccc;
        max-height: 150px;
        overflow-y: auto;
        z-index: 1000;
    }

    .dropdown-list ul {
        list-style: none;
        margin: 0;
        padding: 0;
    }

    .dropdown-list li {
        padding: 8px;
        cursor: pointer;
    }

    .dropdown-list li:hover {
        background-color: #f0f0f0;
    }
</style>

