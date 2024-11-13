<template>
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
</template>

<script setup>
import { ref } from 'vue'
import draggable from 'vuedraggable'
import { useRouter } from 'vue-router'

const router = useRouter()
const drag = ref(false)

const dockItems = ref([
  {
    id: 1,
    label: '问答录入',
    icon: 'M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H6l-2 2V4h16v12z',
    bgColor: '#10B981',
    active: false
  },
  {
    id: 2,
    label: '数据分析',
    icon: 'M4 19h16v2H4zm4-4h2v4H8zm-4-4h2v8H4zm8 0h2v8h-2zm4 0h2v8h-2zm-6-4h2v12h-2z',
    bgColor: '#6366F1',
    active: false
  },
  {
    id: 3,
    label: '知识图谱',
    icon: 'M17.5 3C15.57 3 14 4.57 14 6.5V8h-4V6.5C10 4.57 8.43 3 6.5 3S3 4.57 3 6.5 4.57 10 6.5 10H8v4H6.5C4.57 14 3 15.57 3 17.5S4.57 21 6.5 21s3.5-1.57 3.5-3.5V16h4v1.5c0 1.93 1.57 3.5 3.5 3.5s3.5-1.57 3.5-3.5-1.57-3.5-3.5-3.5H16v-4h1.5c1.93 0 3.5-1.57 3.5-3.5S19.43 3 17.5 3z',
    bgColor: '#F59E0B',
    active: true
  },
  {
    id: 4,
    label: '公文统计',
    icon: 'M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H6l-2 2V4h16v12z',
    bgColor: '#EC4899',
    active: false
  }
])

const handleIconClick = (element) => {
  dockItems.value.forEach(item => {
    item.active = item.id === element.id
  })

  if (element.label === '问答录入') {
    router.push('/')
  } else if (element.label === '数据分析') {
    router.push('/analysis')
  } else if (element.label === '知识图谱') {
    router.push('/knowledge-graph')
  } else if (element.label === '公文统计') {
    router.push('/document-stats')
  }
}
</script>

<style scoped>
.floating-dock {
  position: fixed;
  left: 50%;
  bottom: 20px;
  transform: translateX(-50%);
  z-index: 9999;
  pointer-events: none;
}

.icon-dock {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 8px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  pointer-events: auto;
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
  cursor: pointer;
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

.dock-item:hover {
  transform: translateY(-4px);
}

.dock-item:hover .dock-label {
  opacity: 1;
}

.dock-item:hover .dock-icon-wrapper {
  filter: brightness(1.1);
}

.dock-item.active .dock-icon-wrapper {
  transform: scale(1.1);
  box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.5);
}
</style> 