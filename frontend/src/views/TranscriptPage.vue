<template>
    <div class="container-fluid py-4">
        <!-- 上传部分 -->
        <div v-if="isTranscribed === -1" class="row justify-content-center">
            <div class="col-md-8">
                <div class="card shadow-sm">
                    <div class="card-body text-center p-5">
                        <el-upload
                            class="upload-area"
                            drag
                            :before-upload="beforeUpload"
                            accept="audio/*"
                            :limit="1"
                        >
                            <el-icon class="el-icon--upload fs-1 mb-3">
                                <UploadFilled />
                            </el-icon>
                            <div class="el-upload__text mb-2"
                                >拖拽文件到此处或 <em>点击上传</em></div
                            >
                            <template #tip>
                                <div class="text-muted small"
                                    >支持上传音频文件 (MP3 或 WAV, 小于 50MB)</div
                                >
                            </template>
                        </el-upload>

                        <div v-if="fileToUpload" class="alert alert-info mt-3">
                            <p class="mb-0 text-white">已选择文件：{{ fileToUpload.name }}</p>
                        </div>

                        <div class="mt-4">
                            <el-button type="primary" size="large" @click="handleUpload">
                                开始上传
                            </el-button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- 转录内容显示部分 -->
        <div v-else class="transcript-section">
            <div class="row g-4">
                <!-- 左侧转录内容 -->
                <div class="col-md-6">
                    <div class="card shadow-sm h-100">
                        <div
                            class="card-header bg-primary text-white d-flex justify-content-between align-items-center"
                        >
                            <h5 class="mb-0 text-white fs-3">会议转录</h5>
                            <el-button
                                v-if="isTranscribed === 2"
                                type="primary"
                                plain
                                @click="
                                    () => {
                                        dialogVisible = true;
                                        fetchParticipants();
                                    }
                                "
                            >
                                对应参会人员
                            </el-button>
                        </div>
                        <div class="card-body" style="height: 55vh; overflow-y: auto">
                            <el-dialog v-model="dialogVisible" title="对应参会人员" width="500">
                                <div
                                    v-for="index in count"
                                    :key="index"
                                    style="margin-bottom: 16px"
                                >
                                    <div>发言人{{ index }}：</div>
                                    <el-select
                                        v-model="selections[index - 1]"
                                        placeholder="请选择"
                                        style="width: 240px"
                                    >
                                        <el-option
                                            v-for="option in speakerOptions"
                                            :key="option.value"
                                            :label="option.label"
                                            :value="option.value"
                                        />
                                    </el-select>
                                </div>
                                <template #footer>
                                    <div class="dialog-footer">
                                        <el-button @click="dialogVisible = false">取消</el-button>
                                        <el-button type="primary" @click="changeRoles"
                                            >确认</el-button
                                        >
                                    </div>
                                </template>
                            </el-dialog>

                            <pre class="mb-3 fs-5" style="white-space: pre-wrap">{{
                                Text || '请点击生成文字'
                            }}</pre>

                            <el-button
                                v-if="isTranscribed === 0"
                                type="primary"
                                @click="createTasks"
                                >生成文字</el-button
                            >
                        </div>
                    </div>
                </div>

                <!-- 右侧翻译内容 -->
                <div class="col-md-6">
                    <div class="card shadow-sm h-100">
                        <div class="card-header bg-primary text-white">
                            <h5 class="mb-0 text-white fs-3">翻译</h5>
                            <div class="mt-2 d-flex gap-2" v-if="[1, 2].includes(isTranscribed)">
                                <el-select v-model="value" placeholder="Select" class="flex-grow-1">
                                    <el-option
                                        v-for="item in options"
                                        :key="item.value"
                                        :label="item.label"
                                        :value="item.value"
                                    />
                                </el-select>
                                <el-button type="primary" @click="translateTasks"> 翻译 </el-button>
                            </div>
                        </div>
                        <div class="card-body" style="height: 55vh; overflow-y: auto">
                            <pre
                                v-if="[1, 2].includes(isTranscribed)"
                                class="fs-5"
                                style="white-space: pre-wrap"
                                >{{ translateText || '请选择要翻译成的语言' }}</pre
                            >
                            <p v-if="[-1, 0].includes(isTranscribed)" class="text-muted">
                                请先转录会议
                            </p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 音频播放器 -->
            <div class="mt-4">
                <div class="card shadow-sm">
                    <div class="card-body">
                        <audio ref="audioPlayer" controls class="w-100">
                            <source :src="audioSrc" type="audio/mp3" />
                            Your browser does not support the audio element.
                        </audio>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
    import { ref, onMounted } from 'vue';
    import { UploadFilled } from '@element-plus/icons-vue';
    import axios from '@/axios';
    import { ElMessage } from 'element-plus';
    import { useRoute } from 'vue-router';

    const route = useRoute();
    const meetingId = route.query.meeting_id;
    console.log(route.query.meeting_id);
    const isTranscribed = ref(-1); // 默认状态是-1，表示没有转录
    const audioSrc = ref('');
    let Text = ref('');
    let translateText = ref('');
    let isChanged = ref(false);
    let dialogVisible = ref(false);
    let fileToUpload = ref(null); // 用于存储选中的文件
    let count = ref(0);

    const value = ref('');
    const speakerOptions = ref([]);
    const selections = ref(new Array(count.value).fill(null)); // 存储每个选择器的值
    const options = [
        {
            value: 'zh',
            label: '中文',
        },
        {
            value: 'en',
            label: '英语',
        },
        {
            value: 'ru',
            label: '俄语',
        },
        {
            value: 'fra',
            label: '法语',
        },
        {
            value: 'de',
            label: '德语',
        },
    ];
    // 获取转录状态
    const getTranscriptionStatus = async () => {
        try {
            const response = await axios.get('/api/getTransStatus', {
                params: { meeting_id: meetingId },
            });
            console.log(response);
            // 根据返回值修改 isTranscribed
            if (response.data.status === 0) {
                isTranscribed.value = 0; // 没有转录内容
            } else if (response.data.status === 1) {
                isTranscribed.value = 1; // 转录中
            } else if (response.data.status === 2) {
                isTranscribed.value = 2; // 转录已完成
            } else {
                isTranscribed.value = -1;
            }
            Text.value = response.data.content;
            audioSrc.value = response.data.video_url;
            isChanged.value = response.data.ischanged;
            count.value = response.data.speaker_count;
        } catch (error) {
            console.error('请求失败', error);
            ElMessage.error('获取转录状态失败');
        }
    };

    const fetchParticipants = async () => {
        try {
            const response = await axios.get('/api/getParticipants', {
                params: { meeting_id: meetingId },
            }); // 请求用户数据的 API
            speakerOptions.value = response.data.map(user => ({
                value: user.participant_name, // 选项的值
                label: user.participant_name, // 选项的标签
            }));
        } catch (error) {
            console.error('Failed to fetch participants:', error);
            alert('Failed to load participant options.');
        }
    };

    // 组件加载时调用接口获取转录状态
    onMounted(() => {
        getTranscriptionStatus();
    });

    // 处理上传的文件
    const handleUpload = () => {
        if (fileToUpload.value) {
            // 创建 FormData 并附加文件
            const formData = new FormData();
            formData.append('file', fileToUpload.value);
            formData.append('meeting_id', meetingId);

            // 手动上传文件到后端
            axios
                .post('/api/upload', formData, {
                    headers: { 'Content-Type': 'multipart/form-data' },
                })
                .then(response => {
                    if (response.status === 200) {
                        ElMessage.success('文件上传成功');
                        isTranscribed.value = 0; // 切换显示内容
                    } else {
                        ElMessage.error('上传失败');
                    }
                })
                .catch(error => {
                    console.error('上传失败', error);
                    ElMessage.error('文件上传失败');
                });
        }
    };

    // 修改beforeUpload以便用户选择文件后，触发handleUpload
    const beforeUpload = file => {
        fileToUpload.value = file;
        return false; // 阻止自动上传
    };

    const changeRoles = async () => {
        try {
            // 构造 POST 请求的表单数据
            const formData = new FormData();
            formData.append('meeting_id', meetingId);
            formData.append('speakers', JSON.stringify(selections.value)); // 将选择器的值序列化为 JSON

            // 发送请求到后端
            const response = await axios.post('/api/setSpeaker', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data', // 设置表单数据类型
                },
            });

            console.log('Task started successfully:', response.data);

            Text.value = response.data.content;
            dialogVisible.value = false;
            getTranscriptionStatus();
            // 处理成功响应，例如记录任务信息或更新 UI
        } catch (error) {
            console.error('Error creating task:', error);
            // 处理错误，例如显示提示消息
        }
    };

    // 其他按钮功能（保持不变）
    const createTasks = async () => {
        try {
            // 发送 POST 请求到后端的 /transcript 路由
            isTranscribed.value = 1;
            Text.value =
                '正在转录中，请稍候。系统会在转录完成后通知您，请在收到通知后刷新该页面查看内容。';
            const formData = new FormData();
            formData.append('meeting_id', meetingId);
            const response = await axios.post('/api/transcript', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data', // 设置表单数据类型
                },
            });
            console.log('Task started successfully:', response.data);
            // 这里可以处理响应，例如提取返回的 task_id 等信息
        } catch (error) {
            console.error('Error creating task:', error);
        }
        // console.log('Generating summary...');
    };

    const translateTasks = async () => {
        try {
            // 发送 POST 请求到后端的 /transcript 路由
            const formData = new FormData();
            formData.append('meeting_id', meetingId);
            formData.append('to_language', value.value);
            const response = await axios.post('/api/translate', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data', // 设置表单数据类型
                },
            });
            console.log('Task started successfully:', response.data);
            // 这里可以处理响应，例如提取返回的 task_id 等信息
            translateText.value = response.data.translated;
        } catch (error) {
            console.error('Error creating task:', error);
        }
        // console.log('Translating tasks...');
    };
</script>

<style scoped>
    .upload-area {
        min-height: 300px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    /* 保持 Element Plus 上传组件的样式 */
    :deep(.el-upload-dragger) {
        width: 100%;
        height: 200px;
        max-width: 400px;
    }

    /* 自定义滚动条样式 */
    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #f1f1f1;
    }

    ::-webkit-scrollbar-thumb {
        background: #888;
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #555;
    }
</style>
