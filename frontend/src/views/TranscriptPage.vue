<template>
    <div class="app-container">
        <!-- 控制显示上传组件还是文本和播放器 -->
        <div v-if="isTranscribed === -1" class="upload-section">
            <el-upload
                class="upload-demo"
                drag
                :before-upload="beforeUpload"
                accept="audio/*"
                :show-file-list="true"
            >
                <el-icon class="el-icon--upload">
                    <UploadFilled />
                </el-icon>
                <div class="el-upload__text">Drop file here or <em>click to upload</em></div>
                <template #tip>
                    <div class="el-upload__tip">Upload audio files (MP3 or WAV, under 50MB)</div>
                </template>
            </el-upload>
            <!-- 上传按钮 -->
            <el-button type="primary" @click="handleUpload">开始上传</el-button>
        </div>

        <!-- 显示文本和音频播放器 -->
        <div v-else class="transcript-section">
            <div class="text-display">
                <div class="left-text" style="max-height: 60vh; overflow-y: auto">
                    <h3>会议转录</h3>
                    <el-button
                        v-if="!isChanged && isTranscribed === 2"
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

                    <!-- 对话框 -->
                    <el-dialog v-model="dialogVisible" title="对应参会人员" width="500">
                        <div v-for="index in count" :key="index" style="margin-bottom: 16px">
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
                                <el-button type="primary" @click="changeRoles">确认</el-button>
                            </div>
                        </template>
                    </el-dialog>
                    <pre style="white-space: pre-wrap; word-wrap: break-word">{{
                        Text || '请点击生成文字'
                    }}</pre>
                    <el-button v-if="isTranscribed === 0" type="primary" @click="createTasks"
                        >生成文字</el-button
                    >
                </div>
                <div class="right-text" style="max-height: 60vh; overflow-y: auto">
                    <h3>翻译</h3>
                    <el-button
                        v-if="[1, 2].includes(isTranscribed)"
                        type="primary"
                        class="translate-button"
                        @click="translateTasks"
                        >翻译</el-button
                    >
                    <el-select
                        v-model="value"
                        v-if="[1, 2].includes(isTranscribed)"
                        placeholder="Select"
                        style="width: 240px"
                    >
                        <el-option
                            v-for="item in options"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                        />
                    </el-select>
                    <pre
                        style="white-space: pre-wrap; word-wrap: break-word"
                        v-if="[1, 2].includes(isTranscribed)"
                        >{{ translateText || '请选择要翻译成的语言' }}</pre
                    >
                    <p v-if="[-1, 0].includes(isTranscribed)">{{ '请先转录会议' }}</p>
                </div>
            </div>

            <!-- 音频播放器 -->
            <div class="audio-player">
                <audio ref="audioPlayer" controls>
                    <source :src="audioSrc" type="audio/mp3" />
                    Your browser does not support the audio element.
                </audio>
            </div>

            <div class="action-buttons">
                <el-button v-if="isTranscribed === 2" type="primary" @click="generateSummary"
                    >Summary</el-button
                >
                <el-button v-if="isTranscribed === 2" type="primary" @click="generateTasks"
                    >Tasks</el-button
                >
            </div>
        </div>
    </div>
</template>

<script setup>
    import { ref, onMounted } from 'vue';
    import { UploadFilled } from '@element-plus/icons-vue';
    import axios from 'axios';
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
    let fileToUpload = null; // 用于存储选中的文件
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
            const response = await axios.get('http://localhost:8000/api/getTransStatus', {
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
            const response = await axios.get('http://localhost:8000/api/getParticipants', {
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
        if (fileToUpload) {
            // 创建 FormData 并附加文件
            const formData = new FormData();
            formData.append('file', fileToUpload);
            formData.append('meeting_id', meetingId);

            // 手动上传文件到后端
            axios
                .post('http://localhost:8000/api/upload', formData, {
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
        fileToUpload = file;
        return false; // 阻止自动上传
    };

    const changeRoles = async () => {
        try {
            // 构造 POST 请求的表单数据
            const formData = new FormData();
            formData.append('meeting_id', meetingId);
            formData.append('speakers', JSON.stringify(selections.value)); // 将选择器的值序列化为 JSON

            // 发送请求到后端
            const response = await axios.post('http://localhost:8000/api/setSpeaker', formData, {
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
            const response = await axios.post('http://localhost:8000/api/transcript', formData, {
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
            const response = await axios.post('http://localhost:8000/api/translate', formData, {
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

    const generateSummary = () => {
        console.log('Generating summary...');
    };
    const generateTasks = () => {
        console.log('Generating tasks...');
    };
</script>

<style scoped>
    .app-container {
        max-width: 80%; /* 设置为宽度的 80% */
        height: 80vh; /* 设置高度为视口的 80% */
        margin: 0 auto;
        padding: 5px;
        flex-direction: column;
        align-items: center;
        justify-content: center; /* 垂直居中 */
    }

    .text-display {
        width: 100%;
        height: 65vh; /* 设置固定高度为屏幕的 70% */
        display: flex;
        justify-content: space-between;
        padding: 40px;
        background-color: #f9f9f9;
        border: 1px solid #ddd;
        border-radius: 8px;
        margin-bottom: 20px;
        overflow-y: auto; /* 超出时显示垂直滚动条 */
    }

    .text-display .left-text,
    .text-display .right-text {
        width: 45%; /* 保持左右两部分的宽度为 45% */
    }

    .text-display h3 {
        color: #333;
    }

    .text-display p {
        color: #555;
        white-space: normal; /* 允许自动换行 */
        word-wrap: break-word; /* 强制长单词换行 */
    }

    .upload-section {
        margin-bottom: 20px;
        height: 60vh;
    }

    .audio-player {
        width: 100%;
    }

    audio {
        width: 100%;
        outline: none;
    }

    .action-buttons {
        margin-top: 10px;
    }

    .action-buttons .el-button {
        margin-left: 10px;
    }

    .translate-button {
        margin-top: auto; /* 将按钮推到最底部 */
        font-size: 12px;
    }
</style>
