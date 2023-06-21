<template>
    <div class="ideas-wrapper">
        <div class="headline">
            <div class="text">Идеи</div>
        </div>
        <div class="ideas-container">
            <Idea :idea="idea" v-for="idea in ideas" />
        </div>
    </div>
</template>
<script setup>
import { Service } from "@/client";

const ideas = await Service.getIdeasApiV1IdeasGet(1);
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
