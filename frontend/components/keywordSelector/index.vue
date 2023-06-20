<template>
    <div class="topic-selector">
        <div class="keywords search">
            <AppInput
                v-model="searchText"
                label="Выберите ключевые слова"
                placeholder="Поиск по тегам"
            />
            <template v-if="!resultsEmpty">
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
            </template>
        </div>
        <div class="keywords">
            <keywordSelectorItem
                :keyword="keyword"
                v-for="keyword in selectedKeywords"
                :key="keyword.id"
                @click="deleteKeyword(keyword)"
                :selectedKeywords="selectedKeywords"
                :borderRadiusString="borderRadiusString"
            />
        </div>
    </div>
</template>
<script setup>
const { searchText, keywords, clearSearch } = useKeywordSearch();
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

const selectedKeywords = computed({
    get: () => props.selectedKeywords,
    set: (val) => emit("update:selectedKeywords", val),
});

const selectKeyword = (keywords) => {
    clearSearch();
    selectedKeywords.value.push(keywords);
};
const deleteKeyword = (keyword) => {
    selectedKeywords.value = selectedKeywords.value.filter(
        (item) => item.id !== keyword.id
    );
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
        padding: 5px;
        border-radius: v-bind(borderRadiusString);
        &.search {
            border: 1px solid $color-gray-roboflow-500;
        }
    }
}
</style>
