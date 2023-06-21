<template>
    <nuxt-link
        class="user-card"
        :to="{ name: 'user-id', params: { id: user.id } }"
    >
        <div class="picture">
            <img :src="user.picture" v-if="user.picture" />
            <Icon name="material-symbols:person" v-else />
        </div>
        <div class="title">
            {{ user.username }}
        </div>
    </nuxt-link>
</template>
<script setup>
const { user } = defineProps(["user"]);
</script>
<style scoped lang="scss">
.user-card {
    padding: 10px;
    cursor: pointer;
    background-color: $color-gray-roboflow-200;
    border-radius: 10px;
    @include flex-center;
    flex-direction: column;
    gap: 10px;

    width: 100%;
    max-width: 300px;
    .picture {
        width: 100%;
        aspect-ratio: 1;
        border-radius: 50%;
        overflow: hidden;
        @include flex-center;
        background-color: $color-gray-roboflow-300;
        img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        svg {
            font-size: 30px;
        }
    }
    .title {
        font-size: 20px;
        font-weight: 500;
    }
}
</style>
