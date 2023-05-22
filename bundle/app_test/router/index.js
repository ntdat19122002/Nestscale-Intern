import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import NotFound from '../views/NotFound.vue'
import DetailView from '../views/DetailView.vue'
import TermView from '../views/TermView.vue'

const router = createRouter({
  history: createWebHistory('/'),
  routes: [
    {
      path: '/bundle',
      name: 'home',
      component: HomeView
    },
    {
      path: '/bundle/shop/page/:page',
      name: 'shopPage',
      component: () => import('../views/ShopView.vue')
    },
    {
      path: '/bundle/product/:id',
      name: 'detail',
      component: DetailView,
      props: true
    },
    {
      path: '/bundle/contact',
      name: 'contact',
      component: () => import('../views/ContactView.vue')
    },
    {
      path: '/bundle/term',
      name: 'term',
      component: TermView
    },
    {
      path: '/bundle/cart',
      name: 'cart',
      component: () => import('../views/CartView.vue')
    },
    {
      path: '/bundle/:catchAll(.*)',
      name: 'NotFound',
      component: NotFound
    }
  ]
})

export default router
