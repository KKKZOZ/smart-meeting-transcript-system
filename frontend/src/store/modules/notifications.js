// store/modules/notifications.js
import axios from '@/axios';

export default {
    state: {
        unreadCount: 0,
    },
    mutations: {
        SET_UNREAD_COUNT(state, count) {
            state.unreadCount = count;
        },
        DECREMENT_UNREAD_COUNT(state) {
            if (state.unreadCount > 0) {
                state.unreadCount--;
            }
        },
        INCREMENT_UNREAD_COUNT(state) {
            state.unreadCount++;
        },
    },
    actions: {
        async fetchUnreadCount({ commit }) {
            try {
                const response = await axios.get('/api/notifications/users');
                const count = response.data.filter(n => n.status === 'UNREAD').length;
                commit('SET_UNREAD_COUNT', count);
            } catch (error) {
                console.error('获取未读通知数量失败:', error);
            }
        },
        updateUnreadCount({ commit }, { oldStatus, newStatus }) {
            if (oldStatus === 'UNREAD' && newStatus === 'READ') {
                commit('DECREMENT_UNREAD_COUNT');
            } else if (oldStatus === 'READ' && newStatus === 'UNREAD') {
                commit('INCREMENT_UNREAD_COUNT');
            }
        },
    },
};
