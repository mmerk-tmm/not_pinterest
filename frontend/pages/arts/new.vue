<template>
    <div class="new-art-wrapper">
        <div class="new-art-container">
            <div class="editor" @submit.prevent="save">
                <div class="column">
                    <Upload
                        border-radius="20px"
                        @file="handlePictureSelect"
                        :imageUrl="picture"
                    />
                </div>
                <div class="column">
                    <div class="art-info">
                        <AppInput
                            label="В лентах видны только первые 40 символов"
                            placeholder="Добавьте название арта"
                            v-model="name"
                            :max-length="MAX_POST_NAME_LENGTH"
                            :minLength="MIN_POST_NAME_LENGTH"
                            showWordLimit
                        />
                        <AppInput
                            placeholder="Ссылка на первоначальный источник"
                            label="Пользователь сможет перейти на оригинальную страницу с изображением"
                            v-model="source"
                        />
                        <div class="info-buttons">
                            <div
                                class="info-button"
                                @click="selectIdeaModal = true"
                            >
                                {{ ideaID !== null ? "Изменить" : "Выбрать" }}
                            </div>
                            <ModalDialog
                                :active="selectIdeaModal"
                                @close="selectIdeaModal = false"
                            >
                                <template #header></template>
                                <template #content>
                                    <IdeaSelector @select="selectIdea" />
                                </template>
                            </ModalDialog>
                        </div>
                    </div>
                </div>
            </div>
            <el-input
                type="textarea"
                placeholder="Добавьте описание арта"
                label="Когда люди нажимают на изображение они видят 50 первых символов"
                v-model="description"
                :max-length="MAX_POST_DESCRIPTION_LENGTH"
                show-word-limit
            />
            <KeywordSelector
                v-model:selectedKeywords="keywords"
                class="keyword-selector"
            />
            <div class="buttons">
                <div class="save-button" @click="save">Сохранить</div>
            </div>
        </div>
    </div>
</template>
<script setup>
import { Service } from "@/client";

const router = useRouter();
const { $toast } = useNuxtApp();
const runtimeConfig = useRuntimeConfig();
const {
    MAX_POST_NAME_LENGTH,
    MAX_POST_DESCRIPTION_LENGTH,
    MIN_POST_NAME_LENGTH,
} = runtimeConfig.public;
const picture = ref(null);
const pictureBlob = ref(null);
const handlePictureSelect = (file) => {
    picture.value = URL.createObjectURL(file);
    pictureBlob.value = file;
};
const name = ref("");
const ideaID = ref(null);
const description = ref("");
const source = ref("");
const keywords = ref([]);
const selectIdeaModal = ref(false);
const selectIdea = (idea) => {
    selectIdeaModal.value = false;
    ideaID.value = idea.id;
};
const buttonActive = computed(
    () =>
        name.value.length >= MIN_POST_NAME_LENGTH &&
        name.value.length <= MAX_POST_NAME_LENGTH &&
        description.value.length <= MAX_POST_DESCRIPTION_LENGTH &&
        keywords.value.length > 0 &&
        ideaID.value
);
const formRef = ref(null);
const save = async () => {
    if (!buttonActive.value) {
        if (name.value.length < MIN_POST_NAME_LENGTH) {
            $toast.error("Название слишком короткое");
        } else if (name.value.length > MAX_POST_NAME_LENGTH) {
            $toast.error("Название слишком длинное");
        } else if (description.value.length > MAX_POST_DESCRIPTION_LENGTH) {
            $toast.error("Описание слишком длинное");
        } else if (keywords.value.length === 0) {
            $toast.error("Добавьте хотя бы один тег");
        } else if (!ideaID.value) {
            $toast.error("Выберите идею");
        }
        return;
    }
    var form = new FormData();
    const data = {
        title: name.value,
        description: description.value,
        url: source.value,
        keywords: keywords.value.map((keyword) => keyword.name),
    };
    form.append("post_data", JSON.stringify(data));
    form.append("post_image", pictureBlob.value);
    try {
        const postData = await Service.createPostApiV1IdeasIdeaIdPostPost(
            ideaID.value,
            {
                post_data: data,
                post_image: pictureBlob.value,
            }
        );
        router.push({
            name: "arts-id",
            params: { id: postData.id },
        });
    } catch (error) {
        $toast.error("Ошибка при создании арта");
    }
};
</script>
<style lang="scss">
.new-art-wrapper {
    padding: 16px 0px;
    justify-content: center;
    display: flex;

    .new-art-container {
        padding: 20px;
        display: flex;
        flex-direction: column;
        width: 100%;
        gap: 10px;
        max-width: 750px;
        border-radius: 20px;
        background-color: $color-gray-roboflow-200;

        .buttons {
            display: flex;
            justify-content: right;
            gap: 10px;

            .save-button {
                background-color: $g-colorRed100;
                padding: 10px;
                border-radius: 10px;
                color: white;
                font-weight: 600;
                cursor: pointer;

                &:hover {
                    background-color: $g-colorRed0;
                }
            }
        }

        .editor {
            display: grid;
            grid-template-columns: 200px 1fr;
            gap: 10px;

            .column {
                display: flex;
                flex-direction: column;
                gap: 10px;

                .art-info {
                    display: flex;
                    flex-direction: column;
                    gap: 10px;

                    .info-buttons {
                        display: flex;
                        gap: 10px;

                        .info-button {
                            @include button;
                        }
                    }
                }
            }
        }
    }
}
</style>
