<template>
  <div class="right-panel">
    <div class="panel-header">
      <h3>
        <svg class="header-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M4 4V20C4 21.1046 4.89543 22 6 22H18C19.1046 22 20 21.1046 20 20V8.34162C20 7.8034 19.7831 7.28789 19.3982 6.91161L14.9579 2.56999C14.5842 2.20459 14.0824 2 13.5597 2H6C4.89543 2 4 2.89543 4 4Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M14 2V6C14 7.10457 14.8954 8 16 8H20" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M8 13H16M8 17H16" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        问答预览
      </h3>
      <div class="actions">
        <button @click="handlePrint" class="action-button">
          <i class="icon-print"></i>
          预览打印
        </button>
        <button @click="exportExcel" class="action-button">
          <i class="icon-download"></i>
          导出报表
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
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { saveAs } from 'file-saver'
import * as XLSX from 'xlsx'

const props = defineProps({
  qaList: {
    type: Array,
    required: true
  }
})

const handlePrint = () => {
  // 创建打印样式
  const printWindow = window.open('', '_blank')
  const html = `
    <html>
      <head>
        <title>问答数据打印预览</title>
        <style>
          body { font-family: Arial, sans-serif; padding: 20px; }
          table { width: 100%; border-collapse: collapse; margin-top: 20px; }
          th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
          th { background-color: #f8f9fa; }
          .header { margin-bottom: 20px; }
          @media print {
            .no-print { display: none; }
            button { display: none; }
          }
        </style>
      </head>
      <body>
        <div class="header">
          <h2>问答数据</h2>
          <p>生成时间：${new Date().toLocaleString()}</p>
        </div>
        <button class="no-print" onclick="window.print()">打印</button>
        <table>
          <thead>
            <tr>
              <th>序号</th>
              <th>问题</th>
              <th>答案</th>
            </tr>
          </thead>
          <tbody>
            ${props.qaList.map((qa, index) => `
              <tr>
                <td>${index + 1}</td>
                <td>${qa.question}</td>
                <td>${qa.answer}</td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </body>
    </html>
  `
  printWindow.document.write(html)
  printWindow.document.close()
}

const exportExcel = () => {
  try {
    const data = props.qaList.map((item, index) => ({
      '序号': index + 1,
      '问题': item.question,
      '答案': item.answer
    }))

    const ws = XLSX.utils.json_to_sheet(data)
    const wb = XLSX.utils.book_new()
    XLSX.utils.book_append_sheet(wb, ws, '问答数据')
    
    // 设置列宽
    const colWidths = [{ wch: 6 }, { wch: 40 }, { wch: 40 }]
    ws['!cols'] = colWidths

    const excelBuffer = XLSX.write(wb, { bookType: 'xlsx', type: 'array' })
    const dataBlob = new Blob([excelBuffer], { 
      type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' 
    })
    
    // 使用当前时间作为文件名
    const fileName = `问答数据_${new Date().toLocaleDateString().replace(/\//g, '')}.xlsx`
    saveAs(dataBlob, fileName)
  } catch (error) {
    console.error('导出失败:', error)
    alert('导出失败，请稍后重试')
  }
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
</style> 