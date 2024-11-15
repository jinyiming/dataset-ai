<template>
  <div class="file-viewer">
    <div v-if="loading" class="loading">
      <div class="loading-spinner"></div>
      <span>加载中...</span>
    </div>
    <div v-else-if="error" class="error">
      {{ error }}
    </div>
    <div v-else class="viewer-content">
      <!-- 直接使用 iframe 预览所有类型文件 -->
      <iframe 
        :src="previewUrl"
        class="preview-frame"
        sandbox="allow-same-origin allow-scripts allow-forms allow-popups allow-downloads allow-modals"
      ></iframe>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const props = defineProps({
  fileId: String,
  moduleId: String,
  fileName: String,
  fileSuffix: String,
  apiUrl: String,
  token: String
})

const loading = ref(true)
const error = ref(null)
const previewUrl = ref('')

// 组件挂载时获取文件
onMounted(async () => {
  try {
    console.log('开始获取文件:', props.fileId)
    
    // 直接构建预览URL
    previewUrl.value = `${props.apiUrl}/attachment/downloadEgovAttFile?id=${props.fileId}&moduleId=${props.moduleId}&x-auth-token=${props.token}`
    loading.value = false
    
  } catch (err) {
    error.value = '加载文件失败: ' + err.message
    loading.value = false
    console.error('加载文件失败:', err)
  }
})
</script>

<style scoped>
.file-viewer {
  width: 100%;
  height: 100%;
  position: relative;
  background: #f3f4f6;
}

.loading {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: rgba(255, 255, 255, 0.9);
  gap: 12px;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #059669;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.error {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #dc2626;
}

.viewer-content {
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.preview-frame {
  width: 100%;
  height: 100%;
  border: none;
  background: white;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style> 