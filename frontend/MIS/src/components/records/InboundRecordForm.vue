<template>
    <DialogContent class="sm:max-w-lg">
      <DialogHeader>
        <DialogTitle>新增入库记录</DialogTitle>
        <DialogDescription>
          填写物资入库的详细信息。系统将自动更新库存。
        </DialogDescription>
      </DialogHeader>
      <form @submit.prevent="handleSubmit" class="space-y-4 py-4">
        <div>
          <Label for="material_id">物资 <span class="text-destructive">*</span></Label>
          <Select v-model="form.material_id" required>
            <SelectTrigger id="material_id">
              <SelectValue placeholder="选择入库物资" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem v-for="material in materials" :key="material.id" :value="material.id.toString()">
                {{ material.name }} ({{ material.code }}) - 当前库存: {{ getMaterialStock(material.id) }}
              </SelectItem>
            </SelectContent>
          </Select>
          <p v-if="errors.material_id" class="text-sm text-destructive mt-1">{{ errors.material_id }}</p>
        </div>
  
        <div>
          <Label for="quantity">入库数量 <span class="text-destructive">*</span></Label>
          <Input id="quantity" type="number" v-model.number="form.quantity" required min="1" />
          <p v-if="errors.quantity" class="text-sm text-destructive mt-1">{{ errors.quantity }}</p>
        </div>
  
        <div>
          <Label for="inbound_order_number">入库单号</Label>
          <Input id="inbound_order_number" v-model="form.inbound_order_number" />
        </div>
  
        <div>
          <Label for="remarks">备注</Label>
          <Textarea id="remarks" v-model="form.remarks" />
        </div>
  
        <DialogFooter>
          <Button type="button" variant="outline" @click="$emit('close-form')">取消</Button>
          <Button type="submit" :disabled="isSubmitting">
              <Loader2 v-if="isSubmitting" class="w-4 h-4 mr-2 animate-spin" />
              {{ isSubmitting ? '提交中...' : '确认入库' }}
          </Button>
        </DialogFooter>
      </form>
    </DialogContent>
  </template>
  
  <script setup>
  import { ref, reactive, onMounted, defineEmits } from 'vue';
  import apiService from '@/services/apiService';
  import { Button } from '@/components/ui/button';
  import { Input } from '@/components/ui/input';
  import { Label } from '@/components/ui/label';
  import { Textarea } from '@/components/ui/textarea';
  import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
  import {
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogDescription,
    DialogFooter,
    // DialogClose,
  } from '@/components/ui/dialog';
  import { toast } from 'vue-sonner';
  import { Loader2 } from 'lucide-vue-next';
  
  const emit = defineEmits(['submit-success', 'close-form']);
  
  const materials = ref([]);
  const inventoryBalances = ref({}); // To store stock for selected material: { material_id: quantity }
  const isSubmitting = ref(false);
  const form = reactive({
    material_id: '',
    quantity: null,
    inbound_order_number: '',
    remarks: '',
  });
  const errors = reactive({});
  
  async function fetchMaterialsAndStock() {
  try {
    const materialsResponse = await apiService.getMaterials({ limit: 200, is_active: true }); // 假设后端已支持 is_active 和更大的 limit
    materials.value = materialsResponse.data.items;
    // ... (获取库存逻辑) ...
  } catch (err) { // 对应之前的行号约 96, 97
    console.error('Error fetching materials for form:', err); //
    // 正确使用 toast
    toast.error('加载可用物资列表失败');
  }
}
  
  function getMaterialStock(materialId) {
      return inventoryBalances.value[materialId] !== undefined ? inventoryBalances.value[materialId] : 'N/A';
  }
  
  function resetForm() {
      form.material_id = '';
      form.quantity = null;
      form.inbound_order_number = '';
      form.remarks = '';
      Object.keys(errors).forEach(key => delete errors[key]);
  }
  
  async function handleSubmit() {
    isSubmitting.value = true;
    Object.keys(errors).forEach(key => delete errors[key]);
  
    if (!form.material_id) errors.material_id = '请选择物资。';
    if (!form.quantity || form.quantity <= 0) errors.quantity = '入库数量必须大于0。'; //
  
    if (Object.keys(errors).length > 0) {
        isSubmitting.value = false;
        return;
    }
  
    const payload = {
        material_id: parseInt(form.material_id),
        quantity: form.quantity,
        inbound_order_number: form.inbound_order_number || null,
        remarks: form.remarks || null,
    };
  
    try {
      await apiService.createInboundRecord(payload); //
      // toast.success({ title: '成功', description: '入库操作已完成。' });
      resetForm();
      emit('submit-success');
    } catch (err) {
      console.error('Error creating inbound record:', err);
      const errorDetail = err.response?.data?.detail || '创建入库记录失败。';
      toast.error({ title: '提交失败', description: errorDetail, variant: 'destructive' });
    } finally {
      isSubmitting.value = false;
    }
  }
  
  onMounted(fetchMaterialsAndStock);
  </script>