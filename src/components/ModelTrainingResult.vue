<template>
  <div v-if="modelTrainingResult" class="model-result-container">
    <h2><span class="section-icon">⚙️</span> 模型训练结果</h2>
    <div class="result-text">
      <p>{{ modelTrainingResult }}</p>
    </div>
    
    <!-- 特征重要性图表 -->
    <div v-if="featureImportance" class="feature-importance">
      <h3><span class="section-icon">🌟</span> 特征重要性</h3>
      <div class="importance-chart">
        <div v-for="(importance, feature) in featureImportance" :key="feature" class="chart-bar">
          <div class="bar-label">{{ feature }}</div>
          <div class="bar" :style="{ width: (importance / Math.max(...Object.values(featureImportance))) * 100 + '%' }">
            {{ (importance * 100).toFixed(2) }}%
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ModelTrainingResult',
  props: {
    modelTrainingResult: {
      type: String,
      default: ''
    },
    featureImportance: {
      type: Object,
      default: null
    }
  }
}
</script>

<style scoped>
.model-result-container {
  background-color: white;
  border-radius: 12px;
  padding: 25px;
  margin-top: 20px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.08);
  text-align: left;
  transition: all 0.3s ease;
  border: 1px solid #f0f0f0;
}

.model-result-container:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.12);
}

.section-icon {
  margin-right: 10px;
  font-size: 1.4em;
  display: inline-block;
  animation: spin 3s linear infinite;
}

.section-icon:nth-child(2) { /* For the star icon */
  animation: pulse-alt 2s infinite;
}


@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes pulse-alt {
  0% { transform: scale(1); }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); }
}

.model-result-container h2,
.feature-importance h3 {
  color: #3a7bd5;
  font-size: 1.8rem;
  margin-top: 0;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #f0f0f0;
  position: relative;
}

.model-result-container h2::after,
.feature-importance h3::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: -2px;
  width: 80px;
  height: 2px;
  background-color: #3a7bd5;
  transition: width 0.3s ease;
}

.model-result-container:hover h2::after,
.feature-importance:hover h3::after {
  width: 150px;
}

.result-text {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 25px;
  border-left: 4px solid #3a7bd5;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

.result-text p {
  margin: 0;
  line-height: 1.6;
  color: #333;
}

.feature-importance {
  background-color: white;
  border-radius: 10px;
  padding: 25px;
  margin-top: 20px;
  box-shadow: 0 3px 10px rgba(0,0,0,0.05);
  border: 1px solid #f0f0f0;
  transition: all 0.3s ease;
}

.feature-importance:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 15px rgba(0,0,0,0.1);
}

.importance-chart {
  margin-top: 15px;
}

.chart-bar {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
  transition: all 0.3s ease;
}

.chart-bar:hover {
  transform: translateX(5px);
}

.bar-label {
  width: 180px; /* Increased width for potentially longer feature names */
  text-align: right;
  padding-right: 15px;
  font-size: 14px;
  font-weight: 500;
  color: #555;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.bar {
  background: linear-gradient(90deg, #3a7bd5, #6998e0);
  color: white;
  padding: 8px 12px;
  border-radius: 6px;
  min-width: 40px;
  text-align: left;
  transition: width 0.5s ease-in-out; /* Smoother transition */
  box-shadow: 0 2px 5px rgba(58, 123, 213, 0.3);
  position: relative;
  overflow: hidden;
}

.bar::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,0.2), rgba(255,255,255,0));
  transform: translateX(-100%);
  animation: shimmer 3s infinite;
}

@keyframes shimmer {
  100% {
    transform: translateX(100%);
  }
}

@media (max-width: 768px) {
  .model-result-container,
  .feature-importance {
    padding: 15px;
  }
  
  .bar-label {
    width: 120px;
    font-size: 12px;
  }
}
</style>