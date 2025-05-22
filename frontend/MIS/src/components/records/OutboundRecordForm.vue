<template>
    <DialogContent class="sm:max-w-lg">
      <DialogHeader>
        <DialogTitle>新增出库记录</DialogTitle>
        <DialogDescription>
          填写物资出库信息。系统将检查库存并自动更新。
        </DialogDescription>
      </DialogHeader>
      <form @submit.prevent="handleSubmit" class="space-y-4 py-4">
        <div>
          <Label for="out_material_id">物资 <span class="text-destructive">*</span></Label>
          <Select v-model="form.material_id" required @update:modelValue="handleMaterialSelect">
            <SelectTrigger id="out_material_id">
              <SelectValue placeholder="选择出库物资" />
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
          <Label for="out_quantity">出库数量 <span class="text-destructive">*</span></Label>
          <Input id="out_quantity" type="number" v-model.number="form.quantity" required min="1" :max="currentMaterialStock" />
          <p v-if="currentMaterialStock !== null && form.quantity > currentMaterialStock" class="text-sm text-destructive mt-1">
              出库数量不能超过当前库存 ({{ currentMaterialStock }})。
          </p>
          <p v-if="errors.quantity" class="text-sm text-destructive mt-1">{{ errors.quantity }}</p>
        </div>
  
        <div>
          <Label for="outbound_order_number">出库单号</Label>
          <Input id="outbound_order_number" v-model="form.outbound_order_number" />
        </div>
  
        <div>
          <Label for="recipient">领用人/客户</Label>
          <Input id="recipient" v-model="form.recipient" />
        </div>
  
        <div>
          <Label for="out_remarks">备注</Label>
          <Textarea id="out_remarks" v-model="form.remarks" />
        </div>
  
        <DialogFooter>
          <Button type="button" variant="outline" @click="$emit('close-form')">取消</Button>
          <Button type="submit" :disabled="isSubmitting || (form.quantity > currentMaterialStock && currentMaterialStock !== null) ">
              <Loader2 v-if="isSubmitting" class="w-4 h-4 mr-2 animate-spin" />
              {{ isSubmitting ? '提交中...' : '确认出库' }}
          </Button>
        </DialogFooter>
      </form>
    </DialogContent>
  </template>
  
  <script setup>
  import { ref, reactive, onMounted, defineEmits, computed } from 'vue';
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
  } from '@/components/ui/dialog';
  import { toast } from 'vue-sonner';
  import { Loader2 } from 'lucide-vue-next';
  
  const emit = defineEmits(['submit-success', 'close-form']);
  
  const materials = ref([]);
  const inventoryBalances = ref({}); // { material_id: quantity }
  const isSubmitting = ref(false);
  const form = reactive({
    material_id: '',
    quantity: null,
    outbound_order_number: '',
    recipient: '',
    remarks: '',
  });
  const errors = reactive({});
  
  const currentMaterialStock = computed(() => {
      if (form.material_id && inventoryBalances.value[form.material_id] !== undefined) {
          return inventoryBalances.value[form.material_id];
      }
      return null; // Or a very large number if you don't want to disable button initially
  });
  
  async function fetchMaterialsAndStock() {
    try {
      const materialsResponse = await apiService.getMaterials({ limit: 200, is_active: true });
      materials.value = materialsResponse.data.items;
  
      const inventoryResponse = await apiService.getInventoryBalances({ limit: 200 });
      inventoryResponse.data.forEach(item => {
          inventoryBalances.value[item.material_id] = item.current_quantity;
      });
    } catch (err) {
      console.error('Error fetching materials for form:', err);
      toast.error('加载物资列表失败');
    }
  }
  
  function getMaterialStock(materialId) {
      return inventoryBalances.value[materialId] !== undefined ? inventoryBalances.value[materialId] : 'N/A';
  }
  
  function handleMaterialSelect(selectedMaterialId) {
      form.material_id = selectedMaterialId; // Ensure form is updated
      // Reset quantity if material changes, or validate existing quantity
      if (form.quantity && currentMaterialStock.value !== null && form.quantity > currentMaterialStock.value) {
          // form.quantity = currentMaterialStock.value; // Optionally cap it
      }
  }
  
  
  function resetForm() {
      form.material_id = '';
      form.quantity = null;
      form.outbound_order_number = '';
      form.recipient = '';
      form.remarks = '';
      Object.keys(errors).forEach(key => delete errors[key]);
  }
  
  async function handleSubmit() {
    isSubmitting.value = true;
    Object.keys(errors).forEach(key => delete errors[key]);
  
    if (!form.material_id) errors.material_id = '请选择物资。';
    if (!form.quantity || form.quantity <= 0) errors.quantity = '出库数量必须大于0。'; //
    if (currentMaterialStock.value !== null && form.quantity > currentMaterialStock.value) {
        errors.quantity = `出库数量不能超过当前库存 (${currentMaterialStock.value})。`;
    }
  
  
    if (Object.keys(errors).length > 0) {
        isSubmitting.value = false;
        return;
    }
  
    const payload = {
        material_id: parseInt(form.material_id),
        quantity: form.quantity,
        outbound_order_number: form.outbound_order_number || null,
        recipient: form.recipient || null,
        remarks: form.remarks || null,
    };
  
    try {
      await apiService.createOutboundRecord(payload); //
      toast.success('出库操作已完成');
      resetForm();
      emit('submit-success');
      // Refresh stock for the dropdown after successful outbound
      if (payload.material_id && inventoryBalances.value[payload.material_id] !== undefined) {
          inventoryBalances.value[payload.material_id] -= payload.quantity;
      }
    } catch (err) {
      console.error('Error creating outbound record:', err);
      const errorDetail = err.response?.data?.detail || '创建出库记录失败。';
      toast.error('提交失败');
    } finally {
      isSubmitting.value = false;
    }
  }
  
  onMounted(fetchMaterialsAndStock);
  </script>