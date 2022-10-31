<template>
    <div class="new-idea-wrapper">
        <div class="new-idea-container">
            <h1>Черновики пинов-идей</h1>
        </div>
    </div>
</template>
<style lang="scss">
@use '@/assets/styles/helpers';

.new-idea-wrapper {
    padding: 16px 0px;
    justify-content: center;
    display: flex;

    .new-idea-container {
        padding: 32px 0px;
        display: flex;
        flex-direction: column;
        max-width: 400px;

        h1 {
            font-weight: 600;
            word-wrap: break-word;
            font-family: var( --font-family-default-latin);
        }
    }
}
</style>
<script>
</script>