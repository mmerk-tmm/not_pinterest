<template>
    <div class="new-idea-wrapper">
        <div class="new-idea-container">
            <AppInput
                label="Название идеи"
                placeholder="Добавьте название идеи"
                v-model="name"
                :max-length="MAX_IDEA_NAME_LENGTH"
                :minLength="MIN_IDEA_NAME_LENGTH"
                showWordLimit
            />
            <AppInput
                placeholder="Описание"
                label="Опишите идею"
                v-model="description"
                :max-length="MAX_IDEA_DESCRIPTION_LENGTH"
                showWordLimit
            />
            <KeywordSelector
                v-model:selectedKeywords="keywords"
                class="keyword-selector"
            />
            <div class="buttons">
                <div
                    :class="[{ active: buttonActive }, 'send-button']"
                    @click="sendIdea"
                >
                    Отправить
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { Service } from "@/client";
import { useToast } from "vue-toastification";

const router = useRouter();
const toast = useToast();
const runtimeConfig = useRuntimeConfig();
const {
    MAX_IDEA_NAME_LENGTH,
    MAX_IDEA_DESCRIPTION_LENGTH,
    MIN_IDEA_NAME_LENGTH,
} = runtimeConfig.public;

const name = ref("");

const description = ref("");

const keywords = ref([]);

const buttonActive = computed(() => {
    return (
        name.value.length >= MIN_IDEA_NAME_LENGTH &&
        name.value.length <= MAX_IDEA_NAME_LENGTH &&
        description.value.length <= MAX_IDEA_DESCRIPTION_LENGTH
    );
});
const sendIdea = async () => {
    if (!buttonActive.value) return;
    try {
        await Service.createIdeaApiV1IdeasPost({
            name: name.value,
            description: description.value,
        });
        router.push({ path: "/ideas" });
    } catch (error) {
        if (error?.response?.status === 400) {
            toast.error(HandleOpenApiError(error).message);
        } else {
            throw error;
        }
    }
};
</script>
<style scoped lang="scss">
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
        background-color: $color-gray-roboflow-200;

        .buttons {
            display: flex;
            gap: 10px;

            .send-button {
                user-select: none;
                padding: 10px;
                border-radius: 10px;
                flex-grow: 1;
                text-align: center;
                font-weight: 600;
                cursor: pointer;
                @include button-colors;
            }
        }
    }
}
</style>
