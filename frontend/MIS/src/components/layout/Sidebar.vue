<template>
    <aside class="hidden w-64 border-r bg-background md:block shrink-0">
      <div class="flex flex-col h-full">
        <div class="flex items-center h-16 px-6 border-b">
          <router-link to="/" class="flex items-center gap-2 font-semibold">
            <Package2 class="w-6 h-6 text-primary" />
            <span class="text-sidebar-foreground">库存管理</span>
          </router-link>
        </div>
        <nav class="flex-1 px-4 py-4 space-y-1">
          <router-link
            v-for="item in navItems"
            :key="item.name"
            :to="item.path"
            custom
            v-slot="{ href, navigate, isActive }"
          >
            <a
              :href="href"
              @click="navigate"
              class="flex items-center px-3 py-2 text-sm font-medium rounded-md"
              :class="[
                isActive
                  ? 'bg-primary text-primary-foreground'
                  : 'text-muted-foreground hover:bg-muted hover:text-foreground',
              ]"
            >
              <component :is="item.icon" class="w-5 h-5 mr-3" />
              {{ item.name }}
            </a>
          </router-link>
        </nav>
      </div>
    </aside>
  </template>
  
  <script setup>
  import { Home, Package, Archive, ArrowRightLeft, ListChecks } from 'lucide-vue-next'; // lucide-vue-next 图标库
  
  // 用于 Logo 的示例图标
  const Package2 = Package;
  
  const navItems = [
    { name: '总览仪表盘', path: '/', icon: Home },
    { name: '物资管理', path: '/materials', icon: Package },
    { name: '库存查看', path: '/inventory', icon: Archive },
    { name: '入库管理', path: '/inbound', icon: ArrowRightLeft }, // 可以换个更合适的图标
    { name: '出库管理', path: '/outbound', icon: ListChecks }, // 可以换个更合适的图标
  ];
  </script>