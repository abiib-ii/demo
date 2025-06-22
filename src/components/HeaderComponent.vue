<template>
  <header class="app-header">
    <nav class="navbar">
      <router-link to="/" class="nav-logo">学生压力预测系统</router-link>
      <div class="nav-links">
        <router-link to="/" class="nav-link">
          <span class="nav-icon">🏠</span> 返回首页
        </router-link>
      </div>
    </nav>
    <div class="header-content">
      <h1>压力预测系统</h1>
      <p class="subtitle">基于随机森林算法的压力水平分析工具</p>
    </div>
  </header>
</template>

<script>
export default {
  name: 'HeaderComponent'
}
</script>

<style scoped>
.app-header {
  margin-bottom: 0;
  background-color: white;
  border-radius: 10px 10px 0 0;
  box-shadow: 0 -5px 20px rgba(0, 0, 0, 0.03);
  overflow: hidden;
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: white;
  padding: 1rem 2rem;
  color: #333;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  border-bottom: 1px solid #f0f0f0;
}

.nav-logo {
  color: #333;
  font-size: 1.5rem;
  font-weight: 700;
  text-decoration: none;
  transition: transform 0.3s ease;
}

.nav-logo:hover {
  transform: scale(1.05);
}

.nav-links {
  display: flex;
  align-items: center;
}

.nav-link {
  display: flex;
  align-items: center;
  color: #333;
  text-decoration: none;
  font-weight: 600;
  padding: 8px 15px;
  border-radius: 20px;
  transition: all 0.3s ease;
  background-color: #f5f5f5;
}

.nav-link:hover {
  background-color: #e0e0e0;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
}

.nav-icon {
  margin-right: 5px;
}

.header-content {
  padding: 20px;
  text-align: center;
  background-color: white;
  border-bottom: 1px solid #f0f0f0;
  transition: all 0.3s ease;
}

.header-content h1 {
  color: #3a7bd5;
  margin-bottom: 5px;
}

.subtitle {
  color: #666;
  font-size: 16px;
  margin-top: 0;
}

@media (max-width: 768px) {
  .navbar {
    flex-direction: column;
    padding: 1rem;
  }
  
  .nav-links {
    margin-top: 10px;
  }
}
</style>