<template>
    <div class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
      <Card v-if="summary.material_types_count !== null">
        <CardHeader class="flex flex-row items-center justify-between pb-2 space-y-0">
          <CardTitle class="text-sm font-medium">物资种类总数</CardTitle>
          <Package class="w-4 h-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div class="text-2xl font-bold">{{ summary.material_types_count }}</div>
          <p class="text-xs text-muted-foreground">系统中已定义的物资种类</p>
        </CardContent>
      </Card>
  
      <Card v-if="summary.total_stock_quantity !== null">
        <CardHeader class="flex flex-row items-center justify-between pb-2 space-y-0">
          <CardTitle class="text-sm font-medium">当前库存总量</CardTitle>
          <Archive class="w-4 h-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div class="text-2xl font-bold">{{ summary.total_stock_quantity }}</div>
          <p class="text-xs text-muted-foreground">所有物资当前库存数量的总和</p>
        </CardContent>
      </Card>
  
      <Card v-if="summary.stock_alert_count !== null">
        <CardHeader class="flex flex-row items-center justify-between pb-2 space-y-0">
          <CardTitle class="text-sm font-medium">库存预警数量</CardTitle>
          <AlertTriangle class="w-4 h-4 text-destructive" />
        </CardHeader>
        <CardContent>
          <div class="text-2xl font-bold">{{ summary.stock_alert_count }}</div>
          <p class="text-xs text-muted-foreground">低于最小库存预警线的物资种类</p>
        </CardContent>
      </Card>
  
      <div v-if="loading" class="col-span-full text-center py-10">
        <p>加载中...</p>
      </div>
      <div v-if="error" class="col-span-full text-center py-10 text-destructive">
        <p>加载数据失败: {{ error }}</p>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import apiService from '@/services/apiService';
  import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
  import { Package, Archive, AlertTriangle } from 'lucide-vue-next';
  
  const summary = ref({
    material_types_count: null,
    total_stock_quantity: null,
    stock_alert_count: null,
  });
  const loading = ref(true);
  const error = ref(null);
  
  async function fetchSummary() {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiService.getDashboardSummary(); //
      summary.value = response.data;
    } catch (err) {
      console.error('Error fetching dashboard summary:', err);
      error.value = err.message;
    } finally {
      loading.value = false;
    }
  }
  
  onMounted(fetchSummary);
  </script>