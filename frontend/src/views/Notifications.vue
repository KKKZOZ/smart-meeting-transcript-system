<template>
    <div class="container-fluid">
        <div class="row justify-content-center">
            <div class="col-12 col-xl-10">
                <h2 class="my-4">通知列表</h2>

                <!-- 移动端卡片视图 -->
                <div class="d-block d-lg-none">
                    <div
                        v-for="notification in notifications"
                        :key="notification.notification_id"
                        class="card mb-3"
                        :class="{ 'border-primary': notification.status === 'UNREAD' }"
                    >
                        <div class="card-body">
                            <div class="d-flex justify-content-between align-items-center mb-2">
                                <span
                                    class="badge fs-6"
                                    :class="getNotificationType(notification).bootstrapClass"
                                >
                                    {{ getNotificationType(notification).text }}
                                </span>
                                <span
                                    class="badge fs-6"
                                    :class="
                                        notification.status === 'UNREAD'
                                            ? 'bg-primary'
                                            : 'bg-secondary'
                                    "
                                >
                                    {{ notification.status === 'UNREAD' ? '未读' : '已读' }}
                                </span>
                            </div>
                            <p class="card-text mb-2">{{ notification.content }}</p>
                            <p class="card-text">
                                <small class="text-muted"
                                    >截止时间: {{ formatDate(notification.ddl) }}</small
                                >
                            </p>
                            <div class="d-flex gap-2 mt-3">
                                <button
                                    class="btn btn-primary btn-sm flex-grow-1"
                                    @click="toggleStatus(notification)"
                                >
                                    {{ notification.status === 'UNREAD' ? '标记已读' : '标记未读' }}
                                </button>
                                <button
                                    class="btn btn-success btn-sm flex-grow-1"
                                    @click="handleDetailClick(notification)"
                                >
                                    查看详情
                                </button>
                                <button
                                    class="btn btn-danger btn-sm flex-grow-1"
                                    @click="deleteNotification(notification.notification_id)"
                                >
                                    删除
                                </button>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 桌面端表格视图 -->
                <div class="d-none d-lg-block">
                    <div class="table-responsive bg-white rounded shadow-sm">
                        <table class="table table-hover align-middle mb-0">
                            <thead class="table-light">
                                <tr>
                                    <th style="min-width: 100px; width: 12%">类型</th>
                                    <th style="min-width: 200px; width: 35%">内容</th>
                                    <th style="min-width: 150px; width: 15%">截止时间</th>
                                    <th style="min-width: 80px; width: 10%">状态</th>
                                    <th style="min-width: 300px; width: 28%">操作</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr
                                    v-for="notification in notifications"
                                    :key="notification.notification_id"
                                    :class="{ 'table-info': notification.status === 'UNREAD' }"
                                >
                                    <td>
                                        <span
                                            class="badge fs-6"
                                            :class="
                                                getNotificationType(notification).bootstrapClass
                                            "
                                        >
                                            {{ getNotificationType(notification).text }}
                                        </span>
                                    </td>
                                    <td class="text-truncate content-cell">
                                        {{ notification.content }}
                                    </td>
                                    <td>{{ formatDate(notification.ddl) }}</td>
                                    <td>
                                        <span
                                            class="badge fs-6"
                                            :class="
                                                notification.status === 'UNREAD'
                                                    ? 'bg-primary'
                                                    : 'bg-secondary'
                                            "
                                        >
                                            {{ notification.status === 'UNREAD' ? '未读' : '已读' }}
                                        </span>
                                    </td>
                                    <td>
                                        <div class="d-flex gap-2 operation-buttons">
                                            <button
                                                class="btn btn-primary btn-sm operation-btn"
                                                @click="toggleStatus(notification)"
                                            >
                                                {{
                                                    notification.status === 'UNREAD'
                                                        ? '标记已读'
                                                        : '标记未读'
                                                }}
                                            </button>
                                            <button
                                                class="btn btn-success btn-sm operation-btn"
                                                @click="handleDetailClick(notification)"
                                            >
                                                查看详情
                                            </button>
                                            <button
                                                class="btn btn-danger btn-sm operation-btn"
                                                @click="
                                                    deleteNotification(notification.notification_id)
                                                "
                                            >
                                                删除
                                            </button>
                                        </div>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
    import { ref, onMounted } from 'vue';
    import { useRouter } from 'vue-router';
    import { useStore } from 'vuex';
    import axios from '@/axios';

    const router = useRouter();
    const store = useStore();
    const notifications = ref([]);

    const getNotificationType = notification => {
        if (notification.meeting_id) {
            return {
                text: '会议通知',
                class: 'type-meeting',
                bootstrapClass: 'bg-primary',
            };
        } else if (notification.task_id) {
            return {
                text: '任务通知',
                class: 'type-task',
                bootstrapClass: 'bg-success',
            };
        }
        return {
            text: '其他通知',
            class: 'type-other',
            bootstrapClass: 'bg-secondary',
        };
    };

    // 获取当前用户的通知列表
    const getNotifications = async () => {
        try {
            const response = await axios.get('/api/notifications/users');
            notifications.value = response.data;
        } catch (error) {
            console.error('获取通知列表失败:', error);
        }
    };

    // 删除通知
    const deleteNotification = async id => {
        try {
            const notification = notifications.value.find(n => n.notification_id === id);
            await axios.delete(`/api/notifications/${id}`);
            notifications.value = notifications.value.filter(n => n.notification_id !== id);

            // 如果删除的是未读通知，更新计数
            if (notification.status === 'UNREAD') {
                store.commit('DECREMENT_UNREAD_COUNT');
            }
        } catch (error) {
            console.error('删除通知失败:', error);
        }
    };

    // 切换通知状态
    const toggleStatus = async notification => {
        try {
            const oldStatus = notification.status;
            const newStatus = oldStatus === 'UNREAD' ? 'READ' : 'UNREAD';

            const response = await axios.put(`/api/notifications/${notification.notification_id}`, {
                status: newStatus,
            });

            const index = notifications.value.findIndex(
                n => n.notification_id === notification.notification_id,
            );
            notifications.value[index] = response.data;

            // 更新未读计数
            store.dispatch('updateUnreadCount', {
                oldStatus,
                newStatus,
            });
        } catch (error) {
            console.error('更新通知状态失败:', error);
        }
    };

    // 处理详情按钮点击
    const handleDetailClick = notification => {
        if (notification.meeting_id) {
            router.push({
                path: '/transcript-page',
                query: { meeting_id: notification.meeting_id },
            });
        } else if (notification.task_id) {
            // console.debug(`需要跳转到任务详情页面，任务ID: ${notification.task_id}`);
            router.push({
                path: '/tasks',
            });
        }
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
    /* 表格内容样式 */
    .content-cell {
        max-width: 300px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }

    /* 操作按钮容器 */
    .operation-buttons {
        flex-wrap: nowrap;
        min-width: 300px;
        justify-content: flex-start;
        justify-items: center;
        align-items: center; /* 添加这行来使按钮垂直居中 */
        height: 100%; /* 确保容器占满单元格高度 */
    }

    /* 操作按钮样式 */
    .operation-btn {
        min-width: 90px;
        white-space: nowrap;
        padding: 0.25rem 0.25rem;
        font-size: 0.875rem;
        margin: 0;
    }

    /* 卡片样式 */
    .card {
        transition: all 0.3s ease;
        border-radius: 8px;
    }

    .card:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }

    /* 表格响应式样式 */
    .table-responsive {
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
        max-width: 100%;
    }

    /* 表格hover效果 */
    .table-hover tbody tr:hover {
        background-color: rgba(0, 0, 0, 0.02);
    }

    /* 美化滚动条 */
    .table-responsive::-webkit-scrollbar {
        height: 8px;
    }

    .table-responsive::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 4px;
    }

    .table-responsive::-webkit-scrollbar-thumb {
        background: #888;
        border-radius: 4px;
    }

    .table-responsive::-webkit-scrollbar-thumb:hover {
        background: #555;
    }

    /* 响应式调整 */
    @media (max-width: 1200px) {
        .content-cell {
            max-width: 250px;
        }
    }

    @media (max-width: 992px) {
        .content-cell {
            max-width: 200px;
        }

        .operation-btn {
            padding: 0.2rem 0.4rem;
        }
    }

    /* 移动端卡片按钮样式 */
    @media (max-width: 576px) {
        .card .btn {
            font-size: 0.875rem;
            padding: 0.25rem 0.5rem;
        }

        .card .card-body {
            padding: 1rem;
        }
    }

    /* 确保表格内容垂直居中 */
    .table td,
    .table th {
        vertical-align: middle;
    }

    /* Badge样式优化 */
    .badge {
        font-weight: 500;
        padding: 0.5em 0.75em;
    }
</style>
