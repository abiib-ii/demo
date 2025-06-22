<template>
  <div v-if="dataSummary" class="data-summary">
    <h2><span class="section-icon">📊</span> 数据摘要</h2>
    <div class="summary-card">
      <div class="summary-item">
        <h3>数据总行数</h3>
        <p class="highlight-number">{{ dataSummary.数据总行数 }}</p>
      </div>
      <div class="summary-item">
        <h3>特征数量</h3>
        <p class="highlight-number">{{ dataSummary.特征数量 }}</p>
      </div>
    </div>
    <div class="feature-list">
      <h3>特征列表</h3>
      <ul>
        <li v-for="(feature, index) in dataSummary.特征列表" :key="index">{{ feature }}</li>
      </ul>
    </div>
    <div class="stress-distribution">
      <h3>压力水平分布</h3>
      <div class="distribution-chart">
        <div v-for="(count, level) in dataSummary.压力水平分布" :key="level" class="chart-bar">
          <div class="bar-label">压力水平 {{ level }}</div>
          <div class="bar" :style="{ width: (count / Math.max(...Object.values(dataSummary.压力水平分布))) * 100 + '%' }">
            {{ count }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DataSummary',
  props: {
    dataSummary: {
      type: Object,
      default: null
    }
  }
}
</script>

<style scoped>
.data-summary {
  background-color: white;
  border-radius: 12px;
  padding: 25px;
  margin-bottom: 25px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
  border: 1px solid #f0f0f0;
  transition: all 0.3s ease;
}

.data-summary:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
}

.data-summary h2 {
  color: #3a7bd5;
  font-size: 1.8rem;
  margin-top: 0;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #f0f0f0;
  position: relative;
}

.data-summary h2::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: -2px;
  width: 80px;
  height: 2px;
  background-color: #3a7bd5;
  transition: width 0.3s ease;
}

.data-summary:hover h2::after {
  width: 150px;
}

.section-icon {
  margin-right: 10px;
  font-size: 1.4em;
  display: inline-block;
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-5px); }
}

.summary-card {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 20px;
}

.summary-item {
  background-color: white;
  border-radius: 10px;
  padding: 20px;
  flex: 1;
  min-width: 200px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
  border: 1px solid #f0f0f0;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.summary-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 0;
  background-color: #3a7bd5;
  transition: height 0.3s ease;
}

.summary-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
}

.summary-item:hover::before {
  height: 100%;
}

.summary-item h3 {
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

.summary-item:hover .highlight-number {
  transform: scale(1.1);
}

.feature-list, .stress-distribution {
  background-color: white;
  border-radius: 10px;
  padding: 20px;
  margin-top: 20px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
  border: 1px solid #f0f0f0;
  transition: all 0.3s ease;
}

.feature-list:hover, .stress-distribution:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
}

.feature-list h3, .stress-distribution h3 {
  color: #3a7bd5;
  margin-top: 0;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #f0f0f0;
  position: relative;
}

.feature-list h3::after, .stress-distribution h3::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: -1px;
  width: 50px;
  height: 2px;
  background-color: #3a7bd5;
  transition: width 0.3s ease;
}

.feature-list:hover h3::after, .stress-distribution:hover h3::after {
  width: 100px;
}

.feature-list ul {
  columns: 3;
  -webkit-columns: 3;
  -moz-columns: 3;
  list-style-type: none;
  padding-left: 0;
  margin-top: 15px;
}

.feature-list li {
  margin-bottom: 8px;
  padding: 8px 12px;
  background-color: #f8f9fa;
  border-radius: 6px;
  border-left: 3px solid #3a7bd5;
  transition: all 0.3s ease;
  font-size: 14px;
}

.feature-list li:hover {
  background-color: #e9f0fd;
  transform: translateX(5px);
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
  .feature-list ul {
    columns: 1;
    -webkit-columns: 1;
    -moz-columns: 1;
  }
  
  .summary-card {
    flex-direction: column;
  }
  
  .data-summary {
    padding: 15px;
  }
  
  .feature-list, .stress-distribution {
    padding: 15px;
  }
  
  .bar-label {
    width: 120px;
    font-size: 12px;
  }
}
</style>