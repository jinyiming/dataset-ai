<template>
  <div class="right-panel">
    <div class="panel-header">
      <h3>问答预览</h3>
      <div class="actions">
        <button @click="handlePrint" class="action-button">
          <i class="icon-print"></i>
          预览打印
        </button>
        <button @click="exportExcel" class="action-button">
          <i class="icon-download"></i>
          导出报表
        </button>
        <button @click="showDatasetDialog" class="action-button">
          <i class="icon-dataset"></i>
          导出数据集
        </button>
      </div>
    </div>
    <div class="excel-preview">
      <table>
        <thead>
          <tr>
            <th class="index-column">#</th>
            <th>问题</th>
            <th>答案</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(qa, index) in qaList" :key="qa.id">
            <td class="index-column">{{ index + 1 }}</td>
            <td class="question-cell">{{ qa.question }}</td>
            <td class="answer-cell">{{ qa.answer }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 添加模板选择对话框 -->
    <div v-if="showTemplateDialog" class="template-dialog">
      <div class="dialog-content">
        <div class="dialog-header">
          <h3>选择导出模板</h3>
          <button @click="closeTemplateDialog" class="close-button">×</button>
        </div>
        
        <div class="template-list">
          <div v-for="template in templates" :key="template.id" class="template-item">
            <div class="template-header">
              <input type="checkbox" 
                     :value="template.id" 
                     v-model="selectedTemplates"
                     :id="template.id">
              <label :for="template.id">{{ template.subject }}</label>
            </div>
            <div v-if="selectedTemplates.includes(template.id)" class="field-mapping">
              <div class="template-fields">
                <h4>字段映射</h4>
                <div class="mapping-container">
                  <div class="current-fields">
                    <div class="field-title">当前数据字段</div>
                    <div class="field-item">
                      <span class="field-label">问题</span>
                      <span class="field-example">{{ qaList[0]?.question || '示例问题' }}</span>
                    </div>
                    <div class="field-item">
                      <span class="field-label">答案</span>
                      <span class="field-example">{{ qaList[0]?.answer || '示例答案' }}</span>
                    </div>
                  </div>
                  <div class="mapping-arrows">
                    <div v-for="field in getTemplateFields(template)" 
                         :key="field"
                         class="mapping-row">
                      <div class="field-info">
                        <span class="field-name">{{ field }}</span>
                        <span class="field-type">{{ getFieldType(template, field) }}</span>
                        <span class="field-description">{{ getFieldDescription(template, field) }}</span>
                      </div>
                      <select v-model="fieldMapping[field]" class="field-select">
                        <option value="">不映射</option>
                        <option value="question">问题</option>
                        <option value="answer">答案</option>
                        <option value="custom">自定义</option>
                      </select>
                      <div class="arrow" :class="{ 'mapped': fieldMapping[field] }">→</div>
                      <input v-if="fieldMapping[field] === 'custom'"
                             v-model="customValues[field]"
                             :placeholder="getFieldPlaceholder(template, field)"
                             class="custom-input">
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="dialog-footer">
          <button @click="exportDataset" class="export-button">
            <i class="icon-export"></i>
            导出数据集
          </button>
          <button @click="closeTemplateDialog" class="cancel-button">取消</button>
        </div>
      </div>
    </div>

    <!-- 添加导出成功提示 -->
    <div v-if="showExportSuccess" class="export-success">
      <div class="success-content">
        <i class="icon-success"></i>
        <span>导出成功！</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  qaList: {
    type: Array,
    default: () => []
  }
})

const showTemplateDialog = ref(false)
const templates = ref([])
const selectedTemplates = ref([])
const fieldMapping = ref({})
const customValues = ref({})

const emit = defineEmits(['show-template-dialog'])

const showDatasetDialog = () => {
  emit('show-template-dialog')
}

const closeTemplateDialog = () => {
  showTemplateDialog.value = false
  selectedTemplates.value = []
  fieldMapping.value = {}
  customValues.value = {}
}

const getTemplateFields = (template) => {
  try {
    const content = JSON.parse(template.content)
    if (Array.isArray(content) && content.length > 0) {
      return Object.keys(content[0])
    }
    return []
  } catch (e) {
    console.error('解析模板内容失败:', e)
    return []
  }
}

const exportDataset = () => {
  if (selectedTemplates.value.length === 0) {
    alert('请至少选择一个模板')
    return
  }

  const exportData = selectedTemplates.value.map(templateId => {
    const template = templates.value.find(t => t.id === templateId)
    const fields = getTemplateFields(template)
    
    return {
      templateName: template.subject,
      data: props.qaList.map(qa => {
        const mappedData = {}
        fields.forEach(field => {
          const mapping = fieldMapping.value[field]
          if (mapping === 'question') {
            mappedData[field] = qa.question
          } else if (mapping === 'answer') {
            mappedData[field] = qa.answer
          } else if (mapping === 'custom') {
            mappedData[field] = customValues.value[field] || ''
          } else {
            mappedData[field] = ''
          }
        })
        return mappedData
      })
    }
  })

  console.log('导出数据:', exportData)
  const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' })
  const fileName = `数据集_${new Date().toLocaleDateString()}.json`
  const url = window.URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = fileName
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  window.URL.revokeObjectURL(url)
  
  closeTemplateDialog()
}

// 获取字段类型
const getFieldType = (template, field) => {
  try {
    const content = JSON.parse(template.content)
    if (Array.isArray(content) && content.length > 0) {
      const firstItem = content[0]
      return typeof firstItem[field]
    }
    return 'unknown'
  } catch (e) {
    return 'unknown'
  }
}

// 获取字段描述
const getFieldDescription = (template, field) => {
  try {
    const content = JSON.parse(template.content)
    if (Array.isArray(content) && content.length > 0) {
      const firstItem = content[0]
      return firstItem[field] || '无示例值'
    }
    return '无示例值'
  } catch (e) {
    return '无示例值'
  }
}

// 获取字段占位符
const getFieldPlaceholder = (template, field) => {
  return `请输入${field}的值`
}

// 定义导出成功状态
const showExportSuccess = ref(false)

// 导出成功后的处理
const handleExportSuccess = () => {
  showExportSuccess.value = true
  setTimeout(() => {
    showExportSuccess.value = false
  }, 3000)
}

// 添加导出报表功能
const exportExcel = () => {
  if (props.qaList.length === 0) {
    alert('没有可导出的数据')
    return
  }
  
  // 创建表格数据
  let csvContent = "数据序号,问题,答案\n"
  
  props.qaList.forEach((qa, index) => {
    // 处理CSV中的特殊字符
    const question = `"${qa.question.replace(/"/g, '""')}"`
    const answer = `"${qa.answer.replace(/"/g, '""')}"`
    csvContent += `${index + 1},${question},${answer}\n`
  })
  
  // 创建Blob对象
  const blob = new Blob([new Uint8Array([0xEF, 0xBB, 0xBF]), csvContent], { type: 'text/csv;charset=utf-8' })
  const fileName = `问答报表_${new Date().toLocaleDateString()}.csv`
  
  // 创建下载链接
  const url = window.URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = fileName
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  window.URL.revokeObjectURL(url)
  
  // 显示导出成功提示
  handleExportSuccess()
}
</script>

<style scoped>
.right-panel {
  width: 460px;
  padding: 20px;
  border-left: 1px solid #e5e7eb;
  background-color: #ffffff;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.panel-header {
  padding-bottom: 16px;
  border-bottom: 1px solid #e5e7eb;
  margin-bottom: 20px;
}

.panel-header h3 {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 1.25rem;
  color: #374151;
  margin: 0 0 12px 0;
}

.header-icon {
  width: 24px;
  height: 24px;
  color: #10a37f;
}

.actions {
  display: flex;
  gap: 12px;
}

.action-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  background: #fff;
  color: #374151;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 13px;
}

.action-button:hover {
  background: #f3f4f6;
  border-color: #10a37f;
  color: #10a37f;
}

.action-button:active {
  transform: scale(0.98);
}

.excel-preview {
  flex: 1;
  overflow-y: auto;
  background: #fff;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
  table-layout: fixed;
}

th, td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #e5e7eb;
  line-height: 1.5;
}

th {
  background-color: #f9fafb;
  font-weight: 600;
  color: #374151;
  position: sticky;
  top: 0;
  z-index: 1;
  white-space: nowrap;
}

.index-column {
  width: 40px;
  text-align: center;
  color: #6b7280;
  font-size: 12px;
}

.question-cell, .answer-cell {
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: normal;
  word-break: break-word;
}

tr:hover {
  background-color: #f9fafb;
}

/* 自定义滚动条 */
.excel-preview::-webkit-scrollbar {
  width: 6px;
}

.excel-preview::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.excel-preview::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.excel-preview::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* 图标样式 */
.icon-print, .icon-download {
  width: 16px;
  height: 16px;
  display: inline-block;
  background-size: contain;
  background-repeat: no-repeat;
}

.icon-print {
  background-image: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" /></svg>');
}

.icon-download {
  background-image: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" /></svg>');
}

/* 打印样式 */
@media print {
  .actions {
    display: none;
  }
  
  .right-panel {
    width: 100%;
    border: none;
  }

  .excel-preview {
    border: none;
  }

  table {
    font-size: 12px;
  }
}

.template-dialog {
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

.dialog-content {
  background: white;
  border-radius: 16px;
  padding: 32px;
  width: 900px;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid #e5e7eb;
}

.dialog-header h3 {
  font-size: 1.5rem;
  color: #111827;
  margin: 0;
}

.mapping-container {
  display: grid;
  grid-template-columns: 1fr;
  gap: 24px;
}

.field-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 200px;
}

.field-name {
  font-weight: 600;
  color: #1e293b;
}

.field-type {
  font-size: 0.8rem;
  color: #64748b;
  padding: 2px 6px;
  background: #f1f5f9;
  border-radius: 4px;
  display: inline-block;
}

.field-description {
  font-size: 0.85rem;
  color: #94a3b8;
  font-style: italic;
}

.field-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 8px;
  background: white;
  border-radius: 6px;
  border: 1px solid #e2e8f0;
}

.field-label {
  font-weight: 500;
  color: #1e293b;
}

.field-example {
  font-size: 0.9rem;
  color: #64748b;
  font-style: italic;
}

.mapping-row {
  display: grid;
  grid-template-columns: 2fr 1fr auto 2fr;
  gap: 16px;
  align-items: center;
  padding: 12px;
  background: white;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;
}

.mapping-row:hover {
  border-color: #10a37f;
  box-shadow: 0 2px 8px rgba(16, 163, 127, 0.1);
}

.arrow {
  color: #cbd5e1;
  font-size: 1.2rem;
  transition: all 0.3s ease;
}

.arrow.mapped {
  color: #10a37f;
  transform: scale(1.2);
}

.field-select {
  padding: 8px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  background: white;
  color: #1e293b;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.field-select:focus {
  border-color: #10a37f;
  outline: none;
  box-shadow: 0 0 0 2px rgba(16, 163, 127, 0.1);
}

.custom-input {
  padding: 8px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 0.9rem;
  width: 100%;
  transition: all 0.3s ease;
}

.custom-input:focus {
  border-color: #10a37f;
  outline: none;
  box-shadow: 0 0 0 2px rgba(16, 163, 127, 0.1);
}

.icon-dataset {
  width: 16px;
  height: 16px;
  background-image: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4" /></svg>');
}

.icon-export {
  width: 16px;
  height: 16px;
  background-image: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>');
}

.export-success {
  position: fixed;
  top: 20px;
  right: 20px;
  background: #10b981;
  color: white;
  padding: 12px 24px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  animation: slideIn 0.3s ease;
  z-index: 1000;
}

.success-content {
  display: flex;
  align-items: center;
  gap: 8px;
}

.icon-success {
  width: 20px;
  height: 20px;
  background-image: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="white"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>');
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}
</style> 