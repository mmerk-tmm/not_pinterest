<script setup>
import { RouterLink, RouterView } from 'vue-router'
import AppHeader from './components/AppHeader.vue'
</script>

<template>
  <AppHeader />
  <div class="app-content">
    <RouterView />
  </div>
</template>

<style scoped>
.app-content {
  display: flex;
  flex-direction: column;
}
</style>
