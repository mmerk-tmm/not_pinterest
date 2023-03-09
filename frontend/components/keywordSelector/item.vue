<template>
    <div :class="['topic', { active: isSelected }]">
        <div class="count" v-if="keyword">{{ keyword.count }}</div>
        <slot></slot>
        <div class="text">{{ name ? name : keyword?.name }}</div>
    </div>
</template>
<script setup>
const { keyword, name, borderRadiusString, selectedKeywords } = defineProps({
    keyword: {
        type: Object,
    },
    name: {
        type: String,
        default: null,
    },
    borderRadiusString: {
        type: String,
        default: "5px",
    },
    selectedKeywords: {
        type: Array,
        default: [],
    },
});

const isSelected = computed(() => {
    if (!keyword) return true;
    return selectedKeywords.map((k) => k.name).includes(keyword?.name);
});
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
