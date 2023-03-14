<template>
    <div class="topic-selector">
        <AppInput v-model="searchText" />
        <div class="keywords" v-if="!resultsEmpty">
            <IdeaSelectorItem
                @click="emit('select', idea)"
                :idea="idea"
                v-for="idea in ideas"
                :key="idea.id"
            />
        </div>
        <div class="create-idea" v-else>
            <div class="test">
                Идея не найдена,
                <nuxt-link to="/ideas/new" target="_blank">
                    создайте новую
                </nuxt-link>
            </div>
        </div>
    </div>
</template>
<script setup>
import { Service } from "~~/client";
const emit = defineEmits(["select"]);
const searchText = ref("");
const ideas = ref([]);

watch(
    searchText,
    async (value) => {
        if (value.length > 0) {
            const data = await Service.searchIdeasApiV1IdeasSearchGet(value);
            ideas.value = data;
        } else {
            ideas.value = [];
        }
    },
    { immediate: true }
);
const resultsEmpty = computed(() => ideas.value.length === 0);
</script>
<style lang="scss">
.topic-selector {
    .keywords {
        display: flex;
        flex-direction: column;
        .idea-selector-item {
            margin-bottom: 10px;
        }
    }
    .create-idea {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100px;
        .test {
            font-size: 14px;
            color: #000000;
            font-weight: 500;
            line-height: 17px;
            a {
                color: #000000;
                font-weight: 500;
                line-height: 17px;
                text-decoration: underline;
            }
        }
    }
}
</style>
