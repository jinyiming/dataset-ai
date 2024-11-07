<template>
                <div class="main-container">
                  <!-- 屏保组件 -->
                  <Screensaver 
                    v-if="showScreensaver" 
                    @close="hideScreensaver"
                    :show="showScreensaver"
                  />
              
                  <!-- 进度条和状态显示 -->
                  <div v-if="isProcessing" class="processing-overlay">
                    <div class="processing-container">
                      <!-- 添加标题 -->
                      <div class="process-header">
                        <svg class="factory-icon" viewBox="0 0 24 24" fill="none">
                          <path d="M21 12v3h-3v-3h3zm-12 0v3H6v-3h3zm6 0v3h-3v-3h3zm-6-6v3H6V6h3zm6 0v3h-3V6h3zm6 0v3h-3V6h3zM3 21h18v-3H3v3z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                          <path d="M3 13.5V21M21 13.5V21" stroke="currentColor" stroke-width="2"/>
                          <path d="M3 6c0-1.1.9-2 2-2h14a2 2 0 012 2v3H3V6z" stroke="currentColor" stroke-width="2"/>
                        </svg>
                        <h2>自动化工厂</h2>
                      </div>
              
                      <!-- 进度条步骤 -->
                      <div class="progress-steps">
                        <!-- 文档识别步骤 -->
                        <div class="step" :class="{ active: progress >= 25, completed: progress > 25 }">
                          <div class="step-icon">
                            <svg v-if="progress <= 25" class="icon" viewBox="0 0 24 24" fill="none">
                              <path d="M4 4v16c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V8l-6-6H6c-1.1 0-2 .9-2 2z" stroke="currentColor" stroke-width="2"/>
                              <path d="M14 2v6h6" stroke="currentColor" stroke-width="2"/>
                            </svg>
                            <svg v-else class="icon completed" viewBox="0 0 24 24" fill="none">
                              <path d="M5 13l4 4L19 7" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                            </svg>
                          </div>
                          <span class="step-label">识别文档</span>
                          <div class="step-detail" v-if="currentStep === 'document'">
                            <div class="file-info">
                              <span class="file-name">{{ processingDetails.fileName }}</span>
                              <span class="file-size">{{ processingDetails.fileSize }}</span>
                            </div>
                          </div>
                        </div>
                        
                        <!-- 提取标题步骤 -->
                        <div class="step" :class="{ active: progress >= 50, completed: progress > 50 }">
                          <div class="step-icon">
                            <svg v-if="progress < 50" class="icon" viewBox="0 0 24 24" fill="none">
                              <path d="M4 6h16M4 10h16M4 14h16M4 18h16" stroke="currentColor" stroke-width="2"/>
                            </svg>
                            <svg v-else class="icon completed" viewBox="0 0 24 24" fill="none">
                              <path d="M5 13l4 4L19 7" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                            </svg>
                          </div>
                          <span class="step-label">提取标题</span>
                          <div class="step-detail" v-if="currentStep === 'titles'">
                            <div class="title-info">
                              <div class="title-count">已识别 {{ processingDetails.titleCount }} 个标题</div>
                              <div class="current-title" v-if="processingDetails.currentTitle">
                                <span class="title-level">H{{ processingDetails.currentTitle.level }}</span>
                                <span class="title-text">{{ processingDetails.currentTitle.text }}</span>
                              </div>
                            </div>
                          </div>
                        </div>
                        
                        <!-- 修改组装问答步骤的显示 -->
                        <div class="step" :class="{ active: progress >= 75, completed: progress > 75 }">
                          <div class="step-icon">
                            <svg v-if="progress < 75" class="icon" viewBox="0 0 24 24" fill="none">
                              <path d="M12 4v16m-8-8h16" stroke="currentColor" stroke-width="2"/>
                            </svg>
                            <svg v-else class="icon completed" viewBox="0 0 24 24" fill="none">
                              <path d="M5 13l4 4L19 7" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                            </svg>
                          </div>
                          <span class="step-label">组装问答</span>
                          <div class="step-detail" v-if="currentStep === 'qa'">
                            <div class="qa-info">
                              <div class="qa-progress">
                                <div class="current-title">
                                  <span class="title-badge">当前标题</span>
                                  <span class="title-text">{{ processingDetails.currentTitle?.text }}</span>
                                </div>
                                <div class="qa-count">
                                  处理进度: {{ processingDetails.currentQA }} / {{ processingDetails.totalQA }}
                                </div>
                              </div>
                              <div class="qa-preview" v-if="processingDetails.currentPair">
                                <div class="preview-question">Q: {{ processingDetails.currentPair.question }}</div>
                                <div class="preview-answer">A: {{ processingDetails.currentPair.answer }}</div>
                              </div>
                            </div>
                          </div>
                        </div>
                        
                        <!-- 提交完成步骤 -->
                        <div class="step" :class="{ active: progress >= 100, completed: progress === 100 }">
                          <div class="step-icon">
                            <svg v-if="progress < 100" class="icon" viewBox="0 0 24 24" fill="none">
                              <path d="M5 13l4 4L19 7" stroke="currentColor" stroke-width="2"/>
                            </svg>
                            <svg v-else class="icon completed" viewBox="0 0 24 24" fill="none">
                              <path d="M20 6L9 17l-5-5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                            </svg>
                          </div>
                          <span class="step-label">提交完成</span>
                          <div class="step-detail" v-if="currentStep === 'complete'">
                            <div class="complete-info">
                              <div class="total-count">共处理 {{ processingDetails.totalQA }} 组问答对</div>
                              <div class="success-rate">成功率 100%</div>
                            </div>
                          </div>
                        </div>
                      </div>
              
                      <!-- 添加进度指示器 -->
                      <div class="progress-indicator">
                        <div class="progress-bar">
                          <div class="progress-fill" :style="{ width: `${progress}%` }"></div>
                        </div>
                        <div class="progress-percentage">{{ Math.round(progress) }}%</div>
                      </div>
              
                      <div class="status-text">{{ statusText }}</div>
                    </div>
                  </div>
              
                  <!-- 面板容器 -->
                  <div class="panels-container">
                    <LeftPanel 
                      @generate-qa="handleGenerateQA" 
                      @loading="handleLoading"
                      @process-start="handleProcessStart"
                      @process-update="handleProcessUpdate"
                      @process-end="handleProcessEnd"
                      class="panel left-gradient"
                    />
                    <div class="panel-divider"></div>
                    <MiddlePanel 
                      :qaList="qaList" 
                      :isLoading="isLoading"
                      @update-qa="handleUpdateQA"
                      class="panel middle-gradient"
                    />
                    <div class="panel-divider"></div>
                    <RightPanel :qaList="qaList" class="panel right-gradient" />
                  </div>
              
                  <!-- 浮动图标栏 -->
                  <div class="floating-dock">
                    <div class="icon-dock">
                      <draggable 
                        v-model="dockItems" 
                        item-key="id"
                        @start="drag=true" 
                        @end="drag=false"
                        class="dock-items-container"
                      >
                        <template #item="{ element }">
                          <div class="dock-item" :class="{ active: element.active }" @click="handleIconClick(element)">
                            <div class="dock-icon-wrapper" :style="{ backgroundColor: element.bgColor }">
                              <svg class="dock-icon" viewBox="0 0 24 24" fill="none">
                                <path :d="element.icon" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                              </svg>
                            </div>
                            <span class="dock-label">{{ element.label }}</span>
                          </div>
                        </template>
                      </draggable>
                    </div>
                  </div>
              
                  <!-- 问答录入对话框 -->
                  <QADialog v-if="showDialog" @save="handleSave" @close="showDialog = false" />
              
                  <!-- 添加设置对话框 -->
                  <SettingsPage v-if="showSettings" @close="showSettings = false" />
                </div>
              </template>
              
              <script setup>
              import { ref, onMounted, onUnmounted, onBeforeUnmount } from 'vue'
              import draggable from 'vuedraggable'
              import LeftPanel from '@/components/LeftPanel.vue'
              import MiddlePanel from '@/components/MiddlePanel.vue'
              import RightPanel from '@/components/RightPanel.vue'
              import QADialog from '@/components/QADialog.vue'
              import Screensaver from '@/components/Screensaver.vue'
              import SettingsPage from '@/views/SettingsPage.vue'
              
              const qaList = ref([])
              const isLoading = ref(false)
              const showDialog = ref(false)
              const drag = ref(false)
              const showScreensaver = ref(true)
              let lastActivityTime = Date.now()
              let inactivityTimer = null
              
              const isProcessing = ref(false)
              const progress = ref(0)
              const statusText = ref('')
              
              const currentStep = ref('document')
              const processingDetails = ref({
                fileName: '',
                fileSize: '',
                titleCount: 0,
                currentTitle: null,
                currentQA: 0,
                totalQA: 0,
                currentPair: null
              })
              
              const showSettings = ref(false)
              
              // 检查用户活动
              const checkInactivity = () => {
                const now = Date.now()
                if (now - lastActivityTime > 5 * 60 * 1000) { // 5分钟
                  showScreensaver.value = true
                }
              }
              
              // 重置活动计时器
              const resetActivityTimer = () => {
                lastActivityTime = Date.now()
              }
              
              // 监听用户活动
              onMounted(() => {
                // 显示初始屏保
                showScreensaver.value = true

                // 添加事件监听
                document.addEventListener('mousemove', resetActivityTimer)
                document.addEventListener('keydown', resetActivityTimer)
                document.addEventListener('click', resetActivityTimer)
                
                // 启动不活动检查
                inactivityTimer = setInterval(checkInactivity, 10000) // 每10秒检查一次
              })
              
              // 组件卸载时清理
              onBeforeUnmount(() => {
                // 移除事件监听
                document.removeEventListener('mousemove', resetActivityTimer)
                document.removeEventListener('keydown', resetActivityTimer)
                document.removeEventListener('click', resetActivityTimer)
                
                // 清除定时器
                if (inactivityTimer) {
                  clearInterval(inactivityTimer)
                }
              })
              
              const hideScreensaver = () => {
                showScreensaver.value = false
                resetActivityTimer()
              }
              
              // 处理进度相关的事件
              const handleProcessStart = () => {
                isProcessing.value = true
                progress.value = 0
              }
              
              const handleProcessUpdate = (data) => {
                progress.value = data.progress
                statusText.value = data.status
                
                // 更新处理详情
                if (data.details) {
                  processingDetails.value = {
                    ...processingDetails.value,
                    ...data.details
                  }
                }
                
                // 更新当前步骤
                if (progress.value <= 25) {
                  currentStep.value = 'document'
                } else if (progress.value <= 50) {
                  currentStep.value = 'titles'
                } else if (progress.value <= 75) {
                  currentStep.value = 'qa'
                } else {
                  currentStep.value = 'complete'
                }
              }
              
              const handleProcessEnd = () => {
                setTimeout(() => {
                  isProcessing.value = false
                  progress.value = 0
                }, 1500)
              }
              
              // 图标数据
              const dockItems = ref([
                {
                  id: 1,
                  label: '问答',
                  icon: 'M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 13.8214 2.48697 15.5291 3.33782 17L2.5 21.5L7 20.6622C8.47087 21.513 10.1786 22 12 22Z',
                  bgColor: '#10B981',
                  active: true
                },
                {
                  id: 2,
                  label: '历史',
                  icon: 'M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z',
                  bgColor: '#6366F1',
                  active: false
                },
                {
                  id: 3,
                  label: '记录',
                  icon: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2',
                  bgColor: '#F59E0B',
                  active: false
                },
                {
                  id: 4,
                  label: '设置',
                  icon: 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z',
                  bgColor: '#8B5CF6',
                  active: false
                }
              ])
              
              const handleGenerateQA = (aiResponse) => {
                qaList.value = aiResponse.map((item, index) => ({
                  id: index,
                  question: item.question,
                  answer: item.answer
                }))
              }
              
              const handleLoading = (loading) => {
                isLoading.value = loading
              }
              
              const handleUpdateQA = (updatedQA) => {
                const index = qaList.value.findIndex(item => item.id === updatedQA.id)
                if (index !== -1) {
                  qaList.value[index] = updatedQA
                }
              }
              
              // 修改图标点击处理函数
              const handleIconClick = (element) => {
                if (element.label === '问答') {
                  showDialog.value = true
                } else if (element.label === '设置') {
                  window.open('/settings', '_blank')  // 在新窗口打开设置页面
                }
              }
              
              // 处理保存问答对
              const handleSave = (data) => {
                qaList.value.push(data); // 将数据添加到 qaList
                // 不关闭对话框，允许连续保存
              }
              </script>
              
              <style scoped>
              .main-container {
                display: flex;
                min-height: 100vh;
                width: 100vw;
                background: linear-gradient(135deg, #f5f7fa 0%, #e4e7eb 100%);
                padding: 16px;
                box-sizing: border-box;
              }
              
              .panels-container {
                display: flex;
                width: 100%;
                gap: 12px;
                height: calc(100vh - 32px);
              }
              
              .panel {
                height: 100%;
                overflow-y: auto;
                border-radius: 16px;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
                transition: all 0.3s ease;
                backdrop-filter: blur(10px);
                display: flex;
                flex-direction: column;
              }
              
              .panel-divider {
                width: 1px;
                background: linear-gradient(to bottom, transparent, rgba(0, 0, 0, 0.05), transparent);
                margin: 0;
                align-self: stretch;
              }
              
              /* 调整面板宽度 */
              .left-gradient, .right-gradient {
                width: 380px;
                flex-shrink: 0;
              }
              
              /* 中间面板自适应宽度 */
              .middle-gradient {
                flex: 1;
                min-width: 0;
              }
              
              /* 动态背景渐变 */
              .left-gradient {
                background: linear-gradient(-45deg, #e3f2fd, #bbdefb, #90caf9, #64b5f6);
                background-size: 400% 400%;
                animation: gradientBG 15s ease infinite;
              }
              
              .middle-gradient {
                background: linear-gradient(-45deg, #f5f5f5, #eeeeee, #e0e0e0, #bdbdbd);
                background-size: 400% 400%;
                animation: gradientBG 15s ease infinite;
                animation-delay: 0.5s;
              }
              
              .right-gradient {
                background: linear-gradient(-45deg, #e8eaf6, #c5cae9, #9fa8da, #7986cb);
                background-size: 400% 400%;
                animation: gradientBG 15s ease infinite;
                animation-delay: 1s;
              }
              
              @keyframes gradientBG {
                0% {
                  background-position: 0% 50%;
                }
                50% {
                  background-position: 100% 50%;
                }
                100% {
                  background-position: 0% 50%;
                }
              }
              
              /* 面板悬停效果 */
              .panel:hover {
                transform: translateY(-2px);
                box-shadow: 0 12px 20px -8px rgba(0, 0, 0, 0.15);
              }
              
              /* 自定义滚动条 */
              .panel::-webkit-scrollbar {
                width: 6px;
              }
              
              .panel::-webkit-scrollbar-track {
                background: transparent;
              }
              
              .panel::-webkit-scrollbar-thumb {
                background: rgba(0, 0, 0, 0.1);
                border-radius: 3px;
              }
              
              .panel::-webkit-scrollbar-thumb:hover {
                background: rgba(0, 0, 0, 0.2);
              }
              
              /* 修改浮动图标栏样式 */
              .floating-dock {
                position: fixed;
                left: 50%;
                bottom: 20px;
                transform: translateX(-50%) translateY(0);
                z-index: 9999;
                transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
              }
              
              .dock-hidden {
                transform: translateX(-50%) translateY(150%);
              }
              
              .icon-dock {
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                padding: 8px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
              }
              
              /* 添加鼠标悬停时的显示效果 */
              .floating-dock:hover {
                transform: translateX(-50%) translateY(0) !important;
              }
              
              .dock-items-container {
                display: flex;
                gap: 20px;
              }
              
              .dock-item {
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 8px;
                cursor: move;
                transition: transform 0.3s ease;
              }
              
              .dock-icon-wrapper {
                width: 40px;
                height: 40px;
                border-radius: 10px;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: all 0.3s ease;
              }
              
              .dock-icon {
                width: 20px;
                height: 20px;
                color: white;
              }
              
              .dock-label {
                font-size: 12px;
                color: #374151;
                font-weight: 500;
                opacity: 0;
                transition: opacity 0.3s ease;
                position: absolute;
                top: -25px;
                left: 50%;
                transform: translateX(-50%);
                background: rgba(0, 0, 0, 0.8);
                color: white;
                padding: 4px 8px;
                border-radius: 4px;
                white-space: nowrap;
              }
              
              /* 悬停效果 */
              .dock-item:hover {
                transform: translateY(-4px);
              }
              
              .dock-item:hover .dock-label {
                opacity: 1;
              }
              
              .dock-item:hover .dock-icon-wrapper {
                filter: brightness(1.1);
              }
              
              /* 拖拽时的样式 */
              .sortable-ghost {
                opacity: 0.5;
              }
              
              .sortable-drag {
                opacity: 0.9;
              }
              
              /* 确保面板内容不被遮挡 */
              .panel {
                margin-bottom: 80px; /* 为底部图标栏留出空间 */
              }
              
              /* 修改进度条样式 - 确保在整个页面居中 */
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
                animation: slideIn 0.3s ease;
              }
              
              .progress-steps {
                display: flex;
                justify-content: space-between;
                margin-bottom: 20px;
                position: relative;
              }
              
              .step {
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 8px;
                flex: 1;
                position: relative;
                opacity: 0.5;
                transition: all 0.5s ease;
              }
              
              .step.active {
                opacity: 1;
                animation: stepActive 0.5s ease;
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
                background: linear-gradient(
                  to right,
                  #e5e7eb 0%,
                  #e5e7eb 50%,
                  transparent 50%,
                  transparent 100%
                );
                background-size: 20px 2px;
                z-index: -1;
                animation: moveStripes 1s linear infinite;
              }
              
              .step.completed:not(:last-child)::after {
                background: linear-gradient(
                  to right,
                  #10a37f 0%,
                  #10a37f 50%,
                  rgba(16, 163, 127, 0.3) 50%,
                  rgba(16, 163, 127, 0.3) 100%
                );
                background-size: 20px 2px;
                animation: moveStripes 1s linear infinite;
              }
              
              @keyframes moveStripes {
                0% {
                  background-position: 0 0;
                }
                100% {
                  background-position: 20px 0;
                }
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
                transition: all 1s ease;
                position: relative;
                overflow: hidden;
              }
              
              .step.active .step-icon {
                animation: iconPulse 2s infinite;
              }
              
              .step.completed .step-icon {
                animation: iconComplete 1s ease;
              }
              
              .icon {
                width: 20px;
                height: 20px;
                color: currentColor;
                transition: all 0.3s ease;
              }
              
              .step.completed .icon {
                animation: iconSpin 0.5s ease;
              }
              
              .step-label {
                font-size: 14px;
                font-weight: 500;
                transition: all 0.3s ease;
              }
              
              .status-text {
                text-align: center;
                font-size: 14px;
                color: #374151;
                margin-top: 16px;
                animation: fadeIn 0.3s ease;
              }
              
              /* 动画关键帧 */
              @keyframes slideIn {
                from {
                  opacity: 0;
                  transform: translate(-50%, -60%);
                }
                to {
                  opacity: 1;
                  transform: translate(-50%, -50%);
                }
              }
              
              @keyframes stepActive {
                0% {
                  transform: scale(0.95);
                  opacity: 0.7;
                }
                50% {
                  transform: scale(1.05);
                  opacity: 0.9;
                }
                100% {
                  transform: scale(1);
                  opacity: 1;
                }
              }
              
              @keyframes iconPulse {
                0% {
                  box-shadow: 0 0 0 0 rgba(16, 163, 127, 0.4);
                }
                70% {
                  box-shadow: 0 0 0 10px rgba(16, 163, 127, 0);
                }
                100% {
                  box-shadow: 0 0 0 0 rgba(16, 163, 127, 0);
                }
              }
              
              @keyframes iconComplete {
                0% {
                  transform: scale(0.8);
                  opacity: 0.5;
                }
                50% {
                  transform: scale(1.2);
                  opacity: 0.8;
                }
                100% {
                  transform: scale(1);
                  opacity: 1;
                }
              }
              
              @keyframes iconSpin {
                from {
                  transform: rotate(-180deg);
                }
                to {
                  transform: rotate(0deg);
                }
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
              
              .step-detail {
                margin-top: 8px;
                padding: 8px;
                background: rgba(255, 255, 255, 0.9);
                border-radius: 6px;
                font-size: 0.9rem;
                max-width: 300px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
              }
              
              .file-info, .title-info, .qa-info, .complete-info {
                display: flex;
                flex-direction: column;
                gap: 4px;
              }
              
              .file-name {
                font-weight: 500;
                color: #10a37f;
              }
              
              .file-size {
                font-size: 0.8rem;
                color: #6b7280;
              }
              
              .title-count {
                color: #10a37f;
                font-weight: 500;
              }
              
              .current-title {
                display: flex;
                align-items: center;
                gap: 6px;
              }
              
              .title-level {
                padding: 2px 4px;
                background: #e5e7eb;
                border-radius: 4px;
                font-size: 0.8rem;
                color: #374151;
              }
              
              .title-text {
                flex: 1;
                overflow: hidden;
                text-overflow: ellipsis;
                white-space: nowrap;
              }
              
              .qa-progress {
                color: #10a37f;
                font-weight: 500;
              }
              
              .qa-preview {
                font-size: 0.8rem;
                color: #4b5563;
                max-height: 80px;
                overflow-y: auto;
              }
              
              .preview-question, .preview-answer {
                margin: 2px 0;
              }
              
              .complete-info {
                text-align: center;
              }
              
              .total-count {
                color: #10a37f;
                font-weight: 500;
              }
              
              .success-rate {
                color: #059669;
                font-size: 0.8rem;
              }
              
              /* 添加标题式 */
              .process-header {
                display: flex;
                align-items: center;
                gap: 12px;
                margin-bottom: 24px;
                padding-bottom: 16px;
                border-bottom: 1px solid #e5e7eb;
              }
              
              .factory-icon {
                width: 32px;
                height: 32px;
                color: #10a37f;
              }
              
              .process-header h2 {
                margin: 0;
                font-size: 1.5rem;
                color: #374151;
                font-weight: 600;
              }
              
              /* 优化进度条样式 */
              .progress-indicator {
                margin-top: 20px;
                padding: 0 20px;
              }
              
              .progress-bar {
                height: 8px;
                background: #e5e7eb;
                border-radius: 4px;
                overflow: hidden;
                position: relative;
              }
              
              .progress-fill {
                height: 100%;
                background: linear-gradient(90deg, #10a37f, #34d399);
                transition: width 0.3s ease;
                position: relative;
                border-radius: 4px;
              }
              
              .progress-fill::after {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: linear-gradient(
                  90deg,
                  rgba(255, 255, 255, 0) 0%,
                  rgba(255, 255, 255, 0.3) 50%,
                  rgba(255, 255, 255, 0) 100%
                );
                animation: shimmer 2s infinite;
              }
              
              .progress-percentage {
                text-align: center;
                margin-top: 8px;
                font-size: 14px;
                font-weight: 500;
                color: #10a37f;
              }
              
              /* 优化当前处理标题的显示 */
              .current-title {
                background: #f0fdf4;
                padding: 8px 12px;
                border-radius: 6px;
                margin-bottom: 8px;
                border: 1px solid #10a37f;
              }
              
              .title-badge {
                background: #10a37f;
                color: white;
                padding: 2px 6px;
                border-radius: 4px;
                font-size: 12px;
                margin-right: 8px;
              }
              
              .title-text {
                font-weight: 500;
                color: #10a37f;
              }
              
              .qa-count {
                font-size: 14px;
                color: #6b7280;
                margin-top: 4px;
              }
              
              @keyframes shimmer {
                0% {
                  transform: translateX(-100%);
                }
                100% {
                  transform: translateX(100%);
                }
              }
              </style>
              