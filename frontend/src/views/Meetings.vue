<script setup>
    import { ref, onMounted } from 'vue';
    import axios from '@/axios';
    import ArgonInput from '@/components/ArgonInput.vue';
    import ArgonButton from '@/components/ArgonButton.vue';

    // 会议列表的响应式引用
    const meetings = ref([]);
    const searchKeyword = ref('');

    // 获取会议列表
    const fetchMeetings = async () => {
        try {
            const response = await axios.get('/api/getMeetings');
            meetings.value = response.data;
            console.log(meetings.value);
        } catch (error) {
            console.error('获取会议列表失败:', error.response?.data?.detail || error.message);
        }
    };

    // 删除会议
    const handleDelete = async meetingId => {
        if (confirm('确定要删除这个会议吗？')) {
            try {
                await axios.delete('/api/deleteMeeting', {
                    data: { meeting_id: meetingId },
                });
                await fetchMeetings();
            } catch (error) {
                console.error('删除会议失败:', error.response?.data?.detail || error.message);
                alert('删除失败：' + (error.response?.data?.detail || error.message));
            }
        }
    };

    // 搜索会议
    const handleSearch = async () => {
        try {
            const response = await axios.post('/api/searchMeeting', {
                keyword: searchKeyword.value,
            });
            meetings.value = response.data;
        } catch (error) {
            console.error('搜索会议失败:', error.response?.data?.detail || error.message);
        }
    };

    onMounted(() => {
        fetchMeetings();
    });
</script>

<template>
    <div class="py-4 container-fluid">
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-header pb-0 d-flex justify-content-between align-items-center">
                        <h4>我的会议列表</h4>
                        <argon-button
                            color="success"
                            size="sm"
                            @click="$router.push('/create-trans')"
                            class="mb-0 text-md"
                            style="font-size: 0.875rem"
                        >
                            <span class="text-md">创建新会议</span>
                        </argon-button>
                        <div class="d-flex align-items-center gap-2" style="height: 40px">
                            <argon-input
                                type="text"
                                placeholder="搜索会议..."
                                v-model="searchKeyword"
                                @keyup.enter="handleSearch"
                                class="w-auto mb-0"
                                style="min-width: 200px"
                            />
                            <argon-button
                                color="info"
                                size="sm"
                                @click="handleSearch"
                                class="mb-0 text-md"
                                style="font-size: 0.875rem"
                            >
                                <span class="text-md">搜索</span>
                            </argon-button>
                        </div>
                    </div>
                    <div class="card-body px-0 pt-0 pb-2">
                        <div class="table-responsive p-0">
                            <table class="table align-items-center mb-0">
                                <thead>
                                    <tr>
                                        <th
                                            class="text-secondary text-md font-weight-bolder opacity-7"
                                        >
                                            会议名称
                                        </th>
                                        <th
                                            class="text-secondary text-md font-weight-bolder opacity-7 ps-2"
                                        >
                                            开始时间
                                        </th>
                                        <th
                                            class="text-secondary text-md font-weight-bolder opacity-7 ps-2"
                                        >
                                            结束时间
                                        </th>
                                        <th
                                            class="text-center text-secondary text-md font-weight-bolder opacity-7"
                                        >
                                            会议所有者
                                        </th>
                                        <th
                                            class="text-center text-secondary text-md font-weight-bolder opacity-7"
                                        >
                                            操作
                                        </th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="meeting in meetings" :key="meeting.meeting_id">
                                        <td>
                                            <div class="d-flex px-2 py-1">
                                                <div
                                                    class="d-flex flex-column justify-content-center"
                                                >
                                                    <h6 class="mb-0 text-md">
                                                        {{ meeting.title }}
                                                    </h6>
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
                                                    @click="handleDelete(meeting.meeting_id)"
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
