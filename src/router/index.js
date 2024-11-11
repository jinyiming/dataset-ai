import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import SettingsPage from '../views/SettingsPage.vue'
import DataAnalysis from '../views/DataAnalysis.vue'
import KnowledgeGraph from '../views/KnowledgeGraph.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: {
      title: 'Data Search'
    }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: SettingsPage,
    meta: {
      title: 'Data Search - 设置'
    }
  },
  {
    path: '/analysis',
    name: 'Analysis',
    component: DataAnalysis,
    meta: {
      title: 'Data Search - 数据分析'
    }
  },
  {
    path: '/knowledge-graph',
    name: 'KnowledgeGraph',
    component: KnowledgeGraph,
    meta: {
      title: 'AI 问答系统 - 知识图谱'
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 