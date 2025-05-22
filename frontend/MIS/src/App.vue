<template>
  <router-view />
  <Toaster richColors position="top-right"
  :toastOptions="{
      class: 'custom-toast-class', // 为所有 toast 添加一个通用自定义类
      classes: { // 为特定类型的 toast 添加类
        success: 'success-toast',
        error: 'error-toast',
      }
    }"
  />
</template>

<script setup>
import { onMounted } from 'vue';
import { Toaster } from 'vue-sonner';

// onMounted(() => {
//   document.documentElement.classList.add('root'); 
// });
</script>
