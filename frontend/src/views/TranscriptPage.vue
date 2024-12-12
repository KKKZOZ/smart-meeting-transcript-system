<template>
  <div class="app-container">
    <!-- 文本显示框 -->
    <div class="text-display">
      <h2>Transcribed Text</h2>
      <p>{{ transcript || 'Waiting for transcription...' }}</p>
    </div>

    <!-- 上传音频按键 -->
    <div class="upload-section">
      <input
        type="file"
        accept="audio/*"
        @change="handleFileUpload"
        id="audio-upload"
        hidden
      />
      <label for="audio-upload" class="upload-button">Upload Audio</label>
    </div>

    <!-- 音频播放器 -->
    <div class="audio-player">
      <audio ref="audioPlayer" controls>
        <source :src="audioSrc" type="audio/mp3" />
        Your browser does not support the audio element.
      </audio>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from '@/axios';

// 状态变量
const audioSrc = ref('');
const transcript = ref('');
const audioPlayer = ref(null);

// 处理文件上传
const handleFileUpload = async (event) => {
  const file = event.target.files[0];
  if (!file) return;

  // 生成音频URL用于播放
  audioSrc.value = URL.createObjectURL(file);

  // 创建FormData上传文件
  const formData = new FormData();
  formData.append('audio', file);

  try {
    // 模拟请求发送到后端并接收返回数据
    const response = await axios.post('/api/transcribe', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    // 将返回的文本赋值给 transcript
    transcript.value = response.data.text;
  } catch (error) {
    console.error('Error uploading file:', error);
    alert('Failed to upload or process audio.');
  }
};
</script>

<style scoped>
.app-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.text-display {
  width: 100%;
  padding: 20px;
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 8px;
  margin-bottom: 20px;
  text-align: center;
}

.text-display h2 {
  margin-bottom: 10px;
  color: #333;
}

.text-display p {
  color: #555;
}

.upload-section {
  margin-bottom: 20px;
}

.upload-button {
  display: inline-block;
  padding: 10px 20px;
  background-color: #007BFF;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  text-align: center;
  transition: background-color 0.3s;
}

.upload-button:hover {
  background-color: #0056b3;
}

.audio-player {
  width: 100%;
}

audio {
  width: 100%;
  outline: none;
}
</style>
