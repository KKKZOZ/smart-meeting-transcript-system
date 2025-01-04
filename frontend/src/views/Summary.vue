<template>
    <div class="search-container">
        <input class="searchArea" type="text" v-model="searchQuery" placeholder="搜索历史会议..." />
        <button class="search_button" @click="search">
            <img src="@/assets/img/magnifier.png" alt="Search" />
        </button>
    </div>
    <div class="table-container">
        <table class="showTable">
            <thead>
                <tr>
                    <th>会议名称</th>
                    <th>会议内容</th>
                    <th>转录时间</th>
                    <th></th>
                    <th></th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(item, index) in title" :key="index">
                    <td>{{ item }}</td>
                    <td>
                        <textarea v-model="content[index]" readonly></textarea>
                    </td>
                    <td>{{ timestamp[index] }}</td>
                    <td>
                        <button @click="create(index)">创建摘要</button>
                    </td>
                    <td>
                        <button @click="checkHistory(index)">历史摘要</button>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>

    <div v-if="showModal" class="modal">
        <div class="modal-content">
            <h2>{{ meetingTitle }}会议</h2>
            <div class="form-group">
                <label for="summaryType" style="font-size: 18px">(请输入您对摘要的要求)</label>
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
                        style="
                            width: 100%;
                            height: 300px;
                            font-size: 20px;
                            line-height: 1.6;
                            padding: 10px;
                        "
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
        <div class="table-container2">
            <h2 style="text-align: center">{{ meetingTitle }}会议</h2>

            <div class="showTable2">
                <table>
                    <thead>
                        <tr>
                            <th>生成时间</th>
                            <th>摘要类型</th>
                            <th></th>
                            <th></th>
                        </tr>
                    </thead>
                    <tr v-for="(item, index) in historyTime" :key="index">
                        <td>{{ item }}</td>
                        <td>
                            <textarea readonly v-model="historyType[index]"> </textarea>
                        </td>
                        <td>
                            <button @click="checkHistoryItem(index)">查看摘要</button>
                        </td>
                        <td>
                            <button @click="deleteHistory(index)">删除摘要</button>
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
                    <!-- <label @input="updateText" style="width: 300px; height: 200px;">
                        {{ HistoryItem }}
                    </label> -->
                    <textarea
                        v-model="HistoryItem"
                        @input="updateText"
                        style="
                            width: 100%;
                            height: 300px;
                            font-size: 20px;
                            line-height: 1.6;
                            padding: 10px;
                        "
                        readonly
                    ></textarea>
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
    .search-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 20px;
    }

    .searchArea {
        width: 60%;
        padding: 10px 20px;
        border-radius: 25px;
        border: 1px solid #ddd;
        font-size: 16px;
        transition: all 0.3s ease-in-out;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    .searchArea:focus {
        border-color: #24adf3;
        outline: none;
        box-shadow: 0 4px 8px rgba(36, 173, 243, 0.3);
    }

    .search_button {
        width: 50px;
        height: 50px;
        background: linear-gradient(135deg, #f0f0f0, #ffffff); /* #0b96dc, #1d8ecf); /* 渐变背景 */
        border-radius: 50%;
        border: none;
        cursor: pointer;
        margin-left: 15px;
        transition:
            background-color 0.3s ease,
            transform 0.2s ease,
            box-shadow 0.3s ease;
        display: flex;
        justify-content: center;
        align-items: center;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* 初始阴影 */
    }

    .search_button:hover {
        background: linear-gradient(135deg, #27b76b, #2dce89); /*悬浮时背景渐变 */
        transform: scale(1.1); /* 悬浮时按钮稍微放大 */
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3); /* 悬浮时阴影加深 */
    }

    .search_button:active {
        transform: scale(0.95); /* 点击时按钮稍微缩小 */
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 点击时恢复阴影 */
    }

    .search_button img {
        width: 2550%;
        height: 220%;
        transition: transform 0.2s ease;
    }

    .search_button:hover img {
        transform: scale(1.2); /* 悬浮时放大图标 */
    }

    /* Table styles */
    .table-container {
        width: 90%;
        margin: 30px auto;
        padding: 20px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        border-radius: 8px;
        background-color: #fff;
    }

    /* Table styles */
    .table-container2 {
        position: relative;
        top: 20%;
        /* left: 20%; */
        width: 60%;
        margin: 30px auto;
        padding: 20px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        border-radius: 8px;
        background-color: #fff;
    }

    .showTable {
        width: 100%;
        border-collapse: collapse;
        background-color: #fff;
        text-align: center;
    }

    .showTable2 {
        width: 100%;
        border-collapse: collapse;
        background-color: #fff;
        text-align: center;
    }
    /* 设置showTable.td的样式，让每列更宽一点，填充上一层 */
    .showTable2 td {
        font-size: 18px;
        /* padding: 10px; */
        /* 设置右侧padding，增加每列的宽度 */
        padding-right: 40px;
        padding-left: 40px;
        color: #333;
        border-bottom: 1px solid #f0f0f0;
    }

    .showTable2 th {
        background-color: #f5f5f5;
        font-size: 1.5em;
        padding: 15px;
        color: #333;
        border-bottom: 2px solid #ddd;
    }

    .showTable2 tr:hover {
        background-color: #f9f9f9;
    }

    .showTable th {
        background-color: #f5f5f5;
        font-size: 1.5em;
        padding: 15px;
        color: #333;
        border-bottom: 2px solid #ddd;
    }

    .showTable td {
        font-size: 18px;
        padding: 15px;
        color: #333;
        border-bottom: 1px solid #f0f0f0;
    }

    .showTable tr:hover {
        background-color: #f9f9f9;
    }

    textarea {
        width: 100%;
        height: 100px;
        padding: 10px;
        border-radius: 8px;
        border: 1px solid #ddd;
        resize: none;
        font-size: 16px;
        color: #79859c;
        background-color: #f7f7f7;
    }

    textarea:focus {
        border-color: #24adf3;
        outline: none;
    }

    button {
        background: linear-gradient(145deg, #2dce89, #27b76b); /* 渐变绿色背景 */
        color: #fff;
        font-size: 16px;
        padding: 12px 24px; /* 增加按钮的内边距，增强点击区域 */
        border-radius: 30px; /* 圆角效果更大，显得更柔和 */
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1); /* 初始阴影效果 */
        text-transform: uppercase; /* 按钮文本转大写，增强可读性 */
        font-weight: bold; /* 字体加粗 */
        letter-spacing: 1px; /* 字符间距增加，提升视觉效果 */
    }

    button:hover {
        background: linear-gradient(145deg, #27b76b, #2dce89); /* 悬浮时背景渐变颜色反转 */
        transform: translateY(-2px); /* 悬浮时按钮稍微上移，模拟点击反馈 */
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2); /* 悬浮时阴影加深 */
    }

    button:active {
        transform: translateY(2px); /* 点击时按钮下沉效果 */
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 点击时阴影恢复 */
    }

    button:focus {
        outline: none; /* 去掉焦点时的外边框 */
        box-shadow: 0 0 0 4px rgba(45, 206, 137, 0.3); /* 焦点时显示清晰的轮廓阴影 */
    }

    /* Responsiveness */
    @media (max-width: 768px) {
        .searchArea {
            width: 80%;
        }

        .showTable {
            width: 100%;
        }

        .search_button {
            margin-left: 10px;
        }
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
        width: 500px;
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
        if (summaryType.value == '') {
            summaryType.value = '简要概述';
        }

        const response = await axios.get('/api/genSummary', {
            params: { type: summaryType.value, content: content.value[now_index.value] },
            timeout: 100000,
        }); // 请求用户数据的 APIdata
        summaryContent.value = response.data;
        showModalResult.value = true;
        showModal.value = false;
    };

    const confirm = async () => {
        const response = await axios.get('/api/confirmSummary', {
            params: {
                content: summaryContent.value,
                meeting_id: meeting_id.value[now_index.value],
                type: summaryType.value,
            },
        }); // 请求用户数据的 APIdata
        showModalResult.value = false;
    };

    const checkHistory = async index => {
        now_index.value = index;
        const response = await axios.get('/api/checkhistory', {
            params: { meeting_id: meeting_id.value[now_index.value] },
        }); // 请求用户数据的 APIdata
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
        historyTime.value = response.data.time;
        historyType.value = response.data.type;
        historyContent.value = response.data.content;
    };

    const checkHistoryItem = async index => {
        showModalhistory.value = false;
        showModalHistoryItem.value = true;
        HistoryItem.value = historyContent.value[index];
    };

    onMounted(() => {
        fetchData();
    });
</script>
