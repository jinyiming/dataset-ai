<template>
                <div class="analysis-container">
                  <!-- 左侧筛选面板 -->
                  <div class="filter-panel">
                    <!-- 添加标题导航栏 -->
                    <div class="nav-header">
                      <div class="nav-title">
                        <svg class="nav-icon" viewBox="0 0 24 24">
                          <path d="M12 4C5.383 4 0 9.383 0 16v4h24v-4c0-6.617-5.383-12-12-12zm10 14H2v-2c0-5.514 4.486-10 10-10s10 4.486 10 10v2z"/>
                          <path d="M12 6c-5.514 0-10 4.486-10 10v2h20v-2c0-5.514-4.486-10-10-10zm8 10H4v-.411C4.164 11.014 7.674 8 12 8s7.836 3.014 8 7.589V16z"/>
                        </svg>
                        <span>数据统计分析</span>
                      </div>
                      <div class="nav-subtitle">Data Statistics & Analysis</div>
                    </div>
              
                    <!-- 原有的筛选内容 -->
                    <div class="filter-content">
                      <!-- 文件类型筛选 -->
                      <div class="filter-section">
                        <div class="section-header" @click="toggleSection('type')">
                          <div class="header-left">
                            <svg class="icon" viewBox="0 0 24 24">
                              <path d="M14 2H6a2 2 0 0 0-2 2v16c0 1.1.9 2 2 2h12a2 2 0 0 0 2-2V8l-6-6z"/>
                            </svg>
                            <h3>文件类型</h3>
                          </div>
                          <svg class="arrow-icon" :class="{ 'rotated': expandedSections.type }" viewBox="0 0 24 24">
                            <path d="M7 10l5 5 5-5z"/>
                          </svg>
                        </div>
                        <div class="section-content" v-show="expandedSections.type">
                          <div class="radio-group">
                            <label v-for="type in fileTypes" 
                                   :key="type.value" 
                                   class="radio-label">
                              <input 
                                type="radio" 
                                v-model="selectedType" 
                                :value="type.value"
                                class="radio-input"
                              >
                              <span class="radio-text">{{ type.label }}</span>
                            </label>
                          </div>
                        </div>
                      </div>
              
                      <!-- 系统编码筛选 -->
                      <div class="filter-section">
                        <div class="section-header" @click="toggleSection('system')">
                          <div class="header-left">
                            <svg class="icon" viewBox="0 0 24 24">
                              <path d="M12 7V3H2v18h20V7H12zM6 19H4v-2h2v2z"/>
                            </svg>
                            <h3>系统编码</h3>
                          </div>
                          <svg class="arrow-icon" :class="{ 'rotated': expandedSections.system }" viewBox="0 0 24 24">
                            <path d="M7 10l5 5 5-5z"/>
                          </svg>
                        </div>
                        <div class="section-content" v-show="expandedSections.system">
                          <div class="radio-group">
                            <label v-for="system in systemCodes" 
                                   :key="system.value" 
                                   class="radio-label">
                              <input 
                                type="radio" 
                                v-model="selectedSystem" 
                                :value="system.value"
                                class="radio-input"
                              >
                              <span class="radio-text">{{ system.label }}</span>
                            </label>
                          </div>
                        </div>
                      </div>
              
                      <!-- 文件格式筛选 -->
                      <div class="filter-section">
                        <div class="section-header" @click="toggleSection('format')">
                          <div class="header-left">
                            <svg class="icon" viewBox="0 0 24 24">
                              <path d="M14 2H6a2 2 0 0 0-2 2v16c0 1.1.9 2 2 2h12a2 2 0 0 0 2-2V8l-6-6z"/>
                            </svg>
                            <h3>文件格式</h3>
                          </div>
                          <svg class="arrow-icon" :class="{ 'rotated': expandedSections.format }" viewBox="0 0 24 24">
                            <path d="M7 10l5 5 5-5z"/>
                          </svg>
                        </div>
                        <div class="section-content" v-show="expandedSections.format">
                          <div class="radio-group">
                            <label v-for="format in fileFormats" 
                                   :key="format.value" 
                                   class="radio-label">
                              <input 
                                type="radio" 
                                v-model="selectedFormat" 
                                :value="format.value"
                                class="radio-input"
                              >
                              <span class="radio-text">{{ format.label }}</span>
                            </label>
                          </div>
                        </div>
                      </div>
              
                      <!-- 模块筛选 -->
                      <div class="filter-section">
                        <div class="section-header" @click="toggleSection('module')">
                          <div class="header-left">
                            <svg class="icon" viewBox="0 0 24 24">
                              <path d="M12 7V3H2v18h20V7H12zM6 19H4v-2h2v2z"/>
                            </svg>
                            <h3>模块</h3>
                          </div>
                          <svg class="arrow-icon" :class="{ 'rotated': expandedSections.module }" viewBox="0 0 24 24">
                            <path d="M7 10l5 5 5-5z"/>
                          </svg>
                        </div>
                        <div class="section-content" v-show="expandedSections.module">
                          <div class="radio-group">
                            <label v-for="module in modules" 
                                   :key="module.value" 
                                   class="radio-label">
                              <input 
                                type="radio" 
                                v-model="selectedModule" 
                                :value="module.value"
                                class="radio-input"
                              >
                              <span class="radio-text">{{ module.label }}</span>
                            </label>
                          </div>
                        </div>
                      </div>
              
                      <div class="filter-section">
                        <h3>时间范围</h3>
                        <div class="date-range">
                          <div class="date-picker">
                            <label>开始日期</label>
                            <input 
                              type="date" 
                              v-model="dateRange.start"
                              :max="dateRange.end"
                              class="date-input"
                            >
                          </div>
                          <div class="date-picker">
                            <label>结束日期</label>
                            <input 
                              type="date" 
                              v-model="dateRange.end"
                              :min="dateRange.start"
                              class="date-input"
                            >
                          </div>
                        </div>
                        <!-- 快捷选择 -->
                        <div class="quick-select">
                          <button 
                            v-for="period in timePeriods" 
                            :key="period.value"
                            @click="selectPeriod(period.value)"
                            :class="['quick-select-btn', { active: period.value === selectedPeriod }]"
                          >
                            {{ period.label }}
                          </button>
                        </div>
                      </div>
              
                      <div class="filter-actions">
                        <button @click="applyFilters" class="apply-button">应用筛选</button>
                        <button @click="resetFilters" class="reset-button">重置</button>
                      </div>
                    </div>
                  </div>
              
                  <!-- 添加加载遮罩 -->
                  <div v-if="loading" class="loading-overlay">
                    <div class="loading-spinner"></div>
                  </div>
              
                  <!-- 右侧图表展示 -->
                  <div class="chart-content">
                    <div class="stats-cards">
                      <div class="stats-card">
                        <div class="stats-title">文件总数</div>
                        <div class="stats-value">{{ totalFiles }}</div>
                      </div>
                      <div class="stats-card">
                        <div class="stats-title">总存储空间</div>
                        <div class="stats-value">{{ formatFileSize(totalSize) }}</div>
                      </div>
                      <div class="stats-card">
                        <div class="stats-title">本月新增</div>
                        <div class="stats-value">{{ monthlyNew }}</div>
                      </div>
                    </div>
              
                    <div class="charts-container">
                      <div class="chart-row">
                        <!-- 文件类型分布 -->
                        <div class="chart-item">
                          <div class="chart-header">
                            <h3>文件类型分布</h3>
                            <div class="chart-actions">
                              <div class="chart-type-selector">
                                <button 
                                  v-for="type in chartTypes" 
                                  :key="type.value"
                                  :class="['type-btn', { active: currentChartType.type === type.value }]"
                                  @click="changeChartType('type', type.value)"
                                >
                                  {{ type.label }}
                                </button>
                              </div>
                              <div class="chart-operations">
                                <button class="op-btn" @click="toggleFullscreen('type')" title="全屏预览">
                                  <i class="icon-fullscreen">
                                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor">
                                      <path d="M4 4h16v16H4z M4 9V4h5 M4 15v5h5 M20 9V4h-5 M20 15v5h-5" stroke-width="2"/>
                                    </svg>
                                  </i>
                                </button>
                                <button class="op-btn" @click="printChart('type')" title="打印">
                                  <i class="icon-print">
                                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor">
                                      <path d="M6 9V2h12v7 M6 18H4v-9h16v9h-2 M6 14h12v8H6z" stroke-width="2"/>
                                    </svg>
                                  </i>
                                </button>
                                <button class="op-btn" @click="toggleDataLimit('type')" title="数据限制">
                                  <i class="icon-filter">
                                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor">
                                      <path d="M3 4h18l-7 8v8l-4-3v-5z" stroke-width="2"/>
                                    </svg>
                                  </i>
                                </button>
                              </div>
                            </div>
                          </div>
                          <div class="chart-wrapper">
                            <div v-if="loading" class="chart-loading">加载中...</div>
                            <div ref="typeChartRef" class="chart"></div>
                          </div>
                        </div>
                        
                        <!-- 系统使用情况 -->
                        <div class="chart-item">
                          <div class="chart-header">
                            <h3>系统使用情况</h3>
                            <div class="chart-actions">
                              <div class="chart-type-selector">
                                <button 
                                  v-for="type in chartTypes" 
                                  :key="type.value"
                                  :class="['type-btn', { active: currentChartType.system === type.value }]"
                                  @click="changeChartType('system', type.value)"
                                >
                                  {{ type.label }}
                                </button>
                              </div>
                              <div class="chart-operations">
                                <button class="op-btn" @click="toggleFullscreen('system')" title="全屏预览">
                                  <i class="icon-fullscreen">
                                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor">
                                      <path d="M4 4h16v16H4z M4 9V4h5 M4 15v5h5 M20 9V4h-5 M20 15v5h-5" stroke-width="2"/>
                                    </svg>
                                  </i>
                                </button>
                                <button class="op-btn" @click="printChart('system')" title="打印">
                                  <i class="icon-print">
                                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor">
                                      <path d="M6 9V2h12v7 M6 18H4v-9h16v9h-2 M6 14h12v8H6z" stroke-width="2"/>
                                    </svg>
                                  </i>
                                </button>
                                <button class="op-btn" @click="toggleDataLimit('system')" title="数据限制">
                                  <i class="icon-filter">
                                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor">
                                      <path d="M3 4h18l-7 8v8l-4-3v-5z" stroke-width="2"/>
                                    </svg>
                                  </i>
                                </button>
                              </div>
                            </div>
                          </div>
                          <div class="chart-wrapper">
                            <div v-if="loading" class="chart-loading">加载中...</div>
                            <div ref="systemChartRef" class="chart"></div>
                          </div>
                        </div>
                      </div>
              
                      <div class="chart-row">
                        <!-- 文件格式分布 -->
                        <div class="chart-item">
                          <div class="chart-header">
                            <h3>文件格式分布</h3>
                            <div class="chart-actions">
                              <div class="chart-type-selector">
                                <button 
                                  v-for="type in chartTypes" 
                                  :key="type.value"
                                  :class="['type-btn', { active: currentChartType.format === type.value }]"
                                  @click="changeChartType('format', type.value)"
                                >
                                  {{ type.label }}
                                </button>
                              </div>
                              <div class="chart-operations">
                                <button class="op-btn" @click="toggleFullscreen('format')" title="全屏预览">
                                  <i class="icon-fullscreen">
                                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor">
                                      <path d="M4 4h16v16H4z M4 9V4h5 M4 15v5h5 M20 9V4h-5 M20 15v5h-5" stroke-width="2"/>
                                    </svg>
                                  </i>
                                </button>
                                <button class="op-btn" @click="printChart('format')" title="打印">
                                  <i class="icon-print">
                                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor">
                                      <path d="M6 9V2h12v7 M6 18H4v-9h16v9h-2 M6 14h12v8H6z" stroke-width="2"/>
                                    </svg>
                                  </i>
                                </button>
                                <button class="op-btn" @click="toggleDataLimit('format')" title="数据限制">
                                  <i class="icon-filter">
                                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor">
                                      <path d="M3 4h18l-7 8v8l-4-3v-5z" stroke-width="2"/>
                                    </svg>
                                  </i>
                                </button>
                              </div>
                            </div>
                          </div>
                          <div class="chart-wrapper">
                            <div v-if="loading" class="chart-loading">加载中...</div>
                            <div ref="formatChartRef" class="chart"></div>
                          </div>
                        </div>
                        
                        <!-- 模块使用趋势 -->
                        <div class="chart-item">
                          <div class="chart-header">
                            <h3>模块使用趋势</h3>
                            <div class="chart-actions">
                              <div class="chart-type-selector">
                                <button 
                                  v-for="type in chartTypes" 
                                  :key="type.value"
                                  :class="['type-btn', { active: currentChartType.module === type.value }]"
                                  @click="changeChartType('module', type.value)"
                                >
                                  {{ type.label }}
                                </button>
                              </div>
                              <div class="chart-operations">
                                <button class="op-btn" @click="toggleFullscreen('module')" title="全屏预览">
                                  <i class="icon-fullscreen">
                                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor">
                                      <path d="M4 4h16v16H4z M4 9V4h5 M4 15v5h5 M20 9V4h-5 M20 15v5h-5" stroke-width="2"/>
                                    </svg>
                                  </i>
                                </button>
                                <button class="op-btn" @click="printChart('module')" title="打印">
                                  <i class="icon-print">
                                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor">
                                      <path d="M6 9V2h12v7 M6 18H4v-9h16v9h-2 M6 14h12v8H6z" stroke-width="2"/>
                                    </svg>
                                  </i>
                                </button>
                                <button class="op-btn" @click="toggleDataLimit('module')" title="数据限制">
                                  <i class="icon-filter">
                                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor">
                                      <path d="M3 4h18l-7 8v8l-4-3v-5z" stroke-width="2"/>
                                    </svg>
                                  </i>
                                </button>
                              </div>
                            </div>
                          </div>
                          <div class="chart-wrapper">
                            <div v-if="loading" class="chart-loading">加载中...</div>
                            <div ref="moduleChartRef" class="chart"></div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
              
                  <!-- 全预览弹窗 -->
                  <div v-if="fullscreenChart" class="fullscreen-dialog">
                    <div class="fullscreen-content">
                      <div class="fullscreen-header">
                        <h3>{{ getChartTitle(fullscreenChart) }}</h3>
                        <button @click="closeFullscreen" class="close-btn">×</button>
                      </div>
                      <div class="fullscreen-body">
                        <div :ref="fullscreenChart + 'FullscreenRef'" class="fullscreen-chart"></div>
                      </div>
                    </div>
                  </div>
                </div>
              </template>
              
              <script setup>
              import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
              import * as echarts from 'echarts'
              import axios from 'axios'
              
              // 筛选条件
              const selectedType = ref('')
              const selectedSystem = ref('')
              const selectedFormat = ref('')
              const selectedModule = ref('')
              
              // 统计数据
              const totalFiles = ref(0)
              const totalSize = ref(0)
              const monthlyNew = ref(0)
              
              // 图表实例
              let typeChart = null
              let systemChart = null
              let formatChart = null
              let moduleChart = null
              
              // 添加筛选选项数据
              const fileTypes = ref([
                { label: '正文', value: 'main_doc', icon: 'file-text' },
                { label: '办理单', value: 'dealForm', icon: 'file-form' },
                { label: '附件', value: 'attachment', icon: 'file-attachment' },
                { label: '版式文件', value: 'main_ofd', icon: 'file-signature' },
                { label: '手写意见', value: 'handle', icon: 'file-signature' },
                { label: '批注文件', value: 'notation', icon: 'file-signature' },
                { label: '公文交换表单', value: 'exDealForm', icon: 'file-signature' },
                { label: '文件分发', value: 'main_trace', icon: 'file-signature' }
              ])
              
              const systemCodes = ref([
                { label: '市政府', value: 'SZF', icon: 'building' },
                { label: '档案系统', value: 'ARC', icon: 'archive' },
                { label: '信访系统', value: 'PET', icon: 'mail' }
              ])
              
              const fileFormats = ref([
                { label: 'Word文档', value: 'doc,docx', icon: 'file-word' },
                { label: 'Excel表格', value: 'xls,xlsx', icon: 'file-excel' },
                { label: 'PDF文件', value: 'pdf', icon: 'file-pdf' },
                { label: '图片文件', value: 'jpg,png,gif', icon: 'image' }
              ])
              
              const modules = ref([
                { label: '收文管理', value: 'RECEIVE,receival', icon: 'inbox' },
                { label: '发文管理', value: 'DISPATCH,dispatch', icon: 'send' },
                { label: '公文交换', value: 'EX,ex', icon: 'edit' }
              ])
              
              // 添加时间相关的状态
              const dateRange = ref({
                start: '',
                end: new Date().toISOString().split('T')[0]  // 默认结束日期为今天
              })
              
              const selectedPeriod = ref('')
              
              // 时间段快捷选择
              const timePeriods = [
                { label: '最近7天', value: '7days' },
                { label: '最近30天', value: '30days' },
                { label: '最近3个月', value: '3months' },
                { label: '最近半年', value: '6months' },
                { label: '最近一年', value: '1year' }
              ]
              
              // 添加加载状态
              const loading = ref(false)
              
              // 快捷选择处理函数
              const selectPeriod = (period) => {
                selectedPeriod.value = period
                const end = new Date()
                let start = new Date()
              
                switch (period) {
                  case '7days':
                    start.setDate(end.getDate() - 7)
                    break
                  case '30days':
                    start.setDate(end.getDate() - 30)
                    break
                  case '3months':
                    start.setMonth(end.getMonth() - 3)
                    break
                  case '6months':
                    start.setMonth(end.getMonth() - 6)
                    break
                  case '1year':
                    start.setFullYear(end.getFullYear() - 1)
                    break
                }
              
                dateRange.value = {
                  start: start.toISOString().split('T')[0],
                  end: end.toISOString().split('T')[0]
                }
              
                // 自动触发数据刷新
                fetchData()
              }
              
              // 获取数据并更新图表
              const fetchData = async () => {
                loading.value = true
                try {
                  console.log('Fetching data...')
                  const response = await axios.get('http://localhost:8000/flask/api/file-stats', {
                    params: {
                      fileType: selectedType.value,
                      system: selectedSystem.value,
                      format: selectedFormat.value,
                      module: selectedModule.value,
                      startDate: dateRange.value.start,
                      endDate: dateRange.value.end
                    }
                  })
                  
                  console.log('Received data:', response.data)
                  const data = response.data
                  if (data) {
                    totalFiles.value = data.totalFiles
                    totalSize.value = data.totalSize
                    monthlyNew.value = data.monthlyNew
              
                    // 重新初始化图表
                    initCharts()
                    // 更新图表数据
                    updateCharts(data)
                  }
                } catch (error) {
                  console.error('获取数据失败:', error)
                } finally {
                  loading.value = false
                }
              }
              
              // 监听日期变化
              watch([() => dateRange.value.start, () => dateRange.value.end], () => {
                selectedPeriod.value = ''  // 清除快捷选择的激活状态
                fetchData()  // 触发数据刷新
              })
              
              // 修改图表引用
              const typeChartRef = ref(null)
              const systemChartRef = ref(null)
              const formatChartRef = ref(null)
              const moduleChartRef = ref(null)
              
              // 修改初始化图表函数
              const initCharts = () => {
                // 销旧的实例
                if (typeChart) typeChart.dispose()
                if (systemChart) systemChart.dispose()
                if (formatChart) formatChart.dispose()
                if (moduleChart) moduleChart.dispose()
              
                // 创建新的实例
                if (typeChartRef.value) {
                  typeChart = echarts.init(typeChartRef.value)
                  console.log('typeChart initialized')
                }
                if (systemChartRef.value) {
                  systemChart = echarts.init(systemChartRef.value)
                  console.log('systemChart initialized')
                }
                if (formatChartRef.value) {
                  formatChart = echarts.init(formatChartRef.value)
                  console.log('formatChart initialized')
                }
                if (moduleChartRef.value) {
                  moduleChart = echarts.init(moduleChartRef.value)
                  console.log('moduleChart initialized')
                }
              }
              
              // 修改图表类型状态
              const currentChartType = ref({
                type: 'pie',
                system: 'bar',
                format: 'pie',
                module: 'line'
              })
              
              // 图表类型选项
              const chartTypes = [
                { label: '饼图', value: 'pie' },
                { label: '柱状图', value: 'bar' },
                { label: '折线图', value: 'line' },
                { label: '散点图', value: 'scatter' },
                { label: '热力图', value: 'heatmap' }
              ]
              
              // 修改切换图表类型函数
              const changeChartType = (chart, type) => {
                currentChartType.value[chart] = type
                if (lastData.value) {
                  // 根据不同的图表类型更新配置
                  const chartConfigs = {
                    pie: {
                      series: [{
                        type: 'pie',
                        radius: '60%',
                        label: {
                          show: true,
                          formatter: '{b}: {c} ({d}%)'
                        }
                      }]
                    },
                    bar: {
                      xAxis: {
                        type: 'category',
                        axisLabel: { rotate: 30 }
                      },
                      yAxis: {
                        type: 'value'
                      },
                      series: [{
                        type: 'bar',
                        barWidth: '40%'
                      }]
                    },
                    line: {
                      xAxis: {
                        type: 'category',
                        boundaryGap: false
                      },
                      yAxis: {
                        type: 'value'
                      },
                      series: [{
                        type: 'line',
                        smooth: true,
                        areaStyle: { opacity: 0.1 }
                      }]
                    },
                    scatter: {
                      xAxis: {
                        type: 'category'
                      },
                      yAxis: {
                        type: 'value'
                      },
                      series: [{
                        type: 'scatter',
                        symbolSize: 10
                      }]
                    }
                  }
              
                  // 获取对应的图表实例和数
                  const chartInstances = {
                    type: typeChart,
                    system: systemChart,
                    format: formatChart,
                    module: moduleChart
                  }
              
                  const chartInstance = chartInstances[chart]
                  if (chartInstance) {
                    const baseOption = {
                      title: chartInstance.getOption().title,
                      tooltip: {
                        trigger: type === 'pie' ? 'item' : 'axis',
                        formatter: type === 'pie' ? '{b}: {c} ({d}%)' : '{b}: {c}'
                      },
                      legend: {
                        orient: type === 'pie' ? 'vertical' : 'horizontal',
                        left: type === 'pie' ? 'left' : 'center',
                        top: type === 'pie' ? 'center' : 'bottom',
                        type: 'scroll'
                      },
                      ...chartConfigs[type]
                    }
              
                    // 根据图表类型处理数据
                    const data = lastData.value
                    if (type === 'pie') {
                      baseOption.series[0].data = data[`${chart}Distribution`] || data[`${chart}Stats`]
                    } else {
                      const chartData = data[`${chart}Distribution`] || data[`${chart}Stats`]
                      baseOption.xAxis.data = chartData.map(item => item.name)
                      baseOption.series[0].data = chartData.map(item => item.value)
                    }
              
                    // 设置新的配置
                    chartInstance.setOption(baseOption, true)
                  }
                }
              }
              
              // 缓存最后一次的数据
              const lastData = ref(null)
              
              // 合并后的 updateCharts 函数
              const updateCharts = (data) => {
                lastData.value = data
              
                // 处理数据限制
                const typeData = processChartData(data.typeDistribution, dataLimits.value.type)
                const systemData = processChartData(data.systemStats, dataLimits.value.system)
                const formatData = processChartData(data.formatDistribution, dataLimits.value.format)
              
                // 文件类型分布图
                if (typeChart) {
                  const typeOption = {
                    title: {
                      text: '文件类型分布',
                      left: 'center'
                    },
                    tooltip: {
                      trigger: currentChartType.value.type === 'pie' ? 'item' : 'axis',
                      formatter: currentChartType.value.type === 'pie' ? '{b}: {c} ({d}%)' : '{b}: {c}'
                    },
                    legend: {
                      orient: 'vertical',
                      left: 'left',
                      type: 'scroll'
                    },
                    xAxis: currentChartType.value.type !== 'pie' ? {
                      type: 'category',
                      data: typeData.map(item => item.name),
                      axisLabel: { rotate: 30 }
                    } : undefined,
                    yAxis: currentChartType.value.type !== 'pie' ? {
                      type: 'value'
                    } : undefined,
                    series: [{
                      name: '文件类型',
                      type: currentChartType.value.type,
                      data: currentChartType.value.type === 'pie' ? 
                        typeData : 
                        typeData.map(item => item.value),
                      radius: currentChartType.value.type === 'pie' ? '60%' : undefined,
                      emphasis: {
                        itemStyle: {
                          shadowBlur: 10,
                          shadowOffsetX: 0,
                          shadowColor: 'rgba(0, 0, 0, 0.5)'
                        }
                      }
                    }]
                  }
                  typeChart.setOption(typeOption)
                }
              
                // 系统使用情况
                if (systemChart) {
                  const systemOption = {
                    title: {
                      text: '系统使用情况',
                      left: 'center'
                    },
                    tooltip: {
                      trigger: 'axis',
                      axisPointer: {
                        type: 'shadow'
                      }
                    },
                    grid: {
                      left: '3%',
                      right: '4%',
                      bottom: '3%',
                      containLabel: true
                    },
                    xAxis: {
                      type: 'category',
                      data: systemData.map(item => item.name),
                      axisLabel: {
                        interval: 0,
                        rotate: 30
                      }
                    },
                    yAxis: {
                      type: 'value'
                    },
                    series: [{
                      name: '文件数量',
                      type: currentChartType.value.system,
                      data: systemData.map(item => item.value),
                      barWidth: '40%',
                      itemStyle: {
                        color: '#6366F1'
                      }
                    }]
                  }
                  systemChart.setOption(systemOption)
                }
              
                // 文件格式分布
                if (formatChart) {
                  const formatOption = {
                    title: {
                      text: '文件格式分布',
                      left: 'center'
                    },
                    tooltip: {
                      trigger: 'item',
                      formatter: '{b}: {c} ({d}%)'
                    },
                    legend: {
                      orient: 'vertical',
                      left: 'left',
                      type: 'scroll'
                    },
                    series: [{
                      name: '文件格式',
                      type: currentChartType.value.format,
                      data: formatData,
                      radius: currentChartType.value.format === 'pie' ? ['40%', '70%'] : undefined,
                      itemStyle: {
                        borderRadius: 10,
                        borderColor: '#fff',
                        borderWidth: 2
                      }
                    }]
                  }
                  formatChart.setOption(formatOption)
                }
              
                // 模块使用趋势
                if (moduleChart) {
                  const moduleOption = {
                    title: {
                      text: '模块使用统计',
                      left: 'center'
                    },
                    tooltip: {
                      trigger: currentChartType.value.module === 'pie' ? 'item' : 'axis',
                      formatter: currentChartType.value.module === 'pie' ? 
                        '{b}: {c} ({d}%)' : 
                        '{b}: {c}'
                    },
                    legend: {
                      type: 'scroll',
                      orient: currentChartType.value.module === 'pie' ? 'vertical' : 'horizontal',
                      left: currentChartType.value.module === 'pie' ? 'left' : 'center',
                      bottom: currentChartType.value.module === 'pie' ? undefined : 10
                    },
                    series: [{
                      name: '模块使用量',
                      type: currentChartType.value.module,
                      radius: currentChartType.value.module === 'pie' ? '60%' : undefined,
                      data: data.moduleStats,
                      label: {
                        show: true,
                        formatter: currentChartType.value.module === 'pie' ? 
                          '{b}: {c}' : 
                          '{c}'
                      },
                      emphasis: {
                        focus: 'series',
                        itemStyle: {
                          shadowBlur: 10,
                          shadowOffsetX: 0,
                          shadowColor: 'rgba(0, 0, 0, 0.5)'
                        }
                      }
                    }]
                  }
              
                  // 添加坐标轴配置（非饼图时）
                  if (currentChartType.value.module !== 'pie') {
                    moduleOption.xAxis = {
                      type: 'category',
                      data: data.moduleStats.map(item => item.name),
                      axisLabel: { rotate: 30 }
                    }
                    moduleOption.yAxis = {
                      type: 'value',
                      name: '使用次数'
                    }
                  }
              
                  moduleChart.setOption(moduleOption)
                }
              }
              
              // 格式化文件大小
              const formatFileSize = (bytes) => {
                if (bytes === 0) return '0 B'
                const k = 1024
                const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
                const i = Math.floor(Math.log(bytes) / Math.log(k))
                return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
              }
              
              // 应用筛选
              const applyFilters = () => {
                loading.value = true
                fetchData()
              }
              
              // 重置筛选
              const resetFilters = () => {
                selectedType.value = ''
                selectedSystem.value = ''
                selectedFormat.value = ''
                selectedModule.value = ''
                fetchData()
              }
              
              // 添加自动刷新功能
              let refreshTimer = null
              
              onMounted(() => {
                console.log('Component mounted')
                // 使用 nextTick 确保 DOM 已渲染
                nextTick(() => {
                  console.log('DOM updated')
                  initCharts()
                  fetchData()
                })
              })
              
              onUnmounted(() => {
                // 清定时器
                if (refreshTimer) {
                  clearInterval(refreshTimer)
                }
                // 销毁图表
                disposeCharts()
              })
              
              // 监听窗口大小变化
              const handleResize = () => {
                typeChart?.resize()
                systemChart?.resize()
                formatChart?.resize()
                moduleChart?.resize()
              }
              
              window.addEventListener('resize', handleResize)
              
              // 组件卸载时清理
              onUnmounted(() => {
                window.removeEventListener('resize', handleResize)
                typeChart?.dispose()
                systemChart?.dispose()
                formatChart?.dispose()
                moduleChart?.dispose()
              })
              
              // 数据限制状态
              const dataLimits = ref({
                type: 10,
                system: 10,
                format: 10,
                module: 10
              })
              
              // 全屏状态
              const fullscreenChart = ref(null)
              let fullscreenInstance = null
              
              // 切换全屏显示
              const toggleFullscreen = (chartKey) => {
                fullscreenChart.value = chartKey
                nextTick(() => {
                  const dom = document.querySelector(`[ref="${chartKey}FullscreenRef"]`)
                  if (dom) {
                    fullscreenInstance = echarts.init(dom)
                    const sourceChart = chartInstances[chartKey]
                    if (sourceChart) {
                      fullscreenInstance.setOption(sourceChart.getOption())
                    }
                  }
                })
              }
              
              // 关闭全屏
              const closeFullscreen = () => {
                if (fullscreenInstance) {
                  fullscreenInstance.dispose()
                }
                fullscreenChart.value = null
              }
              
              // 打印图表
              const printChart = (chartKey) => {
                const chart = chartInstances[chartKey]
                if (chart) {
                  const img = new Image()
                  img.src = chart.getDataURL()
                  const printWindow = window.open('', '_blank')
                  const htmlContent = 
                    '<html>' +
                    '<head>' +
                    '<title>打印图表</title>' +
                    '<style>' +
                    'body { margin: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }' +
                    'img { max-width: 100%; height: auto; }' +
                    '</style>' +
                    '</head>' +
                    '<body>' +
                    '<img src="' + img.src + '" />' +
                    '<script>' +
                    'window.onload = function() { window.print(); window.close(); }' +
                    '<\/script>' +
                    '<\/body>' +
                    '<\/html>'
                  
                  printWindow.document.write(htmlContent)
                  printWindow.document.close()
                }
              }
              
              // 切换数据限制
              const toggleDataLimit = (chartKey) => {
                const limits = [10, 20, 50, 0]  // 0 表示无限制
                const currentLimit = dataLimits.value[chartKey]
                const nextIndex = (limits.indexOf(currentLimit) + 1) % limits.length
                dataLimits.value[chartKey] = limits[nextIndex]
                updateCharts(lastData.value)
              }
              
              // 修改数据处理函数
              const processChartData = (data, limit) => {
                if (!limit || limit === 0) return data
                return data.slice(0, limit).sort((a, b) => b.value - a.value)
              }
              
              // 修改点击外部关闭下拉框的处理
              const handleClickOutside = (e) => {
                try {
                  const dropdownSelects = document.querySelectorAll('.dropdown-select')
                  dropdownSelects.forEach(dropdown => {
                    if (!dropdown.contains(e.target)) {
                      const type = dropdown.getAttribute('data-type')
                      if (type && dropdowns.value[type]) {
                        dropdowns.value[type] = false
                      }
                    }
                  })
                } catch (error) {
                  console.error('处理点击事件时出错:', error)
                }
              }
              
              // 修改下拉框状态管理
              const dropdowns = ref({
                type: false,
                system: false,
                format: false,
                module: false
              })
              
              // 修改切换下拉框的处理
              const toggleDropdown = (type) => {
                try {
                  Object.keys(dropdowns.value).forEach(key => {
                    if (key !== type) {
                      dropdowns.value[key] = false
                    }
                  })
                  dropdowns.value[type] = !dropdowns.value[type]
                  if (dropdowns.value[type]) {
                    updateDropdownPosition(type)
                  }
                } catch (error) {
                  console.error('切换下拉框时出错:', error)
                }
              }
              
              // 添加下拉框位置计算
              const updateDropdownPosition = (type) => {
                nextTick(() => {
                  const trigger = document.querySelector(`[data-type="${type}"] .select-header`)
                  const dropdown = document.querySelector(`[data-type="${type}"] .select-options`)
                  if (trigger && dropdown) {
                    const rect = trigger.getBoundingClientRect()
                    dropdown.style.left = `${rect.left}px`
                    dropdown.style.top = `${rect.bottom + 2}px`
                    dropdown.style.width = `${rect.width}px`
                  }
                })
              }
              
              // 监听窗口大小变化，更新下拉框位置
              window.addEventListener('resize', () => {
                Object.keys(dropdowns.value).forEach(type => {
                  if (dropdowns.value[type]) {
                    updateDropdownPosition(type)
                  }
                })
              })
              
              onMounted(() => {
                document.addEventListener('click', handleClickOutside)
              })
              
              onUnmounted(() => {
                document.removeEventListener('click', handleClickOutside)
              })
              
              // 添加 isAllSelected 函数
              const isAllSelected = (type) => {
                switch(type) {
                  case 'type':
                    return selectedTypes.value.length === fileTypes.value.length
                  case 'system':
                    return selectedSystems.value.length === systemCodes.value.length
                  case 'format':
                    return selectedFormats.value.length === fileFormats.value.length
                  case 'module':
                    return selectedModules.value.length === modules.value.length
                  default:
                    return false
                }
              }
              
              // 添加 selectAll 函数
              const selectAll = (type) => {
                switch(type) {
                  case 'type':
                    if (isAllSelected('type')) {
                      selectedTypes.value = []
                    } else {
                      selectedTypes.value = fileTypes.value.map(item => item.value)
                    }
                    break
                  case 'system':
                    if (isAllSelected('system')) {
                      selectedSystems.value = []
                    } else {
                      selectedSystems.value = systemCodes.value.map(item => item.value)
                    }
                    break
                  case 'format':
                    if (isAllSelected('format')) {
                      selectedFormats.value = []
                    } else {
                      selectedFormats.value = fileFormats.value.map(item => item.value)
                    }
                    break
                  case 'module':
                    if (isAllSelected('module')) {
                      selectedModules.value = []
                    } else {
                      selectedModules.value = modules.value.map(item => item.value)
                    }
                    break
                }
              }
              
              // 添加 getSelectedLabels 函数
              const getSelectedLabels = (type) => {
                switch(type) {
                  case 'type':
                    return selectedTypes.value.map(value => 
                      fileTypes.value.find(item => item.value === value)?.label
                    ).filter(Boolean)
                  case 'system':
                    return selectedSystems.value.map(value => 
                      systemCodes.value.find(item => item.value === value)?.label
                    ).filter(Boolean)
                  case 'format':
                    return selectedFormats.value.map(value => 
                      fileFormats.value.find(item => item.value === value)?.label
                    ).filter(Boolean)
                  case 'module':
                    return selectedModules.value.map(value => 
                      modules.value.find(item => item.value === value)?.label
                    ).filter(Boolean)
                  default:
                    return []
                }
              }
              
              // 添加展开状态管理
              const expandedSections = ref({
                type: true,  // 默认展开文件类型
                system: false,
                format: false,
                module: false
              })
              
              // 切换展开/收起状态
              const toggleSection = (section) => {
                expandedSections.value[section] = !expandedSections.value[section]
              }
              </script>
              
              <style scoped>
              .analysis-container {
                display: flex;
                height: 100vh;
                background: #ecf5ff;
              }
              
              .filter-panel {
                width: 240px;
                padding: 16px;
                background: #f9fafb;
                border-right: 1px solid #e5e7eb;
                overflow-y: auto;
                display: flex;
                flex-direction: column;
              }
              
              .filter-header {
                margin-bottom: 24px;
              }
              
              .filter-section {
                padding: 6px;
                margin-bottom: 6px;
              }
              
              .filter-section h3 {
                margin-bottom: 8px;
                font-size: 0.9rem;
              }
              
              .filter-options {
                display: flex;
                flex-direction: column;
                gap: 8px;
              }
              
              .filter-option {
                display: flex;
                align-items: center;
                gap: 8px;
                cursor: pointer;
              }
              
              .filter-actions {
                display: flex;
                gap: 12px;
                margin-top: 24px;
              }
              
              .apply-button {
                flex: 1;
                padding: 8px;
                background: #10b981;
                color: white;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                transition: all 0.3s ease;
              }
              
              .apply-button:hover {
                background: #059669;
                transform: translateY(-1px);
              }
              
              .reset-button {
                flex: 1;
                padding: 8px;
                background: #e5e7eb;
                color: #374151;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                transition: all 0.3s ease;
              }
              
              .reset-button:hover {
                background: #d1d5db;
                transform: translateY(-1px);
              }
              
              .chart-content {
                flex: 1;
                padding: 20px;
                overflow-y: auto;
              }
              
              .stats-cards {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 20px;
                margin-bottom: 24px;
              }
              
              .stats-card {
                background: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
              }
              
              .charts-container {
                display: flex;
                flex-direction: column;
                gap: 20px;
              }
              
              .chart-row {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
              }
              
              .chart-item {
                position: relative;
                background: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
                height: 400px;
                transition: all 0.3s ease;
              }
              
              .chart-item:hover {
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                transform: translateY(-2px);
              }
              
              .chart {
                width: 100%;
                height: calc(100% - 30px);
                transition: all 0.3s ease;
              }
              
              .date-range {
                display: flex;
                gap: 12px;
                margin-bottom: 12px;
              }
              
              .date-picker {
                flex: 1;
                display: flex;
                flex-direction: column;
                gap: 4px;
              }
              
              .date-picker label {
                font-size: 0.875rem;
                color: #6b7280;
              }
              
              .date-input {
                width: 100%;
                padding: 14px 4px;
                border: 1px solid #e5e7eb;
                border-radius: 4px;
                font-size: 0.875rem;
              }
              
              .quick-select {
                display: flex;
                flex-wrap: wrap;
                gap: 8px;
                margin-bottom: 16px;
              }
              
              .quick-select-btn {
                padding: 4px 8px;
                border: 1px solid #e5e7eb;
                border-radius: 4px;
                background: white;
                color: #374151;
                font-size: 0.875rem;
                cursor: pointer;
                transition: all 0.2s;
              }
              
              .quick-select-btn:hover {
                border-color: #10b981;
                color: #10b981;
              }
              
              .quick-select-btn.active {
                background: #10b981;
                color: white;
                border-color: #10b981;
              }
              
              /* 添加加载遮罩样式 */
              .loading-overlay {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(255, 255, 255, 0.8);
                display: flex;
                justify-content: center;
                align-items: center;
                z-index: 1000;
              }
              
              .loading-spinner {
                width: 50px;
                height: 50px;
                border: 4px solid #f3f3f3;
                border-top: 4px solid #10b981;
                border-radius: 50%;
                animation: spin 1s linear infinite;
              }
              
              .chart-wrapper {
                position: relative;
                width: 100%;
                height: 100%;
                min-height: 300px;  /* 添加最小高度 */
              }
              
              .chart-loading {
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(255, 255, 255, 0.8);
                display: flex;
                justify-content: center;
                align-items: center;
                font-size: 14px;
                color: #6b7280;
              }
              
              @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
              }
              
              /* 添加按钮动画 */
              .apply-button, .reset-button {
                transition: all 0.3s ease;
              }
              
              .apply-button:hover {
                background: #059669;
                transform: translateY(-1px);
              }
              
              .reset-button:hover {
                background: #d1d5db;
                transform: translateY(-1px);
              }
              
              .chart {
                width: 100%;
                height: 100%;
                min-height: 300px;  /* 添加最小高度 */
              }
              
              .chart-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 16px;
              }
              
              .chart-type-selector {
                display: flex;
                gap: 8px;
              }
              
              .type-btn {
                padding: 4px 8px;
                border: 1px solid #e5e7eb;
                border-radius: 4px;
                background: white;
                color: #374151;
                font-size: 0.875rem;
                cursor: pointer;
                transition: all 0.2s;
              }
              
              .type-btn:hover {
                border-color: #10b981;
                color: #10b981;
              }
              
              .type-btn.active {
                background: #10b981;
                color: white;
                border-color: #10b981;
              }
              
              .chart-actions {
                display: flex;
                gap: 12px;
                align-items: center;
              }
              
              .chart-operations {
                display: flex;
                gap: 8px;
              }
              
              .op-btn {
                padding: 4px;
                border: 1px solid #e5e7eb;
                border-radius: 4px;
                background: white;
                cursor: pointer;
                transition: all 0.2s;
              }
              
              .op-btn:hover {
                border-color: #10b981;
                color: #10b981;
              }
              
              .fullscreen-dialog {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0, 0, 0, 0.75);
                display: flex;
                justify-content: center;
                align-items: center;
                z-index: 1100;
              }
              
              .fullscreen-content {
                background: white;
                width: 90vw;
                height: 90vh;
                border-radius: 8px;
                display: flex;
                flex-direction: column;
              }
              
              .fullscreen-header {
                padding: 16px;
                border-bottom: 1px solid #e5e7eb;
                display: flex;
                justify-content: space-between;
                align-items: center;
              }
              
              .fullscreen-body {
                flex: 1;
                padding: 20px;
              }
              
              .fullscreen-chart {
                width: 100%;
                height: 100%;
              }
              
              /* 修改筛选选项样式 */
              .section-header {
                display: flex;
                align-items: center;
                gap: 6px;
                margin-bottom: 8px;
                padding-bottom: 4px;
                border-bottom: 1px solid #e5e7eb;
              }
              
              .section-header .icon {
                width: 14px;
                height: 14px;
                color: #10b981;
                opacity: 0.8;
              }
              
              .section-header h3 {
                margin: 0;
                font-size: 0.9rem;
                color: #374151;
                font-weight: 500;
              }
              
              .filter-option {
                display: flex;
                align-items: center;
                gap: 12px;
                padding: 8px;
                border-radius: 6px;
                transition: all 0.3s ease;
              }
              
              .filter-option:hover {
                background: #f3f4f6;
              }
              
              .checkbox-wrapper {
                position: relative;
                width: 20px;
                height: 20px;
              }
              
              .checkbox-custom {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                border: 2px solid #10b981;
                border-radius: 4px;
                transition: all 0.3s ease;
              }
              
              input[type="checkbox"]:checked + .checkbox-custom {
                background: #10b981;
              }
              
              input[type="checkbox"]:checked + .checkbox-custom::after {
                content: '';
                position: absolute;
                left: 6px;
                top: 2px;
                width: 5px;
                height: 10px;
                border: solid white;
                border-width: 0 2px 2px 0;
                transform: rotate(45deg);
              }
              
              /* 修改统计卡片样式 */
              .stats-card {
                display: flex;
                align-items: center;
                gap: 16px;
                padding: 24px;
                border-radius: 12px;
                transition: all 0.3s ease;
              }
              
              .total-files {
                background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                color: white;
              }
              
              .total-storage {
                background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
                color: white;
              }
              
              .monthly-new {
                background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
                color: white;
              }
              
              .stats-icon {
                font-size: 2rem;
                opacity: 0.8;
              }
              
              .stats-info {
                flex: 1;
              }
              
              .stats-value {
                font-size: 2rem;
                font-weight: 600;
                line-height: 1.2;
              }
              
              .stats-title {
                font-size: 1rem;
                opacity: 0.8;
              }
              
              .dropdown-select {
                position: relative;
                width: 100%;
              }
              
              .select-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 4px 8px;
                min-height: 32px;
              }
              
              .select-header:hover {
                border-color: #10b981;
              }
              
              .arrow-icon {
                width: 16px;
                height: 16px;
                transition: transform 0.3s ease;
                flex-shrink: 0;
              }
              
              .arrow-icon.rotated {
                transform: rotate(180deg);
              }
              
              .select-options {
                position: absolute;  /* 改为绝对定位 */
                top: 100%;          /* 从父元素底部开始 */
                left: 0;
                right: 0;
                margin-top: 4px;
                background: white;
                border: 1px solid #e5e7eb;
                border-radius: 6px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
                z-index: 9999;
                max-height: 240px;
                overflow-y: auto;
              }
              
              .options-list {
                background: white;
                max-height: 200px;
                overflow-y: auto;
              }
              
              .select-all {
                padding: 6px 12px;
                border-bottom: 1px solid #e5e7eb;
                background: #f9fafb;
              }
              
              .checkbox-label:hover {
                background-color: #f3f4f6;
              }
              
              /* 确保下拉框内容不被遮挡 */
              .filter-panel {
                position: relative;
                z-index: 1;
              }
              
              .filter-section {
                position: relative;
                z-index: 1;
              }
              
              .dropdown-select.active {
                z-index: 1000;
              }
              
              /* 添加过渡动画 */
              .select-options {
                transition: opacity 0.2s ease;
              }
              
              /* 优化滚动条样式 */
              .select-options::-webkit-scrollbar {
                width: 4px;
              }
              
              .select-options::-webkit-scrollbar-track {
                background: #f1f1f1;
              }
              
              .select-options::-webkit-scrollbar-thumb {
                background: #d1d5db;
                border-radius: 2px;
              }
              
              .select-options::-webkit-scrollbar-thumb:hover {
                background: #9ca3af;
              }
              
              /* 修改导航标题样式 */
              .nav-header {
                padding: 12px;
                background: linear-gradient(135deg, #575793 0%, #059669 100%);
                color: white;
                margin: -16px -16px 12px -16px;
                border-top-left-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
              }
              
              .nav-title {
                display: flex;
                align-items: center;
                gap: 12px;
                margin-bottom: 4px;
              }
              
              .nav-icon {
                width: 24px;
                height: 24px;
                fill: currentColor;
                opacity: 0.9;
              }
              
              .nav-title span {
                font-size: 1.1rem;
                font-weight: 600;
                letter-spacing: 0.5px;
              }
              
              .nav-subtitle {
                font-size: 0.75rem;
                opacity: 0.8;
                margin-left: 32px;
                font-family: 'Arial', sans-serif;
                letter-spacing: 0.5px;
              }
              
              /* 调整筛选内容区域 */
              .filter-content {
                margin-top: 20px;
              }
              
              /* 修改筛选面板样式以适应新的标题 */
              .filter-panel {
                width: 240px;
                padding: 16px;
                background: #f9fafb;
                border-right: 1px solid #e5e7eb;
                overflow-y: auto;
                display: flex;
                flex-direction: column;
              }
              
              /* 添加 radio 样式 */
              .radio-group {
                display: flex;
                flex-direction: column;
                gap: 4px;
                padding: 4px 0;
              }
              
              .radio-label {
                display: flex;
                align-items: center;
                padding: 4px 6px;
                min-height: 24px;
                cursor: pointer;
                border-radius: 4px;
                transition: background-color 0.2s;
              }
              
              .radio-label:hover {
                background-color: #f3f4f6;
              }
              
              .radio-input {
                margin-right: 6px;
                width: 14px;
                height: 14px;
                cursor: pointer;
              }
              
              .radio-text {
                font-size: 0.85rem;
              }
              
              /* 修改筛选区域样式 */
              .section-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 8px;
                cursor: pointer;
                user-select: none;
                transition: background-color 0.2s;
              }
              
              .section-header:hover {
                background-color: #f3f4f6;
              }
              
              .header-left {
                display: flex;
                align-items: center;
                gap: 8px;
              }
              
              .arrow-icon {
                width: 20px;
                height: 20px;
                transition: transform 0.3s ease;
              }
              
              .arrow-icon.rotated {
                transform: rotate(180deg);
              }
              
              .section-content {
                padding: 8px;
                transition: all 0.3s ease;
              }
              
              /* 添加展开/收起动画 */
              .section-content {
                overflow: hidden;
                transition: max-height 0.3s ease;
              }
              
              .filter-section {
                border: 1px solid #e5e7eb;
                border-radius: 6px;
                margin-bottom: 8px;
                overflow: hidden;
              }
              </style>               
