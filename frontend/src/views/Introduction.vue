<template>
    <div class="carousel-container">
        <h1 class="introduction-title">Introduction</h1>
        <el-carousel
            class="custom-carousel"
            height="75vh"
            direction="vertical"
            type="card"
            :interval="3000"
            :autoplay="true"
            :motion-blur="true"
        >
            <el-carousel-item v-for="(item, index) in features" :key="index">
                <div class="carousel-item-content">
                    <div class="icon-container" :class="`bg-gradient-${item.iconBackground}`">
                        <i :class="item.icon" class="carousel-icon"></i>
                    </div>
                    <div class="text-container">
                        <h3 class="carousel-title">{{ item.title }}</h3>
                        <p class="carousel-text">{{ item.text }}</p>
                    </div>
                </div>
            </el-carousel-item>
        </el-carousel>
    </div>
</template>

<script setup>
    import { ref } from 'vue';

    const features = ref([
        {
            icon: 'ni ni-sound-wave',
            iconBackground: 'primary',
            title: 'Transcription',
            text: 'Accurately transcribes meeting audio into text, supporting multiple languages.',
        },
        {
            icon: 'ni ni-single-copy-04',
            iconBackground: 'danger',
            title: 'Intelligent Summarization',
            text: 'Generates concise and informative meeting summaries using advanced language models.',
        },
        {
            icon: 'ni ni-check-bold',
            iconBackground: 'success',
            title: 'Task & Action Item Extraction',
            text: 'Automatically identifies and extracts tasks, assigns them to team members, and sets due dates.',
        },
        {
            icon: 'ni ni-folder-17',
            iconBackground: 'warning',
            title: 'Secure Data Management',
            text: 'Provides secure storage, retrieval, and management of meeting data with robust access control.',
        },
        {
            icon: 'ni ni-send',
            iconBackground: 'info',
            title: 'Collaboration & Notifications',
            text: 'Facilitates team collaboration with automated task reminders and integration with popular collaboration platforms.',
        },
        {
            icon: 'ni ni-zoom-split-in',
            iconBackground: 'primary',
            title: 'Searchable Transcripts',
            text: 'Enables efficient searching of meeting transcripts by keywords, dates, and other criteria.',
        },
        {
            icon: 'ni ni-bell-55',
            iconBackground: 'danger',
            title: 'Customizable Notifications',
            text: 'Allows users to customize notification frequency and methods for task updates.',
        },
        {
            icon: 'ni ni-collection',
            iconBackground: 'success',
            title: 'Multi-format Summary Options',
            text: 'Supports different summary formats and allows filtering for specific key points.',
        },
        {
            icon: 'ni ni-calendar-grid-58',
            iconBackground: 'warning',
            title: 'Historical Data Access',
            text: 'Provides access to historical meeting records and summaries for review and analysis.',
        },
    ]);
</script>

<style scoped>
    .carousel-container {
        width: 75%;
        margin: 0 auto;
    }

    .custom-carousel {
        border-radius: 15px;
        overflow: hidden;
    }

    .introduction-title {
        font-size: 2.5rem; /* 增大字体 */
        font-weight: 700; /* 加粗 */
        color: #2a82a2; /* 使用主题色 */
        text-align: center;
        margin-bottom: 30px; /* 增加与轮播图的间距 */
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2); /* 添加阴影 */
        position: relative;
        display: inline-block;
        padding-bottom: 10px; /* 为下划线留出空间 */
    }

    .introduction-title::after {
        content: '';
        position: absolute;
        left: 50%;
        bottom: 0;
        width: 60px;
        height: 4px;
        background-color: #82c9e4; /* 下划线颜色 */
        transform: translateX(-50%); /* 居中 */
        border-radius: 2px;
    }

    .carousel-item-content {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100%;
    }

    .icon-container {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* 添加阴影 */
    }

    .carousel-icon {
        font-size: 2.5rem; /* 图标大小 */
        color: white; /* 图标颜色 */
    }

    .text-container {
        background-color: rgba(255, 255, 255, 0.8);
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        width: 90%; /* 增加宽度 */
        max-width: 800px; /* 限制最大宽度 */
        text-align: center;
    }

    .carousel-title {
        font-size: 1.75rem;
        font-weight: 600;
        color: #000; /* 小标题颜色改为黑色 */
        margin-bottom: 10px;
    }

    .carousel-text {
        color: #334e68;
        opacity: 0.9;
        line-height: 1.6;
        margin: 0;
        font-size: 1.25rem;
        font-weight: 400;
        white-space: normal; /* 允许换行 */
        word-wrap: break-word; /* 允许长单词换行 */
    }

    .el-carousel__item {
        display: flex;
        justify-content: center;
        align-items: center;
        border-radius: 15px;
        background-color: rgba(255, 255, 255, 0.9);
        box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.1);
    }

    .el-carousel__item:nth-child(2n) {
        background-color: rgba(42, 130, 162, 0.9);
    }

    .el-carousel__item:nth-child(2n + 1) {
        background-color: rgba(130, 201, 228, 0.9);
    }

    /* 背景渐变样式 */
    .bg-gradient-primary {
        background: linear-gradient(135deg, #2a82a2, #82c9e4);
    }

    .bg-gradient-danger {
        background: linear-gradient(135deg, #f5365c, #f56036);
    }

    .bg-gradient-success {
        background: linear-gradient(135deg, #2dce89, #2dcecc);
    }

    .bg-gradient-warning {
        background: linear-gradient(135deg, #fb6340, #fbb140);
    }

    .bg-gradient-info {
        background: linear-gradient(135deg, #11cdef, #1171ef);
    }
</style>
