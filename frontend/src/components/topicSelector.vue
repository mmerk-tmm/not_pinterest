<template>
    <div class="topic-selector">
        {{ topics }}
        <FormField v-model="searchText" />
    </div>
</template>
<script setup>
import { useTopicsSearch } from '../composables/topics';
import FormField from './FormField.vue';
const { searchText, topics } = useTopicsSearch();
</script>