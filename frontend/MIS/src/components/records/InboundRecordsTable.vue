<template>
    <Card>
      <CardContent class="p-0">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead class="text-center">记录ID</TableHead>
              <TableHead class="text-center">入库单号</TableHead>
              <TableHead class="text-center">物资名称</TableHead>
              <TableHead class="text-center">物资编码</TableHead>
              <TableHead class="text-center">数量</TableHead>
              <TableHead class="text-center">入库时间</TableHead>
              <TableHead class="text-center">备注</TableHead>
              </TableRow>
          </TableHeader>
          <TableBody>
            <template v-if="loading">
              <TableRow>
                <TableCell :colspan="7" class="h-24 text-center">正在加载...</TableCell>
              </TableRow>
            </template>
            <template v-else-if="error">
              <TableRow>
                <TableCell :colspan="7" class="h-24 text-center text-destructive">{{ error }}</TableCell>
              </TableRow>
            </template>
            <template v-else-if="records.length === 0">
              <TableRow>
                <TableCell :colspan="7" class="h-24 text-center">暂无入库记录。</TableCell>
              </TableRow>
            </template>
            <template v-else>
              <TableRow v-for="record in records" :key="record.id">
                <TableCell class="text-center">{{ record.id }}</TableCell>
                <TableCell class="text-center">{{ record.inbound_order_number || '-' }}</TableCell>
                <TableCell class="text-center">{{ record.material?.name || 'N/A' }}</TableCell>
                <TableCell>{{ record.material?.code || 'N/A' }}</TableCell>
                <TableCell class="text-center">{{ record.quantity }} {{ record.material?.unit }}</TableCell>
                <TableCell class="text-center">{{ formatDate(record.inbound_time) }}</TableCell>
                <TableCell class="text-center" :title="record.remarks">{{ record.remarks || '-' }}</TableCell>
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
    records: {
      type: Array,
      required: true,
    },
    loading: Boolean,
    error: String,
  });
  
  // defineEmits(['view-details']);
  
  function formatDate(dateTimeString) {
    if (!dateTimeString) return '-';
    return new Date(dateTimeString).toLocaleString('zh-CN', { hour12: false });
  }
  </script>