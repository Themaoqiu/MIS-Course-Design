<template>
  <div class="flex h-screen bg-muted/40">
    <Sidebar />
    <div class="flex flex-col flex-1 overflow-hidden">
      <header class="flex items-center h-16 px-6 border-b bg-background shrink-0">
        <h1 class="text-xl font-semibold">{{ $route.meta.title || '库存管理' }}</h1>
      </header>
      <main class="flex-1 p-6 overflow-auto">
        <router-view v-slot="{ Component, route }">
          <transition
            enter-active-class="transition-opacity duration-300 ease-out"
            enter-from-class="opacity-0"
            enter-to-class="opacity-100"
            leave-active-class="transition-opacity duration-200 ease-in"
            leave-from-class="opacity-100"
            leave-to-class="opacity-0"
            mode="out-in"
          >
            <keep-alive>
              <component :is="Component" :key="route.path" />
            </keep-alive>
          </transition>
        </router-view>
      </main>
    </div>
  </div>
</template>

<script setup>
import Sidebar from './Sidebar.vue';
// 如果要在 <script setup> 中访问 $route, 需要从 vue-router 导入 useRoute
// import { useRoute } from 'vue-router';
// const route = useRoute(); // 然后在模板中用 route.meta.title
// 不过，在模板中直接用 $route.meta.title 通常是可行的
</script>