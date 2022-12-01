<template>
    <div class="new-idea-wrapper">
        <div class="new-idea-container">
            <FormField label="Название идеи" placeholder="Добавьте название идеи" v-model="name" :border-radius="10"
                off-margin not-empty :force-wrong="nameAlreadyExists" />
            <FormTextArea placeholder="Описание" label="Опишите идею" v-model="description" off-margin not-empty />
            <div class="buttons">
                <div :class="[{ active: buttonActive }, 'send-button']" @click="sendIdea">
                    Отправить
                </div>
            </div>

        </div>
    </div>
</template>

<script setup>
import FormField from '../components/FormField.vue';
import FormTextArea from '../components/FormTextArea.vue';
import { ref } from 'vue';
import { HTTP } from '../http-common.vue';
import { computed } from '@vue/reactivity';
import { useToast } from 'vue-toastification';
import { handleAxiosError } from '../composables/errors';
import { useRouter } from 'vue-router'

const router = useRouter();
const toast = useToast();
const { VITE_MAX_IDEA_NAME_LENGTH, VITE_MAX_IDEA_DESCRIPTION_LENGTH } = import.meta.env;

const MaxNameLength = Number(VITE_MAX_IDEA_NAME_LENGTH);
const name = ref('');
const existingТame = ref('');
const nameIsValid = computed(() => {
    let length = name.value.length;
    return length > 0 && length <= MaxNameLength;
});
const nameAlreadyExists = computed(() => name.value === existingТame.value);

const description = ref('');
const MaxDescriptionLength = Number(VITE_MAX_IDEA_DESCRIPTION_LENGTH);
const descriptionIsValid = computed(() => {
    let length = description.value.length;
    return length > 0 && length <= MaxDescriptionLength
});

const buttonActive = computed(() => nameIsValid.value && descriptionIsValid.value && !nameAlreadyExists.value)
const sendIdea = async () => {
    if (!buttonActive.value) return
    try {
        const { data } = await HTTP.post('ideas', { name: name.value, description: description.value });
        router.push({ path: '/ideas' })
    } catch (error) {
        if (error?.response?.status === 400) {
            toast.error(handleAxiosError(error).message);
        } else {
            throw error;
        }
    }

}
</script>
<style lang="scss">
@use '@/assets/styles/helpers';
@use '@/assets/styles/components';

.new-idea-wrapper {
    padding: 16px 0px;
    justify-content: center;
    display: flex;

    .new-idea-container {
        padding: 20px;
        display: flex;
        flex-direction: column;
        width: 100%;
        gap: 10px;
        max-width: 500px;
        border-radius: 20px;
        background-color: var(--color-gray-roboflow-200);

        .buttons {
            display: flex;
            gap: 10px;

            .send-button {
                @include components.button-colors;
                user-select: none;
                padding: 10px;
                border-radius: 10px;
                flex-grow: 1;
                text-align: center;
                font-weight: 600;
                cursor: pointer;
            }
        }

    }
}
</style>