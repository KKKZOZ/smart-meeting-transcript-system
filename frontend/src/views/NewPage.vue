<!-- src/views/NewPage.vue -->
<template>
  <div>
    <h1>New Page</h1>
    <p>This is a new page.</p>
    <button @click="fetchData">Fetch Data</button>
    <div v-if="data">
      <pre>{{ data }}</pre>
    </div>
  </div>
</template>



<script setup>
import { ref } from 'vue';
import axios from '@/axios';

const data = ref(null);

const fetchData = async () => {
  try {
    const response = await axios.get('/api/test'); // 替换为实际的 API 路径
    console.log('Data fetched:', response.data);
    data.value = response.data;
  } catch (error) {
    console.error('Error fetching data:', error);
  }
};
</script>

<style scoped>
/* 添加页面的样式 */
</style>