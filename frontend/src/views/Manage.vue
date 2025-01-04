<template>
    <div class="py-4 container-fluid">
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                    <!-- 标签页导航 -->
                    <div class="card-header pb-0">
                        <ul class="nav nav-tabs">
                            <li class="nav-item">
                                <a
                                    class="nav-link"
                                    :class="{ active: activeTab === 'meetings' }"
                                    @click="activeTab = 'meetings'"
                                    href="#"
                                >
                                    所有会议
                                </a>
                            </li>
                            <li class="nav-item">
                                <a
                                    class="nav-link"
                                    :class="{ active: activeTab === 'users' }"
                                    @click="activeTab = 'users'"
                                    href="#"
                                >
                                    用户列表
                                </a>
                            </li>
                        </ul>
                    </div>

                    <!-- 会议列表标签页 -->
                    <div v-show="activeTab === 'meetings'" class="card-body px-0 pt-0 pb-2">
                        <div class="d-flex justify-content-end px-3 py-3">
                            <div class="d-flex align-items-center gap-2" style="height: 40px">
                                <argon-input
                                    type="text"
                                    placeholder="搜索会议..."
                                    v-model="meetingsSearchKeyword"
                                    @keyup.enter="handleMeetingsSearch"
                                    class="w-auto mb-0"
                                    style="min-width: 200px"
                                />
                                <argon-button
                                    color="info"
                                    size="sm"
                                    @click="handleMeetingsSearch"
                                    class="mb-0 text-md"
                                >
                                    搜索
                                </argon-button>
                            </div>
                        </div>
                        <div class="table-responsive p-0">
                            <table class="table align-items-center mb-0">
                                <thead>
                                    <tr>
                                        <th
                                            class="text-secondary text-md font-weight-bolder opacity-7"
                                            >会议名称</th
                                        >
                                        <th
                                            class="text-secondary text-md font-weight-bolder opacity-7 ps-2"
                                            >开始时间</th
                                        >
                                        <th
                                            class="text-secondary text-md font-weight-bolder opacity-7 ps-2"
                                            >结束时间</th
                                        >
                                        <th
                                            class="text-center text-secondary text-md font-weight-bolder opacity-7"
                                            >会议所有者</th
                                        >
                                        <th
                                            class="text-center text-secondary text-md font-weight-bolder opacity-7"
                                            >操作</th
                                        >
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="meeting in meetings" :key="meeting.meeting_id">
                                        <td>
                                            <div class="d-flex px-2 py-1">
                                                <div
                                                    class="d-flex flex-column justify-content-center"
                                                >
                                                    <h6 class="mb-0 text-md">{{
                                                        meeting.title
                                                    }}</h6>
                                                </div>
                                            </div>
                                        </td>
                                        <td>
                                            <p class="text-md font-weight-bold mb-0">
                                                {{ new Date(meeting.start_time).toLocaleString() }}
                                            </p>
                                        </td>
                                        <td>
                                            <p class="text-md font-weight-bold mb-0">
                                                {{ new Date(meeting.end_time).toLocaleString() }}
                                            </p>
                                        </td>
                                        <td class="align-middle text-center text-md">
                                            <span class="badge badge-lg bg-gradient-info">
                                                {{ meeting.creator_name }}
                                            </span>
                                        </td>
                                        <td class="align-middle text-center">
                                            <div class="d-flex justify-content-center gap-3">
                                                <router-link
                                                    :to="`/transcript-page?meeting_id=${meeting.meeting_id}`"
                                                    class="text-secondary font-weight-bold text-md"
                                                >
                                                    查看详情
                                                </router-link>
                                                <a
                                                    href="javascript:;"
                                                    class="text-secondary font-weight-bold text-md"
                                                    @click="handleDeleteMeeting(meeting.meeting_id)"
                                                >
                                                    删除
                                                </a>
                                            </div>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <!-- 用户列表标签页 -->
                    <div v-show="activeTab === 'users'" class="card-body px-0 pt-0 pb-2">
                        <div class="d-flex justify-content-end px-3 py-3">
                            <div class="d-flex align-items-center gap-2" style="height: 40px">
                                <argon-input
                                    type="text"
                                    placeholder="搜索用户..."
                                    v-model="usersSearchKeyword"
                                    @keyup.enter="handleUsersSearch"
                                    class="w-auto mb-0"
                                    style="min-width: 200px"
                                />
                                <argon-button
                                    color="info"
                                    size="sm"
                                    @click="handleUsersSearch"
                                    class="mb-0 text-md"
                                >
                                    搜索
                                </argon-button>
                            </div>
                        </div>
                        <div class="table-responsive p-0">
                            <table class="table align-items-center mb-0">
                                <thead>
                                    <tr>
                                        <th
                                            class="text-secondary text-md font-weight-bolder opacity-7"
                                            >用户名</th
                                        >
                                        <th
                                            class="text-secondary text-md font-weight-bolder opacity-7 ps-2"
                                            >邮箱</th
                                        >
                                        <th
                                            class="text-center text-secondary text-md font-weight-bolder opacity-7"
                                            >角色</th
                                        >
                                        <th
                                            class="text-center text-secondary text-md font-weight-bolder opacity-7"
                                            >操作</th
                                        >
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="user in users" :key="user.user_id">
                                        <td>
                                            <div class="d-flex px-2 py-1">
                                                <div
                                                    class="d-flex flex-column justify-content-center"
                                                >
                                                    <h6 class="mb-0 text-md">{{
                                                        user.username
                                                    }}</h6>
                                                </div>
                                            </div>
                                        </td>
                                        <td>
                                            <p class="text-md font-weight-bold mb-0">{{
                                                user.email
                                            }}</p>
                                        </td>
                                        <td class="align-middle text-center text-md">
                                            <span
                                                class="badge badge-lg"
                                                :class="
                                                    user.root
                                                        ? 'bg-gradient-success'
                                                        : 'bg-gradient-info'
                                                "
                                            >
                                                {{ user.root ? '管理员' : '普通用户' }}
                                            </span>
                                        </td>
                                        <td class="align-middle text-center">
                                            <div class="d-flex justify-content-center gap-3">
                                                <a
                                                    href="javascript:;"
                                                    class="text-secondary font-weight-bold text-md"
                                                    @click="handleDeleteUser(user.user_id)"
                                                >
                                                    删除
                                                </a>
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
    </div>
</template>

<script setup>
    import { ref, onMounted } from 'vue';
    import axios from '@/axios';
    import ArgonInput from '@/components/ArgonInput.vue';
    import ArgonButton from '@/components/ArgonButton.vue';

    // 当前激活的标签
    const activeTab = ref('meetings');

    // 会议列表数据
    const meetings = ref([]);
    const meetingsSearchKeyword = ref('');

    // 用户列表数据
    const users = ref([]);
    const usersSearchKeyword = ref('');

    // 获取所有会议
    const fetchAllMeetings = async () => {
        try {
            const response = await axios.get('/api/getAllMeetings');
            meetings.value = response.data;
        } catch (error) {
            console.error('获取会议列表失败:', error.response?.data?.detail || error.message);
        }
    };

    const handleDeleteMeeting = async meetingId => {
        if (confirm('确定要删除这个会议吗？')) {
            try {
                await axios.delete('/api/deleteMeeting', {
                    data: { meeting_id: meetingId },
                });
                await fetchAllMeetings();
            } catch (error) {
                console.error('删除会议失败:', error.response?.data?.detail || error.message);
                alert('删除失败：' + (error.response?.data?.detail || error.message));
            }
        }
    };
    // 搜索会议
    const handleMeetingsSearch = async () => {
        try {
            const response = await axios.post('/api/searchAllMeetings', {
                keyword: meetingsSearchKeyword.value,
            });
            meetings.value = response.data;
        } catch (error) {
            console.error('搜索会议失败:', error.response?.data?.detail || error.message);
        }
    };

    // 获取所有用户
    const fetchAllUsers = async () => {
        try {
            const response = await axios.get('/api/getAllUsers');
            users.value = response.data;
        } catch (error) {
            console.error('获取用户列表失败:', error.response?.data?.detail || error.message);
        }
    };

    // 搜索用户
    const handleUsersSearch = async () => {
        try {
            const response = await axios.post('/api/searchAllUsers', {
                keyword: usersSearchKeyword.value,
            });
            users.value = response.data;
        } catch (error) {
            console.error('搜索用户失败:', error.response?.data?.detail || error.message);
        }
    };
    // 删除用户
    const handleDeleteUser = async userId => {
        if (confirm('确定要删除这个用户吗？')) {
            try {
                await axios.delete('/api/deleteUser', {
                    data: {
                        user_id: userId,
                    },
                });
                await fetchAllUsers();
            } catch (error) {
                console.error('删除用户失败:', error.response?.data?.detail || error.message);
                alert('删除失败：' + (error.response?.data?.detail || error.message));
            }
        }
    };

    onMounted(() => {
        fetchAllMeetings();
        fetchAllUsers();
    });
</script>

<style scoped>
    .nav-tabs {
        border-bottom: 1px solid #dee2e6;
        padding: 0 20px;
    }

    .nav-tabs .nav-link {
        cursor: pointer;
        color: #344767;
        font-weight: 500;
        font-size: 1.1rem;
        padding: 15px 30px;
        margin-right: 10px;
        transition: all 0.2s ease;
    }

    .nav-tabs .nav-link.active {
        color: #344767;
        font-weight: 600;
        border-bottom: 3px solid #344767;
    }

    .nav-tabs .nav-link:hover {
        border-color: transparent;
        background-color: rgba(52, 71, 103, 0.05);
    }

    .badge {
        font-size: 0.75rem;
        padding: 0.5em 0.75em;
    }
</style>
