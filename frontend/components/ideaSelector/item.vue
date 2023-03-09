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
        <div class="idea-item__footer">
            <div class="idea-item__footer__button" @click="select">Выбрать</div>
        </div>
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
    flex-direction: column;
    gap: 10px;
    border: 1px solid $color-gray-roboflow-500;
    padding: 5px;
    border-radius: 5px;
    &__content {
        display: flex;
        flex-direction: column;
        gap: 10px;
        &__name {
            font-size: 20px;
            font-weight: 600;
        }
        &__description {
            font-size: 16px;
        }
    }
    &__footer {
        display: flex;
        justify-content: flex-end;
        &__button {
            padding: 5px 10px;
            border-radius: 5px;
            background-color: $color-red-roboflow-500;
            color: white;
            cursor: pointer;
        }
    }
}
</style>
