<template>
    <div class="ideas-wrapper">
        <div class="headline">
            <div class="text">
                Идеи
            </div>
            <div class="dropdown">
                <div class="selected">
                    <div class="selected-text">
                        Избранные
                    </div>
                    <FontAwesomeIcon icon="fa-chevron-down" />
                </div>
            </div>
        </div>
        <div class="ideas-container">
            <Idea :idea="idea" v-for="idea in ideas" />
        </div>
    </div>
</template>
<script setup>
import { HTTP } from '../http-common.vue';
import Idea from '../components/Ideas/Idea.vue'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { library } from '@fortawesome/fontawesome-svg-core';
import { faChevronDown } from '@fortawesome/free-solid-svg-icons';
library.add(faChevronDown);
const { data: ideas } = await HTTP.get('ideas');
</script>
<style lang="scss">
.ideas-wrapper {
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    width: 100%;
    padding-top: 5rem;

    .headline {
        display: flex;
        justify-content: space-between;

        .text {
            font-size: 30px;
            margin-bottom: 30px;
        }

        .dropdown {
            border-radius: 30px;
            border: 1px solid var(--color-gray-roboflow-500);
            color: var(--color-gray-roboflow-900);
            display: flex;
            height: min-content;


            .selected {
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 5px;
                padding: 10px;
                cursor: pointer;

                svg {
                    height: 14px;
                    width: 14px;
                    color: var(--color-gray-roboflow-900);
                }
            }
        }
    }
}
</style>