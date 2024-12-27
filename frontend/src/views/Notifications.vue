<!-- NotificationList.vue -->
<template>
    <div class="notification-list">
        <h2>通知列表</h2>

        <table class="notifications-table">
            <thead>
                <tr>
                    <th>内容</th>
                    <th>截止时间</th>
                    <th>状态</th>
                    <th>操作</th>
                </tr>
            </thead>
            <tbody>
                <tr
                    v-for="notification in notifications"
                    :key="notification.notification_id"
                    class="notification-item"
                    :class="{ unread: notification.status === 'UNREAD' }"
                    @click="showNotificationDetail(notification)"
                >
                    <td class="content">
                        {{ notification.content }}
                    </td>
                    <td class="time">{{ formatDate(notification.ddl) }}</td>
                    <td class="status">
                        {{ notification.status === 'UNREAD' ? '未读' : '已读' }}
                    </td>
                    <td class="actions">
                        <button @click.stop="toggleStatus(notification)">
                            {{ notification.status === 'UNREAD' ? '标记已读' : '标记未读' }}
                        </button>
                        <button
                            class="delete"
                            @click.stop="deleteNotification(notification.notification_id)"
                        >
                            删除
                        </button>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script setup>
    import { ref, onMounted } from 'vue';
    import axios from '@/axios';

    const notifications = ref([]);
    const showDetail = ref(false);
    const selectedNotification = ref(null);

    // 获取当前用户的通知列表
    const getNotifications = async () => {
        try {
            const response = await axios.get('http://localhost:8000/api/notifications/users');
            notifications.value = response.data;
        } catch (error) {
            console.error('获取通知列表失败:', error);
        }
    };

    // 删除通知
    const deleteNotification = async id => {
        try {
            await axios.delete(`http://localhost:8000/api/notifications/${id}`);
            notifications.value = notifications.value.filter(n => n.notification_id !== id);
        } catch (error) {
            console.error('删除通知失败:', error);
        }
    };

    // 切换通知状态
    const toggleStatus = async notification => {
        try {
            const newStatus = notification.status === 'UNREAD' ? 'READ' : 'UNREAD';
            const response = await axios.put(
                `http://localhost:8000/api/notifications/${notification.notification_id}`, // 使用路径参数
                { status: newStatus }, // 请求体中只包含 status
            );
            const index = notifications.value.findIndex(
                n => n.notification_id === notification.notification_id,
            );
            notifications.value[index] = response.data;
        } catch (error) {
            console.error('更新通知状态失败:', error);
        }
    };

    // 显示通知详情
    const showNotificationDetail = notification => {
        selectedNotification.value = notification;
        showDetail.value = true;
    };

    // 格式化日期
    const formatDate = date => {
        return new Date(date).toLocaleString();
    };

    onMounted(() => {
        getNotifications();
    });
</script>

<style scoped>
    .notification-list {
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
    }

    .notifications-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
    }

    .notifications-table th,
    .notifications-table td {
        text-align: left;
        padding: 12px;
        border-bottom: 1px solid #ddd;
        height: 60px; /* 设置固定高度 */
        vertical-align: middle; /* 可选：垂直居中 */
        background-color: white;
    }

    .notifications-table th {
        background-color: #f5f5f5;
        font-weight: bold;
    }

    .notification-item {
        cursor: pointer;
        height: 60px;
    }

    .notification-item.unread {
        background-color: #f0f7ff;
    }

    .notification-item:hover {
        background-color: #aed3f7;
    }

    .content {
        font-weight: 600;
    }

    .time,
    .status {
        font-size: 0.9em;
        color: #666;
    }

    .actions {
        display: flex;
        gap: 8px;
    }

    .actions button {
        padding: 6px 12px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        font-size: 0.9em;
    }

    .actions button.delete {
        background-color: #ff4444;
        color: white;
    }

    /* 模态框样式，如果你的 Modal 组件有自己的样式，这里可以省略 */
    .modal {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .modal-content {
        background-color: white;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
        min-width: 300px;
        max-width: 80%;
    }

    .detail-content {
        margin: 15px 0;
    }
</style>
