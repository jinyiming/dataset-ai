<template>
  <div class="knowledge-graph">
    <!-- 左侧控制面板 -->
    <div class="filter-panel">
      <!-- 标题导航栏 -->
      <div class="nav-header">
        <div class="nav-title">
          <svg class="nav-icon" viewBox="0 0 24 24">
            <path d="M3 3v17a1 1 0 001 1h17v-2H5V3H3z"/>
            <path d="M15.293 14.707a1 1 0 001.414 0l5-5-1.414-1.414L16 12.586l-2.293-2.293a1 1 0 00-1.414 0l-5 5 1.414 1.414L13 12.414l2.293 2.293z"/>
            <path d="M9.293 16.707l3-3-1.414-1.414-3 3 1.414 1.414z"/>
          </svg>
          <span>知识图谱分析</span>
        </div>
        <div class="nav-subtitle">Knowledge Graph Analysis</div>
      </div>

      <!-- 搜索框 -->
      <div class="search-section">
        <div class="section-header">
          <svg class="icon" viewBox="0 0 24 24">
            <path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/>
          </svg>
          <h3>搜索节点</h3>
        </div>
        <input 
          v-model="searchQuery" 
          placeholder="输入关键字搜索..." 
          @input="handleSearch"
          class="search-input"
        >
      </div>

      <!-- 节点类型筛选 -->
      <div class="filter-section">
        <div class="section-header">
          <h3>节点类型筛选</h3>
        </div>
        <div class="filter-list">
          <div v-for="type in nodeTypes" 
               :key="type.id" 
               class="filter-item"
               :class="{ active: type.checked }"
               @click="() => {
                 type.checked = !type.checked;
                 updateGraphVisibility();
               }">
            <div class="type-icon" :style="{ backgroundColor: nodeStyles[type.id].color }">
              <svg viewBox="0 0 24 24" class="icon">
                <path :d="type.icon" fill="white"/>
              </svg>
            </div>
            <div class="type-info">
              <span class="type-label">{{ type.label }}</span>
              <span class="type-count">({{ type.count }})</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 关系类型图例 -->
      <div class="legend-section">
        <div class="section-header">
          <h3>关系类型</h3>
        </div>
        <div class="legend-list">
          <div v-for="relation in relationTypes" 
               :key="relation.type" 
               class="legend-item">
            <span class="relation-line" :style="{ backgroundColor: relation.color }"></span>
            <span class="relation-label">{{ relation.label }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 右侧图谱展示 -->
    <div class="content-panel">
      <div class="toolbar">
        <button class="tool-btn" @click="zoomIn" title="放大">
          <svg class="tool-icon" viewBox="0 0 24 24">
            <path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/>
          </svg>
        </button>
        <button class="tool-btn" @click="zoomOut" title="缩小">
          <svg class="tool-icon" viewBox="0 0 24 24">
            <path d="M19 13H5v-2h14v2z"/>
          </svg>
        </button>
        <button class="tool-btn" @click="resetZoom" title="重置">
          <svg class="tool-icon" viewBox="0 0 24 24">
            <path d="M12 5V1L7 6l5 5V7c3.31 0 6 2.69 6 6s-2.69 6-6 6-6-2.69-6-6H4c0 4.42 3.58 8 8 8s8-3.58 8-8-3.58-8-8-8z"/>
          </svg>
        </button>
      </div>
      <div ref="graphRef" class="neo4j-graph"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import * as d3 from 'd3'
import axios from 'axios'

const graphRef = ref(null)
const searchQuery = ref('')
const simulation = ref(null)

// 节点类型定义
const nodeTypes = ref([
  { 
    id: 'user', 
    label: '用户', 
    checked: true, 
    count: 0,
    icon: 'M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z'
  },
  { 
    id: 'organization', 
    label: '部门', 
    checked: true, 
    count: 0,
    icon: 'M12 7V3H2v18h20V7H12zM6 19H4v-2h2v2zm0-4H4v-2h2v2zm0-4H4V9h2v2zm0-4H4V5h2v2zm4 12H8v-2h2v2zm0-4H8v-2h2v2zm0-4H8V9h2v2zm0-4H8V5h2v2zm10 12h-8v-2h2v-2h-2v-2h2v-2h-2V9h8v10zm-2-8h-2v2h2v-2zm0 4h-2v2h2v-2z'
    },
    { 
      id: 'document', 
      label: '公文', 
      checked: true, 
      count: 0,
      icon: 'M14 2H6c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V8l-6-6z'
    },
    { 
      id: 'system', 
      label: '系统', 
      checked: true, 
      count: 0,
      icon: 'M4 6h18V4H4c-1.1 0-2 .9-2 2v11H0v3h14v-3H4V6z'
    }
])

// 关系类型定义
const relationTypes = [
  { type: 'BELONGS_TO', label: '属于', color: '#FFD93D' },
  { type: 'DRAFTED', label: '起草', color: '#FF6B6B' },
  { type: 'REGISTERED', label: '登记', color: '#4ECDC4' }
]

// 添加筛选状态
const filterState = ref({
  selectedDepartment: null,
  selectedSystem: null,
  searchText: ''
})

// 添加节点样式定义
const nodeStyles = {
  'user': {
    color: '#FF6B6B',
    label: '用户'
  },
  'organization': {
    color: '#4ECDC4',
    label: '部门'
  },
  'document': {
    color: '#FFD93D',
    label: '公文'
  },
  'system': {
    color: '#45B7D1',
    label: '系统'
  }
}

// 添加关系样式定义
const relationStyles = {
  'BELONGS_TO': {
    color: '#FFD93D',
    label: '属于'
  },
  'DRAFTED': {
    color: '#FF6B6B',
    label: '起草'
  },
  'REGISTERED': {
    color: '#4ECDC4',
    label: '登记'
  },
  'PROCESSED': {
    color: '#45B7D1',
    label: '办理'
  }
}

// 获取图谱数据
const fetchGraphData = async () => {
  try {
    console.log('开始初始化知识图谱...')
    // 修改API路径
    const response = await axios.get('http://localhost:8000/flask/api/knowledge-graph')
    console.log('获取到的原始数据:', response.data)
    
    if (response.data) {
      return {
        nodes: response.data.nodes.map(node => ({
          ...node,
          id: node.id.toString(),
          label: node.label || '未命名',
          type: node.type || 'unknown'
        })),
        links: response.data.links.map(link => ({
          ...link,
          source: link.source.toString(),
          target: link.target.toString(),
          type: link.type
        }))
      }
    }
  } catch (error) {
    console.error('获取图谱数据失败:', error)
  }
  return null
}

// 初始化图谱
const initGraph = (data) => {
  if (!graphRef.value || !data || !data.nodes || !data.links) {
    console.error('缺少必要的图谱数据:', {
      graphRef: !!graphRef.value,
      data: !!data,
      nodes: data?.nodes?.length,
      links: data?.links?.length
    })
    return
  }

  console.log('开始初始化图谱，数据:', data)
  // 清除现有的SVG
  d3.select(graphRef.value).selectAll('*').remove()

  const container = graphRef.value
  const width = container.clientWidth
  const height = container.clientHeight

  // 创建SVG
  const svg = d3.select(container)
    .append('svg')
    .attr('width', width)
    .attr('height', height)
    .attr('viewBox', [0, 0, width, height])

  // 创建箭头标记
  svg.append('defs').selectAll('marker')
    .data(Object.keys(relationStyles))
    .enter().append('marker')
    .attr('id', d => d)
    .attr('viewBox', '0 -5 10 10')
    .attr('refX', 28)
    .attr('refY', 0)
    .attr('markerWidth', 8)
    .attr('markerHeight', 8)
    .attr('orient', 'auto')
    .append('path')
    .attr('d', 'M0,-5L10,0L0,5')
    .attr('fill', d => relationStyles[d].color)

  // 创建容器组
  const g = svg.append('g')

  // 创建连线
  const links = g.append('g')
    .selectAll('line')
    .data(data.links)
    .join('line')
    .attr('stroke', d => relationStyles[d.type]?.color || '#999')
    .attr('stroke-width', 2)
    .attr('marker-end', d => `url(#${d.type})`)

  // 添加关系标签
  const linkLabels = g.append('g')
    .selectAll('text')
    .data(data.links)
    .join('text')
    .attr('class', 'link-label')
    .text(d => relationStyles[d.type]?.label || d.type)
    .attr('text-anchor', 'middle')
    .attr('dy', -5)
    .style('fill', d => relationStyles[d.type]?.color || '#999')

  // 创建节点
  const nodes = g.append('g')
    .selectAll('g')
    .data(data.nodes)
    .join('g')
    .attr('class', 'node')
    .call(d3.drag()
      .on('start', dragstarted)
      .on('drag', dragged)
      .on('end', dragended))

  // 添加节点圆圈
  nodes.append('circle')
    .attr('r', 20)
    .attr('fill', d => nodeStyles[d.type.toLowerCase()]?.color || '#999')

  // 添加节点标签
  nodes.append('text')
    .text(d => d.label)
    .attr('dy', 30)
    .attr('text-anchor', 'middle')
    .attr('fill', '#333')

  // 创建力导向模拟
  simulation.value = d3.forceSimulation(data.nodes)
    .force('link', d3.forceLink(data.links)
      .id(d => d.id)
      .distance(100))
    .force('charge', d3.forceManyBody().strength(-800))
    .force('center', d3.forceCenter(width / 2, height / 2))
    .force('collision', d3.forceCollide().radius(50))

  // 更新函数
  simulation.value.on('tick', () => {
    links
      .attr('x1', d => d.source.x)
      .attr('y1', d => d.source.y)
      .attr('x2', d => d.target.x)
      .attr('y2', d => d.target.y)

    nodes
      .attr('transform', d => `translate(${d.x},${d.y})`)
  })

  // 缩放功能
  const zoom = d3.zoom()
    .scaleExtent([0.2, 3])
    .on('zoom', (event) => {
      g.attr('transform', event.transform)
    })

  svg.call(zoom)

  // 拖拽函数
  function dragstarted(event) {
    if (!event.active) simulation.value.alphaTarget(0.3).restart()
    event.subject.fx = event.subject.x
    event.subject.fy = event.subject.y
  }

  function dragged(event) {
    event.subject.fx = event.x
    event.subject.fy = event.y
  }

  function dragended(event) {
    if (!event.active) simulation.value.alphaTarget(0)
    event.subject.fx = null
    event.subject.fy = null
  }

  // 添加节点点击事件
  nodes.on('click', (event, d) => {
    // 显示节点信息
    const info = document.createElement('div')
    info.className = 'node-info'
    
    let content = `<h3>${d.label}</h3>`
    content += `<p>类型: ${nodeStyles[d.type.toLowerCase()].label}</p>`
    
    // 根据节点类型显示不同的属性
    if (d.type === 'user') {
      content += `
        <p>工号: ${d.properties.user_no}</p>
        <p>姓名: ${d.properties.name}</p>
      `
    } else if (d.type === 'organization') {
      content += `
        <p>部门编号: ${d.properties.org_no}</p>
        <p>部门名称: ${d.properties.name}</p>
      `
    } else if (d.type === 'document') {
      content += `
        <p>文件编号: ${d.properties.id}</p>
        <p>标题: ${d.properties.title}</p>
        <p>类型: ${d.properties.type}</p>
        <p>分类: ${d.properties.category === 'dispatch' ? '发文' : '收文'}</p>
      `
    }
    
    info.innerHTML = content
    
    // 移除旧的信息框
    d3.select('.node-info').remove()
    
    // 添加新的信息框
    document.body.appendChild(info)
    
    // 设置信息框位置
    const rect = event.target.getBoundingClientRect()
    info.style.left = `${rect.right + 10}px`
    info.style.top = `${rect.top}px`
  })

  // 添加样式
  const style = document.createElement('style')
  style.textContent = `
  .node-info {
    position: fixed;
    background: white;
    padding: 16px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
    z-index: 1000;
    max-width: 300px;
  }

  .node-info h3 {
    margin: 0 0 8px 0;
    color: #374151;
    font-size: 1.1rem;
  }

  .node-info p {
    margin: 4px 0;
    color: #6b7280;
    font-size: 0.9rem;
  }

  .link-label {
    pointer-events: none;
    font-size: 12px;
    text-shadow: 
      -1px -1px 3px white,
      -1px 1px 3px white,
      1px -1px 3px white,
      1px 1px 3px white;
  }
  `
  document.head.appendChild(style)

  // 点击其他地方关闭信息框
  document.addEventListener('click', (event) => {
    const info = document.querySelector('.node-info')
    if (info && !event.target.closest('.node') && !event.target.closest('.node-info')) {
      info.remove()
    }
  })
}

// 缩放功能
const zoomIn = () => {
  // 实现放大功能
}

const zoomOut = () => {
  // 实现缩小功能
}

const resetZoom = () => {
  // 实现重置功能
}

// 搜索功能
const handleSearch = () => {
  if (!searchQuery.value) {
    // 重置筛选
    updateGraphVisibility()
    return
  }

  // 在图谱高亮匹配的节点
  const nodes = d3.selectAll('.node')
  nodes.style('opacity', d => {
    const match = d.label.toLowerCase().includes(searchQuery.value.toLowerCase())
    return match ? 1 : 0.1
  })

  // 更新连线显示
  const links = d3.selectAll('line')
  links.style('opacity', d => {
    const sourceVisible = d.source.label.toLowerCase().includes(searchQuery.value.toLowerCase())
    const targetVisible = d.target.label.toLowerCase().includes(searchQuery.value.toLowerCase())
    return sourceVisible || targetVisible ? 1 : 0.1
  })
}

// 获取节点类型数量
const getTypeCount = (type) => {
  // 实现统计功能
  return 0
}

// 更新图谱可见性
const updateGraphVisibility = () => {
  const visibleTypes = nodeTypes.value
    .filter(type => type.checked)
    .map(type => type.id)

  // 更新节点显示
  const nodes = d3.selectAll('.node')
  nodes.style('opacity', d => visibleTypes.includes(d.type.toLowerCase()) ? 1 : 0.1)

  // 更新连线显示
  const links = d3.selectAll('line')
  links.style('opacity', d => {
    const sourceVisible = visibleTypes.includes(d.source.type.toLowerCase())
    const targetVisible = visibleTypes.includes(d.target.type.toLowerCase())
    return sourceVisible && targetVisible ? 1 : 0.1
  })
}

// 修改节点点击处理函数
const handleNodeClick = (event, d) => {
  const nodes = d3.selectAll('.node')
  const links = d3.selectAll('line')
  const type = d.type.toLowerCase()

  // 高亮相关节点和连线
  if (type === 'user') {
    // 点击用户节点时，显示其起草的发文和登记的收文
    nodes.style('opacity', node => {
      const nodeType = node.type.toLowerCase()
      return (nodeType === 'organization' && node.properties.org_no === d.properties.org_no) ||
             (nodeType === 'document' && (
               hasRelation(d.id, node.id, 'DRAFTED') || 
               hasRelation(d.id, node.id, 'REGISTERED')
             )) ||
             node.id === d.id ? 1 : 0.1
    })
  } else if (type === 'organization') {
    // 点击部门节点时，显示其用户和系统
    nodes.style('opacity', node => {
      const nodeType = node.type.toLowerCase()
      return (nodeType === 'user' && node.properties.org_no === d.properties.org_no) ||
             (nodeType === 'system' && hasRelation(d.id, node.id, 'HAS_ACCESS')) ||
             node.id === d.id ? 1 : 0.1
    })
  } else if (type === 'document') {
    // 点击公文节点时，显示相关用户
    nodes.style('opacity', node => {
      const nodeType = node.type.toLowerCase()
      return (nodeType === 'user' && (
        hasRelation(node.id, d.id, 'DRAFTED') || 
        hasRelation(node.id, d.id, 'REGISTERED')
      )) || node.id === d.id ? 1 : 0.1
    })
  }

  // 更新连线显示
  links.style('opacity', link => {
    const sourceVisible = parseFloat(nodes.filter(n => n.id === link.source.id).style('opacity')) === 1
    const targetVisible = parseFloat(nodes.filter(n => n.id === link.target.id).style('opacity')) === 1
    return sourceVisible && targetVisible ? 1 : 0.1
  })
}

// 添加节点统计函数
const updateNodeCounts = (data) => {
  if (!data || !data.nodes) return
  
  const counts = {
    user: 0,
    organization: 0,
    system: 0
  }

  data.nodes.forEach(node => {
    const type = node.type.toLowerCase()
    if (counts.hasOwnProperty(type)) {
      counts[type]++
    }
  })

  nodeTypes.value.forEach(type => {
    type.count = counts[type.id] || 0
  })
}

onMounted(async () => {
  console.log('组件挂载...')
  try {
    // 先调用初始化接口
    await axios.get('http://localhost:8000/flask/api/init-knowledge-graph')
    console.log('知识图谱初始化成功')
    
    // 获取图谱数据
    const data = await fetchGraphData()
    console.log('获取到图谱数据:', data)
    
    if (data) {
      // 更新节点计数
      updateNodeCounts(data)
      // 初始化图谱
      nextTick(() => {
        initGraph(data)
      })
    } else {
      console.error('图谱数据为空')
    }
  } catch (error) {
    console.error('初始化知识图谱失败:', error)
  }
})

onUnmounted(() => {
  if (simulation.value) {
    simulation.value.stop()
  }
})
</script>

<style scoped>
.knowledge-graph {
  display: flex;
  height: 100vh;
  background: #f8fafc;
}

.graph-container {
  flex: 1;
  position: relative;
}

.neo4j-graph {
  width: 100%;
  height: 100%;
  min-height: 500px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.control-panel {
  width: 250px;
  padding: 20px;
  background: white;
  border-left: 1px solid #e5e7eb;
}

.search-box {
  margin-bottom: 20px;
}

.search-box input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
}

.filter-options {
  padding: 16px 0;
}

.filter-options h3 {
  margin: 0 0 12px 0;
  font-size: 1rem;
  color: #374151;
}

.filter-item {
  display: flex;
  align-items: center;
  padding: 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.filter-item:hover {
  background: #f3f4f6;
}

.filter-item.active {
  background: #f0fdf4;
}

.type-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 12px;
}

.type-icon .icon {
  width: 20px;
  height: 20px;
}

.type-info {
  display: flex;
  flex-direction: column;
}

.type-label {
  font-weight: 500;
  color: #374151;
}

.type-count {
  font-size: 0.85rem;
  color: #6b7280;
}

.legend-item {
  display: flex;
  align-items: center;
  padding: 8px 12px;
}

.relation-line {
  width: 40px;
  height: 3px;
  border-radius: 2px;
  margin-right: 12px;
}

.relation-label {
  color: #374151;
}

/* 添加新的样式 */
.node circle {
  stroke: #fff;
  stroke-width: 2px;
}

.node circle.document {
  fill: #4CAF50;
}

.node circle.department {
  fill: #2196F3;
}

.node circle.filetype {
  fill: #FFC107;
}

.link {
  stroke-width: 2px;
}

.link.sent {
  stroke: #4CAF50;
}

.link.received {
  stroke: #2196F3;
}

.link.is-type {
  stroke: #FFC107;
}

.marker-sent {
  fill: #4CAF50;
}

.marker-received {
  fill: #2196F3;
}

.marker-is-type {
  fill: #FFC107;
}

.link {
  stroke-opacity: 0.6;
}

.link-label {
  pointer-events: none;
  text-shadow: 
    -1px -1px 3px white,
    -1px 1px 3px white,
    1px -1px 3px white,
    1px 1px 3px white;
}

.node circle {
  stroke: #fff;
  stroke-width: 2px;
  cursor: pointer;
}

.node text {
  pointer-events: none;
  text-shadow: 
    -1px -1px 3px white,
    -1px 1px 3px white,
    1px -1px 3px white,
    1px 1px 3px white;
}

.node:hover circle {
  filter: brightness(0.9);
}

/* 添加图例样式 */
.legend-section {
  margin-top: 20px;
  padding: 16px;
  background: #f8fafc;
  border-radius: 8px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.relation-line {
  display: inline-block;
  width: 30px;
  height: 2px;
}

.relation-line.sent { background-color: #4CAF50; }
.relation-line.received { background-color: #2196F3; }
.relation-line.is-type { background-color: #FFC107; }

/* 修改导航标题样式 */
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

.nav-icon {
  width: 28px;
  height: 28px;
  fill: currentColor;
  opacity: 0.95;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
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

/* 修改左侧面板样式 */
.filter-panel {
  width: 280px;
  padding: 16px;
  background: #f9fafb;
  border-right: 1px solid #e5e7eb;
  overflow-y: auto;
}

/* 修改搜索框样式 */
.search-section {
  margin-bottom: 20px;
}

.search-input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  background: white;
  font-size: 0.9rem;
}

/* 修改右侧内容区域样式 */
.content-panel {
  flex: 1;
  padding: 20px;
  background: rgb(231 231 231);
  position: relative;
  min-height: 500px;
}

/* 修改工具栏样式 */
.toolbar {
  position: absolute;
  top: 20px;
  right: 20px;
  display: flex;
  gap: 8px;
  z-index: 100;
}

.tool-btn {
  padding: 8px;
  background: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.tool-icon {
  width: 20px;
  height: 20px;
  fill: #4b5563;
}

/* 统一节点和关系样 */
.section-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.section-header .icon {
  width: 16px;
  height: 16px;
  color: #10b981;
}

.section-header h3 {
  margin: 0;
  font-size: 0.95rem;
  color: #374151;
  font-weight: 500;
}

.filter-item {
  display: flex;
  align-items: center;
  padding: 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.filter-item:hover {
  background: #f3f4f6;
}

.filter-item.active {
  background: #f0fdf4;
}

.type-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 12px;
}

.type-icon .icon {
  width: 20px;
  height: 20px;
}

.type-info {
  display: flex;
  flex-direction: column;
}

.type-label {
  font-weight: 500;
  color: #374151;
}

.type-count {
  font-size: 0.85rem;
  color: #6b7280;
}

.legend-item {
  display: flex;
  align-items: center;
  padding: 8px 12px;
}

.relation-line {
  width: 40px;
  height: 3px;
  border-radius: 2px;
  margin-right: 12px;
}

.relation-label {
  color: #374151;
}
</style> 
