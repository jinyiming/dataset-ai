<template>
  <div class="search-engine">
    <!-- 左侧面板：导航和搜索结果 -->
    <div class="left-panel">
      <!-- 导航标题 -->
      <div class="nav-header">
        <div class="nav-title">
          <svg class="nav-icon" viewBox="0 0 24 24">
            <path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5z"/>
          </svg>
          <span>公文搜索</span>
        </div>
        <div class="nav-subtitle">Document Search</div>
      </div>

      <!-- 搜索结果列表 -->
      <div class="results-panel" v-if="hasResults">
        <!-- 发文结果 -->
        <div class="result-category">
          <div class="category-header" @click="toggleCategory('dispatch')">
            <h3>发文 ({{ dispatchResults.length }})</h3>
            <span class="toggle-icon" :class="{ 'expanded': categoryExpanded.dispatch }">▼</span>
          </div>
          <div class="category-content" v-show="categoryExpanded.dispatch">
            <div v-for="item in dispatchResults" :key="item.id" class="result-item">
              <div class="doc-info">
                <h4 class="doc-title" v-html="highlightText(item.title, searchQuery)"></h4>
                <div class="doc-meta">文号: {{ item.doc_no }}</div>
              </div>
              <div class="file-groups" v-if="item.files.length">
                <div v-for="group in item.files" :key="group.type" class="file-group">
                  <div class="group-header">
                    <h5>{{ group.typeLabel }}</h5>
                  </div>
                  <div class="group-files">
                    <div v-for="file in group.files" 
                         :key="file.id" 
                         class="attachment"
                         @click="handleFileClick(file)">
                      <span class="att-name">{{ file.name }}.{{ file.suffix }}</span>
                      <span class="att-size">{{ formatSize(file.size) }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 收文结果 -->
        <div class="result-category" v-if="receivalResults.length">
          <div class="category-header" @click="toggleCategory('receival')">
            <h3>收文 ({{ receivalResults.length }})</h3>
            <span class="toggle-icon" :class="{ 'expanded': categoryExpanded.receival }">▼</span>
          </div>
          <div class="category-content" v-show="categoryExpanded.receival">
            <div v-for="item in receivalResults" :key="item.id" class="result-item">
              <div class="doc-info">
                <h4 class="doc-title" v-html="highlightText(item.title, searchQuery)"></h4>
                <div class="doc-meta">文号: {{ item.doc_no }}</div>
              </div>
              <div class="file-groups" v-if="item.files.length">
                <div v-for="group in item.files" :key="group.type" class="file-group">
                  <div class="group-header">
                    <h5>{{ group.typeLabel }}</h5>
                  </div>
                  <div class="group-files">
                    <div v-for="file in group.files" 
                         :key="file.id" 
                         class="attachment"
                         @click="handleFileClick(file)">
                      <span class="att-name">{{ file.name }}.{{ file.suffix }}</span>
                      <span class="att-size">{{ formatSize(file.size) }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 公文交换结果 -->
        <div class="result-category" v-if="exchangeResults.length">
          <div class="category-header" @click="toggleCategory('exchange')">
            <h3>公文交换 ({{ exchangeResults.length }})</h3>
            <span class="toggle-icon" :class="{ 'expanded': categoryExpanded.exchange }">▼</span>
          </div>
          <div class="category-content" v-show="categoryExpanded.exchange">
            <div v-for="item in exchangeResults" :key="item.id" class="result-item">
              <div class="doc-info">
                <h4 class="doc-title" v-html="highlightText(item.title, searchQuery)"></h4>
                <div class="doc-meta">文号: {{ item.doc_no }}</div>
              </div>
              <div class="file-groups" v-if="item.files.length">
                <div v-for="group in item.files" :key="group.type" class="file-group">
                  <div class="group-header">
                    <h5>{{ group.typeLabel }}</h5>
                  </div>
                  <div class="group-files">
                    <div v-for="file in group.files" 
                         :key="file.id" 
                         class="attachment"
                         @click="handleFileClick(file)">
                      <span class="att-name">{{ file.name }}.{{ file.suffix }}</span>
                      <span class="att-size">{{ formatSize(file.size) }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 右侧面板：搜索框和预览 -->
    <div class="right-panel">
      <!-- 搜索框区域 -->
      <div class="search-section">
        <div class="search-container">
          <input 
            v-model="searchQuery" 
            type="text" 
            class="search-input"
            placeholder="请输入文件标题关键字..."
            @keyup.enter="handleSearch"
          >
          <button class="search-button" @click="handleSearch">
            <svg class="search-icon" viewBox="0 0 24 24">
              <path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5z"/>
            </svg>
          </button>
        </div>
      </div>

      <!-- 预览面板 -->
      <div class="preview-panel" v-if="showPreview">
        <div class="preview-header">
          <h3>{{ currentFile?.name }}.{{ currentFile?.suffix }}</h3>
          <button class="close-preview" @click="closePreview">×</button>
        </div>
        <div class="preview-content">
          <!-- 使用 FileViewer 组件 -->
          <FileViewer
            :fileId="currentFile?.id"
            :moduleId="currentFile?.moduleId"
            :fileName="currentFile?.name"
            :fileSuffix="currentFile?.suffix"
            :apiUrl="apiUrl"
            :token="authToken"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onUnmounted } from 'vue'
import axios from 'axios'
import FloatingDock from '@/components/FloatingDock.vue'
import FileViewer from '@/components/FileViewer.vue'
import { encrypt } from '@/utils/crypto'
import VuePdfEmbed from 'vue-pdf-embed'
import { VueOfficeDocx } from '@vue-office/docx'
import { VueOfficeExcel } from '@vue-office/excel'
import 'viewerjs/dist/viewer.css'
import VViewer from 'v-viewer'

const searchQuery = ref('')
const dispatchResults = ref([])
const receivalResults = ref([])
const exchangeResults = ref([])

const hasResults = computed(() => {
  return dispatchResults.value.length > 0 || 
         receivalResults.value.length > 0 || 
         exchangeResults.value.length > 0
})

const handleSearch = async () => {
  if (!searchQuery.value.trim()) return

  try {
    console.log('开始搜索:', searchQuery.value)  // 添加调试日志
    
    const response = await axios.get('http://localhost:8000/flask/api/search', {
      params: {
        query: searchQuery.value  // 直接传递查询参数
      }
    })

    console.log('搜索结果:', response.data)  // 添加调试日志

    // 更新搜索结果
    dispatchResults.value = response.data.dispatch || []
    receivalResults.value = response.data.receival || []
    exchangeResults.value = response.data.exchange || []
  } catch (error) {
    console.error('搜索失败:', error)
  }
}

const formatSize = (bytes) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const showPreview = ref(false)
const currentFile = ref(null)
const previewUrl = computed(() => {
  if (!currentFile.value) return ''
  return `http://localhost:8000/flask/api/proxy-file?id=${currentFile.value.id}&moduleId=${currentFile.value.moduleId}&api=${apiUrl}&token=${authToken}`
})

// 判断文件类型
const fileType = computed(() => {
  if (!currentFile.value) return ''
  // 直接使用文件的后缀属性
  return currentFile.value.suffix || ''
})

const isOfficeFile = computed(() => {
  const officeExts = ['doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx']
  return officeExts.includes(fileType.value)
})

const isImage = computed(() => {
  const imageExts = ['jpg', 'jpeg', 'png', 'gif']
  return imageExts.includes(fileType.value)
})

// 添加API配置
const apiUrl = 'http://192.168.244.92:2080'
const authToken = 'd257aeeb-c628-417b-9986-1b76c7b32569'

// 添加 HTML 内容的响应式引用
const htmlContent = ref('')

// 修改文件点击处理函数
const handleFileClick = async (file) => {
  try {
    console.log('点击文件:', file)
    currentFile.value = file
    showPreview.value = true
    
    // 获取文件
    const response = await axios.get('http://localhost:8000/flask/api/download-file', {
      params: {
        id: file.id,
        moduleId: file.moduleId,
        api: apiUrl,
        token: authToken,
        suffix: file.suffix
      }
    })
    
    // 处理HTML文件
    if (file.suffix === 'html') {
      htmlContent.value = response.data.content
    } else {
      // 其他文件类型使用临时文件URL
      previewUrl.value = `http://localhost:8000/flask/api/temp-file/${response.data.tempFile.split('/').pop()}`
    }
    
  } catch (error) {
    console.error('获取文件失败:', error)
  }
}

// 下载文件
const downloadFile = () => {
  if (!currentFile.value || !previewUrl.value) return
  
  const link = document.createElement('a')
  link.href = previewUrl.value
  link.setAttribute('download', currentFile.value.name)
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

// 关闭预览
const closePreview = () => {
  showPreview.value = false
  currentFile.value = null
}

// 组件卸载时清理
onUnmounted(() => {
  if (previewUrl.value) {
    URL.revokeObjectURL(previewUrl.value)
  }
})

// 高亮搜索文本
const highlightText = (text, query) => {
  if (!query) return text
  const regex = new RegExp(query, 'gi')
  return text.replace(regex, match => `<span class="highlight">${match}</span>`)
}

// 添加获取文件后缀的函数
const getFileSuffix = (fileName) => {
  if (!fileName) return ''
  const parts = fileName.split('.')
  return parts.length > 1 ? parts.pop().toLowerCase() : ''
}

// 添加类别展开状态管理
const categoryExpanded = ref({
  dispatch: true,
  receival: true,
  exchange: true
})

// 切换类别展开/收起
const toggleCategory = (category) => {
  categoryExpanded.value[category] = !categoryExpanded.value[category]
}

// 获取文件组图标
const getGroupIcon = (type) => {
  const icons = {
    main_doc: 'M14 2H6a2 2 0 0 0-2 2v16h12V8l-6-6z',
    attach: 'M16.5 6v11.5c0 2.21-1.79 4-4 4s-4-1.79-4-4V5a2.5 2.5 0 0 1 5 0v10.5c0 .55-.45 1-1 1s-1-.45-1-1V6H10v9.5a2.5 2.5 0 0 0 5 0V5c0-2.21-1.79-4-4-4S7 2.79 7 5v12.5c0 3.04 2.46 5.5 5.5 5.5s5.5-2.46 5.5-5.5V6h-1.5z',
    // ... 其他类型的图标
  }
  return icons[type] || icons.main_doc
}

// 获取文件图标类名
const getFileIconClass = (suffix) => {
  const iconMap = {
    pdf: 'pdf-icon',
    doc: 'word-icon',
    docx: 'word-icon',
    xls: 'excel-icon',
    xlsx: 'excel-icon',
    // ... 其他文件类型
  }
  return iconMap[suffix] || 'file-icon'
}

// 获取文件图标路径
const getFileIcon = (suffix) => {
  const icons = {
    doc: 'M14 2H6a2 2 0 0 0-2 2v16h12V8l-6-6z',
    docx: 'M16.5 6v11.5c0 2.21-1.79 4-4 4s-4-1.79-4-4V5a2.5 2.5 0 0 1 2.5-2.5h11zM16.5 16v1.5c0 .83-.67 1.5-1.5 1.5h-11C4.67 19 4 18.33 4 17.5V16h12zM5 10h10v2H5v-2zM5 15h10v2H5v-2zM6 9h8v2H6V9z',
    xls: 'M14 2H6a2 2 0 0 0-2 2v16h12V8l-6-6z',
    xlsx: 'M16.5 6v11.5c0 2.21-1.79 4-4 4s-4-1.79-4-4V5a2.5 2.5 0 0 1 2.5-2.5h11zM16.5 16v1.5c0 .83-.67 1.5-1.5 1.5h-11C4.67 19 4 18.33 4 17.5V16h12zM5 10h10v2H5v-2zM5 15h10v2H5v-2zM6 9h8v2H6V9z',
    ppt: 'M14 2H6a2 2 0 0 0-2 2v16h12V8l-6-6z',
    pptx: 'M16.5 6v11.5c0 2.21-1.79 4-4 4s-4-1.79-4-4V5a2.5 2.5 0 0 1 2.5-2.5h11zM16.5 16v1.5c0 .83-.67 1.5-1.5 1.5h-11C4.67 19 4 18.33 4 17.5V16h12zM5 10h10v2H5v-2zM5 15h10v2H5v-2zM6 9h8v2H6V9z',
    jpg: 'M14 2H6a2 2 0 0 0-2 2v16h12V8l-6-6z',
    jpeg: 'M14 2H6a2 2 0 0 0-2 2v16h12V8l-6-6z',
    png: 'M14 2H6a2 2 0 0 0-2 2v16h12V8l-6-6z',
    gif: 'M14 2H6a2 2 0 0 0-2 2v16h12V8l-6-6z',
    html: 'M14 2H6a2 2 0 0 0-2 2v16h12V8l-6-6z',
    text: 'M14 2H6a2 2 0 0 0-2 2v16h12V8l-6-6z',
    file: 'M14 2H6a2 2 0 0 0-2 2v16h12V8l-6-6z'
  }
  return icons[suffix] || icons.file
}
</script>

<style scoped>
/* 整体布局 */
.search-engine {
  display: flex;
  height: 100vh;
  background: #f3f4f6;
}

/* 左侧面板样式 */
.left-panel {
  width: 280px;
  display: flex;
  flex-direction: column;
  background: white;
  border-right: 1px solid #e5e7eb;
}

/* 导航标题样式 */
.nav-header {
  padding: 20px;
  background: linear-gradient(135deg, #575793 0%, #059669 100%);
  color: white;
}

.nav-title {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 4px;
}

.nav-icon {
  width: 28px;
  height: 28px;
  fill: currentColor;
}

.nav-title span {
  font-size: 1.25rem;
  font-weight: 600;
}

.nav-subtitle {
  margin-left: 40px;
  font-size: 0.875rem;
  opacity: 0.8;
}

/* 搜索结果样式 */
.results-panel {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}

.result-category {
  margin-bottom: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.category-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: #f8fafc;
  cursor: pointer;
  border-bottom: 1px solid #e5e7eb;
}

.category-header h3 {
  margin: 0;
  font-size: 1rem;
  color: #374151;
}

.toggle-icon {
  transition: transform 0.3s ease;
}

.toggle-icon.expanded {
  transform: rotate(180deg);
}

.result-item {
  padding: 16px;
  border-bottom: 1px solid #e5e7eb;
}

.doc-title {
  margin: 0 0 8px 0;
  font-size: 1rem;
  color: #111827;
}

.doc-meta {
  font-size: 0.875rem;
  color: #6b7280;
}

/* 文件组样式 */
.file-group {
  margin-top: 12px;
}

.group-header h5 {
  margin: 0;
  font-size: 0.875rem;
  color: #4b5563;
  background: #f3f4f6;
  padding: 4px 8px;
  border-radius: 4px;
  display: inline-block;
}

.attachment {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px;
  margin: 4px 0;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.attachment:hover {
  background: #f3f4f6;
}

/* 右侧面板样式 */
.right-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
}

/* 搜索框区域样式 */
.search-section {
  padding: 20px;
  background: white;
  border-bottom: 1px solid #e5e7eb;
}

.search-container {
  max-width: 900px;
  margin: 0 auto;
  display: flex;
  gap: 12px;
}

.search-input {
  flex: 1;
  padding: 16px 24px;
  font-size: 1.1rem;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.search-input:focus {
  border-color: #059669;
  outline: none;
  box-shadow: 0 0 0 3px rgba(5, 150, 105, 0.1);
}

.search-button {
  padding: 0 24px;
  background: #059669;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
}

.search-button:hover {
  background: #047857;
  transform: translateY(-1px);
}

.search-icon {
  width: 24px;
  height: 24px;
  fill: white;
}

/* 高亮样式 */
.highlight {
  background-color: #fef08a;
  padding: 0 2px;
  border-radius: 2px;
}

/* 预览面板样式 */
.preview-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #f3f4f6;
}

.preview-header {
  padding: 16px;
  background: white;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.preview-header h3 {
  margin: 0;
  font-size: 1.1rem;
  color: #374151;
}

.close-preview {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #6b7280;
  cursor: pointer;
  padding: 4px;
}

.preview-content {
  flex: 1;
  overflow: hidden;
}
</style> 