<template>
  <Card>
    <CardContent class="p-0">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead class="text-center">ID</TableHead>
            <TableHead class="text-center">编码</TableHead>
            <TableHead class="text-center">名称</TableHead>
            <TableHead class="text-center">型号</TableHead>
            <TableHead class="text-center">单位</TableHead>
            <TableHead class="text-center">供应商</TableHead>
            <TableHead class="text-center">状态</TableHead>
            <TableHead class="text-right">操作</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          <template v-if="loading">
            <TableRow>
              <TableCell :colspan="8" class="h-24 text-center">正在加载...</TableCell>
            </TableRow>
          </template>
          <template v-else-if="error">
            <TableRow>
              <TableCell :colspan="8" class="h-24 text-center text-destructive">{{ error }}</TableCell>
            </TableRow>
          </template>
          <template v-else-if="!materials || materials.length === 0">
            <TableRow>
              <TableCell :colspan="8" class="h-24 text-center">暂无物资数据。</TableCell>
            </TableRow>
          </template>
          <template v-else>
            <TableRow v-for="material in materials" :key="material.id">
              <TableCell class="text-center">{{ material.id }}</TableCell>
              <TableCell class="text-center">{{ material.code }}</TableCell>
              <TableCell class="font-medium text-center">{{ material.name }}</TableCell>
              <TableCell class="text-center">{{ material.model || '-' }}</TableCell>
              <TableCell class="text-center">{{ material.unit || '-' }}</TableCell>
              <TableCell class="text-center">{{ material.supplier || '-' }}</TableCell>
              <TableCell class="text-center"> 
                <Badge :variant="material.is_active ? 'outline' : 'destructive'">
                  {{ material.is_active ? '启用' : '禁用' }}
                </Badge>
              </TableCell>
              <TableCell class="text-right space-x-2"> 
                <Button variant="outline" size="sm" @click="$emit('edit', material.id)">
                  <FilePenLine class="w-4 h-4 mr-1" /> 编辑
                </Button>
                <Button variant="destructive" size="sm" @click="$emit('delete', material.id)">
                  <Trash2 class="w-4 h-4 mr-1" /> 删除
                </Button>
              </TableCell>
            </TableRow>
          </template>
        </TableBody>
      </Table>
    </CardContent>
  </Card>
</template>

<script setup>
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { FilePenLine, Trash2 } from 'lucide-vue-next'; // 确保导入了图标

defineProps({
  materials: {
    type: Array,
    required: true,
  },
  loading: Boolean,
  error: String,
});

defineEmits(['edit', 'delete']);
</script>