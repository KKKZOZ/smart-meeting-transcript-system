<template>
    <div class="container-fluid">
        <div class="row justify-content-center">
            <div class="col-12 col-xl-10">
                <h2 class="my-4">Notification List</h2>

                <div class="table-responsive bg-white rounded shadow-sm">
                    <table class="table table-hover align-middle mb-0">
                        <thead class="table-light">
                            <tr>
                                <th class="rounded-top-start" style="width: 12%">Type</th>
                                <th style="width: 35%">Content</th>
                                <th style="width: 15%">DDL</th>
                                <th style="width: 10%">Status</th>
                                <th class="rounded-top-end" style="width: 28%">Operation</th>
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
                                        :class="getNotificationType(notification).bootstrapClass"
                                    >
                                        {{ getNotificationType(notification).text }}
                                    </span>
                                </td>
                                <td class="fs-6 content-cell">{{ notification.content }}</td>
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
                                    <div class="align-middle">
                                        <div class="btn-group" role="group">
                                            <button
                                                class="btn btn-primary btn-sm fs-6"
                                                @click.stop="toggleStatus(notification)"
                                            >
                                                {{
                                                    notification.status === 'UNREAD'
                                                        ? '标记已读'
                                                        : '标记未读'
                                                }}
                                            </button>
                                            <button
                                                class="btn btn-success btn-sm fs-6"
                                                @click.stop="handleDetailClick(notification)"
                                            >
                                                查看详情
                                            </button>
                                            <button
                                                class="btn btn-danger btn-sm fs-6"
                                                @click.stop="
                                                    deleteNotification(notification.notification_id)
                                                "
                                            >
                                                删除
                                            </button>
                                        </div>
                                    </div>
                                </td>
                            </tr>
                        </tbody>
                    </table>
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
            console.debug(`需要跳转到任务详情页面，任务ID: ${notification.task_id}`);
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
    .btn-group .btn {
        margin: 12px 0 !important;
    }

    .content-cell {
        max-width: 300px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    @media (max-width: 768px) {
        .btn-group {
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
        }

        .btn-group .btn {
            width: 100%;
            margin: 0;
        }
    }
</style>
