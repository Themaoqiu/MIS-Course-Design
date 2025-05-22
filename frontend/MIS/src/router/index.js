import { createRouter, createWebHistory } from 'vue-router';
import AppLayout from '@/components/layout/AppLayout.vue';
import DashboardView from '@/views/DashboardView.vue';
import MaterialsView from '@/views/MaterialsView.vue';
import InventoryView from '@/views/InventoryView.vue';
import InboundRecordsView from '@/views/InboundRecordsView.vue';
import OutboundRecordsView from '@/views/OutboundRecordsView.vue';

const routes = [
  {
    path: '/',
    component: AppLayout,
    children: [
      { 
        path: '', 
        name: 'Dashboard', 
        component: DashboardView, 
        meta: { title: '总览仪表盘' } 
      },
      { 
        path: 'materials', 
        name: 'Materials', 
        component: MaterialsView, 
        meta: { title: '物资管理' } 
      },
      { 
        path: 'inventory', 
        name: 'Inventory', 
        component: InventoryView, 
        meta: { title: '库存查看' } 
      },
      { 
        path: 'inbound', 
        name: 'InboundRecords', 
        component: InboundRecordsView, 
        meta: { title: '入库管理' } 
      },
      { 
        path: 'outbound', 
        name: 'OutboundRecords', 
        component: OutboundRecordsView, 
        meta: { title: '出库管理' } 
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

router.beforeEach((to, from, next) => {
  document.title = to.meta.title 
    ? `${to.meta.title} - 库存管理系统` 
    : '库存管理系统';
  next();
});

export default router;