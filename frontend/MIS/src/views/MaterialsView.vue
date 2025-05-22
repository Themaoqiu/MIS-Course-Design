<template>
    <div class="space-y-6">
      <div class="flex items-center justify-between">
        <h2 class="text-2xl font-semibold">物资列表</h2>
        <Dialog :open="isAddMaterialDialogOpen" @update:open="isAddMaterialDialogOpen = $event">
        <DialogTrigger as-child>
          <Button @click="openAddMaterialDialog"><Plus class="w-4 h-4 mr-2" /> 添加物资</Button>
        </DialogTrigger>
        <MaterialForm
          :key="'add-material'" 
          @submit-success="handleFormSuccess"
          @close-dialog="handleFormCancel"
        />
      </Dialog>
    </div>
  
      <div class="flex gap-2 mb-4">
        <Input type="text" placeholder="按编码搜索..." v-model="searchCode" @input="debouncedFetchMaterials" class="max-w-xs" />
        <Input type="text" placeholder="按名称搜索..." v-model="searchName" @input="debouncedFetchMaterials" class="max-w-xs" />
      </div>
  
      <MaterialsTable
        :materials="materials"
        :loading="loading"
        :error="error"
        @edit="openEditDialog"
        @delete="handleDeleteMaterial"
      />
  
      <div class="flex items-center justify-end space-x-2 py-4" v-if="totalPages > 1">
          <Button
            variant="outline"
            size="sm"
            @click="prevPage"
            :disabled="currentPage === 1"
          >
            上一页
          </Button>
          <span>第 {{ currentPage }} 页 / 共 {{ totalPages }} 页</span>
          <Button
            variant="outline"
            size="sm"
            @click="nextPage"
            :disabled="currentPage === totalPages"
          >
            下一页
          </Button>
        </div>
  
        <Dialog :open="isEditDialogOpen" @update:open="isEditDialogOpen = $event">
      <MaterialForm
        :key="editingMaterialId"
        :material-id="editingMaterialId"
        @submit-success="handleFormSuccess"
        @close-dialog="handleFormCancel"
      />
    </Dialog>
  </div>
</template>
  
<script setup>
  import { ref, onMounted, watch } from 'vue';
  import apiService from '@/services/apiService';
  import MaterialsTable from '@/components/materials/MaterialsTable.vue';
  import MaterialForm from '@/components/materials/MaterialForm.vue';
  import { Button } from '@/components/ui/button';
  import { Input } from '@/components/ui/input';
  import { Dialog, DialogTrigger } from '@/components/ui/dialog';
  import { toast } from 'vue-sonner';
  import { Plus } from 'lucide-vue-next';


  const materials = ref([]);
  const loading = ref(true);
  const error = ref(null);
  const isAddMaterialDialogOpen = ref(false);
  const isEditDialogOpen = ref(false); 
  const editingMaterialId = ref(null);

  const searchCode = ref('');
  const searchName = ref('');
  const currentPage = ref(1);
  const limit = ref(10); // 每页数量
  const totalItems = ref(0);
  const totalPages = ref(0);

  let debounceTimer = null;

  async function fetchMaterials() {
  loading.value = true;
  error.value = null;
  try {
    const params = {
      skip: (currentPage.value - 1) * limit.value,
      limit: limit.value,
      code: searchCode.value || undefined,
      name: searchName.value || undefined,
    };
    const response = await apiService.getMaterials(params);

    if (response && response.data && Array.isArray(response.data.items)) {
      materials.value = response.data.items;
      totalItems.value = response.data.total !== undefined ? response.data.total : 0;
      totalPages.value = response.data.pages !== undefined ? response.data.pages : 0;
    } else {
      console.error("获取物资失败或响应数据格式不正确:", response);
      materials.value = [];
      totalItems.value = 0;
      totalPages.value = 0;
      error.value = '获取物资数据格式不正确。';
      
    }
  } catch (err) {
    console.error('请求物资列表时出错:', err);
    error.value = '加载物资列表失败，请检查网络或联系管理员。';
    materials.value = []; 
    totalItems.value = 0;
    totalPages.value = 0;
   
  } finally {
    loading.value = false;
  }
  }

  function debouncedFetchMaterials() {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
      currentPage.value = 1; // 重置到第一页
      fetchMaterials();
    }, 500); // 500ms 延迟
  }

  function handleFormCancel() {
  closeAllDialogs(); // 调用一个统一的关闭函数
}

  function prevPage() {
    if (currentPage.value > 1) {
      currentPage.value--;
      fetchMaterials();
    }
  }

  function nextPage() {
    if (currentPage.value < totalPages.value) {
      currentPage.value++;
      fetchMaterials();
    }
  }

  function handleFormSuccess() {
    closeAllDialogs();
    isEditDialogOpen.value = false;
    editingMaterialId.value = null;
    fetchMaterials();
    toast.success('物资信息已保存');
  }

  function openEditDialog(materialId) {
    editingMaterialId.value = materialId;
    isEditDialogOpen.value = true;
  }

  function handleDeleteMaterial(materialId) {
    if (confirm('确定要删除此物资吗？其库存余额必须为零。')) {
      try {
        apiService.deleteMaterial(materialId);
        toast.success('删除成功');
        fetchMaterials();
        window.location.reload();
      } catch (err) {
        console.error('Error deleting material:', err);
        const detail = err.response?.data?.detail || '删除物资失败。';
        toast.warning('删除物资失败，可能是库存不为0或存在过往出入库记录');
      }
    }
  }

  function closeAllDialogs() {
  isAddMaterialDialogOpen.value = false;
  isEditDialogOpen.value = false;
  editingMaterialId.value = null; 
}
  onMounted(fetchMaterials);

  watch([searchCode, searchName], () => {
      // 不需要立即调用，debouncedFetchMaterials 会处理
  });
</script>