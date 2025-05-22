<template>
    <div class="space-y-6">
      <div class="flex items-center justify-between">
        <h2 class="text-2xl font-semibold">库存余额列表</h2>
        </div>
  
      <InventoryTable
        :inventories="inventories"
        :loading="loading"
        :error="error"
      />
  
      <div class="flex items-center justify-end space-x-2 py-4" v-if="totalPages > 0">
          <Button
            variant="outline"
            size="sm"
            @click="prevPage"
            :disabled="currentPage === 1"
          >
            上一页
          </Button>
          <span>第 {{ currentPage }} 页 / 共 {{ totalPages }} 页 (共 {{ totalItems }} 条)</span>
          <Button
            variant="outline"
            size="sm"
            @click="nextPage"
            :disabled="currentPage === totalPages"
          >
            下一页
          </Button>
        </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, computed } from 'vue';
  import apiService from '@/services/apiService';
  import InventoryTable from '@/components/inventory/InventoryTable.vue';
  import { Button } from '@/components/ui/button';
  // import { Input } from '@/components/ui/input'; // 如果添加搜索
  import { toast } from 'vue-sonner';
  
  const allInventories = ref([]); // 用于存储所有获取到的库存数据
  const loading = ref(true);
  const error = ref(null);
  
  const currentPage = ref(1);
  const limit = ref(10); // 每页显示数量
  const totalItems = computed(() => allInventories.value.length); // 后端此接口不直接返回total，前端分页
  const totalPages = computed(() => Math.ceil(totalItems.value / limit.value));
  
  // 前端分页的当前页数据
  const inventories = computed(() => {
    const start = (currentPage.value - 1) * limit.value;
    const end = start + limit.value;
    return allInventories.value.slice(start, end);
  });
  
  
  // 后端 /inventory-balances/ 接口目前不直接支持 total 和 pages，它是简单分页
  // 如果数据量很大，后端需要改造此接口以支持真正的分页 (返回 total, pages, items)
  // 当前实现是获取所有数据后在前端进行分页，这对于大量数据不理想
  async function fetchInventories() {
    loading.value = true;
    error.value = null;
    try {
      // 假设我们一次性获取较多数据，例如 limit=200 (后端API默认是100，可调整)
      // 或者循环获取直到没有数据，但更推荐后端支持完整分页
      const response = await apiService.getInventoryBalances({ skip: 0, limit: 200 }); 
      allInventories.value = response.data;
      // 如果后端支持完整分页，这里应该是:
      // inventories.value = response.data.items;
      // totalItems.value = response.data.total;
      // totalPages.value = response.data.pages;
    } catch (err) {
      console.error('Error fetching inventories:', err);
      error.value = '加载库存列表失败。';
      toast({ title: '错误', description: error.value, variant: 'destructive' });
    } finally {
      loading.value = false;
    }
  }
  
  // let debounceTimer = null;
  // function debouncedFetchInventories() {
  //   clearTimeout(debounceTimer);
  //   debounceTimer = setTimeout(() => {
  //     currentPage.value = 1;
  //     fetchInventories();
  //   }, 500);
  // }
  
  function prevPage() {
    if (currentPage.value > 1) {
      currentPage.value--;
    }
  }
  
  function nextPage() {
    if (currentPage.value < totalPages.value) {
      currentPage.value++;
    }
  }
  
  onMounted(fetchInventories);
  </script>