<script setup>
import { RouterLink, RouterView } from 'vue-router'
import AppHeader from './components/AppHeader.vue'
import { computed } from 'vue';
import AppError from './components/AppError.vue';
</script>

<template>
  <AppHeader @searchOpened="onSearchOpended" />
  <div :class="['app-content', { 'search-opened': isSearchOpended }]">
    <router-view v-slot="{ Component, route }" appear>
      <transition name="list" mode="out-in">
        <div :key="route.matched[0]?.path" class="transition-wrapper">
          <AppError @reset_error="resetError" :inputMessage="error.message" :inputStatusCode="error.status"
            v-if="error" />
          <Suspense v-else>
            <div class="app-content-wrapper">
              <component :is="Component" />
            </div>
            <template #fallback>
              Loading...
            </template>
          </Suspense>
        </div>
      </transition>
    </router-view>
  </div>
</template>
<script>
export default {
  setup() {
    const error = ref(null);
    onErrorCaptured((e) => (error.value = e));
    return { error }
  },
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
    resetError() {
      this.error = null;
    }
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
@use '@/assets/styles/animations';

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

  .transition-wrapper {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;

    .app-content-wrapper {
      width: 100%;
      height: 100%;
      display: flex;
      flex-direction: column;
    }
  }

  @include animations.list;
}
</style>
