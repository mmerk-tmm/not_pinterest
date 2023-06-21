<template>
    <div class="user-page" v-if="user">
        <div class="user-info">
            <div class="avatar">
                <img :src="user.picture" v-if="user.picture" />
                <Icon name="material-symbols:person" v-else />
            </div>
            <div class="username">{{ user.username }}</div>
            <div
                :class="['follow-button', { active: user.liked }]"
                @click="likeUser"
            >
                {{ user.liked ? "Отписаться" : "Подписаться" }}
            </div>
            <div class="followers-count">
                <span>{{ user.followers_count }}</span> подписчиков
            </div>
        </div>
        <div class="posts">
            <PostCard v-for="post in posts" :key="post.id" :post="post" />
        </div>
    </div>
</template>
<script setup>
import { Service } from "@/client";
import { useAuthStore } from "@/stores/auth";
import { storeToRefs } from "pinia";

const { logined } = storeToRefs(useAuthStore());
const { id } = useRoute().params;

const user = ref(await Service.getUserPostsApiV1UsersUserIdGet(id, 1));
const posts = computed(() =>
    user.value.posts.map((post) => ({ ...post, user: user.value }))
);
const likeUser = async () => {
    if (!logined.value) {
        router.push("/login");
        return;
    }
    user.value.liked = await Service.likeUserApiV1UsersUserIdLikePut(
        user.value.id
    );
};
</script>
<style scoped lang="scss">
.user-page {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    .follow-button {
        @include flex-center;
        padding: 10px;
        border-radius: 20px;

        cursor: pointer;
        color: $color-text-rev;
        background-color: $g-colorRed0;
        &.active {
            background-color: $color-black-cosmicore-900;

            &:hover {
                background-color: $color-black-cosmicore-900;
            }
        }

        &:hover {
            background-color: $g-colorRed100;
        }
    }
    .user-info {
        @include flex-center;
        flex-direction: column;
        gap: 1rem;
        .avatar {
            width: 200px;
            height: 200px;
            border-radius: 50%;
            background-color: #ccc;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden;

            img {
                width: 100%;
                height: 100%;
                object-fit: cover;
            }

            svg {
                width: 40px;
                height: 40px;
                fill: #fff;
            }
        }
        .username {
            font-size: 1.5rem;
            font-weight: bold;
        }
    }
    .posts {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 10px;
    }
}
</style>
