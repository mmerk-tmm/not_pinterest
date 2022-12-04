<template>
    <div class="topic-selector">
        <FormField v-model="searchText" :border-radius="borderRadius" off-margin label="Выберите ключевые слова" />
        <div class="topics" v-if="!resultsEmpty">
            <topicItem :topicData="topic" v-for="topic in topics" :key="item.id" @click="selectTopic(topic)"
                :border-radius-string="borderRadiusString" />
            <topicItem class="topic" v-if="notResults" :name="searchText"
                @click="selectTopic({ new: true, name: searchText })">
                <div class="icon">
                    <FontAwesomeIcon icon="fa-plus" />
                </div>
            </topicItem>
        </div>
        {{ selectedTopics }}
    </div>
</template>
<script setup>
import { useTopicsSearch } from '../../composables/topics';
import topicItem from './topicItem.vue';
import FormField from '../FormField.vue';
import { computed, ref, provide } from 'vue';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { library } from '@fortawesome/fontawesome-svg-core';
import { faPlus } from '@fortawesome/free-solid-svg-icons';
library.add(faPlus);
const { searchText, topics } = useTopicsSearch();
const props = defineProps(['borderRadius']);
const borderRadius = props.borderRadius;
const borderRadiusString = borderRadius + 'px';
provide('borderRadiusString', borderRadiusString)

const resultsEmpty = computed(() => searchText.value.length === 0)

const notResults = computed(() => !resultsEmpty.value && topics.value.length === 0);

const selectedTopics = ref([]);
provide('selectedTopics', computed(() => selectedTopics));
const selectTopic = (topic) => {
    // var index = selectedTopics.value.map(topic => topic.name).indexOf(topic.name);
    // if (index !== -1) {
    //     selectedTopics.value.splice(index)
    // }
    selectedTopics.value.push(topic);
}

</script>
<style lang="scss">
.topic-selector {
    display: flex;
    flex-direction: column;
    gap: 10px;


    .topics {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        border: 1px solid var(--color-gray-roboflow-500);
        padding: 5px;
        border-radius: v-bind(borderRadiusString);


    }
}
</style>