<template>
    <Card>
      <CardContent class="p-0">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead class="text-center">库存ID</TableHead>
              <TableHead class="text-center">物资ID</TableHead>
              <TableHead class="text-center">物资名称</TableHead>
              <TableHead class="text-center">物资编码</TableHead>
              <TableHead class="text-center">当前数量</TableHead>
              <TableHead class="text-center">最低库存</TableHead>
              <TableHead class="text-center">最高库存</TableHead>
              <TableHead class="text-center">最后更新时间</TableHead>
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
            <template v-else-if="inventories.length === 0">
              <TableRow>
                <TableCell :colspan="8" class="h-24 text-center">暂无库存数据。</TableCell>
              </TableRow>
            </template>
            <template v-else>
              <TableRow v-for="item in inventories" :key="item.id">
                <TableCell class="text-center">{{ item.id }}</TableCell>
                <TableCell class="text-center">{{ item.material_id }}</TableCell>
                <TableCell class="text-center">{{ item.material?.name || 'N/A' }}</TableCell>
                <TableCell class="text-center">{{ item.material?.code || 'N/A' }}</TableCell>
                <TableCell class="text-center">{{ item.current_quantity }} {{ item.material?.unit }}</TableCell>
                <TableCell class="text-center">{{ item.min_stock_level }}</TableCell>
                <TableCell class="text-center">{{ item.max_stock_level }}</TableCell>
                <TableCell class="text-center">{{ formatDate(item.last_updated_at) }}</TableCell>
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
  // import { Button } from '@/components/ui/button';
  
  defineProps({
    inventories: {
      type: Array,
      required: true,
    },
    loading: Boolean,
    error: String,
  });
  
  // defineEmits(['adjust']); // 如果添加调整功能
  
  function formatDate(dateTimeString) {
    if (!dateTimeString) return '-';
    return new Date(dateTimeString).toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
    });
  }
  </script>