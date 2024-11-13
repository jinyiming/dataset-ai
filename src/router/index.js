import { createRouter, createWebHistory } from 'vue-router'
import KnowledgeGraph from '../views/KnowledgeGraph.vue'

const routes = [
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

export default router 