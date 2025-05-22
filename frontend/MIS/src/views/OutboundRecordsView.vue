<template>
    <div class="space-y-6">
      <div class="flex items-center justify-between">
        <h2 class="text-2xl font-semibold">出库记录列表</h2>
        <Dialog :open="isFormOpen" @update:open="isFormOpen = $event">
          <DialogTrigger as-child>
            <Button @click="openNewRecordForm"><Minus class="w-4 h-4 mr-2" /> 新增出库</Button>
          </DialogTrigger>
          <OutboundRecordForm @submit-success="handleFormSuccess" />
        </Dialog>
      </div>
  
      <div class="flex gap-2 mb-4 items-end">
        <div class="flex-1 max-w-xs">
          <Label for="filterMaterialOut">按物资过滤</Label>
          <Select v-model="filterMaterialId" @update:modelValue="debouncedFetchRecords">
            <SelectTrigger id="filterMaterialOut">
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
  
      <OutboundRecordsTable
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
  import OutboundRecordsTable from '@/components/records/OutboundRecordsTable.vue'; // 需要创建
  import OutboundRecordForm from '@/components/records/OutboundRecordForm.vue'; // 需要创建
  import { Button } from '@/components/ui/button';
  import { Dialog, DialogTrigger } from '@/components/ui/dialog';
  import { Label } from '@/components/ui/label';
  import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
  import { toast } from 'vue-sonner';
  import { Minus } from 'lucide-vue-next'; // Changed icon
  
  
  const records = ref([]);
  const availableMaterials = ref([]);
  const loading = ref(true);
  const error = ref(null);
  const isFormOpen = ref(false);
  
  const filterMaterialId = ref('');
  
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
      };
      const response = await apiService.getOutboundRecords(params); //
      // 同入库，假设后端改造完成支持分页元数据
      // records.value = response.data.items;
      // totalItems.value = response.data.total;
      // totalPages.value = response.data.pages;
  
      // 临时处理
      records.value = response.data;
      const countResponse = await apiService.getOutboundRecords({
          material_id: filterMaterialId.value ? parseInt(filterMaterialId.value) : undefined,
          limit: 200
      });
      totalItems.value = countResponse.data.length;
      totalPages.value = Math.ceil(totalItems.value / limit.value);
  
  
    } catch (err) {
      console.error('Error fetching outbound records:', err);
      error.value = '加载出库记录失败。';
      toast.error('加载出库记录失败');
    } finally {
      loading.value = false;
    }
  }
  
  async function fetchAvailableMaterials() {
    try {
      const response = await apiService.getMaterials({ limit: 200 });
      availableMaterials.value = response.data.items;
    } catch (err) {
      console.error('Error fetching materials for filter:', err);
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
    toast.success('出库记录已保存');
  }
  
  onMounted(() => {
      fetchRecords();
      fetchAvailableMaterials();
  });
  watch(filterMaterialId, debouncedFetchRecords);
  
  </script>