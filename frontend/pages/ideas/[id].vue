<template>
    <div class="idea-page">
        <div class="idea-info">
            <div class="idea-name">
                <h1>{{ idea_data.name }}</h1>
            </div>
            <div class="keywords">
                <div
                    class="keyword"
                    v-for="keyword in idea_data.keywords"
                    :key="keyword"
                >
                    <span>{{ keyword.name }}</span>
                </div>
            </div>
        </div>
        <div class="posts">
            <PostCard
                v-for="post in idea_data.posts"
                :key="post.id"
                :post="post"
            />
        </div>
        <div class="load-more" v-if="show_button" @click="getNextPage">
            Загрузить еще
        </div>
    </div>
</template>
<script setup>
import { Service } from "@/client";
const { id } = useRoute().params;
const page = ref(1);
const show_button = ref(false);
const idea_data = ref(await Service.getIdeaApiV1IdeasIdeaIdGet(id, page.value));
const getNextPage = async () => {
    page.value++;
    const posts = await Service.getIdeaApiV1IdeasIdeaIdGet(id, page.value);
    show_button.value = posts.posts.length == 30;
    idea_data.value.posts.push(...posts.posts);
};
</script>

<style scoped lang="scss">
.idea-page {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    .idea-info {
        @include flex-center;
        flex-direction: column;
        .idea-name {
            h1 {
                font-size: 2rem;
                font-weight: 700;
            }
        }
        .keywords {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            .keyword {
                padding: 0.5rem 1rem;
                border-radius: 20px;
                background-color: $color-black-cosmicore-900;
                color: $color-text-rev;
                font-size: 1rem;
                font-weight: 700;
            }
        }
    }

    .posts {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 10px;
    }
    .load-more {
        @include flex-center;
        padding: 10px;
        border-radius: 20px;
        cursor: pointer;
        color: $color-text-rev;
        background-color: $g-colorRed0;
        &:hover {
            background-color: $color-black-cosmicore-900;
        }
    }
}
</style>
