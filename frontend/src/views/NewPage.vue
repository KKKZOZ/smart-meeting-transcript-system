<template>
    <div class="demo-page">
        <!-- 标题部分 -->
        <h1>DemoItem Management</h1>

        <!-- 添加表单 -->
        <div class="form-section">
            <h2>Add New Item</h2>
            <div class="input-group">
                <input
                    v-model.number="newItem.id"
                    type="number"
                    placeholder="ID"
                    class="id-input"
                />
                <input v-model="newItem.value" placeholder="Value" class="value-input" />
                <button @click="createItem" class="btn-add">Add Item</button>
            </div>
        </div>

        <!-- 项目列表 -->
        <div class="list-section">
            <h2>Items List</h2>
            <div v-if="items.length === 0" class="no-data">No items found</div>
            <div v-else class="items-list">
                <div v-for="item in items" :key="item.id" class="item-card">
                    <!-- 显示/编辑模式切换 -->
                    <div v-if="editingId !== item.id" class="item-view">
                        <div class="item-content">
                            <h3>ID: {{ item.id }}</h3>
                            <p>Value: {{ item.value }}</p>
                        </div>
                        <div class="item-actions">
                            <button @click="startEdit(item)" class="btn-edit">Edit</button>
                            <button @click="deleteItem(item.id)" class="btn-delete">Delete</button>
                        </div>
                    </div>

                    <!-- 编辑表单 -->
                    <div v-else class="item-edit">
                        <input v-model="editingItem.value" placeholder="Value" />
                        <div class="edit-actions">
                            <button @click="updateItem" class="btn-save">Save</button>
                            <button @click="cancelEdit" class="btn-cancel">Cancel</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
    import { ref, onMounted } from 'vue';
    import axios from '@/axios';

    // 数据状态
    const items = ref([]);
    const newItem = ref({ id: null, value: '' });
    const editingId = ref(null);
    const editingItem = ref({ id: null, value: '' });

    // 获取所有项目
    const fetchItems = async () => {
        try {
            const response = await axios.get('/api/demo');
            items.value = response.data;
            // console.log('Fetched items:', response.data);
        } catch (error) {
            console.error('Error fetching items:', error);
        }
    };

    // 创建新项目
    const createItem = async () => {
        // 验证输入
        if (!newItem.value.id) {
            alert('Please enter an ID');
            return;
        }
        if (!newItem.value.value.trim()) {
            alert('Please enter a value');
            return;
        }

        try {
            await axios.post('/api/demo', {
                id: newItem.value.id,
                value: newItem.value.value,
            });
            // 清空表单
            newItem.value = { id: null, value: '' };
            // 刷新列表
            await fetchItems();
        } catch (error) {
            console.error('Error creating item:', error);
            alert(error.response?.data?.detail || 'Error creating item');
        }
    };

    // 开始编辑
    const startEdit = item => {
        editingId.value = item.id;
        editingItem.value = { ...item };
    };

    // 取消编辑
    const cancelEdit = () => {
        editingId.value = null;
        editingItem.value = { id: null, value: '' };
    };

    // 更新项目
    const updateItem = async () => {
        if (!editingItem.value.value.trim()) {
            alert('Please enter a value');
            return;
        }
        try {
            await axios.put(`/api/demo/${editingItem.value.id}`, editingItem.value);
            editingId.value = null;
            await fetchItems();
        } catch (error) {
            console.error('Error updating item:', error);
            alert(error.response?.data?.detail || 'Error updating item');
        }
    };

    // 删除项目
    const deleteItem = async id => {
        if (confirm('Are you sure you want to delete this item?')) {
            try {
                await axios.delete(`/api/demo/${id}`);
                await fetchItems();
            } catch (error) {
                console.error('Error deleting item:', error);
                alert(error.response?.data?.detail || 'Error deleting item');
            }
        }
    };

    // 页面加载时获取数据
    onMounted(fetchItems);
</script>

<style scoped>
    .demo-page {
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
    }

    .form-section,
    .list-section {
        margin-bottom: 30px;
        padding: 20px;
        background-color: #f5f5f5;
        border-radius: 8px;
    }

    .input-group {
        display: flex;
        gap: 10px;
        margin-bottom: 20px;
    }

    .id-input {
        width: 100px;
        /* 为ID输入框设置较小的宽度 */
    }

    .value-input {
        flex: 1;
        /* 值输入框占据剩余空间 */
    }

    input {
        padding: 8px;
        border: 1px solid #ddd;
        border-radius: 4px;
    }

    input[type='number'] {
        -moz-appearance: textfield;
        /* Firefox */
    }

    input[type='number']::-webkit-outer-spin-button,
    input[type='number']::-webkit-inner-spin-button {
        -webkit-appearance: none;
        margin: 0;
    }

    button {
        padding: 8px 16px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        transition: background-color 0.3s;
    }

    .btn-add {
        background-color: #4caf50;
        color: white;
        min-width: 100px;
    }

    .btn-edit {
        background-color: #2196f3;
        color: white;
    }

    .btn-delete {
        background-color: #f44336;
        color: white;
    }

    .btn-save {
        background-color: #4caf50;
        color: white;
    }

    .btn-cancel {
        background-color: #757575;
        color: white;
    }

    .items-list {
        display: grid;
        gap: 20px;
    }

    .item-card {
        padding: 15px;
        background-color: white;
        border-radius: 4px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    .item-view {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .item-content {
        flex: 1;
    }

    .item-actions {
        display: flex;
        gap: 10px;
    }

    .item-edit {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }

    .edit-actions {
        display: flex;
        gap: 10px;
        justify-content: flex-end;
    }

    .no-data {
        text-align: center;
        padding: 20px;
        color: #666;
    }

    h1,
    h2 {
        color: #333;
    }

    h3 {
        margin: 0;
        color: #444;
    }

    p {
        margin: 5px 0;
        color: #666;
    }

    button:hover {
        opacity: 0.9;
    }

    button:active {
        transform: scale(0.98);
    }
</style>
