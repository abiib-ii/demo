<template>
  <div v-if="modelInfo" class="model-info">
    <h2><span class="section-icon">ℹ️</span> 模型信息</h2>
    <div class="info-card">
      <div class="info-item">
        <h3>模型类型</h3>
        <p class="highlight-text">{{ modelInfo.model_type }}</p>
      </div>
      <div class="info-item">
        <h3>决策树数量</h3>
        <p class="highlight-number">{{ modelInfo.n_estimators }}</p>
      </div>
      <div class="info-item">
        <h3>准确率</h3>
        <p class="highlight-number accuracy">{{ (modelInfo.accuracy * 100).toFixed(2) }}%</p>
      </div>
      <div class="info-item">
        <h3>特征数量</h3>
        <p class="highlight-number">{{ modelInfo.feature_count }}</p>
      </div>
    </div>
    
    <!-- 显示前5个重要特征 -->
    <div class="top-features">
      <h3>最重要的特征</h3>
      <div class="importance-chart">
        <div v-for="feature in modelInfo.top_features" :key="feature.name" class="chart-bar">
          <div class="bar-label">{{ feature.name }}</div>
          <div class="bar" :style="{ width: (feature.importance / modelInfo.top_features[0].importance) * 100 + '%' }">
            {{ (feature.importance * 100).toFixed(2) }}%
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ModelInfo',
  props: {
    modelInfo: {
      type: Object,
      default: null
    }
  }
}
</script>

<style scoped>
.model-info {
  background-color: white;
  border-radius: 12px;
  padding: 25px;
  margin-top: 20px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.08);
  text-align: left;
  transition: all 0.3s ease;
  border: 1px solid #f0f0f0;
}

.model-info:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.12);
}

.section-icon {
  margin-right: 10px;
  font-size: 1.4em;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); }
}

.model-info h2 {
  color: #3a7bd5;
  font-size: 1.8rem;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #f0f0f0;
  position: relative;
}

.model-info h2::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: -2px;
  width: 80px;
  height: 2px;
  background-color: #3a7bd5;
  transition: width 0.3s ease;
}

.model-info:hover h2::after {
  width: 150px;
}

.info-card {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 30px;
}

.info-item {
  background-color: white;
  border-radius: 10px;
  padding: 20px;
  flex: 1;
  min-width: 200px;
  box-shadow: 0 3px 10px rgba(0,0,0,0.05);
  border: 1px solid #f0f0f0;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.info-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 0;
  background-color: #3a7bd5;
  transition: height 0.3s ease;
}

.info-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 15px rgba(0,0,0,0.1);
}

.info-item:hover::before {
  height: 100%;
}

.info-item h3 {
  margin-top: 0;
  color: #3a7bd5;
  font-size: 1.1rem;
  margin-bottom: 15px;
}

.highlight-number {
  font-size: 28px;
  font-weight: bold;
  color: #3a7bd5;
  transition: all 0.3s ease;
}

.info-item:hover .highlight-number {
  transform: scale(1.1);
}

.highlight-text {
  font-size: 20px;
  font-weight: bold;
  color: #2c3e50;
  transition: all 0.3s ease;
}

.info-item:hover .highlight-text {
  transform: scale(1.05);
}

.accuracy {
  color: #27ae60;
}

.top-features {
  background-color: white;
  border-radius: 10px;
  padding: 25px;
  margin-top: 20px;
  box-shadow: 0 3px 10px rgba(0,0,0,0.05);
  border: 1px solid #f0f0f0;
  transition: all 0.3s ease;
}

.top-features:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 15px rgba(0,0,0,0.1);
}

.top-features h3 {
  color: #3a7bd5;
  margin-top: 0;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #f0f0f0;
  position: relative;
}

.top-features h3::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: -1px;
  width: 50px;
  height: 2px;
  background-color: #3a7bd5;
  transition: width 0.3s ease;
}

.top-features:hover h3::after {
  width: 100px;
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
  width: 150px;
  text-align: right;
  padding-right: 15px;
  font-size: 14px;
  font-weight: 500;
  color: #555;
}

.bar {
  background: linear-gradient(90deg, #3a7bd5, #6998e0);
  color: white;
  padding: 8px 12px;
  border-radius: 6px;
  min-width: 40px;
  text-align: left;
  transition: all 0.5s ease;
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
  .info-card {
    flex-direction: column;
  }
  
  .model-info {
    padding: 15px;
  }
  
  .info-item, .top-features {
    padding: 15px;
  }
  
  .bar-label {
    width: 120px;
    font-size: 12px;
  }
}
</style>