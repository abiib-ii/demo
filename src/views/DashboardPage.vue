<template>
  <div class="dashboard-container">
    <header-component />
    
    <div class="dashboard-content">
      <button-group 
        :loading="loading"
        @fetch-data="fetchDataSummary"
        @train-model="trainModel"
        @get-model-info="getModelInfo"
        @get-model-plots="getModelPlots"
      />
      
      <loading-indicator :loading="loading" />
      
      <error-message :error="error" />
      
      <transition name="fade">
        <data-summary v-if="dataSummary" :dataSummary="dataSummary" />
      </transition>
      
      <transition name="fade">
        <model-training-result 
          v-if="modelTrainingResult"
          :modelTrainingResult="modelTrainingResult"
          :featureImportance="featureImportance"
        />
      </transition>
      
      <transition name="fade">
        <model-info v-if="modelInfo" :modelInfo="modelInfo" />
      </transition>
      
      <transition name="fade">
        <model-plots v-if="modelPlots" :modelPlots="modelPlots" />
      </transition>
    </div>
    
    <footer-component />
  </div>
</template>

<script>
import axios from 'axios'
import HeaderComponent from '@/components/HeaderComponent.vue'
import ButtonGroup from '@/components/ButtonGroup.vue'
import LoadingIndicator from '@/components/LoadingIndicator.vue'
import DataSummary from '@/components/DataSummary.vue'
import ModelTrainingResult from '@/components/ModelTrainingResult.vue'
import ModelInfo from '@/components/ModelInfo.vue'
import ModelPlots from '@/components/ModelPlots.vue'
import FooterComponent from '@/components/FooterComponent.vue'
import ErrorMessage from '@/components/ErrorMessage.vue'

export default {
  name: 'DashboardPage',
  components: {
    HeaderComponent,
    ButtonGroup,
    LoadingIndicator,
    DataSummary,
    ModelTrainingResult,
    ModelInfo,
    ModelPlots,
    FooterComponent,
    ErrorMessage
  },
  data() {
    return {
      dataSummary: null,
      modelInfo: null,
      error: '',
      loading: false,
      modelTrainingResult: '',
      featureImportance: null,
      modelPlots: null
    }
  },
  methods: {
    async fetchDataSummary() {
      this.loading = true
      this.error = ''
      this.dataSummary = null
      try {
        const response = await axios.get('http://localhost:5000/api/data-summary')
        if (response.data.status === 'success') {
          this.dataSummary = response.data.summary
        } else {
          this.error = response.data.message || '获取数据摘要失败'
        }
      } catch (error) {
        console.error('获取数据摘要失败:', error)
        this.error = '获取数据摘要失败，请稍后重试'
      } finally {
        this.loading = false
      }
    },
    
    async trainModel() {
      this.loading = true
      this.error = ''
      this.modelTrainingResult = ''
      this.featureImportance = null
      try {
        const response = await axios.post('http://localhost:5000/api/train-model')
        if (response.data.status === 'success') {
          this.modelTrainingResult = `模型训练成功，准确率: ${(response.data.accuracy * 100).toFixed(2)}%`
          this.featureImportance = response.data.feature_importance
        } else {
          this.error = response.data.message || '模型训练失败'
        }
      } catch (error) {
        console.error('模型训练失败:', error)
        this.error = '模型训练失败，请稍后重试'
      } finally {
        this.loading = false
      }
    },
    
    async getModelInfo() {
      this.loading = true
      this.error = ''
      this.modelInfo = null
      try {
        const response = await axios.get('http://localhost:5000/api/model-info')
        if (response.data.status === 'success') {
          this.modelInfo = response.data
        } else {
          this.error = response.data.message || '获取模型信息失败'
        }
      } catch (error) {
        console.error('获取模型信息失败:', error)
        this.error = '获取模型信息失败，请稍后重试'
      } finally {
        this.loading = false
      }
    },
    
    async getModelPlots() {
      this.loading = true
      this.error = ''
      this.modelPlots = null
      try {
        const response = await axios.get('http://localhost:5000/api/model-plots')
        if (response.data.status === 'success') {
          this.modelPlots = response.data.plots
        } else {
          this.error = response.data.message || '获取模型可视化图表失败'
        }
      } catch (error) {
        console.error('获取模型可视化图表失败:', error)
        this.error = '获取模型可视化图表失败，请稍后重试'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.dashboard-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: white;
}

.dashboard-content {
  flex: 1;
  background-color: white;
  border-radius: 0 0 10px 10px;
  padding: 20px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.03);
  margin-bottom: 20px;
  position: relative;
  z-index: 1;
}

/* 添加一个连接线效果 */
.dashboard-content::before {
  content: '';
  position: absolute;
  top: -2px; /* 微调位置 */
  left: 50%;
  width: 100px;
  height: 4px;
  background: #3a7bd5;
  transform: translateX(-50%);
  border-radius: 2px;
  z-index: 2;
}

/* 添加淡入淡出动画效果 */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s, transform 0.5s;
}

.fade-enter, .fade-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

@media (max-width: 768px) {
  .dashboard-content {
    padding: 15px;
  }
  
  .dashboard-content::before {
    width: 60px;
  }
}
</style>