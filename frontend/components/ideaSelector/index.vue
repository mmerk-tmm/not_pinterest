<template>
    <div class="topic-selector">
        <AppInput v-model="searchText" />
        <div class="keywords" v-if="!resultsEmpty">
            <IdeaSelectorItem
                :keyword="keyword"
                v-for="keyword in keywords"
                :key="keyword.id"
            />
            <div class="create-idea" v-if="notResults">
                <div class="test">
                    Идея не найдена,
                    <nuxt-link to="/ideas/new">создайте новую</nuxt-link>
                </div>
            </div>
        </div>
    </div>
</template>
<script setup>


const emit = defineEmits(["update:select"]);
const
</script>
<style lang="scss">
.keyword-selector {
    display: flex;
    flex-direction: column;
    gap: 10px;

    .keywords {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        border: 1px solid var(--color-gray-roboflow-500);
        padding: 5px;
        border-radius: v-bind(borderRadiusString);
    }
}
</style>
