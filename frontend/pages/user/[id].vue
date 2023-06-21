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
                v-if="userData && user.id !== userData?.id"
            >
                {{ user.liked ? "Отписаться" : "Подписаться" }}
            </div>

            <div class="followers-count">
                <span>{{ user.followers_count }}</span> подписчиков
            </div>
            <div class="selector">
                <div
                    :class="['selector-item', { active: selectedTab === 'my' }]"
                    @click="selectedTab = 'my'"
                >
                    Мои
                </div>
                <div
                    :class="[
                        'selector-item',
                        { active: selectedTab === 'liked' },
                    ]"
                    @click="selectedTab = 'liked'"
                >
                    Понравившиеся
                </div>
                <div
                    :class="[
                        'selector-item',
                        { active: selectedTab === 'followed' },
                    ]"
                    @click="selectedTab = 'followed'"
                >
                    Подписки
                </div>
            </div>
        </div>
        <div class="posts" v-if="selectedTab !== 'followed'">
            <PostCard v-for="post in posts" :key="post.id" :post="post" />
        </div>
        <div class="posts" v-else>
            <UserCard
                v-for="user in followed_users"
                :key="user.id"
                :user="user"
            />
        </div>
    </div>
</template>
<script setup>
import { Service } from "@/client";
import { useAuthStore } from "@/stores/auth";
import { storeToRefs } from "pinia";

const { logined, userData } = storeToRefs(useAuthStore());
const { id } = useRoute().params;
const selectedTab = ref("my");
const user = ref(await Service.getUserPostsApiV1UsersUserIdGet(id, 1));
const posts = ref([]);
const liked_posts = ref(
    await Service.getLikedPostsApiV1UsersUserIdPostsLikedGet(id, 1)
);
const followed_users = ref(
    await Service.getFollowedUsersApiV1UsersUserIdFollowedGet(id, 1)
);
watch(
    selectedTab,
    () => {
        posts.value = [];
        var new_items =
            selectedTab.value == "my" ? user.value.posts : liked_posts.value;
        posts.value.push(
            ...new_items.map((post) => ({ ...post, user: user.value }))
        );
    },
    { immediate: true }
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

        .selector {
            display: flex;
            gap: 1rem;
            background-color: $color-gray-roboflow-200;
            padding: 10px;
            border-radius: 30px;
            .selector-item {
                cursor: pointer;
                padding: 10px;
                border-radius: 20px;

                &.active {
                    background-color: $color-black-cosmicore-900;
                    color: $color-text-rev;

                    &:hover {
                        background-color: $color-black-cosmicore-900;
                    }
                }
            }
        }
    }
    .posts {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
        gap: 10px;
        padding: 10px;
    }
}
</style>
