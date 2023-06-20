<template>
    <NuxtErrorBoundary @error="handleError">
        <div class="default-layout">
            <AppHeader />

            <div class="app-content">
                <slot />
            </div>
        </div>
        <template #error="{ error }">
            <AppError :error="error" @clearError="fixIssue(error)" />
        </template>
    </NuxtErrorBoundary>
</template>
<style lang="scss">
.default-layout {
    display: grid;
    height: 100%;
    grid-template-rows: 80px 1fr;

    .app-content {
        grid-row: 2;
        overflow: auto;
        padding-inline: 20px;
        @include lg(true) {
            padding-inline: 10px;
        }
        height: 100%;
    }
}
</style>
<script setup>
const fixIssue = (error) => {
    error.value = null;
};
const handleError = (error) => {
    console.error(error);
};
</script>
