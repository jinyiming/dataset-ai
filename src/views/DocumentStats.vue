<template>
  <div class="analysis-container">
    <!-- 添加加载状态显示 -->
    <div v-if="loading" class="loading-overlay">
      <div class="loading-spinner"></div>
    </div>
    
    <!-- 左侧面板 -->
    <div class="filter-panel">
      <!-- 标题 -->
      <div class="nav-header">
        <div class="nav-title">
          <svg class="nav-icon" viewBox="0 0 24 24">
            <path d="M3 3v17a1 1 0 001 1h17v-2H5V3H3z"/>
            <path d="M15.293 14.707a1 1 0 001.414 0l5-5-1.414-1.414L16 12.586l-2.293-2.293a1 1 0 00-1.414 0l-5 5 1.414 1.414L13 12.414l2.293 2.293z"/>
            <path d="M9.293 16.707l3-3-1.414-1.414-3 3 1.414 1.414z"/>
          </svg>
          <span>公文统计分析</span>
        </div>
      </div>

      <!-- 总数统计 -->
      <div class="total-stats">
        <div class="total-item">
          <div class="total-label">公文总数</div>
          <div class="total-value">{{ totalDocs }}</div>
        </div>
      </div>

      <!-- TOP10列表 -->
      <div class="top-stats">
        <h3>文件类型TOP10</h3>
        <div class="top-list">
          <div v-for="(item, index) in topStats.subject" 
               :key="index" 
               class="top-item">
            <span class="rank">{{ index + 1 }}</span>
            <span class="name">{{ item.name }}</span>
            <span class="value">{{ item.value }}件</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 右侧图表区域 -->
    <div class="content-panel" style="background: rgb(231 231 231);">
      <div class="charts-container">
        <!-- 四个图表 -->
        <div v-for="chart in charts" :key="chart.id" class="chart-item">
          <div class="chart-header">
            <h3>{{ chart.title }}</h3>
            <div class="chart-types">
              <button 
                v-for="type in chartTypes" 
                :key="type.value"
                :class="['type-btn', { active: currentChartType[chart.key] === type.value }]"
                @click="changeChartType(chart.key, type.value)"
              >
                {{ type.label }}
              </button>
            </div>
          </div>
          <div :ref="el => chartRefs[chart.key].value = el" class="chart"></div>
        </div>
      </div>
    </div>

    <!-- 添加浮动图标栏 -->
    <FloatingDock />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick, watch } from 'vue'
import * as echarts from 'echarts'
import axios from 'axios'
import FloatingDock from '@/components/FloatingDock.vue'

// 初始化响应式数据
const totalDocs = ref(0)
const loading = ref(false)

// 展开状态管理
const expandedSections = ref({
  type: true,  // 默认展开文件类型
  module: false
})

// 选中的值
const selectedType = ref('')
const selectedModule = ref('')

// 日期范围
const dateRange = ref({
  start: '',
  end: new Date().toISOString().split('T')[0]
})

// 图表引用
const moduleChartRef = ref(null)
const categoryChartRef = ref(null)
const subjectChartRef = ref(null)
const titleChartRef = ref(null)

let moduleChart = null
let categoryChart = null
let subjectChart = null
let titleChart = null

// 公文类型选项
const docTypes = ref([
  { label: '请示', value: 'QS' },
  { label: '报告', value: 'BG' },
  { label: '通知', value: 'TZ' },
  { label: '函', value: 'HAN' }
])

// 公文模块选项
const docModules = ref([
  { label: '发文', value: 'DISPATCH' },
  { label: '收文', value: 'RECEIVAL' },
  { label: '公文交换', value: 'EXCHANGE' }
])

// 图表类型选项
const chartTypes = [
  { label: '饼图', value: 'pie' },
  { label: '柱状图', value: 'bar' },
  { label: '折线图', value: 'line' },
  { label: '散点图', value: 'scatter' },
  { label: '热力图', value: 'heatmap' }
]

// 当前图表类型
const currentChartType = ref({
  module: 'bar',
  category: 'line',
  subject: 'pie',
  title: 'bar'
})

// 添加数据缓存
const lastData = ref(null)
const topStats = ref({
  subject: [],
  category: []
})

// 切换展开/收起状态
const toggleSection = (section) => {
  expandedSections.value[section] = !expandedSections.value[section]
}

// 切换图表类型
const changeChartType = (chart, type) => {
  currentChartType.value[chart] = type
  updateCharts(lastData.value)
}

// 定义图表配置
const charts = [
  { id: 1, key: 'module', title: '模块分布' },
  { id: 2, key: 'category', title: '文种分布' },
  { id: 3, key: 'subject', title: '文件类型分布' },
  { id: 4, key: 'title', title: '标题分类分布' }
]

// 修改获取数据函数
const fetchData = async () => {
  loading.value = true
  try {
    console.log('开始获取数据...')
    const response = await axios.get('http://localhost:8000/flask/api/document-stats')
    console.log('获取到的原始数据:', response.data)
    
    const data = response.data
    if (data) {
      totalDocs.value = data.totalDocs || 0
      topStats.value = data.topStats || { subject: [], category: [] }
      lastData.value = data

      // 确保图表已初始化
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

// 修改图表引用方式
const chartRefs = {
  module: ref(null),
  category: ref(null),
  subject: ref(null),
  title: ref(null)
}

// 修改初始化图表函数
const initCharts = () => {
  console.log('初始化图表...')
  Object.keys(chartRefs).forEach(key => {
    if (chartRefs[key].value && !window[key + 'Chart']) {
      window[key + 'Chart'] = echarts.init(chartRefs[key].value)
      console.log(`${key}图表初始化成功`)
    }
  })
}

// 修改更新图表函数
const updateCharts = (data) => {
  if (!data) return
  console.log('更新图表数据:', data)

  Object.keys(chartRefs).forEach(key => {
    const chart = window[key + 'Chart']
    if (chart) {
      const option = getChartOption(key, data)
      chart.setOption(option, true)
      console.log(`${key}图表更新成功`)
    }
  })
}

// 修改获取图表配置函数
const getChartOption = (chartKey, data) => {
  const baseOption = {
    title: { text: charts.find(c => c.key === chartKey)?.title || '', left: 'center' },
    tooltip: { 
      trigger: currentChartType.value[chartKey] === 'pie' ? 'item' : 'axis',
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left',
      type: 'scroll'
    }
  }

  const chartData = data[chartKey + 'Stats'] || []
  
  if (currentChartType.value[chartKey] === 'pie') {
    return {
      ...baseOption,
      series: [{
        type: 'pie',
        radius: '60%',
        data: chartData,
        label: { show: true, formatter: '{b}: {c}' },
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }]
    }
  } else if (currentChartType.value[chartKey] === 'heatmap') {
    const values = chartData.map(item => item.value)
    const max = Math.max(...values)
    const min = Math.min(...values)

    return {
      ...baseOption,
      visualMap: {
        min: min,
        max: max,
        calculable: true,
        orient: 'horizontal',
        left: 'center',
        bottom: '15%'
      },
      grid: {
        top: '10%',
        height: '50%'
      },
      xAxis: {
        type: 'category',
        data: chartData.map(item => item.name),
        axisLabel: { rotate: 30 }
      },
      yAxis: {
        type: 'category',
        data: ['数量']
      },
      series: [{
        name: charts.find(c => c.key === chartKey)?.title,
        type: 'heatmap',
        data: chartData.map((item, index) => [index, 0, item.value]),
        label: {
          show: true,
          formatter: '{c}'
        },
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }]
    }
  } else {
    return {
      ...baseOption,
      xAxis: {
        type: 'category',
        data: chartData.map(item => item.name),
        axisLabel: { rotate: 30 }
      },
      yAxis: { type: 'value' },
      series: [{
        type: currentChartType.value[chartKey],
        data: chartData.map(item => item.value),
        label: { show: true, position: 'top' }
      }]
    }
  }
}

// 修改组件挂载逻辑
onMounted(() => {
  console.log('组件挂载...')
  nextTick(() => {
    console.log('DOM更新完成')
    initCharts()
    fetchData()
  })
})

// 添加窗口大小变化监听
window.addEventListener('resize', () => {
  if (moduleChart) {
    moduleChart.resize()
  }
  if (categoryChart) {
    categoryChart.resize()
  }
  if (subjectChart) {
    subjectChart.resize()
  }
  if (titleChart) {
    titleChart.resize()
  }
})

// 添加监听器，当筛选条件改时重新获取数据
watch([selectedType, selectedModule, dateRange], () => {
  fetchData()
})

// 修改组件卸载逻辑
onUnmounted(() => {
  if (moduleChart) {
    moduleChart.dispose()
  }
  if (categoryChart) {
    categoryChart.dispose()
  }
  if (subjectChart) {
    subjectChart.dispose()
  }
  if (titleChart) {
    titleChart.dispose()
  }
  window.removeEventListener('resize', () => {
    moduleChart?.resize()
    categoryChart?.resize()
    subjectChart?.resize()
    titleChart?.resize()
  })
})
</script> 

<style scoped>
.analysis-container {
  display: flex;
  height: 100vh;
  background: #f8fafc;
}

/* 左侧筛选面板样式 */
.filter-panel {
  width: 240px;
  padding: 16px;
  background: #f9fafb;
  border-right: 1px solid #e5e7eb;
  overflow-y: auto;
}

/* 导航标题样式 */
.nav-header {
  padding: 20px 16px;
  background: linear-gradient(135deg, #4e4e75 0%, #059669 100%);
  color: white;
  margin: -16px -16px 16px -16px;
  border-top-left-radius: 8px;
}

.nav-title {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 4px;
}

.nav-title span {
  font-size: 1.25rem;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.nav-subtitle {
  font-size: 0.8rem;
  opacity: 0.8;
  margin-left: 32px;
  font-family: 'Arial', sans-serif;
  letter-spacing: 0.5px;
}

/* 筛选区域样式 */
.filter-section {
  margin-bottom: 12px;
  background: white;
  border-radius: 6px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  cursor: pointer;
  user-select: none;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.header-left .icon {
  width: 16px;
  height: 16px;
  color: #10b981;
}

.header-left h3 {
  margin: 0;
  font-size: 0.95rem;
  color: #374151;
  font-weight: 500;
}

.arrow-icon {
  width: 20px;
  height: 20px;
  transition: transform 0.3s ease;
}

.arrow-icon.rotated {
  transform: rotate(180deg);
}

/* 选项组样式 */
.radio-group {
  padding: 8px;
}

.radio-label {
  display: flex;
  align-items: center;
  padding: 6px 8px;
  cursor: pointer;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.radio-label:hover {
  background-color: #f3f4f6;
}

.radio-label input[type="radio"] {
  margin-right: 8px;
  cursor: pointer;
  accent-color: #10b981;
}

/* 右侧内容区域样式 */
.content-panel {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

/* 统计卡片样式 */
.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
  margin-bottom: 24px;
}

.stats-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.stats-info {
  text-align: center;
}

.stats-label {
  font-size: 0.9rem;
  color: #6b7280;
  margin-bottom: 4px;
}

.stats-value {
  font-size: 2rem;
  font-weight: 600;
  color: #10b981;
}

/* 图表区域样式 */
.charts-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
  padding: 24px;
}

.chart-item {
  background: white;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  height: 480px;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.chart-header h3 {
  margin: 0;
  font-size: 1.1rem;
  color: #374151;
}

.chart {
  height: calc(100% - 48px);
}

/* 响应式布局 */
@media (max-width: 1024px) {
  .charts-container {
    grid-template-columns: 1fr;
  }
}

/* 滚动条样式 */
.filter-panel::-webkit-scrollbar {
  width: 4px;
}

.filter-panel::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.filter-panel::-webkit-scrollbar-thumb {
  background: #d1d5db;
  border-radius: 2px;
}

.filter-panel::-webkit-scrollbar-thumb:hover {
  background: #9ca3af;
}

/* TOP10统计样式 */
.top-stats {
  margin-bottom: 24px;
}

.top-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 0 16px;
}

.top-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: #f9fafb;
  border-radius: 8px;
  transition: transform 0.2s ease;
}

.top-item:hover {
  transform: translateX(4px);
}

.rank {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #10b981;
  color: white;
  border-radius: 50%;
  font-weight: 600;
}

.name {
  flex: 1;
  color: #374151;
}

.value {
  color: #10b981;
  font-weight: 500;
}

/* TOP10 颜色变化 */
.top-item:nth-child(1) .rank { background: #ef4444; }
.top-item:nth-child(2) .rank { background: #f97316; }
.top-item:nth-child(3) .rank { background: #f59e0b; }
.top-item:nth-child(4) .rank { background: #10b981; }
.top-item:nth-child(5) .rank { background: #06b6d4; }
.top-item:nth-child(6) .rank { background: #3b82f6; }
.top-item:nth-child(7) .rank { background: #6366f1; }
.top-item:nth-child(8) .rank { background: #8b5cf6; }
.top-item:nth-child(9) .rank { background: #d946ef; }
.top-item:nth-child(10) .rank { background: #ec4899; }

/* 图表类型切换按钮样式 */
.chart-types {
  display: flex;
  gap: 8px;
}

.type-btn {
  padding: 4px 8px;
  border: 1px solid #e5e7eb;
  border-radius: 4px;
  background: white;
  color: #374151;
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

/* 左侧面样式 */
.total-stats {
  background: linear-gradient(135deg, #34ecaf 0%, #96056e 100%);
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
}

.total-item {
  text-align: center;
  color: white;
}

.total-label {
  font-size: 1.1rem;
  opacity: 0.9;
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.total-value {
  font-size: 2.5rem;
  font-weight: 700;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* 图表区域样式 */
.charts-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.chart-item {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  height: 400px;
}

.chart {
  height: calc(100% - 60px);
  width: 100%;
}

/* 添加加载状态样式 */
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
  width: 40px;
  height: 40px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #10b981;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.nav-icon {
  width: 28px;
  height: 28px;
  fill: currentColor;
  opacity: 0.95;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
}
</style> 