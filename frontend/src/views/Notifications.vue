<!-- NotificationList.vue -->
<template>
    <div class="notification-list">
        <h2>通知列表</h2>

        <!-- 通知列表 -->
        <div class="notifications">
            <div
                v-for="notification in notifications"
                :key="notification.notification_id"
                class="notification-item"
                :class="{ unread: notification.status === 'UNREAD' }"
            >
                <!-- 通知内容 -->
                <div class="notification-content" @click="showNotificationDetail(notification)">
                    <div class="title">{{ notification.content }}</div>
                    <div class="time">截止时间: {{ formatDate(notification.ddl) }}</div>
                </div>

                <!-- 操作按钮 -->
                <div class="actions">
                    <button @click="toggleStatus(notification)">
                        {{ notification.status === 'UNREAD' ? '标记已读' : '标记未读' }}
                    </button>
                    <button
                        class="delete"
                        @click="deleteNotification(notification.notification_id)"
                    >
                        删除
                    </button>
                </div>
            </div>
        </div>

        <!-- 通知详情弹窗 -->
        <div v-if="showDetail" class="modal">
            <div class="modal-content">
                <h3>通知详情</h3>
                <div class="detail-content">
                    <p>内容: {{ selectedNotification.content }}</p>
                    <p>截止时间: {{ formatDate(selectedNotification.ddl) }}</p>
                    <p>
                        状态:
                        {{ selectedNotification.status === 'UNREAD' ? '未读' : '已读' }}
                    </p>
                </div>
                <button @click="showDetail = false">关闭</button>
            </div>
        </div>
    </div>
</template>

<script setup>
    import { ref, onMounted } from 'vue';
    import axios from 'axios';

    const notifications = ref([]);
    const showDetail = ref(false);
    const selectedNotification = ref(null);

    // 获取通知列表
    const getNotifications = async () => {
        try {
            const response = await axios.get('http://localhost:8000/api/notifications');
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
                `http://localhost:8000/api/notifications/${notification.notification_id}/status`,
                { status: newStatus },
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

    .notification-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 15px;
        margin-bottom: 10px;
        border: 1px solid #ddd;
        border-radius: 4px;
    }

    .notification-item.unread {
        background-color: #f0f7ff;
    }

    .notification-content {
        flex: 1;
        cursor: pointer;
    }

    .title {
        font-weight: bold;
        margin-bottom: 5px;
    }

    .time {
        font-size: 0.9em;
        color: #666;
    }

    .actions button {
        margin-left: 10px;
        padding: 5px 10px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
    }

    .actions button.delete {
        background-color: #ff4444;
        color: white;
    }

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
        border-radius: 4px;
        min-width: 300px;
    }

    .detail-content {
        margin: 15px 0;
    }
</style>
