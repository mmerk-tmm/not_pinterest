<template>
    <div class="container">
        <PostCard v-for="post in posts" :key="post.id" :post="post" />
    </div>
</template>
<script setup>
import { Service } from "@/client";
const posts = await Service.getPostsApiV1PostsLastGet();
</script>
<style lang="scss" scoped>
.container {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 10px;
    margin: auto;
}
</style>
