<template>
  <div class="knowledge-graph">
    <div class="graph-container">
      <!-- 图谱容器 -->
      <div ref="graphRef" class="neo4j-graph"></div>
    </div>
    <div class="control-panel">
      <div class="search-box">
        <input v-model="searchQuery" placeholder="搜索节点..." @input="handleSearch">
      </div>
      <div class="filter-options">
        <h3>节点类型</h3>
        <div v-for="type in nodeTypes" :key="type.id" class="filter-item">
          <input type="checkbox" :id="type.id" v-model="type.checked">
          <label :for="type.id">{{ type.label }}</label>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as d3 from 'd3'
import axios from 'axios'

const graphRef = ref(null)
const searchQuery = ref('')
const nodeTypes = ref([
  { id: 'concept', label: '概念', checked: true },
  { id: 'entity', label: '实体', checked: true },
  { id: 'relation', label: '关系', checked: true }
])

// 从Neo4j获取数据
const fetchGraphData = async () => {
  try {
    const response = await axios.get('http://localhost:8000/flask/api/knowledge-graph')
    return response.data
  } catch (error) {
    console.error('获取图谱数据失败:', error)
    return null
  }
}

// 初始化图谱
const initGraph = (data) => {
  const width = graphRef.value.clientWidth
  const height = graphRef.value.clientHeight

  const svg = d3.select(graphRef.value)
    .append('svg')
    .attr('width', width)
    .attr('height', height)

  // 创建力导向图
  const simulation = d3.forceSimulation(data.nodes)
    .force('link', d3.forceLink(data.links).id(d => d.id))
    .force('charge', d3.forceManyBody().strength(-300))
    .force('center', d3.forceCenter(width / 2, height / 2))

  // 绘制连线
  const links = svg.append('g')
    .selectAll('line')
    .data(data.links)
    .enter()
    .append('line')
    .attr('stroke', '#999')
    .attr('stroke-opacity', 0.6)

  // 绘制节点
  const nodes = svg.append('g')
    .selectAll('circle')
    .data(data.nodes)
    .enter()
    .append('circle')
    .attr('r', 5)
    .attr('fill', d => getNodeColor(d.type))
    .call(drag(simulation))

  // 添加节点标签
  const labels = svg.append('g')
    .selectAll('text')
    .data(data.nodes)
    .enter()
    .append('text')
    .text(d => d.label)
    .attr('font-size', 12)
    .attr('dx', 8)
    .attr('dy', 4)

  // 更新位置
  simulation.on('tick', () => {
    links
      .attr('x1', d => d.source.x)
      .attr('y1', d => d.source.y)
      .attr('x2', d => d.target.x)
      .attr('y2', d => d.target.y)

    nodes
      .attr('cx', d => d.x)
      .attr('cy', d => d.y)

    labels
      .attr('x', d => d.x)
      .attr('y', d => d.y)
  })
}

// 节点拖拽功能
const drag = (simulation) => {
  const dragstarted = (event) => {
    if (!event.active) simulation.alphaTarget(0.3).restart()
    event.subject.fx = event.subject.x
    event.subject.fy = event.subject.y
  }

  const dragged = (event) => {
    event.subject.fx = event.x
    event.subject.fy = event.y
  }

  const dragended = (event) => {
    if (!event.active) simulation.alphaTarget(0)
    event.subject.fx = null
    event.subject.fy = null
  }

  return d3.drag()
    .on('start', dragstarted)
    .on('drag', dragged)
    .on('end', dragended)
}

// 获取节点颜色
const getNodeColor = (type) => {
  const colors = {
    concept: '#4CAF50',
    entity: '#2196F3',
    relation: '#FFC107'
  }
  return colors[type] || '#999'
}

onMounted(async () => {
  const data = await fetchGraphData()
  if (data) {
    initGraph(data)
  }
})

onUnmounted(() => {
  // 清理D3资源
  d3.select(graphRef.value).selectAll('*').remove()
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
  gap: 8px;
  margin-bottom: 8px;
}

.filter-item label {
  font-size: 0.9rem;
  color: #4b5563;
}
</style> 