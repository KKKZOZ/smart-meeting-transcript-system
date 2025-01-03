<template>
    <div>
        <input class="searchArea" type="text" v-model="searchQuery" placeholder="搜索历史会议..." />
        <button class="search_button" @click="search">
            <img src="@/assets/img/magnifier.png" alt="Search" />
        </button>
    </div>
    <div>
        <table class="showTable">
            <tr>
                <th
                    style="
                        font-size: 1.5em;
                        text-align: center;
                        height: 80px;
                        background-color: #f5f5f5;
                    "
                    >会议名称</th
                >
                <th
                    style="
                        font-size: 1.5em;
                        text-align: center;
                        height: 80px;
                        background-color: #f5f5f5;
                    "
                    >会议内容</th
                >
                <th
                    style="
                        font-size: 1.5em;
                        text-align: center;
                        height: 80px;
                        background-color: #f5f5f5;
                    "
                    >转录时间</th
                >
                <th style="background-color: #f5f5f5"> </th>
                <th style="background-color: #f5f5f5"> </th>
            </tr>
            <tr v-for="(item, index) in title" :key="index">
                <td style="font-size: 20px; text-align: center">{{ item }}</td>
                <td style="font-size: 20px; text-align: center">
                    <textarea
                        v-model="content[index]"
                        readonly
                        style="color: #79859c; font-size: 20px"
                    >
                    </textarea>
                </td>

                <td style="font-size: 20px; text-align: center">{{ timestamp[index] }}</td>
                <td>
                    <button
                        style="
                            background-color: #24adf3;
                            font-size: 18px;
                            color: #ffffff;
                            border: 2px solid gray;
                        "
                        @click="create(index)"
                        >创建摘要</button
                    >
                </td>
                <td>
                    <button
                        style="
                            background-color: #24adf3;
                            font-size: 18px;
                            color: #ffffff;
                            border: 2px solid gray;
                        "
                        @click="checkHistory(index)"
                        >历史摘要</button
                    >
                </td>
            </tr>
        </table>
    </div>

    <div v-if="showModal" class="modal">
        <div class="modal-content">
            <h2>{{ meetingTitle }}会议</h2>
            <div class="form-group">
                <label for="summaryType" style="font-size: 18px">(请输入摘要类型)</label>
                <br />

                <input
                    class="summaryTypeArea"
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
                            <textarea readonly v-model="historyType[index]"> </textarea>
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
    .searchArea {
        width: calc(100% - 500px);
        position: relative;
        left: 200px;
        padding: 10px 20px;
        margin: 10px 0;
        box-sizing: border-box;
        border-radius: 20px;
    }

    .showTable {
        width: 100%;
        position: relative;
        left: 200px;
        width: calc(100% - 460px);
        border-collapse: collapse;
        background-color: #fcfcfc;
        border-radius: 2px;
    }

    .search_button {
        width: 40px;
        height: 40px;
        background: none;
        border: none;
        cursor: pointer;
        position: relative;
        left: 200px;
        padding: 0;
        margin-left: 10px;
        background-color: #f0f5ee;
        border-radius: 8px;
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
    const title = ref([]);
    const content = ref([]);
    const timestamp = ref([]);
    const meeting_id = ref([]);
    const historyTime = ref([]);
    const historyType = ref([]);
    const historyContent = ref([]);
    const searchQuery = ref('');
    const now_index = ref('');
    const showModal = ref(false);
    const showModalResult = ref(false);
    const summaryType = ref('');
    const summaryContent = ref('');
    const meetingTitle = ref('');
    const showModalhistory = ref(false);
    const showModalHistoryItem = ref(false);
    const HistoryItem = ref('');
    const fetchData = async () => {
        try {
            const response = await axios.get('/api/getMeetingData'); // 请求用户数据的 API
            console.log(response);
            title.value = response.data.title;
            content.value = response.data.content;
            timestamp.value = response.data.timestamp;
            meeting_id.value = response.data.meeting_id;
        } catch (error) {
            console.error('Failed to fetch data:', error);
            alert('Failed to load data.');
        }
    };

    const searchData = async () => {
        try {
            const response = await axios.get('/api/searchquery', {
                params: { s_query: searchQuery.value },
            }); // 请求用户数据的 API
            console.log(response);
            title.value = response.data.title;
            content.value = response.data.content;
            timestamp.value = response.data.timestamp;
            meeting_id.value = response.data.meeting_id;
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
        showModalhistory.value = false;
        showModalHistoryItem.value = true;
        HistoryItem.value = historyContent.value[index];
    };

    onMounted(() => {
        fetchData();
    });
</script>
