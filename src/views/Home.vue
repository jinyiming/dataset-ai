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
                    <RightPanel 
                      :qaList="qaList" 
                      class="panel right-gradient"
                      @show-template-dialog="handleShowTemplateDialog"
                    />
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

                          <!-- 添加模板内容预览 -->
                          <div v-if="selectedTemplates.includes(template.id)" class="template-preview">
                            <div class="template-content">
                              <h4>模板结构</h4>
                              <pre class="json-preview">{{ formatJSON(template.content) }}</pre>
                            </div>

                            <div class="field-mapping">
                              <h4>字段映射</h4>
                              <div class="mapping-container">
                                <div v-for="field in getTemplateFields(template)" 
                                     :key="field.path"
                                     class="mapping-row">
                                  <div class="field-info">
                                    <span class="field-path">{{ field.path }}</span>
                                    <span class="field-value">当前值: {{ field.value }}</span>
                                  </div>
                                  <div class="mapping-control">
                                    <select v-model="fieldMapping[field.path]" class="field-select">
                                      <option value="">请选择映射字段</option>
                                      <option value="question">问题</option>
                                      <option value="answer">答案</option>
                                      <option value="custom">自定义值</option>
                                    </select>
                                    <input v-if="fieldMapping[field.path] === 'custom'"
                                           v-model="customValues[field.path]"
                                           :placeholder="'请输入' + field.path + '的值'"
                                           class="custom-input">
                                  </div>
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>

                      <div class="dialog-footer">
                        <button @click="previewDataset" class="preview-button">预览数据集</button>
                        <button @click="exportDataset" class="export-button">导出数据集</button>
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

                  <!-- 添加预览弹窗 -->
                  <div v-if="showPreview" class="preview-dialog">
                    <div class="preview-content">
                      <div class="preview-header">
                        <h3>数据集预览</h3>
                        <button @click="closePreview" class="close-button">×</button>
                      </div>
                      <div class="preview-body">
                        <pre class="json-preview">{{ formattedPreviewData }}</pre>
                      </div>
                    </div>
                  </div>
                </div>
              </template>
              
              <script setup>
              import { ref, onMounted, onUnmounted, onBeforeUnmount, computed } from 'vue'
              import draggable from 'vuedraggable'
              import LeftPanel from '@/components/LeftPanel.vue'
              import MiddlePanel from '@/components/MiddlePanel.vue'
              import RightPanel from '@/components/RightPanel.vue'
              import QADialog from '@/components/QADialog.vue'
              import Screensaver from '@/components/Screensaver.vue'
              import SettingsPage from '@/views/SettingsPage.vue'
              import axios from 'axios'
              
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
              
              const showTemplateDialog = ref(false)
              const showExportSuccess = ref(false)
              const templates = ref([])
              const selectedTemplates = ref([])
              const fieldMapping = ref({})
              const customValues = ref({})
              
              // 添加预览相关的状态
              const showPreview = ref(false)
              const previewData = ref(null)

              // 格式化预览数据
              const formattedPreviewData = computed(() => {
                return JSON.stringify(previewData.value, null, 2)
              })

              // 根据模板格式创建数据
              const createDataByTemplate = (template, qa) => {
                try {
                  // 解析模板内容
                  const templateContent = JSON.parse(template.content)
                  if (!Array.isArray(templateContent) || templateContent.length === 0) {
                    return null
                  }

                  // 使用第一个元素作为模板结构
                  const templateStructure = templateContent[0]
                  
                  // 创建一个新的对象，完全复制模板结构
                  const result = JSON.parse(JSON.stringify(templateStructure))

                  // 递归设置值的函数
                  const setValues = (obj, path = '') => {
                    for (const key in obj) {
                      const currentPath = path ? `${path}.${key}` : key
                      
                      if (Array.isArray(obj[key])) {
                        obj[key] = obj[key].map((item, index) => {
                          if (typeof item === 'object' && item !== null) {
                            return setValues(JSON.parse(JSON.stringify(item)), `${currentPath}[${index}]`)
                          }
                          return item
                        })
                      } else if (typeof obj[key] === 'object' && obj[key] !== null) {
                        obj[key] = setValues(JSON.parse(JSON.stringify(obj[key])), currentPath)
                      } else {
                        const mapping = fieldMapping.value[currentPath]
                        if (mapping === 'question') {
                          obj[key] = qa.question
                        } else if (mapping === 'answer') {
                          obj[key] = qa.answer
                        } else if (mapping === 'custom') {
                          obj[key] = customValues.value[currentPath] || obj[key]
                        }
                      }
                    }
                    return obj
                  }

                  return setValues(result)
                } catch (e) {
                  console.error('创建数据失败:', e)
                  return null
                }
              }

              // 预览数据集
              const previewDataset = () => {
                if (selectedTemplates.value.length === 0) {
                  alert('请至少选择一个模板')
                  return
                }

                try {
                  const template = templates.value.find(t => t.id === selectedTemplates.value[0])
                  const templateContent = JSON.parse(template.content)
                  const templateStructure = templateContent[0]  // 获取单个模板结构
                  
                  // 处理所有问答数据
                  const previewResult = qaList.value.map(qa => {
                    // 创建一个新的空对象，而不是复制模板结构
                    const mappedData = {}
                    
                    // 只处理顶层字段
                    Object.keys(templateStructure).forEach(key => {
                      const mapping = fieldMapping.value[key]
                      if (mapping === 'question') {
                        mappedData[key] = qa.question
                      } else if (mapping === 'answer') {
                        mappedData[key] = qa.answer
                      } else if (mapping === 'custom') {
                        mappedData[key] = customValues.value[key] || ''
                      } else {
                        mappedData[key] = templateStructure[key]  // 使用模板中的默认值
                      }
                    })
                    
                    return mappedData
                  })

                  previewData.value = previewResult
                  showPreview.value = true
                  
                  console.log('预览数据:', previewResult)
                } catch (error) {
                  console.error('预览失败:', error)
                  alert('预览失败，请检查数据格式')
                }
              }

              // 关闭预览
              const closePreview = () => {
                showPreview.value = false
                previewData.value = null
              }

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
                
                // 更新理详情
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

              // 格式化 JSON 显示
              const formatJSON = (content) => {
                try {
                  return JSON.stringify(JSON.parse(content), null, 2)
                } catch (e) {
                  console.error('JSON 格式化失败:', e)
                  return content
                }
              }

              // 在获取模板时添加日志
              const handleShowTemplateDialog = async () => {
                try {
                  const response = await axios.get('http://localhost:8000/flask/api/templates/qa_dataset')
                  if (response.data.templates) {
                    templates.value = response.data.templates
                    console.log('获取到的模板:', templates.value)  // 添加调试日志
                    showTemplateDialog.value = true
                  }
                } catch (error) {
                  console.error('获取模板失败:', error)
                  alert('获取模板失败，请稍后重试')
                }
              }

              const closeTemplateDialog = () => {
                showTemplateDialog.value = false
                selectedTemplates.value = []
                fieldMapping.value = {}
                customValues.value = {}
              }

              // 获取模板字段
              const getTemplateFields = (template) => {
                try {
                  const content = JSON.parse(template.content)
                  if (Array.isArray(content) && content.length > 0) {
                    // 只获取第一个对象的字段
                    const firstItem = content[0]
                    return Object.keys(firstItem).map(key => ({
                      path: key,
                      value: firstItem[key]
                    }))
                  }
                  return []
                } catch (e) {
                  console.error('解析模板内容失败:', e)
                  return []
                }
              }

              // 根据路径设置值
              const setValueByPath = (obj, path, value) => {
                const parts = path.split('.')
                let current = obj
                
                for (let i = 0; i < parts.length - 1; i++) {
                  const part = parts[i]
                  if (part.includes('[') && part.includes(']')) {
                    // 处理数组
                    const arrayName = part.split('[')[0]
                    const index = parseInt(part.split('[')[1].split(']')[0])
                    if (!current[arrayName]) current[arrayName] = []
                    if (!current[arrayName][index]) current[arrayName][index] = {}
                    current = current[arrayName][index]
                  } else {
                    // 处理对象
                    if (!current[part]) current[part] = {}
                    current = current[part]
                  }
                }
                
                const lastPart = parts[parts.length - 1]
                current[lastPart] = value
              }

              // 导出数据集
              const exportDataset = () => {
                if (selectedTemplates.value.length === 0) {
                  alert('请至少选择一个模板')
                  return
                }

                try {
                  const template = templates.value.find(t => t.id === selectedTemplates.value[0])
                  const templateContent = JSON.parse(template.content)
                  const templateStructure = templateContent[0]
                  
                  // 处理所有问答数据
                  const exportData = qaList.value.map(qa => {
                    // 创建一个新的空对象
                    const mappedData = {}
                    
                    // 只处理顶层字段
                    Object.keys(templateStructure).forEach(key => {
                      const mapping = fieldMapping.value[key]
                      if (mapping === 'question') {
                        mappedData[key] = qa.question
                      } else if (mapping === 'answer') {
                        mappedData[key] = qa.answer
                      } else if (mapping === 'custom') {
                        mappedData[key] = customValues.value[key] || ''
                      } else {
                        mappedData[key] = templateStructure[key]  // 使用模板中的默认值
                      }
                    })
                    
                    return mappedData
                  })

                  // 导出文件
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
                  
                  showExportSuccess.value = true
                  setTimeout(() => {
                    showExportSuccess.value = false
                  }, 3000)
                  
                  closeTemplateDialog()
                } catch (error) {
                  console.error('导出失败:', error)
                  alert('导出失败，请检查数据格式')
                }
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
              
              /* 优化度条样式 */
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
                animation: fadeIn 0.3s ease;
              }

              .dialog-content {
                background: white;
                border-radius: 16px;
                padding: 32px;
                width: 900px;
                max-height: 80vh;
                overflow-y: auto;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
                animation: slideUp 0.3s ease;
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
                display: flex;
                align-items: center;
                gap: 12px;
              }

              .dialog-header h3::before {
                content: '';
                width: 24px;
                height: 24px;
                background-image: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="%2310a37f"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4"/></svg>');
              }

              .template-list {
                display: flex;
                flex-direction: column;
                gap: 16px;
              }

              .template-item {
                background: #f9fafb;
                border-radius: 12px;
                padding: 16px;
                transition: all 0.3s ease;
              }

              .template-item:hover {
                background: #f0fdf4;
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(16, 163, 127, 0.1);
              }

              .template-header {
                display: flex;
                align-items: center;
                gap: 12px;
                margin-bottom: 16px;
              }

              .template-header input[type="checkbox"] {
                width: 20px;
                height: 20px;
                border: 2px solid #10a37f;
                border-radius: 4px;
                cursor: pointer;
              }

              .template-header label {
                font-size: 1.1rem;
                font-weight: 500;
                color: #374151;
              }

              .mapping-container {
                background: white;
                border-radius: 8px;
                padding: 20px;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
              }

              .field-title {
                font-weight: 600;
                color: #374151;
                margin-bottom: 12px;
              }

              .mapping-row {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 16px;
                padding: 12px;
                background: white;
                border: 1px solid #e5e7eb;
                border-radius: 6px;
                margin-bottom: 8px;
              }

              .field-path {
                font-weight: 500;
                color: #374151;
                font-family: monospace;
              }

              .field-value {
                font-size: 0.9rem;
                color: #6b7280;
              }

              .mapping-control {
                display: flex;
                align-items: center;
                gap: 16px;
              }

              .field-select {
                padding: 8px 12px;
                border: 1px solid #e5e7eb;
                border-radius: 6px;
                font-size: 0.9rem;
                color: #374151;
                background: white;
                cursor: pointer;
                transition: all 0.3s ease;
              }

              .field-select:hover {
                border-color: #10a37f;
              }

              .arrow {
                color: #10a37f;
                font-size: 1.2rem;
                animation: pulse 2s infinite;
              }

              .template-field {
                font-weight: 500;
                color: #374151;
                padding: 8px 12px;
                background: #e5e7eb;
                border-radius: 6px;
              }

              .custom-input {
                flex: 1;
                padding: 8px 12px;
                border: 1px solid #e5e7eb;
                border-radius: 6px;
                font-size: 0.9rem;
                transition: all 0.3s ease;
              }

              .custom-input:focus {
                outline: none;
                border-color: #10a37f;
                box-shadow: 0 0 0 2px rgba(16, 163, 127, 0.1);
              }

              .dialog-footer {
                margin-top: 24px;
                display: flex;
                justify-content: flex-end;
                gap: 12px;
              }

              .export-button {
                padding: 10px 20px;
                background: #10a37f;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 1rem;
                cursor: pointer;
                display: flex;
                align-items: center;
                gap: 8px;
                transition: all 0.3s ease;
              }

              .export-button:hover {
                background: #059669;
                transform: translateY(-1px);
              }

              .cancel-button {
                padding: 10px 20px;
                background: #f3f4f6;
                color: #374151;
                border: none;
                border-radius: 8px;
                font-size: 1rem;
                cursor: pointer;
                transition: all 0.3s ease;
              }

              .cancel-button:hover {
                background: #e5e7eb;
              }

              /* 动画 */
              @keyframes fadeIn {
                from {
                  opacity: 0;
                }
                to {
                  opacity: 1;
                }
              }

              @keyframes slideUp {
                from {
                  transform: translateY(20px);
                  opacity: 0;
                }
                to {
                  transform: translateY(0);
                  opacity: 1;
                }
              }

              @keyframes pulse {
                0% {
                  transform: scale(1);
                  opacity: 1;
                }
                50% {
                  transform: scale(1.1);
                  opacity: 0.7;
                }
                100% {
                  transform: scale(1);
                  opacity: 1;
                }
              }

              .preview-button {
                padding: 10px 20px;
                background: #6366F1;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 1rem;
                cursor: pointer;
                display: flex;
                align-items: center;
                gap: 8px;
                transition: all 0.3s ease;
              }

              .preview-button:hover {
                background: #4F46E5;
                transform: translateY(-1px);
              }

              .preview-dialog {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0, 0, 0, 0.5);
                display: flex;
                justify-content: center;
                align-items: center;
                z-index: 1001;
                animation: fadeIn 0.3s ease;
              }

              .preview-content {
                background: white;
                border-radius: 16px;
                width: 800px;
                max-height: 80vh;
                display: flex;
                flex-direction: column;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
                animation: slideUp 0.3s ease;
              }

              .preview-header {
                padding: 20px;
                border-bottom: 1px solid #e5e7eb;
                display: flex;
                justify-content: space-between;
                align-items: center;
              }

              .preview-header h3 {
                margin: 0;
                font-size: 1.2rem;
                color: #374151;
              }

              .preview-body {
                flex: 1;
                overflow-y: auto;
                padding: 20px;
              }

              .json-preview {
                margin: 0;
                padding: 16px;
                background: #1e1e1e;
                color: #d4d4d4;
                border-radius: 8px;
                font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
                font-size: 14px;
                line-height: 1.5;
                overflow-x: auto;
                white-space: pre-wrap;
              }

              .icon-preview {
                width: 16px;
                height: 16px;
                background-image: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="white"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>');
              }

              .field-path {
                font-weight: 600;
                color: #374151;
                font-family: monospace;
              }

              .field-value {
                font-size: 0.9rem;
                color: #6b7280;
                background: #f3f4f6;
                padding: 2px 6px;
                border-radius: 4px;
              }

              .field-type {
                font-size: 0.8rem;
                color: #9ca3af;
                font-style: italic;
              }

              .template-preview {
                margin-top: 16px;
                padding: 16px;
                background: #f9fafb;
                border-radius: 8px;
                border: 1px solid #e5e7eb;
              }

              .template-content {
                display: flex;
                flex-direction: column;
                gap: 16px;
              }

              .json-preview {
                margin: 0;
                padding: 12px;
                background: #1e1e1e;
                color: #d4d4d4;
                border-radius: 6px;
                font-family: monospace;
                font-size: 14px;
                line-height: 1.5;
                white-space: pre-wrap;
                overflow-x: auto;
              }

              .field-mapping {
                margin-top: 20px;
              }

              .mapping-row {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 16px;
                padding: 12px;
                background: white;
                border: 1px solid #e5e7eb;
                border-radius: 6px;
                margin-bottom: 8px;
              }

              .field-info {
                display: flex;
                flex-direction: column;
                gap: 4px;
              }

              .mapping-control {
                display: flex;
                align-items: center;
                gap: 16px;
              }

              .no-data {
                text-align: center;
                padding: 20px;
                color: #6b7280;
                font-style: italic;
              }

              .json-preview {
                margin: 0;
                padding: 16px;
                background: #1e1e1e;
                color: #d4d4d4;
                border-radius: 8px;
                font-family: monospace;
                font-size: 14px;
                line-height: 1.5;
                white-space: pre-wrap;
                overflow-x: auto;
              }
              </style>
              