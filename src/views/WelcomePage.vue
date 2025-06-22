<template>
  <div class="layout">
    <nav class="navbar">
      <router-link to="/" class="nav-logo">学生压力预测系统</router-link>
    </nav>
    
    <div class="welcome-section">
      <div class="content-card">
        <h1 class="welcome-title">欢迎使用</h1>
        <p class="welcome-subtitle">基于随机森林算法的学生压力水平分析与预测</p>
        <router-link to="/dashboard" class="explore-btn">
          开始探索
        </router-link>
      </div>
    </div>
    
    <div class="background-animation">
      <div class="wave"></div>
      <div class="wave"></div>
      <div class="wave"></div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'WelcomePage'
}
</script>

<style scoped>
.layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  position: relative;
  overflow: hidden;
  margin: 0;
  padding: 0;
  border-radius: 0;
  box-shadow: none;
}

.background-animation {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  z-index: -1;
  background: white;
  overflow: hidden;
  border-radius: 0;
}

.wave {
  position: absolute;
  width: 200%;
  height: 200%;
  background: rgba(0, 0, 0, 0.02);
  border-radius: 43%;
}

.wave:nth-child(1) {
  bottom: -80%;
  left: -50%;
  animation: rotate 10000ms infinite linear;
}

.wave:nth-child(2) {
  bottom: -70%;
  left: -30%;
  animation: rotate 16000ms infinite linear;
  opacity: 0.3;
}

.wave:nth-child(3) {
  bottom: -60%;
  left: -10%;
  animation: rotate 20000ms infinite linear;
  opacity: 0.1;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.navbar {
  background-color: white;
  padding: 1rem 2rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  z-index: 10;
  border-bottom: 1px solid #f0f0f0;
  border-radius: 0;
}

.nav-logo {
  color: #333;
  font-size: 1.5rem;
  font-weight: 700;
  text-decoration: none;
}

.welcome-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: 2rem;
  z-index: 5;
}

.content-card {
  background-color: white;
  padding: 3rem;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  max-width: 600px;
  width: 100%;
  border: 1px solid #f0f0f0;
  animation: float 6s ease-in-out infinite;
  transition: all 0.3s ease;
}

.content-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
}

@keyframes float {
  0% { transform: translateY(0px); }
  50% { transform: translateY(-15px); }
  100% { transform: translateY(0px); }
}

.welcome-title {
  font-size: 2.8rem;
  margin-bottom: 1rem;
  color: #333;
}

.welcome-subtitle {
  font-size: 1.2rem;
  margin-bottom: 3rem;
  color: #666;
  max-width: 600px;
  line-height: 1.6;
}

.explore-btn {
  padding: 15px 40px;
  background: #3a7bd5;
  color: white;
  border: none;
  border-radius: 30px;
  font-size: 1.2rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
  display: inline-block;
  position: relative;
  overflow: hidden;
  z-index: 1;
  box-shadow: 0 4px 15px rgba(58, 123, 213, 0.3);
}

.explore-btn:before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 0%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.1);
  transition: all 0.5s ease;
  z-index: -1;
  border-radius: 30px;
}

.explore-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.15);
}

.explore-btn:hover:before {
  width: 100%;
}

@media (max-width: 768px) {
  .content-card {
    padding: 2rem;
  }
  
  .welcome-title {
    font-size: 2.2rem;
  }
  
  .welcome-subtitle {
    font-size: 1rem;
    margin-bottom: 2rem;
  }
  
  .explore-btn {
    padding: 12px 30px;
    font-size: 1rem;
  }
}
</style>