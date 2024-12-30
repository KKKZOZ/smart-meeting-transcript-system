<template>
    <div>
        <input type="text" v-model="searchQuery" placeholder="搜索历史会议..." />
        <button class="search_button" @click="search">
            <img src="@/assets/img/magnifier.png" alt="Search" />
        </button>
    </div>
    <div>
        <table>
            <tr>
                <th>Meeting Title</th>
                <th>Meeting Content</th>
                <th>Transcription Time</th>
                <th> </th>
                <th> </th>
            </tr>
            <tr v-for="(item, index) in title" :key="index">
                <td>{{ item }}</td>
                <td>
                    <textarea v-model="content[index]"> </textarea>
                </td>

                <td>{{ timestamp[index] }}</td>
                <td>
                    <button @click="create(index)">Create</button>
                </td>
                <td>
                    <button @click="checkHistory(index)">History Summary</button>
                </td>
            </tr>
        </table>
    </div>

    <div v-if="showModal" class="modal">
        <div class="modal-content">
            <h2>{{ meetingTitle }}会议</h2>
            <div class="form-group">
                <label for="summaryType">请输入您要选择的摘要类型</label>

                <br />

                <input
                    type="text"
                    id="summaryType"
                    v-model="summaryType"
                    placeholder="简要概述"
                    style="width: 300px; height: 40px"
                />
            </div>
            <div class="modal-footer">
                <button @click="goBack">返回</button>
                <button @click="generateSummary">生成</button>
            </div>
        </div>
    </div>

    <div v-if="showModalResult" class="modal">
        <div class="modal-content">
            <h2>{{ meetingTitle }}会议</h2>
            <div class="form-group">
                <!-- <label for="summaryType">
                    {{ summaryContent }}

                </label> -->
                <div>
                    <textarea
                        v-model="summaryContent"
                        @input="updateText"
                        placeholder="“{{summaryContent}}”"
                        style="width: 300px; height: 200px"
                    ></textarea>
                </div>
                <div class="modal-footer">
                    <button @click="confirm">确定</button>
                    <button @click="goBack">返回</button>
                </div>
            </div>
        </div>
    </div>

    <div v-if="showModalhistory" class="modal">
        <div class="modal-content">
            <h2>{{ meetingTitle }}会议</h2>
            <div class="form-group">
                <table>
                    <tr v-for="(item, index) in historyTime" :key="index">
                        <td>{{ item }}</td>
                        <td>
                            <textarea v-model="historyType[index]"> </textarea>
                        </td>
                        <td>
                            <button @click="checkHistoryItem(index)">查看</button>
                        </td>
                        <td>
                            <button @click="deleteHistory(index)">删除</button>
                        </td>
                    </tr>
                </table>
                <div class="modal-footer">
                    <button @click="goBack">返回</button>
                </div>
            </div>
        </div>
    </div>

    <div v-if="showModalHistoryItem" class="modal">
        <div class="modal-content">
            <h2>{{ meetingTitle }}会议</h2>
            <div class="form-group">
                <!-- <label for="summaryType">
                    {{ summaryContent }}

                </label> -->
                <div>
                    <label @input="updateText" style="width: 300px; height: 200px">
                        {{ HistoryItem }}
                    </label>
                </div>
                <div class="modal-footer">
                    <!-- <button @click="confirm">确定</button> -->
                    <button @click="goBack">返回</button>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
    input {
        width: calc(100% - 500px);
        position: relative;
        left: 40px;
        padding: 10px 20px;
        margin: 10px 0;
        box-sizing: border-box;
        border-radius: 20px;
    }

    table {
        width: 100%;
        position: relative;
        left: 40px;
        width: calc(100% - 460px);
        border-collapse: collapse;
        background-color: #ffffff;
    }

    .search_button {
        width: 40px;
        height: 40px;
        background: none;
        border: none;
        cursor: pointer;
        position: relative;
        left: 40px;
        padding: 0;
        margin-left: 10px;
    }

    button img {
        width: 100%;
        height: 100%;
    }
    .modal {
        display: flex;
        justify-content: center;
        align-items: center;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5);
    }

    .modal-content {
        background-color: white;
        padding: 20px;
        border-radius: 5px;
        width: 400px;
        text-align: center;
    }

    .form-group {
        margin-bottom: 20px;
    }

    .modal-footer {
        display: flex;
        justify-content: space-between;
    }
    .text-container {
        width: 300px;
        min-height: 50px; /* 设置最小高度 */
        border: 1px solid #ccc;
        padding: 10px;
        word-wrap: break-word;
        overflow-wrap: break-word;
        white-space: pre-wrap;
    }
</style>

<script setup>
    import { ref, onMounted } from 'vue';
    import axios from '@/axios';
    // import { textProps } from 'element-plus';
    // import debounce from 'lodash/debounce';
    // import { useRouter } from 'vue-router';
    // const router = useRouter();
    const title = ref([]);
    const content = ref([]);
    const timestamp = ref([]);
    const meeting_id = ref([]);
    const historyTime = ref([]);
    const historyType = ref([]);
    const historyContent = ref([]);
    const searchQuery = ref('');
    const now_index = ref('');
    // const sum_index = ref('');
    const showModal = ref(false);
    const showModalResult = ref(false);
    const summaryType = ref('');
    const summaryContent = ref('');
    const meetingTitle = ref('');
    const showModalhistory = ref(false);
    const showModalHistoryItem = ref(false);
    const HistoryItem = ref('');
    // const newsummary = ref('');
    // 从后端获取用户列表
    const fetchData = async () => {
        try {
            const response = await axios.get('/api/getMeetingData'); // 请求用户数据的 API
            console.log(response);
            title.value = response.data.title;
            content.value = response.data.content;
            timestamp.value = response.data.timestamp;
            meeting_id.value = response.data.meeting_id;
            // alert('load user options.');
        } catch (error) {
            console.error('Failed to fetch data:', error);
            alert('Failed to load data.');
        }
    };

    const searchData = async () => {
        try {
            // alert('searching');
            const response = await axios.get('/api/searchquery', {
                params: { s_query: searchQuery.value },
            }); // 请求用户数据的 API
            console.log(response);
            title.value = response.data.title;
            content.value = response.data.content;
            timestamp.value = response.data.timestamp;
            meeting_id.value = response.data.meeting_id;
            // alert('load user options.');
        } catch (error) {
            console.error('Failed to fetch users:', error);
            alert('Failed to load user options.');
        }
    };
    const search = async () => {
        console.log('Searching for:', searchQuery.value);
        searchData();
    };

    const create = index => {
        console.log(`Create button clicked for index: ${meeting_id.value[index]}`);
        // 在这里添加你的逻辑
        // router.push({ name: 'summaryCreate', params: {meetingId,meetingTitle} });
        now_index.value = index;
        showModal.value = true;
        meetingTitle.value = title.value[index];
    };
    const goBack = () => {
        showModal.value = false;
        showModalResult.value = false;
        showModalhistory.value = false;
        showModalHistoryItem.value = false;
    };

    const generateSummary = async () => {
        console.log('generateSummary called');
        if (summaryType.value == '') {
            summaryType.value = '简要概述';
        }

        const response = await axios.get('/api/genSummary', {
            params: { type: summaryType.value, content: content.value[now_index.value] },
            timeout: 10000,
        }); // 请求用户数据的 APIdata
        console.log(response.data);
        summaryContent.value = response.data;
        showModalResult.value = true;
        showModal.value = false;
    };

    const confirm = async () => {
        console.log('confirm called');

        // alert(summaryContent.value+meeting_id.value[now_index.value]+summaryType.value);
        const response = await axios.get('/api/confirmSummary', {
            params: {
                content: summaryContent.value,
                meeting_id: meeting_id.value[now_index.value],
                type: summaryType.value,
            },
        }); // 请求用户数据的 APIdata
        console.log(response.data);
        showModalResult.value = false;
    };

    const checkHistory = async index => {
        console.log('checkHistory called');
        now_index.value = index;
        // alert(meeting_id.value[now_index.value]);
        const response = await axios.get('/api/checkhistory', {
            params: { meeting_id: meeting_id.value[now_index.value] },
        }); // 请求用户数据的 APIdata
        console.log(response.data);
        historyTime.value = response.data.time;
        historyType.value = response.data.type;
        historyContent.value = response.data.content;
        meetingTitle.value = title.value[index];
        showModalhistory.value = true;
    };

    const deleteHistory = async index => {
        // alert(historyContent.value[index]);
        const response = await axios.get('/api/deletehistory', {
            params: {
                meeting_id: meeting_id.value[now_index.value],
                content: historyContent.value[index],
            },
        }); // 请求用户数据的 APIdata
        console.log(response.data);
        historyTime.value = response.data.time;
        historyType.value = response.data.type;
        historyContent.value = response.data.content;
    };

    const checkHistoryItem = async index => {
        console.log('checkHistoryItem called');
        // alert(historyContent.value[index]);
        showModalhistory.value = false;
        showModalHistoryItem.value = true;
        HistoryItem.value = historyContent.value[index];
    };

    onMounted(() => {
        fetchData();
    });
</script>
