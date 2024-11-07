<template>
  <div class="left-panel">
    <div class="content-wrapper">
      <div class="chat-header">
        <h2>
          <svg class="header-icon" viewBox="0 0 24 24" fill="none">
            <path d="M21 11.5a8.38 8.38 0 01-.9 3.8 8.5 8.5 0 01-7.6 4.7 8.38 8.38 0 01-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 01-.9-3.8 8.5 8.5 0 014.7-7.6 8.38 8.38 0 013.8-.9h.5a8.48 8.48 0 018 8v.5z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M12 8v4M12 16h.01" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          智能问答助手
        </h2>
      </div>

      <div class="chat-history">
        <div class="dialog-history">
          <div v-for="(dialog, index) in dialogList" :key="index" class="dialog-item">
            <div class="dialog-prompt">
              <svg class="user-icon" viewBox="0 0 24 24" fill="none">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" stroke="#4b5563" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <circle cx="12" cy="7" r="4" stroke="#4b5563" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <div class="prompt-content">
                <div class="prompt-text">{{ dialog.prompt }}</div>
                <div class="generation-info">
                  <svg class="generation-icon" viewBox="0 0 24 24" fill="none">
                    <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83" stroke="#10a37f" stroke-width="2" stroke-linecap="round"/>
                  </svg>
                  <span>已生成 {{ dialog.count }} 组问答</span>
                </div>
              </div>
            </div>
            <div class="dialog-time">{{ dialog.timestamp }}</div>
          </div>
        </div>
      </div>

      <div class="input-wrapper">
        <div class="input-container">
          <div class="main-input-wrapper">
            <textarea
              v-model="aiPrompt"
              placeholder="请输入您的问题..."
              class="chat-input"
              rows="3"
              @keydown.enter.exact.prevent="handleEnterPress"
            ></textarea>
            <div class="button-group">
              <input 
                type="file" 
                accept=".docx" 
                @change="handleFileUpload" 
                ref="fileInput"
                style="display: none"
              >
              <button @click="$refs.fileInput.click()" class="action-button">
                <svg class="attachment-icon" viewBox="0 0 24 24" fill="none">
                  <path d="M21.44 11.05l-9.19 9.19a6 6 0 01-8.49-8.49l9.19-9.19a4 4 0 015.66 5.66l-9.2 9.19a2 2 0 01-2.83-2.83l8.49-8.48" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </button>
              <button 
                ref="submitButton"
                @click="generateQA" 
                class="action-button" 
                :class="{ 'submitting': isSubmitting }"
                :disabled="isGenerating || isSubmitting"
              >
                <svg class="send-icon" viewBox="0 0 24 24" fill="none">
                  <path d="M22 2L11 13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M22 2L15 22L11 13L2 9L22 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </button>
            </div>
          </div>
          <div class="count-input-container">
            <div class="count-label">生成数量：</div>
            <input
              v-model.number="qaCount"
              type="number"
              min="1"
              max="50"
              class="count-input"
              @keydown.enter.prevent="generateQA"
            />
            <div class="count-suffix">对</div>
          </div>
        </div>
      </div>
    </div>
    <div class="file-upload">
      <input 
        type="file" 
        accept=".docx" 
        @change="handleFileUpload" 
        ref="fileInput"
        style="display: none"
      >
      <button @click="$refs.fileInput.click()" class="upload-button">
        上传文档
      </button>
    </div>
    <div class="doc-sections" v-if="sections.length">
      <div v-for="(section, index) in sections" :key="index" class="section">
        <h3 :class="'heading-' + section.level">{{ section.title }}</h3>
        <div class="content">
          <p v-for="(content, cIndex) in section.content" :key="cIndex">
            {{ content }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import axios from 'axios'

const aiPrompt = ref('')
const qaCount = ref(10)
const isGenerating = ref(false)
const dialogList = ref([])
const isHovering = ref(false)
const emit = defineEmits(['generate-qa', 'loading', 'process-start', 'process-update', 'process-end'])
const sections = ref([])
const isProcessing = ref(false)
const progress = ref(0)
const statusText = ref('')
const isSubmitting = ref(false)
const inputArea = ref(null)
const submitButton = ref(null)

const handleMouseEnter = () => {
  isHovering.value = true
}

const handleMouseLeave = () => {
  isHovering.value = false
}

const generateQA = async () => {
  if (aiPrompt.value.trim() === '' || isGenerating.value) return;
  
  isGenerating.value = true
  emit('loading', true)

  try {
    const response = await axios.post('http://localhost:8000/flask/api/generate', {
      prompt: aiPrompt.value,
      count: qaCount.value
    })
    
    if (response.status === 200) {
      emit('generate-qa', response.data.qa_pairs)
      // 添加到对话历史
      dialogList.value.unshift({
        prompt: aiPrompt.value,
        count: qaCount.value,
        timestamp: new Date().toLocaleString()
      })
    }
  } catch (error) {
    console.error('生成问答失败:', error)
    alert('生成失败，请重试！')
  } finally {
    isGenerating.value = false
    emit('loading', false)
  }
}

const handleFileUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  try {
    // 开始处理 - 25%
    emit('process-start')
    emit('process-update', { 
      progress: 25, 
      status: '正在识别文档...',
      details: {
        fileName: file.name,
        fileSize: `${(file.size / 1024).toFixed(2)} KB`
      }
    })
    
    await new Promise(resolve => setTimeout(resolve, 2000))

    const formData = new FormData()
    formData.append('file', file)
    
    const response = await axios.post(
      'http://localhost:8000/flask/api/process-doc',
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }
    )

    if (response.status === 200) {
      // 文档识别完成 - 50%
      const sections = response.data.sections
      emit('process-update', { 
        progress: 50, 
        status: '正在提取标题...',
        details: {
          titleCount: sections.length
        }
      })
      
      await new Promise(resolve => setTimeout(resolve, 2000))

      // 组装问答对
      let processedCount = 0
      let allQAPairs = [] // 存储所有生成的问答对

      // 逐个处理每个标题和内容
      for (let i = 0; i < sections.length; i++) {
        const section = sections[i]
        
        // 更新进度 - 50% 到 75% 之间
        const currentProgress = 50 + (25 * (i + 1) / sections.length)
        emit('process-update', { 
          progress: currentProgress, 
          status: `正在处理第 ${i + 1}/${sections.length} 个标题...`,
          details: {
            currentTitle: {
              level: section.level,
              text: section.title
            }
          }
        })

        // 为每个标题生成问答对
        const qa = {
          question: section.title,
          answer: section.content.join(' ')
        }

        // 设置输入框内容
        aiPrompt.value = `${qa.question}：${qa.answer}`
        
        await new Promise(resolve => setTimeout(resolve, 1500))
        
        // 使用输入框下方设置的问答对数量
        try {
          const response = await axios.post('http://localhost:8000/flask/api/generate', {
            prompt: aiPrompt.value,
            count: qaCount.value
          })
          
          if (response.status === 200) {
            // 将新生成的问答对添加到总列表中
            allQAPairs = [...allQAPairs, ...response.data.qa_pairs]
            
            // 更新处理进度
            processedCount++

            // 更新进度 - 75% 到 100% 之间
            const finalProgress = 75 + (25 * processedCount / sections.length)
            emit('process-update', { 
              progress: finalProgress, 
              status: `已处理 ${processedCount}/${sections.length} 个标题，共生成 ${allQAPairs.length} 组问答对`,
              details: {
                currentQA: processedCount,
                totalQA: sections.length,
                currentPair: qa,
                qaPerTitle: qaCount.value
              }
            })

            // 更新对话历史
            dialogList.value.unshift({
              prompt: aiPrompt.value,
              count: qaCount.value,
              timestamp: new Date().toLocaleString()
            })

            // 发送所有问答对到父组件
            emit('generate-qa', allQAPairs.map((item, index) => ({
              id: index,
              question: item.question,
              answer: item.answer
            })))
          }
        } catch (error) {
          console.error('生成问答对失败:', error)
        }

        await new Promise(resolve => setTimeout(resolve, 1000))
      }

      // 完成处理 - 100%
      emit('process-update', { 
        progress: 100, 
        status: `处理完成！共处理 ${sections.length} 个标题，生成 ${allQAPairs.length} 组问答对`,
        details: {
          totalQA: allQAPairs.length,
          qaPerTitle: qaCount.value
        }
      })
      
      await new Promise(resolve => setTimeout(resolve, 2000))
      emit('process-end')
    }
  } catch (error) {
    console.error('处理文档失败:', error)
    emit('process-update', { progress: 100, status: '处理失败，请重试' })
    emit('process-end')
  }
}

// 添加回车提交处理函数
const handleEnterPress = (e) => {
  if (!e.shiftKey && !e.ctrlKey && !e.altKey) {
    generateQA()
  }
}
</script>

<style scoped>
.left-panel {
  width: 340px;
  height: 100%;
  position: relative;
  display: flex;
  flex-direction: column;
}

.content-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  height: 100%;
  position: relative;
  padding: 20px;
}

.chat-header {
  padding: 8px 0;
  margin-bottom: 12px;
  border-bottom: 1px solid rgba(229, 231, 235, 0.5);
}

.chat-header h2 {
  margin: 0;
  font-size: 1.25rem;
  color: #374151;
  display: flex;
  align-items: center;
  gap: 8px;
}

.header-icon {
  width: 24px;
  height: 24px;
  color: #10a37f;
}

.chat-history {
  flex: 1;
  overflow-y: auto;
  padding: 20px 0;
}

.input-wrapper {
  position: sticky;
  bottom: 0;
  left: 0;
  right: 0;
  background: white;
  padding: 20px;
  border-top: 1px solid rgba(229, 231, 235, 0.5);
  margin-top: auto;
}

.input-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  padding: 12px;
}

.main-input-wrapper {
  position: relative;
  margin-bottom: 8px;
}

.chat-input {
  width: 85%;
  padding: 12px;
  padding-right: 44px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  resize: none;
  font-size: 14px;
  background: #fff;
  transition: all 0.3s ease;
  line-height: 1.5;
}

.button-group {
  position: absolute;
  right: 2px;
  bottom: 8px;
  display: flex;

}

.action-button {
  background: none;
  border: none;
  padding: 8px;
  cursor: pointer;
  transition: all 0.2s;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-button:hover {
  background-color: rgba(16, 163, 127, 0.1);
}

.action-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.send-icon, .attachment-icon {
  width: 17px;
  height: 15px;
  color: #10a37f;
}

.count-input-container {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 0 2px;
}

.count-label {
  font-size: 13px;
  color: #666;
  white-space: nowrap;
}

.count-input {
  width: 60px;
  padding: 4px 8px;
  border: 1px solid #e5e7eb;
  border-radius: 4px;
  font-size: 13px;
  text-align: center;
  transition: all 0.3s;
}

.count-input:focus {
  outline: none;
  border-color: #10a37f;
  box-shadow: 0 0 0 2px rgba(16, 163, 127, 0.1);
}

.count-suffix {
  font-size: 13px;
  color: #666;
}

.count-input::-webkit-inner-spin-button,
.count-input::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

.count-input[type=number] {
  -moz-appearance: textfield;
  appearance: textfield;  /* 添加标准属性以确保兼容性 */
}

.dialog-history {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
  margin-bottom: 10px;
}

.dialog-item {
  background: white;
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.dialog-prompt {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.prompt-content {
  flex: 1;
}

.prompt-text {
  font-size: 14px;
  line-height: 1.6;
  color: #374151;
  margin-bottom: 4px;
}

.prompt-count {
  font-size: 12px;
  color: #6b7280;
}

.dialog-time {
  font-size: 12px;
  color: #9ca3af;
  text-align: right;
  margin-top: 8px;
}

.user-icon, .ai-icon {
  width: 24px;
  height: 24px;
  flex-shrink: 0;
}

.response-text {
  color: #10a37f;
}

.generation-info {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 8px;
  color: #10a37f;
  font-size: 13px;
  font-weight: 500;
}

.generation-icon {
  width: 16px;
  height: 16px;
  color: #10a37f;
}

.dialog-item {
  background: white;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 16px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  transition: transform 0.2s ease;
}

.dialog-item:hover {
  transform: translateY(-2px);
}

.file-upload {
  display: none;
}

.doc-sections {
  margin-top: 20px;
}

.section {
  margin-bottom: 20px;
}

.heading-1 { font-size: 1.5em; font-weight: bold; }
.heading-2 { font-size: 1.3em; font-weight: bold; }
.heading-3 { font-size: 1.1em; font-weight: bold; }

.content {
  margin-left: 20px;
}

.content p {
  margin: 8px 0;
}

/* 进度条样式 */
.processing-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.processing-container {
  background: white;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  width: 500px;
  position: fixed;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
}

.progress-steps {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  flex: 1;
  position: relative;
  opacity: 0.5;
  transition: all 0.3s ease;
}

.step.active {
  opacity: 1;
}

.step.completed {
  opacity: 1;
  color: #10a37f;
}

.step:not(:last-child)::after {
  content: '';
  position: absolute;
  right: -50%;
  top: 20px;
  width: 100%;
  height: 2px;
  background: #e5e7eb;
  z-index: -1;
}

.step.completed:not(:last-child)::after {
  background: #10a37f;
}

.step-icon {
  width: 40px;
  height: 40px;
  background: white;
  border: 2px solid #e5e7eb;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.step.active .step-icon {
  border-color: #10a37f;
  background: #f0fdf4;
}

.step.completed .step-icon {
  background: #10a37f;
  border-color: #10a37f;
  color: white;
}

.icon {
  width: 20px;
  height: 20px;
  color: currentColor;
}

.step-label {
  font-size: 14px;
  font-weight: 500;
}

.status-text {
  text-align: center;
  font-size: 14px;
  color: #374151;
  margin-top: 16px;
}

/* 手势动画 */
.gesture-animation {
  position: absolute;
  right: 20px;
  bottom: 20px;
  animation: clickGesture 1s ease-in-out infinite;
}

.hand-icon {
  width: 32px;
  height: 32px;
  color: #10a37f;
}

@keyframes clickGesture {
  0% { transform: scale(1) translateY(0); }
  50% { transform: scale(0.9) translateY(4px); }
  100% { transform: scale(1) translateY(0); }
}

/* 提交按钮动画 */
.action-button.submitting {
  animation: pulse 0.5s ease;
}

.action-button.clicking {
  transform: scale(0.95);
  background-color: rgba(16, 163, 127, 0.2);
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(0.95); }
  100% { transform: scale(1); }
}

/* 输入框动画 */
.chat-input {
  transition: all 0.3s ease;
}

.chat-input:focus {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(16, 163, 127, 0.1);
}
</style> 