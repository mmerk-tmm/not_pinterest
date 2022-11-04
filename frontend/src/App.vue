<script setup>
import { RouterLink, RouterView } from 'vue-router'
import AppHeader from './components/AppHeader.vue'
</script>

<template>
  <AppHeader @searchOpened="onSearchOpended" />
  <div :class="['app-content', { 'search-opened': isSearchOpended }]">
    <RouterView />
  </div>
</template>
<script>
export default {
  data() {
    return {
      isSearchOpended: false,
    }
  },
  methods: {
    onSearchOpended(value) {
      this.isSearchOpended = value;
    }
  },
  provide: {
    runValidation(){
      return false
    }
  }
}
</script>
<style scoped lang="scss">
.app-content {
  display: flex;
  flex-direction: column;
  height: 100%;

  &.search-opened {
    position: relative;
    // filter: blur(10px);

    &::after {
      content: '';
      position: absolute;
      inset: 0;
      background-color: rgba($color: #000000, $alpha: 0.3);
    }
  }
}
</style>
