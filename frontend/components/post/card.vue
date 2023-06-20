<template>
    <nuxt-link class="card" :to="{ name: 'arts-id', params: { id: post.id } }">
        <img :src="post.picture" alt="" />
        <div class="info">
            <div class="user-info">{{ post.description }}</div>
            <div class="desc">
                {{ post.user.username }}
            </div>
        </div>
    </nuxt-link>
</template>
<script setup>
const { post } = defineProps({
    post: {
        type: Object,
        required: true,
    },
});
</script>
<style lang="scss" scoped>
.card {
    padding: 10px;
    background-color: rgba($color: #000000, $alpha: 0.1);
    border-radius: 20px;
    display: flex;
    flex-direction: column;
    position: relative;

    img {
        border-radius: 20px;
        object-fit: cover;
        width: 100%;
        max-height: 200px;
    }
    .info {
        padding: 10px;
        .user-info {
            font-weight: bold;
        }
        .desc {
            text-overflow: ellipsis;

            /* Needed to make it work */
            overflow: hidden;
            white-space: nowrap;
        }
    }
}
</style>
