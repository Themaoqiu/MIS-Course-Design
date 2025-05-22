<template>
    <div class="space-y-6">
      <div class="flex items-center justify-between">
        <h2 class="text-2xl font-semibold">入库记录列表</h2>
        <Dialog :open="isFormOpen" @update:open="isFormOpen = $event">
          <DialogTrigger as-child>
            <Button @click="openNewRecordForm"><Plus class="w-4 h-4 mr-2" /> 新增入库</Button>
          </DialogTrigger>
          <InboundRecordForm @submit-success="handleFormSuccess" />
        </Dialog>
      </div>
  
      <div class="flex gap-2 mb-4 items-end">
        <div class="flex-1 max-w-xs">
          <Label for="filterMaterial">按物资过滤</Label>
          <Select v-model="filterMaterialId" @update:modelValue="debouncedFetchRecords">
            <SelectTrigger id="filterMaterial">
              <SelectValue placeholder="选择物资" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="">所有物资</SelectItem>
              <SelectItem v-for="material in availableMaterials" :key="material.id" :value="material.id.toString()">
                {{ material.name }} ({{ material.code }})
              </SelectItem>
            </SelectContent>
          </Select>
        </div>
         <Button variant="outline" @click="clearFilters">清除过滤</Button>
      </div>
  
      <InboundRecordsTable
        :records="records"
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
  import { ref, onMounted, watch } from 'vue';
  import apiService from '@/services/apiService';
  import InboundRecordsTable from '@/components/records/InboundRecordsTable.vue';
  import InboundRecordForm from '@/components/records/InboundRecordForm.vue';
  import { Button } from '@/components/ui/button';
  import { Dialog, DialogTrigger } from '@/components/ui/dialog';
  import { Label } from '@/components/ui/label';
  import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
  import { toast } from 'vue-sonner';
  import { Plus } from 'lucide-vue-next';
  
  const records = ref([]);
  const availableMaterials = ref([]);
  const loading = ref(true);
  const error = ref(null);
  const isFormOpen = ref(false);
  
  const filterMaterialId = ref('');
  // const filterStartTime = ref(null);
  // const filterEndTime = ref(null);
  
  const currentPage = ref(1);
  const limit = ref(10);
  const totalItems = ref(0);
  const totalPages = ref(0);
  
  let debounceTimer = null;
  
  async function fetchRecords() {
    loading.value = true;
    error.value = null;
    try {
      const params = {
        skip: (currentPage.value - 1) * limit.value,
        limit: limit.value,
        material_id: filterMaterialId.value ? parseInt(filterMaterialId.value) : undefined,
        // start_time: filterStartTime.value,
        // end_time: filterEndTime.value,
      };
      const response = await apiService.getInboundRecords(params); //
      // 假设后端返回 { items: [], total: 0, page: 0, size: 0, pages: 0 } 结构
      // 但后端 get_inbound_records 实际是直接返回 list，没有分页元数据
      // 为了演示分页，我们需要改造后端或模拟
      // 暂时假设后端改造完成，如果未改造，分页将不准确
      // records.value = response.data.items;
      // totalItems.value = response.data.total;
      // totalPages.value = response.data.pages;
  
      // 临时处理：如果后端直接返回列表
      records.value = response.data; // 假设这已经是当前页的数据
      // 需要手动获取总数（或估算）来实现分页，或者后端支持
      const countResponse = await apiService.getInboundRecords({ // 模拟获取总数
          material_id: filterMaterialId.value ? parseInt(filterMaterialId.value) : undefined,
          limit: 200 // 一个大数
      });
      totalItems.value = countResponse.data.length; // 这是一个不好的方法
      totalPages.value = Math.ceil(totalItems.value / limit.value);
  
  
    } catch (err) {
      console.error('Error fetching inbound records:', err);
      error.value = '加载入库记录失败。';
      toast('错误');
    } finally {
      loading.value = false;
    }
  }
  
  async function fetchAvailableMaterials() { // 对应之前的行号约 130, 133, 134
  try {
    const response = await apiService.getMaterials({ limit: 200, is_active: true }); 
    availableMaterials.value = response.data.items;
  } catch (err) { //
    console.error('Error fetching materials for filter:', err);
    toast.error('加载可用物资列表失败', {description: err.message || '请稍后再试。'});
  }
}
  
  
  function debouncedFetchRecords() {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
      currentPage.value = 1;
      fetchRecords();
    }, 500);
  }
  
  function clearFilters() {
      filterMaterialId.value = '';
      // filterStartTime.value = null;
      // filterEndTime.value = null;
      debouncedFetchRecords();
  }
  
  
  function prevPage() {
    if (currentPage.value > 1) {
      currentPage.value--;
      fetchRecords();
    }
  }
  
  function nextPage() {
    if (currentPage.value < totalPages.value) {
      currentPage.value++;
      fetchRecords();
    }
  }
  
  function openNewRecordForm() {
    isFormOpen.value = true;
  }
  
  function handleFormSuccess() {
    isFormOpen.value = false;
    fetchRecords();
    toast.success('入库记录已保存');
  }
  
  onMounted(() => {
      fetchRecords();
      fetchAvailableMaterials();
  });
  
  watch(filterMaterialId, debouncedFetchRecords);
  
  </script>