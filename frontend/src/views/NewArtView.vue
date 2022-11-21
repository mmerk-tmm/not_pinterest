<template>
    <div class="new-art-wrapper">
        <div class="new-art-container">
            <div class="buttons">
                <div class="save-button">
                    Сохранить
                </div>
            </div>
            <div class="editor">
                <div class="column">
                    <SelectImage />
                </div>
            </div>
        </div>
    </div>
</template>
<style lang="scss">
@use '@/assets/styles/helpers';

.new-art-wrapper {
    padding: 16px 0px;
    justify-content: center;
    display: flex;

    .new-art-container {
        padding: 32px 0px;
        display: flex;
        flex-direction: column;
        width: 100%;
        max-width: 880px;
        border-radius: 20px;
        background-color: var(--color-gray-roboflow-200);
        padding: 10px;

        .buttons {
            display: flex;
            justify-content: right;
            gap: 10px;

            .save-button {
                background-color: var(--g-colorRed100);
                padding: 10px;
                border-radius: 10px;
                color: white;
                font-weight: 600;
                cursor: pointer;
            }
        }

        .editor {
            display: grid;
            grid-template-columns: 270px 1fr;
        }
    }
}
</style>
<script>
import SelectImage from '../components/SelectImage.vue';
export default {
    components: {SelectImage}
}
</script>