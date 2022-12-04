<template>
    <div :class="['topic', { active: isSelected }]">
        <div class="count" v-if="topicData?.count">{{ topicData?.count }}</div>
        <slot></slot>
        <div class="text"> {{ name }}</div>
    </div>
</template>
<script setup>
import { computed, inject } from 'vue';
const props = defineProps(['topicData', 'borderRadiusString', 'name']);
const topicData = props.topicData;
const borderRadiusString = inject('borderRadiusString');
const name = topicData.name || props.name;
const selectedTopics = inject('selectedTopics');
const isSelected = computed(() => selectedTopics.value.value.map(topic => topic.name).includes(topicData.name))

</script>
<style lang="scss">
.topic {
    background-color: var(--color-gray-roboflow-300);
    padding: 5px 10px;
    border-radius: calc(v-bind(borderRadiusString) - 5px);
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 5px;
    cursor: pointer;

    &.active {
        background-color: black;
        color: white;

        svg {
            color: white;
        }
    }

    .text {
        word-break: break-all;
    }

    svg {
        width: 15px;
        height: 15px;
        color: var(--color-gray-roboflow-600);
    }
}
</style>