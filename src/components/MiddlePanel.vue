<template>
  <!-- 中间面板内容 -->
  <div class="middle-panel">
    <!-- 加载动画遮罩层 -->
    <div v-if="isLoading" class="loading-overlay">
      <div class="loading-spinner">
        <svg class="spinner-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <circle class="spinner-track" cx="12" cy="12" r="10" stroke="#e2e8f0" stroke-width="4"/>
          <circle class="spinner-head" cx="12" cy="12" r="10" stroke="#10a37f" stroke-width="4" stroke-linecap="round" stroke-dasharray="16 48"/>
        </svg>
        <span class="loading-text">正在生成问答对...</span>
      </div>
    </div>

    <div class="panel-header">
      <h2>
        <svg class="header-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M8 10H16M8 14H16M12 4H6C4.89543 4 4 4.89543 4 6V18C4 19.1046 4.89543 20 6 20H18C19.1046 20 20 19.1046 20 18V12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M15 5L18 8M18 8L21 5M18 8V2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        问答编辑区
      </h2>
      <button v-if="qaList.length > 0 && !isSaving" @click="saveQA" class="save-button">保存</button>
      <button v-if="isSaving" class="save-button loading" disabled>
        <svg class="save-spinner" viewBox="0 0 24 24" fill="none">
          <circle class="spinner-track" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" stroke-opacity="0.2"/>
          <circle class="spinner-head" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-dasharray="16 48"/>
        </svg>
        保存中...
      </button>
    </div>
    <div class="qa-container">
      <div v-for="qa in qaList" :key="qa.id" class="qa-pair">
        <div class="qa-card">
          <div class="qa-content">
            <div class="input-group">
              <label>Q{{qa.id + 1}}:</label>
              <textarea
                v-model="qa.question"
                @input="updateQA(qa)"
                placeholder="请输入问题..."
                class="qa-input"
                rows="2"
              ></textarea>
            </div>
            <div class="input-group">
              <label>A{{qa.id + 1}}:</label>
              <textarea
                v-model="qa.answer"
                @input="updateQA(qa)"
                placeholder="请输入答案..."
                class="qa-input"
                rows="2"
              ></textarea>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits, ref } from 'vue'
import axios from 'axios'

const props = defineProps({
  qaList: {
    type: Array,
    required: true
  },
  isLoading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update-qa'])
const isSaving = ref(false)

const updateQA = (qa) => {
  emit('update-qa', qa)
}

const saveQA = async () => {
  if (isSaving.value) {
    alert('操作频繁，请稍后再试！')
    return
  }

  isSaving.value = true

  try {
    const response = await axios.post('http://localhost:8000/flask/api/save', {
      qaList: props.qaList,
      qContent: props.qaList.map(qa => qa.question).join(', ')
    })

    if (response.status === 200) {
      alert('问答对已成功保存！')
    } else {
      alert(response.data.message || '保存失败，请重试！')
    }
  } catch (error) {
    console.error('保存问答对失败:', error)
    alert('保存失败，请重试！')
  } finally {
    isSaving.value = false
  }
}
</script>

<style scoped>
/* 中间面板样式 */
.middle-panel {
  flex: 1;
  padding: 12px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  position: relative;
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 0;
  margin-bottom: 12px;
}

.panel-header h2 {
  margin: 0;
  font-size: 1.25rem;
  color: #374151;
  display: flex;
  align-items: center;
  gap: 8px;
}

.save-button {
  padding: 6px 12px;
  background-color: #10a37f;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.save-button:hover {
  background-color: #0e906f;
}

.loading-button {
  padding: 6px 12px;
  background-color: #10a37f;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: not-allowed;
  display: flex;
  align-items: center;
}

.loading-icon {
  width: 20px;
  height: 20px;
  margin-right: 8px;
  animation: spin 1s linear infinite; /* 添加旋转动画 */
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.header-icon {
  width: 24px;
  height: 24px;
  color: #10a37f;
}

.qa-container {
  flex: 1;
  overflow-y: auto;
  padding-right: 4px;
  position: relative;
  z-index: 1;
}

.qa-pair {
  margin-bottom: 4px;
}

.qa-card {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 6px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(229, 231, 235, 0.5);
}

.qa-content {
  padding: 8px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.input-group {
  display: flex;
  align-items: flex-start;
  gap: 8px;
}

.input-group label {
  font-weight: 500;
  color: #4b5563;
  font-size: 0.9rem;
  min-width: 30px;
  padding-top: 6px;
}

.qa-input {
  flex: 1;
  padding: 6px;
  border: 1px solid #e5e7eb;
  border-radius: 4px;
  font-size: 13px;
  line-height: 1.4;
  resize: vertical;
  min-height: 32px;
  max-height: 120px;
}

.qa-input:focus {
  outline: none;
  border-color: #10a37f;
  box-shadow: 0 0 0 1px rgba(16, 163, 127, 0.1);
}

/* 自定义滚动条样式 */
.qa-container::-webkit-scrollbar {
  width: 6px;
}

.qa-container::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.qa-container::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.qa-container::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* 添加加载动画相关样式 */
.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.9);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}

.loading-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.spinner-icon {
  width: 60px;
  height: 60px;
  animation: rotate 2s linear infinite;
}

.spinner-track {
  opacity: 0.2;
}

.spinner-head {
  animation: dash 1.5s ease-in-out infinite;
}

.loading-text {
  color: #10a37f;
  font-size: 16px;
  font-weight: 500;
}

@keyframes rotate {
  100% {
    transform: rotate(360deg);
  }
}

@keyframes dash {
  0% {
    stroke-dasharray: 1, 150;
    stroke-dashoffset: 0;
  }
  50% {
    stroke-dasharray: 90, 150;
    stroke-dashoffset: -35;
  }
  100% {
    stroke-dasharray: 90, 150;
    stroke-dashoffset: -124;
  }
}

/* 保存按钮加载状态 */
.save-button.loading {
  display: flex;
  align-items: center;
  gap: 8px;
  opacity: 0.8;
}

.save-spinner {
  width: 20px;
  height: 20px;
  animation: rotate 2s linear infinite;
}
</style> 