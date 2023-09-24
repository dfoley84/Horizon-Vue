import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'horizon',
    component: () => import(/* webpackChunkName: "about" */ '../views/HorizonView.vue')
  },
  {
    path: '/search',
    name: 'search',
    component: () => import(/* webpackChunkName: "about" */ '../views/SearchView.vue')
  },
  {
    path: '/:catchAll(.*)',
    name: 'NotFound',
    component: () => import(/* webpackChunkName: "notfound" */ '../views/404View.vue')
  },
  {
    path: '/terminal',
    name: 'terminal',
    component: () => import(/* webpackChunkName: "terminal" */ '../views/TerminalView.vue'),
    meta: { hideUI: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router;
