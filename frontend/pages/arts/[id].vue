<template>
    <div class="art-page-container">
        <div class="art-page">
            <img :src="post.picture" alt="" />
            <div class="info">
                <div class="user-info">{{ post.description }}</div>
                <div class="desc">
                    {{ post.user.username }}
                </div>
            </div>
        </div>
    </div>
</template>
<script setup>
import { Service } from "@/client";
const { id } = useRoute().params;
console.log(id);
const post = await Service.getPostApiV1PostsPostIdGet(id);
</script>
<style lang="scss" scoped>
.art-page-container {
    @include flex-center;
    height: 100%;

    .art-page {
        width: 100%;
        max-width: 900px;
        padding: 20px;
        background-color: #fff;
        border-radius: 20px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
        display: grid;
        grid-template-columns: 1fr 2fr;
        gap: 10px;

        img {
            border-radius: 20px;
            object-fit: cover;
            width: 100%;
        }
    }
}
</style>
