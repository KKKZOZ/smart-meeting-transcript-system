<script setup>
    import { ref, onMounted } from 'vue';
    import axios from '@/axios';
    import MiniStatisticsCard from '@/examples/Cards/MiniStatisticsCard.vue';
    import GradientLineChart from '@/examples/Charts/GradientLineChart.vue';
    import Carousel from './components/Carousel.vue';
    import CategoriesList from './components/CategoriesList.vue';

    // 定义响应式数据
    const overview = ref({
        createdMeetings: '0/0',
        participatedMeetings: '0/0',
        collaborators: '0',
        totalDuration: '0',
    });

    // 获取概览数据
    const fetchOverview = async () => {
        try {
            const response = await axios.get('/api/overview');
            overview.value = {
                createdMeetings: response.data.created_meetings || '0/0',
                participatedMeetings: response.data.participated_meetings || '0/0',
                collaborators: response.data.collaborators || '0',
                totalDuration: response.data.total_duration || '0',
            };
        } catch (error) {
            console.error('获取概览数据失败:', error.response?.data?.detail || error.message);
        }
    };

    onMounted(() => {
        fetchOverview();
    });
</script>

<template>
    <div class="py-4 container-fluid">
        <div class="row">
            <div class="col-lg-12">
                <div class="row">
                    <div class="col-lg-3 col-md-6 col-12">
                        <mini-statistics-card
                            title="我创建的会议"
                            :value="overview.createdMeetings"
                            :icon="{
                                component: 'ni ni-money-coins',
                                background: 'bg-gradient-primary',
                                shape: 'rounded-circle',
                            }"
                        />
                    </div>
                    <div class="col-lg-3 col-md-6 col-12">
                        <mini-statistics-card
                            title="我参与的会议"
                            :value="overview.participatedMeetings"
                            :icon="{
                                component: 'ni ni-world',
                                background: 'bg-gradient-danger',
                                shape: 'rounded-circle',
                            }"
                        />
                    </div>
                    <div class="col-lg-3 col-md-6 col-12">
                        <mini-statistics-card
                            title="合作的用户数量"
                            :value="overview.collaborators"
                            :icon="{
                                component: 'ni ni-paper-diploma',
                                background: 'bg-gradient-success',
                                shape: 'rounded-circle',
                            }"
                        />
                    </div>
                    <div class="col-lg-3 col-md-6 col-12">
                        <mini-statistics-card
                            title="参与的会议总时长(分钟)"
                            :value="overview.totalDuration"
                            :icon="{
                                component: 'ni ni-cart',
                                background: 'bg-gradient-warning',
                                shape: 'rounded-circle',
                            }"
                        />
                    </div>
                </div>
                <div class="row">
                    <div class="col-lg-11 mb-lg mx-auto">
                        <!-- line chart -->
                        <div class="card z-index-2">
                            <gradient-line-chart
                                id="chart-line"
                                title="Meetings Overview"
                                :chart="{
                                    labels: [
                                        'Apr',
                                        'May',
                                        'Jun',
                                        'Jul',
                                        'Aug',
                                        'Sep',
                                        'Oct',
                                        'Nov',
                                        'Dec',
                                    ],
                                    datasets: [
                                        {
                                            label: 'Mobile Apps',
                                            data: [50, 40, 300, 220, 500, 250, 400, 230, 500],
                                        },
                                    ],
                                }"
                            />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
