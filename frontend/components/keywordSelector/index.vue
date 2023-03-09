<template>
    <div class="topic-selector">
        <AppInput v-model="searchText" label="Выберите ключевые слова" />
        <div class="keywords" v-if="!resultsEmpty">
            <keywordSelectorItem
                :keyword="keyword"
                v-for="keyword in keywords"
                :key="keyword.id"
                @click="selectKeyword(keyword)"
                :selectedKeywords="selectedKeywords"
                :borderRadiusString="borderRadiusString"
            />
            <keywordSelectorItem
                v-if="notResults"
                :name="searchText"
                @click="selectKeyword({ new: true, name: searchText })"
            >
                <div class="icon">
                    <Icon name="material-symbols:add" />
                </div>
            </keywordSelectorItem>
        </div>
        {{ selectedKeywords }}
    </div>
</template>
<script setup>
const { searchText, keywords } = useKeywordSearch();
const props = defineProps({
    borderRadius: {
        type: Number,
        default: 5,
    },
    selectedKeywords: {
        type: Array,
        default: () => [],
    },
});
const emit = defineEmits(["update:selectedKeywords"]);
const borderRadius = props.borderRadius;
const borderRadiusString = borderRadius + "px";

const resultsEmpty = computed(() => searchText.value.length === 0);

const notResults = computed(
    () => !resultsEmpty.value && keywords.value.length === 0
);

const selectedKeywords = ref(props.selectedKeywords);

const selectKeyword = (keywords) => {
    selectedKeywords.value.push(keywords);
};

watch(selectedKeywords, (val) => {
    emit("update:selectedKeywords", val);
});
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
