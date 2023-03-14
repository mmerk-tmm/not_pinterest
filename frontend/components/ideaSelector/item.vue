<template>
    <div class="idea-item">
        <div class="idea-item__content">
            <div class="idea-item__content__name">
                {{ idea.name }}
            </div>
            <div class="idea-item__content__description">
                {{ idea.description }}
            </div>
        </div>
        <div class="idea-item_button" @click="select">Выбрать</div>
    </div>
</template>
<script setup>
const { idea } = defineProps({
    idea: {
        type: Object,
        required: true,
    },
});
</script>
<style scoped lang="scss">
.idea-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px;
    border-bottom: 1px solid #e6e6e6;
    color: $color-text;
    background-color: $color-gray-roboflow-300;
    cursor: pointer;
    &:hover {
        background-color: $color-gray-roboflow-400;
    }
    &__content {
        &__name {
            font-size: 16px;
            font-weight: 500;
            margin-bottom: 5px;
        }
        &__description {
            font-size: 14px;
            color: #666;
        }
    }
    &_button {
        padding: 5px 10px;
        border-radius: 5px;
        background-color: #f5f5f5;
        &:hover {
            background-color: #e6e6e6;
        }
    }
}
</style>
