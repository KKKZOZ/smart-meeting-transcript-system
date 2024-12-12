<template>
  <div class="create-meeting">
    <h2>Create a Meeting</h2>

    <!-- 表单部分 -->
    <form @submit.prevent="submitMeeting">
      <!-- 会议名称 -->
      <div class="form-group">
        <label for="meeting-name">Meeting Name:</label>
        <input 
          id="meeting-name" 
          v-model="meeting.name" 
          type="text" 
          placeholder="Enter meeting name" 
          required
        />
      </div>

      <!-- 起止时间 -->
      <div class="form-group">
        <label for="start-time">Start Time:</label>
        <input 
          id="start-time" 
          v-model="meeting.startTime" 
          type="datetime-local" 
          required
        />

        <label for="end-time">End Time:</label>
        <input 
          id="end-time" 
          v-model="meeting.endTime" 
          type="datetime-local" 
          required
        />
      </div>

      <!-- 会议语言 -->
      <div class="form-group">
        <label for="language">Language:</label>
        <select id="language" v-model="meeting.language" required>
          <option value="Chinese">Chinese</option>
          <option value="English">English</option>
        </select>
      </div>

      <!-- 提交按钮 -->
      <button type="submit">Create Meeting</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from '@/axios';
import router from "../router";

// 表单数据
const meeting = ref({
  name: '',
  startTime: '',
  endTime: '',
  language: 'Chinese',
});


// 提交表单数据
const submitMeeting = async () => {
  const payload = {
    title: meeting.value.name,  // 后端期望的字段是 title
    start_time: meeting.value.startTime,  // 后端期望的字段是 start_time
    end_time: meeting.value.endTime,  // 后端期望的字段是 end_time
    language: meeting.value.language,  // 后端期望的字段是 language
  };

  try {
    const response = await axios.post('/api/meetings', payload);
    console.log(response)
    alert('Meeting created successfully!');
    router.push('/transcript-page');
  } catch (error) {
    console.log(error)
    console.error('Error creating meeting:', error);
    alert('Failed to create meeting.');
    // router.push('/transcript-page');
  }
};
</script>

<style scoped>
.create-meeting {
  max-width: 600px;
  margin: 20px auto;
  padding: 20px;
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

input, select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

button {
  padding: 10px 20px;
  background-color: #007BFF;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #0056b3;
}
</style>
