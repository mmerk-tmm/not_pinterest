<template>
    <div class="settings-selection">
        <h1>Общедоступный профиль</h1>
        <!-- <div class="detail">В вашем профиле можно будет увидеть указанную информацию</div> -->
        <div class="picture-editor">
            <SelectImage />
            <div class="picture-editor-content">
                <FormField :borderRadius="10" placeholder="Имя" offMargin />
                <FormField :borderRadius="10" placeholder="Фамилия" offMargin />
            </div>
        </div>
        <FormTextArea class="description" label="Описание" placeholder="Расскажите свою историю" :rows="5" offMargin />
        <FormField :borderRadius="10" label="Веб-сайт"
            placeholder="Добавьте ссылку для привлечения трафика на свой сайт" offMargin />
        <FormField :borderRadius="10" label="Имя пользователя" placeholder="И пусть это имя войдет в историю..."
            offMargin notEmpty />
        <div class="button active">Сохранить</div>
        <div class="button">Сбросить</div>
    </div>
</template>
<script>
import SelectImage from './SelectImage.vue';
import FormField from './FormField.vue';
import FormTextArea from './FormTextArea.vue';
export default {
    components: {
        SelectImage,
        FormField,
        FormTextArea
    }
}
</script>
<style lang="scss" scoped>


.picture-editor {
    margin-top: 10px;
    display: grid;
    grid-template-columns: 95px 1fr;
    gap: 10px;

    .picture-editor-content {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
}

.button {
    padding: 10px;
    border-radius: 10px;
    background-color: var(--color-gray-roboflow-300);
    text-align: center;

    &.active {
        background: black;
        color: white;
        cursor: pointer;
    }
}
</style>