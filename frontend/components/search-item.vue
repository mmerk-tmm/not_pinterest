<template>
    <div class="search-item" @click="GoToItem">
        <div class="picture">
            <img
                :src="item.info.picture"
                alt="picture"
                v-if="item.info.picture"
            />
            <Icon
                name="material-symbols:person"
                v-else-if="item.type === 'user'"
            />
            <Icon name="mdi:lightbulb-on" v-else-if="item.type === 'idea'" />
        </div>
        <div class="title">
            {{ title }}
        </div>
        <Icon name="material-symbols:chevron-right" class="end" />
    </div>
</template>
<script setup>
const emit = defineEmits(["select"]);
const { item } = defineProps(["item"]);

const linkName = computed(() => {
    switch (item.type) {
        case "idea":
            return "ideas-id";
        case "post":
            return "arts-id";
        case "user":
            return "user-id";
    }
});
const title = computed(() => {
    switch (item.type) {
        case "idea":
            return item.info.name;
        case "post":
            return item.info.title;
        case "user":
            return item.info.username;
    }
});
const router = useRouter();
const GoToItem = () => {
    router.push({ name: linkName.value, params: { id: item.info.id } });
    emit("select");
};
</script>
<style scoped lang="scss">
.search-item {
    padding: 10px;
    cursor: pointer;
    background-color: $color-gray-roboflow-200;
    border-radius: 10px;
    @include flex-center;
    gap: 10px;
    flex-direction: row;

    &:hover {
        background-color: $color-gray-roboflow-300;
    }

    .picture {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        overflow: hidden;
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: $color-gray-roboflow-100;

        img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
    }
    .end {
        margin-left: auto;
    }
}
</style>
