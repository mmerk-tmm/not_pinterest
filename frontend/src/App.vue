<script setup>
import { RouterLink, RouterView } from 'vue-router'
import AppHeader from './components/AppHeader.vue'
import { computed } from 'vue';
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
      scrollY: window.scrollY,
    }
  },
  methods: {
    onSearchOpended(value) {
      this.isSearchOpended = value;
    },
    onScroll() {
      this.scrollY = window.scrollY
    },
  },
  mounted() {
    this.$nextTick(() => {
      window.addEventListener('scroll', this.onScroll);
    });
  },
  beforeDestroy() {
    window.removeEventListener('scroll', this.onScroll);
  },
  provide() {
    return {
      runValidation() {
        return false
      },
      scrollY: computed(() => this.scrollY),
    }
  }
}
</script>
<style scoped lang="scss">
.app-content {
  display: flex;
  flex-direction: column;
  height: 100%;
  padding-top: 80px;

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
