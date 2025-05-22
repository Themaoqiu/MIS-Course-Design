<template>
    <DialogContent class="sm:max-w-lg">
      <DialogHeader>
        <DialogTitle>{{ isEditMode ? '编辑物资' : '添加新物资' }}</DialogTitle>
        <DialogDescription>
          {{ isEditMode ? '修改物资的详细信息。' : '填写新物资的详细信息。' }}
        </DialogDescription>
      </DialogHeader>
      <form @submit.prevent="handleSubmit" class="space-y-4 py-4">
        <div>
          <Label for="code">物资编码 <span class="text-destructive">*</span></Label>
          <Input id="code" v-model="form.code" required />
          <p v-if="errors.code" class="text-sm text-destructive mt-1">{{ errors.code }}</p>
        </div>
        <div>
          <Label for="name">物资名称 <span class="text-destructive">*</span></Label>
          <Input id="name" v-model="form.name" required />
           <p v-if="errors.name" class="text-sm text-destructive mt-1">{{ errors.name }}</p>
        </div>
        <div>
          <Label for="model">型号规格</Label>
          <Input id="model" v-model="form.model" />
        </div>
        <div>
          <Label for="unit">单位</Label>
          <Input id="unit" v-model="form.unit" />
        </div>
        <div>
          <Label for="supplier">供应商</Label>
          <Input id="supplier" v-model="form.supplier" />
        </div>
        <div>
          <Label for="remarks">备注</Label>
          <Textarea id="remarks" v-model="form.remarks" />
        </div>
         <div class="flex items-center space-x-2">
          <Checkbox id="is_active" v-model:checked="form.is_active" />
          <label
            for="is_active"
            class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
          >
            是否启用
          </label>
        </div>
        <DialogFooter>
          <Button type="button" variant="outline" @click="handleCancel">取消</Button>
          <Button type="submit" :disabled="isSubmitting">
              <Loader2 v-if="isSubmitting" class="w-4 h-4 mr-2 animate-spin" />
              {{ isSubmitting ? (isEditMode ? '保存中...' : '添加中...') : (isEditMode ? '保存更改' : '确认添加') }}
          </Button>
        </DialogFooter>
      </form>
    </DialogContent>
  </template>
  
  <script setup>
  import { ref, reactive, watchEffect, defineEmits, defineProps, getCurrentInstance } from 'vue';
  import apiService from '@/services/apiService';
  import { Button } from '@/components/ui/button';
  import { Input } from '@/components/ui/input';
  import { Label } from '@/components/ui/label';
  import { Textarea } from '@/components/ui/textarea';
  import { Checkbox } from '@/components/ui/checkbox';
  import {
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogDescription,
    DialogFooter,
    // DialogClose, // Not needed if controlling open state from parent
  } from '@/components/ui/dialog';
  import { toast } from 'vue-sonner';
  import { Loader2 } from 'lucide-vue-next';
  
  const props = defineProps({
    materialId: {
      type: Number,
      default: null,
    },
  });
  const emit = defineEmits(['submit-success', 'close-dialog']);
  const instance = getCurrentInstance(); // To control dialog open state
  
  const isEditMode = ref(false);
  const isSubmitting = ref(false);
  const form = reactive({
    code: '',
    name: '',
    model: '',
    unit: '',
    supplier: '',
    remarks: '',
    is_active: true,
  });
  const errors = reactive({}); // For field-specific errors
  
  function resetForm() {
      form.code = '';
      form.name = '';
      form.model = '';
      form.unit = '';
      form.supplier = '';
      form.remarks = '';
      form.is_active = true;
      Object.keys(errors).forEach(key => delete errors[key]);
  }
  
  watchEffect(async () => {
    resetForm();
    if (props.materialId) {
      isEditMode.value = true;
      try {
        const response = await apiService.getMaterialById(props.materialId); //
        const data = response.data;
        form.code = data.code;
        form.name = data.name;
        form.model = data.model || '';
        form.unit = data.unit || '';
        form.supplier = data.supplier || '';
        form.remarks = data.remarks || '';
        form.is_active = data.is_active;
      } catch (err) {
        console.error('Error fetching material for edit:', err);
        toast({ title: '错误', description: '加载物资信息失败。', variant: 'destructive' });
        closeDialog();
      }
    } else {
      isEditMode.value = false;
    }
  });
  
  async function handleSubmit() {
    isSubmitting.value = true;
    Object.keys(errors).forEach(key => delete errors[key]); // Clear previous errors
  
    // Basic frontend validation
    if (!form.code.trim()) errors.code = '物资编码不能为空。';
    if (!form.name.trim()) errors.name = '物资名称不能为空。';
    if (Object.keys(errors).length > 0) {
        isSubmitting.value = false;
        return;
    }
  
    const payload = { ...form };
  
    try {
      if (isEditMode.value) {
        await apiService.updateMaterial(props.materialId, payload); //
      } else {
        await apiService.createMaterial(payload); //
      }
      emit('submit-success');
      closeDialog();
    } catch (err) {
      console.error('Error submitting material form:', err);
      const errorDetail = err.response?.data?.detail;
      if (typeof errorDetail === 'string') {
          if (errorDetail.includes("物资编码") && errorDetail.includes("已存在")) {
              errors.code = errorDetail;
          } else {
            toast.error('物资编码已存在');
          }
      } else {
        // toast.error(errorDetail);
      }
    } finally {
      isSubmitting.value = false;
    }
  }
  
  function handleCancel() {
  emit('close-dialog'); // 发出 'close-dialog' 事件
}
  </script>