<template>
    <div class="idea">
        <div class="user-info">
            <div :class="['user-picture', { empty: !idea_user.picture }]">
                <img :src="idea_user.picture" v-if="idea_user.picture">
                <FontAwesomeIcon icon="fa-user" />
            </div>
            <div class="user-meta">
                <div class="user-meta-column">
                    <div class="user-meta-row dot-splitter">
                        <div class="name">{{ showedName }}</div>
                        <div class="date">{{ idea.created }}</div>
                    </div>
                    <div class="user-meta-row dot-splitter">
                        <div class="description" v-if="idea_user.description">{{ idea_user.description }}</div>
                    </div>
                </div>
                <div class="user-meta-column likes" v-if="likeButtonShowed">
                    <div :class="['like', { active: liked }]" @click="like">
                        <FontAwesomeIcon icon="fa-heart" />
                    </div>
                </div>
            </div>
        </div>
        <div class="idea-info">
            <div class="idea-headline">{{ idea.name }}</div>
            <div class="idea-description" v-if="idea.description">
                {{ idea.description }}
            </div>
            <div class="tags">
                <div class="tag">Зашлепок</div>
                <div class="tag">Зашлепок</div>
                <div class="tag">Зашлепок</div>
            </div>
        </div>
    </div>
</template>
<script setup>
import { library } from '@fortawesome/fontawesome-svg-core';
import { faHeart, faUser } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { computed } from '@vue/reactivity';
import { ref } from 'vue';
import { HTTP } from '../../http-common.vue';
library.add(faUser, faHeart);
const props = defineProps(['idea'])
const idea = props.idea;
const idea_user = props.idea.user;
const showedName = computed(() => [idea_user.first_name, idea_user.last_name].filter(Boolean).join(' ') || idea_user.username)

const likeButtonShowed = computed(() => idea.liked !== undefined)
const liked = ref(idea.liked);
const like = async () => {
    const { data } = await HTTP.post('ideas/like', null, { params: { idea_id: idea.id } });
    liked.value = data;
}
</script>
<style lang="scss">
@use '@/assets/styles/helpers';

.idea {
    padding: 20px 10px;
    border-top: 1px solid var(--color-gray-roboflow-300);
    width: 100%;
    gap: 15px;
    display: flex;
    flex-direction: column;

    &:hover {
        background-color: var(--color-gray-roboflow-50);
        cursor: pointer;
    }

    .user-info {
        display: grid;
        grid-template-columns: 45px 1fr;
        gap: 20px;

        .user-meta {
            display: flex;
            color: var(--color-gray-roboflow-500);
            align-items: center;

            .user-meta-column {
                display: flex;
                flex-direction: column;

                &.likes {
                    flex-grow: 1;
                    display: flex;
                    justify-content: right;
                    flex-direction: row;

                    .like {
                        display: flex;
                        padding: 15px;
                        border-radius: 50%;

                        &.active {
                            svg {
                                color: var(--g-colorRed100);
                            }
                        }

                        &:hover {
                            background-color: var(--color-gray-roboflow-200);
                        }

                        svg {
                            width: 20px;
                            height: 20px;
                        }
                    }
                }

                .user-meta-row {
                    display: flex;
                    align-items: center;
                    gap: 10px;

                    &>* {
                        display: flex;
                        gap: 10px;
                        font-size: 0.8em;
                    }

                    &.dot-splitter {
                        gap: 10px;

                        &>* {
                            display: flex;
                            gap: 10px;
                            align-items: center;
                            justify-content: center;
                        }

                        &>*:not(:last-child)::after {
                            content: '';
                            display: inline-block;
                            width: 4px;
                            height: 4px;
                            background-color: var(--color-gray-roboflow-600);
                            border-radius: 50%;
                            margin-top: 3px;
                        }
                    }

                    .name {
                        font-weight: 600;
                        color: var(--color-gray-roboflow-700);
                        font-size: 1em;
                    }
                }
            }
        }

        .user-picture {
            aspect-ratio: 1;
            overflow: hidden;
            border-radius: 50%;

            &.empty {
                @include helpers.flex-center;
                background-color: var(--color-gray-roboflow-200);
            }

            img {

                object-fit: cover;
                width: 100%;
                height: 100%;
            }
        }

    }

    .idea-info {

        grid-column: 1 /-1;
        display: flex;
        flex-direction: column;
        gap: 10px;

        .idea-headline {
            font-size: 25px;
        }

        .idea-description {

            color: var(--color-gray-roboflow-500);
            font-size: 0.9em;
        }
    }

    .tags {
        margin-top: 20px;
        display: flex;
        gap: 5px;

        .tag {
            color: var(--color-gray-roboflow-500);
            background-color: var(--color-gray-roboflow-200);
            padding: 10px 20px;
            border-radius: 30px;
            font-size: 0.9em;
            cursor: pointer;

            &:hover {
                background-color: var(--color-gray-roboflow-300);
            }
        }
    }
}
</style>