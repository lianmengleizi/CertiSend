<template>
  <div class="admin-container">
    <div class="header">
      <el-avatar :size="80" src="@/assets/admin-avatar.jpg" />
      <div class="stats">
        <h2>证书发放管理</h2>
        <el-progress 
          type="dashboard" 
          :percentage="sentPercentage"
          :color="colors"
          :width="120"
        >
          <template #default>
            <div class="progress-text">
              <span class="percentage">{{ sentPercentage }}%</span>
              <span class="label">已发放</span>
            </div>
          </template>
        </el-progress>
        <el-button 
          type="warning" 
          plain 
          @click="scrollToFirstUnsent"
          class="unsent-btn"
        >
          还有 {{ unsentCount }} 人未发放
        </el-button>
      </div>
    </div>

    <el-table
      :data="tableData"
      v-loading="loading"
      border
      stripe
      highlight-current-row
      style="width: 100%; margin-top: 20px"
      :row-class-name="rowClassName"
    >
      <el-table-column prop="name" label="姓名" width="100" align="center" />
      <el-table-column prop="phone" label="电话" width="140" align="center" />
      <el-table-column prop="id_number" label="身份证号" width="180" />
      <el-table-column prop="exam_number" label="准考证号" width="180" />
      <el-table-column prop="full_address" label="地址" min-width="200" />
      <el-table-column label="是否已发" width="120" align="center">
        <template #default="{ row }">
          <el-tag :type="row.is_sent ? 'success' : 'danger'" size="large">
            {{ row.is_sent ? '已发' : '未发' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="120" align="center">
        <template #default="{ row }">
          <el-switch
            v-model="row.is_sent"
            active-color="#13ce66"
            inactive-color="#ff4949"
            @change="updateStatus(row)"
          />
        </template>
      </el-table-column>
    </el-table>

    <div class="action-bar">
      <el-button type="primary" @click="saveAll" :loading="saving">
        保存所有修改
      </el-button>
      <el-button type="success" @click="exportData">
        导出数据
      </el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const tableData = ref([])
const loading = ref(false)
const saving = ref(false)

const colors = [
  { color: '#f56c6c', percentage: 20 },
  { color: '#e6a23c', percentage: 40 },
  { color: '#5cb87a', percentage: 60 },
  { color: '#1989fa', percentage: 80 },
  { color: '#6f7ad3', percentage: 100 }
]

const sentPercentage = computed(() => {
  const total = tableData.value.length
  if (!total) return 0
  const sent = tableData.value.filter(item => item.is_sent).length
  return Math.round((sent / total) * 100)
})
const updateStatus = async (row) => {
  try {
    // 更新每一行的状态
    await axios.put(`http://127.0.0.1:8000/api/user-info/${row.id}/`, row);  // 假设每个 row 都有 id 字段
    ElMessage.success("状态更新成功");
  } catch (error) {
    console.error("更新状态失败:", error);
    ElMessage.error("更新状态失败，请稍后再试");
  }
};
const saveAll = async () => {
  saving.value = true;  // 显示保存按钮的加载状态
  try {
    // 获取所有需要保存的行
    const updatedRows = tableData.value.filter(row => row.is_sent !== row.original_is_sent);  // 比较原始和修改后的状态

    // 逐个提交修改的行
    for (let row of updatedRows) {
      await axios.put(`http://127.0.0.1:8000/api/user-info/${row.id}/`, row);
    }
    ElMessage.success("所有修改已保存");
  } catch (error) {
    console.error("保存所有修改失败:", error);
    ElMessage.error("保存失败，请稍后再试");
  } finally {
    saving.value = false;
  }
};

const unsentCount = computed(() => {
  return tableData.value.length - tableData.value.filter(item => item.is_sent).length
})

const fetchData = async () => {
  loading.value = true  // 显示加载动画
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/user-info/')  // 后端数据请求
    tableData.value = response.data  // 将获取到的数据赋值给表格数据
  } catch (error) {
    console.error('获取数据失败:', error)
    ElMessage.error('获取数据失败，请稍后再试')
  } finally {
    loading.value = false  // 隐藏加载动画
  }
}

onMounted(() => {
  fetchData();
  tableData.value.forEach(row => {
    row.original_is_sent = row.is_sent;  // 添加原始状态
  });
});
</script>

<style scoped>
.admin-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

.header {
  display: flex;
  align-items: center;
  gap: 30px;
  margin-bottom: 20px;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
}

.stats {
  flex: 1;
}

.stats h2 {
  margin-bottom: 15px;
  color: #333;
}

.progress-text {
  text-align: center;
}

.progress-text .percentage {
  display: block;
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 5px;
}

.progress-text .label {
  font-size: 14px;
  color: #888;
}

.unsent-btn {
  margin-top: 15px;
}

.action-bar {
  margin-top: 20px;
  text-align: right;
}

/* 未发送行样式 */
:deep(.el-table .row-not-sent) {
  --el-table-tr-bg-color: #fff8f8;
}
</style>