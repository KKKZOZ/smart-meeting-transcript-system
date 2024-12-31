<template>
    <div class="todo-app">
        <h1>待办事项管理</h1>

        <!-- 检查人下拉菜单和添加待办事项按钮 -->
        <div class="header">
            <div class="form-group">
                <label>选择检查人:</label>
                <select v-model="selectedReviewer">
                    <option value="" disabled>请选择检查人</option>
                    <option v-for="(user, idx) in users" :key="idx" :value="user">{{ user }}</option>
                </select>
            </div>
            <button class="add-btn" @click="addTodoItem">增加待办事项</button>
        </div>

        <!-- 待办事项列表 -->
        <div class="todo-items">
            <div v-for="(todo, index) in todoList" :key="index" class="todo-item">
                <div class="todo-header">
                    <span class="todo-index">#{{ index + 1 }}</span>
                </div>
                <div class="form-group todo-content">
                    <label>待办事项内容:</label>
                    <input type="text" v-model="todo.content" placeholder="请输入待办事项内容" />
                </div>
                <div class="form-group todo-executor">
                    <label>执行人:</label>
                    <select v-model="todo.executor">
                        <option value="" disabled>请选择执行人</option>
                        <option v-for="(user, idx) in users" :key="idx" :value="user">{{ user }}</option>
                    </select>
                </div>

                <!-- 截止时间选择 -->
                <div class="form-group datetime-group">
                    <label>截止时间:</label>
                    <div class="time-input">
                        <input type="date" v-model="todo.dueDate" />
                        <select v-model="todo.dueTime.hours">
                            <option value="" disabled>小时</option>
                            <option v-for="h in hours" :key="h" :value="h">{{ h }}</option>
                        </select>
                        <span>:</span>
                        <select v-model="todo.dueTime.minutes">
                            <option value="" disabled>分钟</option>
                            <option v-for="m in minutes" :key="m" :value="m">{{ m }}</option>
                        </select>
                    </div>
                </div>

                <!-- 删除按钮 -->
                <button class="delete-btn" @click="deleteTodoItem(index)">删除</button>
            </div>
        </div>

        <!-- 提交按钮 -->
        <button :disabled="todoList.length === 0" class="submit-btn" @click="submitTodoList">
            创建待办事项
        </button>
    </div>
</template>

<script setup>
    import { ref, onMounted } from 'vue';
    import router from '../router';
    const todoList = ref([]) // 存储待办事项列表
    const users = ref(['张三', '李四', '王五', '赵六']); // 执行人和检查人的候选列表
    const selectedReviewer = ref(''); // 当前选中的检查人
    const hours = ref(Array.from({ length: 24 }, (_, i) => String(i).padStart(2, '0'))) // 小时列表
    const minutes = ref(Array.from({ length: 60 }, (_, i) => String(i).padStart(2, '0'))) // 分钟列表
    onMounted(() => {
        // 模拟从 URL 或其他地方传入的参数，进行初始化
        const initialTodos = getInitialTodos(); // 获取待办事项的初始数据
        if (initialTodos) {
            todoList.value = initialTodos;
        }
    });
    // 模拟获取初始传入的待办事项（例如，来自 URL 或 API）
    const getInitialTodos = () => {
        // 假设传入的待办事项数据
        return [
            {
                content: '完成项目报告',
                executor: '张三',
                dueDate: '2024-12-31',
                dueTime: { hours: '14', minutes: '30' },
            },
            {
                content: '准备会议材料',
                executor: '李四',
                dueDate: '2024-12-31',
                dueTime: { hours: '16', minutes: '00' },
            },
        ];
    };
    // 添加待办事项
    const addTodoItem = () => {
        todoList.value.push({
            content: '',
            executor: '',
            dueDate: '',
            dueTime: { hours: '', minutes: '' },
        });
    };
    // 删除待办事项
    const deleteTodoItem = (index) => {
        todoList.value.splice(index, 1);
    };
    // 提交待办事项
    const submitTodoList = () => {
        // 检查待办事项是否填写完整
        for (let todo of todoList.value) {
            if (!todo.content || !todo.executor || !todo.dueDate || !todo.dueTime.hours || !todo.dueTime.minutes) {
                alert('请填写所有待办事项的内容、执行人和截止时间！');
                return;
            }
        }

        // 检查是否选择了检查人
        if (!selectedReviewer.value) {
            alert('请选择检查人！');
            return;
        }

        console.log('提交的待办事项：', todoList.value, '检查人：', selectedReviewer.value);
        alert('待办事项提交成功！');
        router.push("/tasks");
    };
</script>

<style scoped>
    .todo-app {
        width: 80%;
        /* 宽度适中 */
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
    input[type="text"],
    input[type="date"] {
        width: 100%;
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 4px;
        font-size: 14px;
    }

    input[type="text"]:focus,
    select:focus,
    input[type="date"]:focus {
        border-color: #4caf50;
        outline: none;
    }

    .add-btn {
        padding: 12px 20px;
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

    .todo-items {
        flex-grow: 1;
        margin-bottom: 20px;
        overflow-y: auto;
    }

    .todo-item {
        display: flex;
        flex-direction: column;
        margin-bottom: 15px;
        padding: 15px;
        border: 1px solid #ddd;
        border-radius: 8px;
        background-color: #ffffff;
        position: relative;
    }

    .todo-header {
        font-size: 16px;
        color: #333;
        margin-bottom: 10px;
    }

    .todo-index {
        font-weight: bold;
    }

    .todo-content,
    .todo-executor,
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
</style>