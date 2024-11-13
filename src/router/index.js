import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import DataAnalysis from '../views/DataAnalysis.vue'
import DocumentStats from '../views/DocumentStats.vue'
import KnowledgeGraph from '../views/KnowledgeGraph.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/analysis',
    name: 'DataAnalysis',
    component: DataAnalysis
  },
  {
    path: '/document-stats',
    name: 'DocumentStats',
    component: DocumentStats
  },
  {
    path: '/knowledge-graph',
    name: 'KnowledgeGraph',
    component: KnowledgeGraph
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 添加路由调试
router.beforeEach((to, from, next) => {
  console.log('路由变化:', { from: from.path, to: to.path })
  next()
})

export default router 