<template>
  <div v-if="modelPlots" class="model-plots-container">
    <h2><span class="section-icon">📈</span> 模型可视化图表</h2>
    <div class="plots-description">
      <p>以下图表展示了模型的各种可视化分析结果，帮助您更好地理解模型的性能和特征影响。</p>
    </div>
    
    <div class="plots-grid">
      <div class="plot-card">
        <h3><span class="card-icon">🎯</span> 特征重要性</h3>
        <p>展示各个特征对模型预测结果的影响程度。</p>
        <div class="image-container">
          <img :src="'data:image/png;base64,' + modelPlots.feature_importance" alt="特征重要性图" />
        </div>
      </div>
      
      <div class="plot-card">
        <h3><span class="card-icon">🔀</span> 混淆矩阵</h3>
        <p>展示模型在各个压力水平上的预测准确性。</p>
        <div class="image-container">
          <img :src="'data:image/png;base64,' + modelPlots.confusion_matrix" alt="混淆矩阵" />
        </div>
      </div>
      
      <div class="plot-card">
        <h3><span class="card-icon">📊</span> 特征分布图</h3>
        <p>展示不同压力水平下重要特征的分布情况。</p>
        <div class="image-container">
          <img :src="'data:image/png;base64,' + modelPlots.feature_distribution" alt="特征分布图" />
        </div>
      </div>
      
      <div class="plot-card">
        <h3><span class="card-icon">🔍</span> 预测结果分析</h3>
        <p>展示各个压力水平的精确率、召回率和F1分数。</p>
        <div class="image-container">
          <img :src="'data:image/png;base64,' + modelPlots.classification_report" alt="预测结果分析" />
        </div>
      </div>

      <div class="plot-card">
        <h3><span class="card-icon">📉</span> AUC-ROC 曲线</h3>
        <p>展示模型在所有类别上的接收者操作特征曲线 (ROC) 和曲线下面积 (AUC)。</p>
        <div class="image-container">
          <img :src="'data:image/png;base64,' + modelPlots.auc_roc_curve" alt="AUC-ROC 曲线图" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ModelPlots',
  props: {
    modelPlots: {
      type: Object,
      default: null
    }
  }
}
</script>

<style scoped>
.model-plots-container {
  background-color: white;
  border-radius: 12px;
  padding: 25px;
  margin-top: 20px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.08);
  text-align: left;
  transition: all 0.3s ease;
  border: 1px solid #f0f0f0;
}

.model-plots-container:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.12);
}

.section-icon {
  margin-right: 10px;
  font-size: 1.4em;
  display: inline-block;
  animation: wave-icon 2.5s infinite;
}

@keyframes wave-icon {
  0%, 100% { transform: rotate(0deg); }
  25% { transform: rotate(10deg); }
  75% { transform: rotate(-10deg); }
}

.model-plots-container h2 {
  color: #3a7bd5;
  font-size: 1.8rem;
  margin-top: 0;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 2px solid #f0f0f0;
  position: relative;
}

.model-plots-container h2::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: -2px;
  width: 80px;
  height: 2px;
  background-color: #3a7bd5;
  transition: width 0.3s ease;
}

.model-plots-container:hover h2::after {
  width: 150px;
}

.plots-description {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 25px;
  border-left: 4px solid #3a7bd5;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

.plots-description p {
  margin: 0;
  line-height: 1.6;
  color: #555;
  font-size: 0.95rem;
}

.plots-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); /* Adjusted minmax for better fit */
  gap: 25px; /* Increased gap */
}

.plot-card {
  background-color: white;
  border-radius: 10px;
  padding: 20px; /* Increased padding */
  box-shadow: 0 4px 12px rgba(0,0,0,0.07); /* Softer shadow */
  border: 1px solid #e9ecef;
  transition: all 0.3s ease-in-out;
  display: flex;
  flex-direction: column;
}

.plot-card:hover {
  transform: translateY(-8px) scale(1.02); /* Enhanced hover effect */
  box-shadow: 0 10px 20px rgba(0,0,0,0.1);
}

.card-icon {
  margin-right: 8px;
  font-size: 1.1em;
}

.plot-card h3 {
  color: #3a7bd5;
  margin-top: 0;
  margin-bottom: 10px; /* Adjusted margin */
  font-size: 1.3rem; /* Slightly larger card title */
  display: flex;
  align-items: center;
}

.plot-card p {
  margin-bottom: 15px;
  color: #666;
  font-size: 0.9rem; /* Slightly smaller description text */
  line-height: 1.5;
  flex-grow: 1; /* Allows description to take available space */
}

.image-container {
  overflow: hidden;
  border-radius: 8px; /* Consistent with card radius */
  box-shadow: 0 4px 8px rgba(0,0,0,0.08);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  margin-top: auto; /* Pushes image to the bottom if text is short */
}

.plot-card:hover .image-container {
  transform: scale(1.03); /* Slightly more pronounced scale on card hover */
  box-shadow: 0 6px 12px rgba(0,0,0,0.12);
}

.plot-card img {
  width: 100%;
  height: auto; /* Ensure aspect ratio is maintained */
  display: block; /* Removes extra space below image */
  border-radius: 8px; /* Match container radius */
  /* Removed individual image shadow as container has one */
}

@media (max-width: 992px) { /* Adjusted breakpoint for better responsiveness */
  .plots-grid {
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  }
}

@media (max-width: 768px) {
  .plots-grid {
    grid-template-columns: 1fr; /* Single column on smaller screens */
  }
  .model-plots-container {
    padding: 15px;
  }
  .plot-card {
    padding: 15px;
  }
}
</style>