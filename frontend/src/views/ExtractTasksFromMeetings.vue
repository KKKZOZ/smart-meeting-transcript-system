<template>
    <div class="py-4 container-fluid">
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-header pb-0 d-flex justify-content-between align-items-center">
                        <h6>选择会议</h6>
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
                                            >会议名称</th
                                        >
                                        <th
                                            class="text-secondary text-md font-weight-bolder opacity-7"
                                            >会议内容(前100字)</th
                                        >
                                        <th
                                            class="text-secondary text-md font-weight-bolder opacity-7"
                                            >开始时间</th
                                        >
                                        <th
                                            class="text-center text-secondary text-md font-weight-bolder opacity-7"
                                        >
                                            会议创建者</th
                                        >
                                        <th
                                            class="text-center text-secondary text-md font-weight-bolder opacity-7"
                                            >操作
                                        </th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr
                                        v-for="meeting in filteredMeetings"
                                        :key="meeting.meeting_id"
                                    >
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
                                            <div
                                                style="
                                                    max-height: 10vh;
                                                    overflow-y: auto;
                                                    word-wrap: break-word;
                                                    white-space: normal;
                                                "
                                            >
                                                <p class="text-md font-weight-bold mb-0">{{
                                                    meeting.content
                                                }}</p>
                                            </div>
                                        </td>
                                        <td>
                                            <p class="text-md font-weight-bold mb-0">
                                                {{ new Date(meeting.start_time).toLocaleString() }}
                                            </p>
                                        </td>
                                        <td class="align-middle text-center text-md">
                                            <span class="badge badge-lg bg-gradient-info">{{
                                                meeting.creator_name
                                            }}</span>
                                        </td>
                                        <td class="align-middle text-center">
                                            <div class="d-flex justify-content-center gap-3">
                                                <argon-button
                                                    color="success"
                                                    size="sm"
                                                    @click="handleExtract(meeting.meeting_id)"
                                                    class="mb-0 text-md"
                                                >
                                                    <span class="text-md">提取待办事项</span>
                                                </argon-button>
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
    import { onMounted, ref } from 'vue';
    import axios from '@/axios';
    import router from '../router';
    import ArgonInput from '@/components/ArgonInput.vue';
    import ArgonButton from '@/components/ArgonButton.vue';

    const meetings = ref([]);
    const filteredMeetings = ref([]);

    const fetchMeetings = async () => {
        try {
            const response = await axios.post('/api/meetings-to-extract');
            meetings.value = response.data;
            filteredMeetings.value = meetings.value;
            console.log(meetings.value);
        } catch (error) {
            console.error('获取会议列表失败:', error.response?.data?.detail || error.message);
        }
    };

    const handleSearch = () => {
        const keyword = searchKeyword.value.toLowerCase(); // 转小写以便不区分大小写搜索
        filteredMeetings.value = meetings.value.filter(meeting => {
            return meeting.title.toLowerCase().includes(keyword);
        });
    };

    const searchKeyword = ref('');

    const handleExtract = meeting_id => {
        router.push({
            path: '/new-tasks',
            query: { meeting_id: meeting_id },
        });
    };

    onMounted(() => {
        fetchMeetings();
    });
</script>
