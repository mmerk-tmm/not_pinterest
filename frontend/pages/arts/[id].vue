<template>
    <div>
        <h1>Art</h1>
        <p>Art ID: {{ id }}</p>
    </div>
</template>
<script setup>
import { Service } from "@/client";
const { id } = useRoute();
</script>
