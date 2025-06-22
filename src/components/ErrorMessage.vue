<template>
  <div v-if="error" class="error">
    <p>{{ error }}</p>
  </div>
</template>

<script>
export default {
  name: 'ErrorMessage',
  props: {
    error: {
      type: String,
      default: ''
    }
  }
}
</script>

<style scoped>
.error {
  background-color: #ffebee;
  border-left: 6px solid #f44336;
  padding: 15px;
  margin-top: 20px;
  text-align: left;
  border-radius: 4px;
}
</style>