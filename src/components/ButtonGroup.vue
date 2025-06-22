<template>
  <div class="button-group-container">
    <h3 class="section-title">功能选择</h3>
    <div class="button-group">
      <button @click="$emit('fetch-data')" :disabled="loading" class="data-button">
        <span class="button-icon">📊</span>
        {{ loading ? '获取中...' : '获取数据摘要' }}
        <span class="button-effect"></span>
      </button>
      <button @click="$emit('train-model')" :disabled="loading" class="train-button">
        <span class="button-icon">🔄</span>
        {{ loading ? '训练中...' : '训练随机森林模型' }}
        <span class="button-effect"></span>
      </button>
      <button @click="$emit('get-model-info')" :disabled="loading" class="info-button">
        <span class="button-icon">ℹ️</span>
        {{ loading ? '获取中...' : '获取模型信息' }}
        <span class="button-effect"></span>
      </button>
      <button @click="$emit('get-model-plots')" :disabled="loading" class="plots-button">
        <span class="button-icon">📈</span>
        {{ loading ? '生成中...' : '获取模型可视化图表' }}
        <span class="button-effect"></span>
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ButtonGroup',
  props: {
    loading: {
      type: Boolean,
      default: false
    }
  }
}
</script>

<style scoped>
.button-group-container {
  background-color: white;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.button-group-container:hover {
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.section-title {
  text-align: left;
  color: #3a7bd5;
  margin-top: 0;
  margin-bottom: 15px;
  font-size: 1.2rem;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
  position: relative;
  overflow: hidden;
}

.section-title::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: 0;
  height: 2px;
  width: 50px;
  background-color: #3a7bd5;
  animation: slide-right 2s ease-in-out infinite alternate;
}

@keyframes slide-right {
  from { width: 0; }
  to { width: 100px; }
}

.button-group {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 15px;
}

button {
  background-color: #3a7bd5;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  display: flex;
  align-items: center;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  flex: 1;
  min-width: 200px;
  justify-content: center;
  position: relative;
  overflow: hidden;
  z-index: 1;
}

.button-icon {
  margin-right: 8px;
  font-size: 1.2em;
  transition: transform 0.3s ease;
}

button:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
}

button:hover .button-icon {
  transform: scale(1.2) rotate(10deg);
}

button:active {
  transform: translateY(2px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.button-effect {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  transition: all 0.5s ease;
  z-index: -1;
}

button:hover .button-effect {
  width: 300px;
  height: 300px;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

button:disabled .button-icon {
  transform: none;
}

button:disabled .button-effect {
  display: none;
}

.data-button {
  background: linear-gradient(135deg, #3a7bd5, #2c5ea3);
}

.train-button {
  background: linear-gradient(135deg, #3a7bd5, #2c5ea3);
}

.info-button {
  background: linear-gradient(135deg, #3a7bd5, #2c5ea3);
}

.plots-button {
  background: linear-gradient(135deg, #3a7bd5, #2c5ea3);
}

@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(58, 123, 213, 0.4); }
  70% { box-shadow: 0 0 0 10px rgba(58, 123, 213, 0); }
  100% { box-shadow: 0 0 0 0 rgba(58, 123, 213, 0); }
}

button:not(:disabled) {
  animation: pulse 2s infinite;
}

@media (max-width: 768px) {
  .button-group {
    flex-direction: column;
    align-items: center;
  }
  
  button {
    width: 100%;
    max-width: 300px;
    margin: 5px 0;
  }
}
</style>