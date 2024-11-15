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
    active: false
  },
  {
    id: 4,
    label: '公文统计',
    icon: 'M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H6l-2 2V4h16v12z',
    bgColor: '#EC4899',
    active: false
  },
  {
    id: 5,
    label: '系统配置',
    icon: 'M19.14 12.94c.04-.3.06-.61.06-.94 0-.32-.02-.64-.07-.94l2.03-1.58c.18-.14.23-.41.12-.61l-1.92-3.32c-.12-.22-.37-.29-.59-.22l-2.39.96c-.5-.38-1.03-.7-1.62-.94l-.36-2.54c-.04-.24-.24-.41-.48-.41h-3.84c-.24 0-.43.17-.47.41l-.36 2.54c-.59.24-1.13.57-1.62.94l-2.39-.96c-.22-.08-.47 0-.59.22L2.74 8.87c-.12.21-.08.47.12.61l2.03 1.58c-.05.3-.09.63-.09.94s.02.64.07.94l-2.03 1.58c-.18.14-.23.41-.12.61l1.92 3.32c.12.22.37.29.59.22l2.39-.96c.5.38 1.03.7 1.62.94l.36 2.54c.05.24.24.41.48.41h3.84c.24 0 .44-.17.47-.41l.36-2.54c.59-.24 1.13-.56 1.62-.94l2.39.96c.22.08.47 0 .59-.22l1.92-3.32c.12-.22.07-.47-.12-.61l-2.01-1.58zM12 15.6c-1.98 0-3.6-1.62-3.6-3.6s1.62-3.6 3.6-3.6 3.6 1.62 3.6 3.6-1.62 3.6-3.6 3.6z',
    bgColor: '#8B5CF6',
    active: false
  },
  {
    id: 6,
    label: '模版管理',
    icon: 'M14 2H6c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V8l-6-6zM6 20V4h7v5h5v11H6z',
    bgColor: '#3B82F6',
    active: false
  },
  {
    id: 7,
    label: '搜索引擎',
    icon: 'M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z',
    bgColor: '#EF4444',
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
  } else if (element.label === '系统配置') {
    router.push('/settings')
  } else if (element.label === '模版管理') {
    router.push('/settings')
  } else if (element.label === '搜索引擎') {
    router.push('/search')
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