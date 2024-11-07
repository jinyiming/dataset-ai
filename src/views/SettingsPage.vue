<template>
  <div class="settings-page">
    <div class="settings-container">
      <div class="settings-header">
        <h1>模板设计器</h1>
        <div class="header-actions">
          <button @click="showExample" class="example-button">模板示例</button>
          <button @click="saveTemplate" class="save-button">保存模板</button>
        </div>
      </div>

      <!-- 消息提示 -->
      <div v-if="showMessage" class="message-container" :class="messageType">
        <div class="message-content">
          {{ message }}
          <button @click="showMessage = false" class="close-message">×</button>
        </div>
      </div>

      <div class="main-content">
        <!-- 左侧编辑区域 -->
        <div class="editor-section">
          <!-- 模板基本信息 -->
          <div class="template-info">
            <div class="template-name-input">
              <label>模板名称：</label>
              <input 
                v-model="templateName"
                type="text"
                placeholder="请输入模板名称..."
                class="name-input"
              />
            </div>

            <!-- 添加模板类型选择 -->
            <div class="template-type">
              <label>模板类型：</label>
              <div class="type-options">
                <label v-for="type in templateTypes" :key="type.value" class="type-option">
                  <input
                    type="radio"
                    :value="type.value"
                    v-model="selectedType"
                    name="templateType"
                  >
                  <span>{{ type.label }}</span>
                </label>
              </div>
            </div>
          </div>

          <!-- 操作按钮 -->
          <div class="editor-actions">
            <button @click="formatJSON" class="action-button format">格式化</button>
            <button @click="validateJSON" class="action-button validate">验证</button>
          </div>

          <div class="editor-container">
            <textarea
              v-model="jsonContent"
              class="json-editor"
              placeholder="请输入 JSON 模板..."
              @input="handleEditorInput"
            ></textarea>
          </div>
        </div>

        <!-- 右侧预览区域 -->
        <div class="preview-section">
          <h3>实时预览</h3>
          <div class="preview-container">
            <template v-if="parsedTemplate && parsedTemplate.length > 0">
              <div v-for="(item, index) in parsedTemplate" :key="index" class="preview-field">
                <div class="field-preview">
                  <label>{{ item.instruction }}</label>
                  <input 
                    type="text"
                    :placeholder="item.output"
                    class="preview-input"
                    disabled
                  />
                </div>
              </div>
            </template>
          </div>
        </div>
      </div>

      <!-- 添加示例弹窗 -->
      <div v-if="showExampleDialog" class="example-dialog">
        <div class="example-content">
          <div class="example-header">
            <h3>模板示例</h3>
            <button @click="closeExample" class="close-button">×</button>
          </div>
          <pre class="example-code">
[{
  "instruction": "Can you tell me a little bit about yourself?",
  "input": "",
  "output": "I am {{name}}, an AI assistant trained by {{author}}."
}]</pre>
          <button @click="useExample" class="use-example-button">使用此示例</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const templateName = ref('')
const selectedType = ref('qa_dataset') // 默认选择问答数据集

// 模板类型选项
const templateTypes = [
  { label: '问答数据集', value: 'qa_dataset' },
  { label: '增强标注数据集', value: 'enhanced_dataset' },
  { label: '自监督学习数据集', value: 'self_supervised' },
  { label: '多模态数据集', value: 'multimodal' }
]

const jsonContent = ref(`{
  "fields": [
    {
      "type": "text",
      "label": "问题",
      "placeholder": "请输入问题",
      "required": true
    },
    {
      "type": "textarea",
      "label": "答案",
      "placeholder": "请输入答案",
      "required": true
    },
    {
      "type": "text",
      "label": "作者",
      "placeholder": "请输入作者",
      "required": false
    }
  ]
}`)

const editorError = ref('')
const parsedTemplate = ref(null)
const showMessage = ref(false)
const message = ref('')
const messageType = ref('info')

const showExampleDialog = ref(false)

const showExample = () => {
  showExampleDialog.value = true
}

const closeExample = () => {
  showExampleDialog.value = false
}

const useExample = () => {
  jsonContent.value = JSON.stringify([{
    "instruction": "Can you tell me a little bit about yourself?",
    "input": "",
    "output": "I am {{name}}, an AI assistant trained by {{author}}."
  }], null, 2)
  showExampleDialog.value = false
  handleEditorInput() // 触发预览更新
}

// 解析 JSON
const handleEditorInput = () => {
  try {
    const parsed = JSON.parse(jsonContent.value)
    console.log('解析的JSON:', parsed)
    parsedTemplate.value = parsed
    editorError.value = ''
  } catch (e) {
    console.error('JSON解析错误:', e)
    editorError.value = '无效的 JSON 格式'
    parsedTemplate.value = null
  }
}

// 格式化 JSON
const formatJSON = () => {
  try {
    const parsed = JSON.parse(jsonContent.value)
    jsonContent.value = JSON.stringify(parsed, null, 2)
    message.value = 'JSON 格式化成功！'
    messageType.value = 'success'
    showMessage.value = true
    setTimeout(() => {
      showMessage.value = false
    }, 3000)
  } catch (e) {
    message.value = '无法格式化：无效的 JSON'
    messageType.value = 'error'
    showMessage.value = true
  }
}

// 验证 JSON
const validateJSON = () => {
  try {
    JSON.parse(jsonContent.value)
    message.value = 'JSON 格式验证通过！'
    messageType.value = 'success'
    showMessage.value = true
    setTimeout(() => {
      showMessage.value = false
    }, 3000)
  } catch (e) {
    message.value = '无效的 JSON 格式：' + e.message
    messageType.value = 'error'
    showMessage.value = true
  }
}

// 保存模板
const saveTemplate = async () => {
  if (!templateName.value) {
    message.value = '请输入模板名称'
    messageType.value = 'error'
    showMessage.value = true
    return
  }

  if (!selectedType.value) {
    message.value = '请选择模板类型'
    messageType.value = 'error'
    showMessage.value = true
    return
  }

  try {
    const template = JSON.parse(jsonContent.value)
    
    const response = await axios.post('http://localhost:8000/flask/api/save-template', {
      subject: templateName.value,
      type: selectedType.value,
      content: jsonContent.value,
      draft_user_name: 'jin'
    })

    if (response.status === 200) {
      message.value = '模板保存成功！'
      messageType.value = 'success'
    } else {
      message.value = response.data.message || '保存失败，请重试！'
      messageType.value = 'error'
    }
  } catch (e) {
    message.value = e.response?.data?.message || '保存失败，请重试'
    messageType.value = 'error'
  }
  showMessage.value = true
  setTimeout(() => {
    showMessage.value = false
  }, 3000)
}
</script>

<style scoped>
.settings-page {
  min-height: 100vh;
  background: #f9fafb;
  padding: 20px;
}

.settings-container {
  max-width: 1200px;
  margin: 0 auto;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.settings-header {
  padding: 20px;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.main-content {
  display: flex;
  gap: 20px;
  padding: 20px;
  height: calc(100vh - 180px);
}

.editor-section {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.preview-section {
  flex: 1;
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  overflow-y: auto;
}

.json-editor {
  width: 100%;
  height: 100%;
  background: transparent;
  color: #ffffff;
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 14px;
  line-height: 1.5;
  padding: 12px;
  border: none;
  resize: none;
}

.editor-container {
  flex: 1;
  background: #1e1e1e;
  border-radius: 8px;
  padding: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.editor-actions {
  display: flex;
  gap: 12px;
  margin: 12px 0;
}

.action-button {
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s;
  flex: 1;
}

.action-button.format {
  background: #2563eb;
  color: white;
}

.action-button.validate {
  background: #059669;
  color: white;
}

.action-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.icon {
  width: 18px;
  height: 18px;
}

.save-button {
  padding: 8px 16px;
  background: #10a37f;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.error-message {
  color: #ef4444;
  font-size: 14px;
  margin-top: 8px;
}

.template-field {
  margin-bottom: 16px;
}

.field-input {
  width: 100%;
  padding: 8px;
  border: 1px solid #e5e7eb;
  border-radius: 4px;
  margin-top: 4px;
}

label {
  display: block;
  margin-bottom: 4px;
  color: #374151;
  font-weight: 500;
}

/* 添加模板名称输入框样式 */
.template-name-input {
  margin-bottom: 16px;
}

.name-input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  font-size: 14px;
  transition: all 0.3s;
}

.name-input:focus {
  outline: none;
  border-color: #10a37f;
  box-shadow: 0 0 0 2px rgba(16, 163, 127, 0.1);
}

/* 预览区域样式优化 */
.preview-field {
  margin-bottom: 20px;
  animation: fadeIn 0.3s ease;
}

.preview-field label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #374151;
}

.field-preview {
  width: 100%;
}

.preview-input,
.preview-textarea,
.preview-select {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  font-size: 14px;
  background: white;
  transition: all 0.3s;
}

.preview-textarea {
  resize: vertical;
  min-height: 80px;
}

/* 修改滚动条样式 */
.json-editor::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

.json-editor::-webkit-scrollbar-track {
  background: #2d2d2d;
}

.json-editor::-webkit-scrollbar-thumb {
  background: #555;
  border-radius: 4px;
}

.json-editor::-webkit-scrollbar-thumb:hover {
  background: #666;
}

/* 添加消息提示样式 */
.message-container {
  position: fixed;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1000;
  padding: 16px 24px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  animation: slideDown 0.3s ease;
}

.message-content {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 1rem;
}

.message-container.success {
  background: #059669;
  color: white;
}

.message-container.error {
  background: #dc2626;
  color: white;
}

.close-message {
  background: none;
  border: none;
  color: white;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0 4px;
}

@keyframes slideDown {
  from {
    transform: translate(-50%, -100%);
    opacity: 0;
  }
  to {
    transform: translate(-50%, 0);
    opacity: 1;
  }
}

/* 优化预览区域样式 */
.preview-section {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.header-actions {
  display: flex;
  gap: 12px;
}

.example-button {
  padding: 8px 16px;
  background: #6366F1;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
}

.example-button:hover {
  background: #4F46E5;
}

.example-dialog {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.example-content {
  background: white;
  border-radius: 12px;
  padding: 24px;
  width: 600px;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.example-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.example-header h3 {
  margin: 0;
  font-size: 1.2rem;
  color: #374151;
}

.close-button {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #6B7280;
  cursor: pointer;
  padding: 4px;
}

.example-code {
  background: #1E1E1E;
  color: #FFFFFF;
  padding: 16px;
  border-radius: 8px;
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 14px;
  line-height: 1.5;
  overflow-x: auto;
  margin: 0;
  white-space: pre;
}

.use-example-button {
  margin-top: 16px;
  padding: 8px 16px;
  background: #10a37f;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  width: 100%;
  transition: all 0.2s;
}

.use-example-button:hover {
  background: #0E906F;
}

.template-info {
  margin-bottom: 20px;
  background: #f9fafb;
  padding: 16px;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

.template-name-input {
  margin-bottom: 16px;
}

.template-name-input label,
.template-type label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #374151;
}

.type-options {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.type-option {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.type-option input[type="radio"] {
  width: 16px;
  height: 16px;
  cursor: pointer;
}

.type-option span {
  font-size: 14px;
  color: #374151;
}

.name-input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  font-size: 14px;
  transition: all 0.3s;
}

.name-input:focus {
  outline: none;
  border-color: #10a37f;
  box-shadow: 0 0 0 2px rgba(16, 163, 127, 0.1);
}
</style> 