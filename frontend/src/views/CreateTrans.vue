<template>
    <div class="container py-4">
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="card shadow">
                    <div class="card-header bg-primary text-white">
                        <h2 class="mb-0 fs-4 text-white">创建新会议</h2>
                    </div>

                    <div class="card-body">
                        <form @submit.prevent="submitMeeting">
                            <!-- 会议名称 -->
                            <div class="mb-3">
                                <label for="meeting-name" class="form-label">会议名称</label>
                                <input
                                    id="meeting-name"
                                    v-model="meeting.name"
                                    type="text"
                                    class="form-control"
                                    placeholder="请在框内输入会议名称"
                                    required
                                />
                            </div>

                            <!-- 起止时间 -->
                            <div class="row mb-3">
                                <div class="col-md-6">
                                    <label for="start-time" class="form-label">会议开始时间</label>
                                    <input
                                        id="start-time"
                                        v-model="meeting.startTime"
                                        type="datetime-local"
                                        class="form-control"
                                        required
                                    />
                                </div>
                                <div class="col-md-6">
                                    <label for="end-time" class="form-label">会议结束时间</label>
                                    <input
                                        id="end-time"
                                        v-model="meeting.endTime"
                                        type="datetime-local"
                                        class="form-control"
                                        required
                                    />
                                </div>
                            </div>

                            <!-- 会议语言 -->
                            <div class="mb-3">
                                <label for="language" class="form-label">请选择会议主语言</label>
                                <select
                                    id="language"
                                    v-model="meeting.language"
                                    class="form-select"
                                    required
                                >
                                    <option value="zh">汉语</option>
                                    <option value="en">英语</option>
                                </select>
                            </div>

                            <!-- 参会人员 -->
                            <div class="mb-3">
                                <label class="form-label">参会人员</label>
                                <el-select
                                    v-model="value1"
                                    multiple
                                    collapse-tags
                                    collapse-tags-tooltip
                                    placeholder="选择"
                                    class="w-100"
                                >
                                    <el-option
                                        v-for="item in options"
                                        :key="item.value"
                                        :label="item.label"
                                        :value="item.value"
                                    />
                                </el-select>
                            </div>

                            <!-- 提交按钮 -->
                            <div class="d-grid">
                                <button type="submit" class="btn btn-primary">创建会议</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
    import { ref, onMounted } from 'vue';
    import axios from '@/axios';
    import router from '../router';

    // 表单数据
    const meeting = ref({
        name: '',
        startTime: '',
        endTime: '',
        language: 'zh',
    });

    const value1 = ref([]);
    const options = ref([]);

    // 从后端获取用户列表
    const fetchUsers = async () => {
        try {
            const response = await axios.get('/api/getUsers'); // 请求用户数据的 API
            options.value = response.data.map(user => ({
                value: user.participant_id, // 选项的值
                label: user.participant_name, // 选项的标签
            }));
        } catch (error) {
            console.error('Failed to fetch users:', error);
            alert('Failed to load user options.');
        }
    };

    // 提交表单数据
    const submitMeeting = async () => {
        // 验证参会人员是否至少选择了一个
        if (value1.value.length === 0) {
            alert('请至少选择一个参会人员！');
            return;
        }

        // 验证会议开始时间是否早于结束时间
        const startTime = new Date(meeting.value.startTime);
        const endTime = new Date(meeting.value.endTime);
        if (startTime >= endTime) {
            alert('会议开始时间必须早于结束时间！');
            return;
        }

        const payload = {
            title: meeting.value.name, // 后端期望的字段是 title
            start_time: meeting.value.startTime, // 后端期望的字段是 start_time
            end_time: meeting.value.endTime, // 后端期望的字段是 end_time
            language: meeting.value.language, // 后端期望的字段是 language
            participants: value1.value,
        };

        try {
            const response = await axios.post('/api/meetings', payload);
            console.log(response);
            alert('Meeting created successfully!');
            router.push({
                path: '/transcript-page',
                query: { meeting_id: response.data.meeting_id },
            });
        } catch (error) {
            console.log(error);
            console.error('Error creating meeting:', error);
            alert('Failed to create meeting.');
        }
    };

    onMounted(() => {
        fetchUsers();
    });
</script>

<style scoped>
    .el-select {
        width: 100% !important;
    }
</style>
