import axios from 'axios';

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export default {
  // --- 统计 ---
  getDashboardSummary() {
    return apiClient.get('/statistics/dashboard-summary');
  },

  // --- 物资 ---
  getMaterials(params) {  // params: { skip, limit, code, name }
    return apiClient.get('/materials/', { params });
  },
  createMaterial(data) {
    return apiClient.post('/materials/', data);
  },
  getMaterialById(id) {
    return apiClient.get(`/materials/${id}`);
  },
  updateMaterial(id, data) {
    return apiClient.put(`/materials/${id}`, data);
  },
  deleteMaterial(id) {
    return apiClient.delete(`/materials/${id}`);
  },

  // --- 库存余額 ---
  getInventoryBalances(params) {  // params: { skip, limit }
    return apiClient.get('/inventory-balances/', { params });
  },
  getInventoryBalanceByMaterialId(materialId) {
    return apiClient.get(`/inventory-balances/material/${materialId}`);
  },

  // --- 入库记录 ---
  getInboundRecords(params) {  // params: { skip, limit, material_id, start_time, end_time }
    return apiClient.get('/inbound-records/', { params });
  },
  createInboundRecord(data) {
    return apiClient.post('/inbound-records/', data);
  },

  // --- 出库记录 ---
  getOutboundRecords(params) {  // params: { skip, limit, material_id, start_time, end_time }
    return apiClient.get('/outbound-records/', { params });
  },
  createOutboundRecord(data) {
    return apiClient.post('/outbound-records/', data);
  },
};