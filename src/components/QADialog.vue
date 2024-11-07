<template>
  <div class="dialog-overlay" @click.self="closeDialog">
    <div 
      class="dialog-content" 
      :style="{ left: position.x + 'px', top: position.y + 'px' }"
      ref="dialogRef"
    >
      <!-- 标题栏 -->
      <div class="dialog-header" @mousedown="startDrag">
        
        <h2>问答录入</h2>
        
        <button @click="closeDialog" class="close-button">关闭</button>
      </div>
      
      <!-- 输入区域 -->
      <div class="input-container">
        <div class="input-row">
          <div class="input-group">
            <label>问题:</label>
            <textarea 
              v-model="question" 
              placeholder="请输入问题..."
              @keydown.enter.exact.prevent="saveQA"
              ref="questionInput"
            ></textarea>
          </div>
          
          <div class="input-group">
            <label>答案:</label>
            <textarea 
              v-model="answer" 
              placeholder="请输入答案..."
              @keydown.enter.exact.prevent="saveQA"
            ></textarea>
          </div>
        </div>
        <div class="type-group">
          <label>类型:</label>
          <select v-model="type">
            <option value="general">一般</option>
            <option value="specific">特定</option>
          </select>
        </div>
       
      </div>

      <!-- 按钮区域 -->
      <div class="button-group">
        <button @click="saveQA" class="save-button">保存</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'

const emit = defineEmits(['save', 'close'])
const question = ref('')
const answer = ref('')
const type = ref('general')
const dialogRef = ref(null)
const questionInput = ref(null)

// 拖拽相关状态
const isDragging = ref(false)
const position = ref({ x: 100, y: 100 })
const dragOffset = ref({ x: 0, y: 0 })

// 初始化对话框位置
onMounted(() => {
  position.value = {
    x: 100,
    y: Math.min(window.innerHeight / 2 - 200, window.innerHeight - 400)
  }
})

// 开始拖拽
const startDrag = (e) => {
  isDragging.value = true
  dragOffset.value = {
    x: e.clientX - position.value.x,
    y: e.clientY - position.value.y
  }
  document.addEventListener('mousemove', handleDrag)
  document.addEventListener('mouseup', stopDrag)
}

// 处理拖拽
const handleDrag = (e) => {
  if (!isDragging.value) return
  
  let newX = e.clientX - dragOffset.value.x
  let newY = e.clientY - dragOffset.value.y
  
  const maxX = window.innerWidth - (dialogRef.value?.offsetWidth || 0)
  const maxY = window.innerHeight - (dialogRef.value?.offsetHeight || 0)
  
  newX = Math.max(0, Math.min(newX, maxX))
  newY = Math.max(0, Math.min(newY, maxY))
  
  position.value = { x: newX, y: newY }
}

// 停止拖拽
const stopDrag = () => {
  isDragging.value = false
  document.removeEventListener('mousemove', handleDrag)
  document.removeEventListener('mouseup', stopDrag)
}

const saveQA = () => {
  if (!question.value.trim() || !answer.value.trim()) {
    alert('请填写问题和答案！')
    return
  }
  
  emit('save', {
    question: question.value,
    answer: answer.value,
    type: type.value
  })
  
  // 清空输入框，准备下一次输入
  answer.value = ''
  type.value = 'general'
  question.value = ''
  
  // 聚焦到问题输入框
  nextTick(() => {
    questionInput.value?.focus()
  })
}

const closeDialog = () => {
  emit('close')
}
</script>

<style scoped>
.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.3);
  z-index: 1000;
}

.dialog-content {
  position: fixed;
  background: white;
  padding: 16px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  width: 800px;
  max-height: 400px;
}

.dialog-header {
  cursor: move;
  padding: 12px 16px;
  margin: -16px -16px 16px -16px;
  background: #f8f9fa;
  border-top-left-radius: 12px;
  border-top-right-radius: 12px;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.dialog-header h2 {
  margin: 0;
  font-size: 1rem;
  color: #374151;
  user-select: none;
}

.close-button {
  background: none;
  border: none;
  padding: 4px 8px;
  cursor: pointer;
  color: #6b7280;
  font-size: 0.9rem;
}

.input-container {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.input-row {
  display: flex;
  gap: 16px;
}

.input-group {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.input-group label {
  font-weight: 500;
  color: #374151;
  font-size: 0.9rem;
}

textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  font-size: 0.9rem;
  resize: vertical;
  min-height: 100px;
}

.type-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

select {
  padding: 6px;
  border: 1px solid #e5e7eb;
  border-radius: 4px;
  font-size: 0.9rem;
  width: 120px;
}

.button-group {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: 16px;
}

.save-button, .cancel-button {
  padding: 6px 16px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.save-button {
  background-color: #10a37f;
  color: white;
}

.cancel-button {
  background-color: #e5e7eb;
  color: #374151;
}

/* 输入框焦点样式 */
textarea:focus, select:focus {
  outline: none;
  border-color: #10a37f;
  box-shadow: 0 0 0 2px rgba(16, 163, 127, 0.1);
}
</style> 