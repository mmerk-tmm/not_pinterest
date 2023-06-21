<template>
    <div class="art-page-container">
        <div class="art-page">
            <img :src="post.picture" alt="" />
            <div class="info">
                <div class="controls">
                    <div class="copy-link" @click="copyLink">
                        <Icon name="material-symbols:link" />
                        <div class="text">Скопировать ссылку</div>
                    </div>
                    <div
                        :class="['button save', { active: post.liked }]"
                        @click="toggleSave"
                    >
                        {{ post.liked ? "Сохранено" : "Сохранить" }}
                    </div>
                </div>
                <div class="title">
                    {{ post.title }}
                </div>
                <div class="desc">
                    {{ post.user.username }}
                </div>
                <nuxt-Link class="user-info" :to="`/user/${post.user.id}`">
                    <div class="avatar">
                        <img
                            :src="post.user.picture"
                            v-if="post.user.picture"
                            alt=""
                        />
                        <Icon name="material-symbols:person" v-else />
                    </div>
                    <div class="info-data">
                        <div class="username">
                            {{ post.user.username }}
                        </div>
                        <div class="folowers">
                            {{ post.user.followers_count }} подписчиков
                        </div>
                    </div>
                    <div
                        @click.prevent="likeUser"
                        :class="['follow button', { active: post.user.liked }]"
                    >
                        {{ post.user.liked ? "Подписан" : "Подписаться" }}
                    </div>
                </nuxt-Link>
                <div class="comments">
                    <div class="headline">Комментарии</div>
                    <div class="comments-items" v-if="post.comments.length">
                        <div
                            class="user-info comment"
                            v-for="comment in post.comments"
                        >
                            <div class="avatar">
                                <img
                                    :src="comment.user.picture"
                                    v-if="comment.user.picture"
                                    alt=""
                                />
                                <Icon name="material-symbols:person" v-else />
                            </div>
                            <div class="info-data">
                                <nuxt-link
                                    class="username"
                                    :to="`/user/${comment.user.id}`"
                                >
                                    {{ comment.user.username }}
                                </nuxt-link>
                                <div class="content">
                                    {{ comment.content }}
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="empty-comments" v-else>
                        У этого поста еще нет комментариев
                    </div>
                    <div class="comment-form">
                        <AppInput
                            v-model="comment"
                            placeholder="Напишите комментарий"
                            :max-length="180"
                        />
                        <div class="button" @click="sendComment">Отправить</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script setup>
import { Service } from "@/client";
import { useAuthStore } from "@/stores/auth";
import { storeToRefs } from "pinia";

const { logined } = storeToRefs(useAuthStore());
const { id } = useRoute().params;
const post = ref(await Service.getPostApiV1PostsPostIdGet(id));
const router = useRouter();
const toggleSave = async () => {
    if (!logined.value) {
        router.push("/login");
        return;
    }
    post.value.liked = await Service.likePostApiV1PostsPostIdLikePut(id);
};
const comment = ref("");
const likeUser = async () => {
    if (!logined.value) {
        router.push("/login");
        return;
    }
    post.value.user.liked = await Service.likeUserApiV1UsersUserIdLikePut(
        post.value.user.id
    );
};
const sendComment = async () => {
    if (!logined.value) {
        router.push("/login");
        return;
    }
    const new_comment =
        await Service.createPostCommentApiV1PostsPostIdCommentsPost(id, {
            text: comment.value,
        });
    post.value.comments.push(new_comment);
    comment.value = "";
};
const copyLink = () => {
    navigator.clipboard.writeText(
        window.location.origin + "/arts/" + post.value.id
    );
};
</script>
<style lang="scss" scoped>
.button {
    @include flex-center;
    padding: 10px;
    border-radius: 20px;
    background-color: $color-gray-roboflow-300;
    cursor: pointer;

    &:hover {
        background-color: $color-gray-roboflow-400;
    }
}
.art-page-container {
    @include flex-center;
    height: 100%;

    .art-page {
        width: 100%;
        height: 100%;
        max-width: 900px;
        padding: 20px;
        background-color: #fff;
        border-radius: 20px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
        display: grid;
        grid-template-columns: 1fr 2fr;
        gap: 10px;

        @include lg(true) {
            grid-template-columns: 1fr;
        }

        & > img {
            border-radius: 20px;
            object-fit: cover;
            width: 100%;
        }

        .info {
            display: flex;
            flex-direction: column;
            gap: 10px;
            padding: 10px;

            .controls {
                display: flex;
                gap: 10px;
                justify-content: space-between;
                .copy-link {
                    @include flex-center;
                    width: 40px;
                    height: 40px;
                    border-radius: 50%;
                    cursor: pointer;
                    background-color: $color-gray-roboflow-300;
                    .text {
                        display: none;
                    }
                    @include lg(true) {
                        width: auto;
                        height: auto;
                        border-radius: 20px;
                        padding: 10px;
                        display: flex;
                        gap: 10px;
                        .text {
                            display: block;
                        }
                    }
                    &:hover {
                        background-color: $color-gray-roboflow-400;
                    }
                }
                .save {
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
            }

            .title {
                font-size: 24px;
                font-weight: 700;
            }
            .user-info {
                display: grid;
                gap: 10px;
                grid-template-columns: 50px 1fr 100px;

                .avatar {
                    width: 50px;
                    height: 50px;
                    border-radius: 50%;
                    overflow: hidden;
                    background-color: $color-gray-roboflow-300;
                    @include flex-center;

                    img {
                        width: 100%;
                        height: 100%;
                        object-fit: cover;
                    }
                }
                .info-data {
                    display: flex;
                    flex-direction: column;

                    .username {
                        font-size: 16px;
                        font-weight: 700;

                        &:hover {
                            text-decoration: underline;
                        }
                    }
                    .folowers {
                        font-size: 14px;
                        font-weight: 400;
                    }
                }

                .follow {
                    margin-left: auto;

                    &.active {
                        background-color: $color-black-cosmicore-900;
                        color: $color-text-rev;

                        &:hover {
                            background-color: $color-black-cosmicore-900;
                        }
                    }
                }
            }

            .comments {
                display: flex;
                flex-direction: column;
                gap: 10px;
                margin-top: 20px;
                .comments-items {
                    display: flex;
                    flex-direction: column;
                    gap: 10px;
                    .comment {
                        background-color: $color-gray-roboflow-200;
                        padding: 10px;
                        border-radius: 10px;
                        grid-template-columns: 50px 1fr;
                        .content {
                            overflow-wrap: anywhere;
                        }
                    }
                }

                .headline {
                    font-size: 20px;
                    font-weight: 700;
                }
                .comment-form {
                    display: flex;
                    gap: 10px;
                }
            }
        }
    }
}
</style>
