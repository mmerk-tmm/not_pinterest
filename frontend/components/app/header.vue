<template>
    <header>
        <template v-if="logined">
            <nuxt-link class="link" to="/">Главная</nuxt-link>
            <div
                class="link dropdown"
                @click.self="createToggle = !createToggle"
            >
                Создать
                <Icon name="mdi:chevron-down" />
                <div :class="['list', { active: createToggle }]">
                    <nuxt-link class="item" to="/ideas/new">
                        Создать идею
                    </nuxt-link>
                    <nuxt-link class="item" to="/arts/new">
                        Создать арт
                    </nuxt-link>
                </div>
            </div>
            <nuxt-link class="link" to="/ideas">Идеи</nuxt-link>
            <div class="search">
                <div class="icon" v-if="!searchFocused">
                    <Icon name="mdi:magnify" />
                </div>
                <input
                    placeholder="Поиск"
                    type="text"
                    @focus="searchFocused = true"
                    @blur="searchFocused = false"
                />
                <div class="results-list" v-if="searchFocused">adsasdasd</div>
            </div>
            <div class="button">
                <Icon name="mdi:bell" />
            </div>
            <router-link to="/settings" class="button">
                <Icon name="mdi:account" />
            </router-link>
            <div
                :class="
                    (['button', 'menu', { mouseDown: menuButtonPushed }],
                    { active: optionsOpen })
                "
                @click="optionsOpen = !optionsOpen"
                @mousedown="menuButtonPushed = true"
                @mouseup="menuButtonPushed = false"
            >
                <Icon name="mdi:chevron-down" />
            </div>
            <div class="options" v-if="optionsOpen">
                <div class="items">
                    <div class="item" @click="logout">Выйти</div>
                </div>
            </div>
        </template>
        <div class="not-logined" v-else>
            <nuxt-link to="/login" class="link active red">Войти</nuxt-link>
            <nuxt-link to="/sign-in" class="link hovered">
                Регистрация
            </nuxt-link>
        </div>
    </header>
</template>
<script setup>
import { useAuthStore } from "@/stores/auth";
import { useToast } from "vue-toastification";
import { storeToRefs } from "pinia";
const authStore = useAuthStore();
const { logined } = storeToRefs(authStore);
const toast = useToast();

const logout = () => {
    authStore.logout();
    toast.success("Вы вышли из аккаунта");
};

const optionsOpen = ref(false);
const menuButtonPushed = ref(false);
const searchFocused = ref(false);
const createToggle = ref(false);
</script>
<style lang="scss">
header {
    height: 100%;
    display: flex;
    align-items: center;
    padding: 4px 16px;
    width: 100%;
    background: $color-background;
    transition: box-shadow 0.2s;
    z-index: 10;
    @include md(true) {
        padding: 0px;
    }
    .not-logined {
        display: flex;
        gap: 5px;
        margin-left: auto;

        .hovered {
            background-color: $g-colorGray100;

            &:hover {
                background-color: $g-colorGray100Hovered;
            }
        }
    }

    .link {
        height: 48px;
        min-width: 60px;
        border-radius: 24px;
        @include flex-center;
        color: $color-text;
        padding-inline: 15px;
        text-decoration: none;
        font-weight: 600;
        gap: 5px;
        cursor: pointer;

        svg {
            width: 15px;
            height: 15px;
        }

        &.dropdown {
            user-select: none;
            position: relative;

            .list {
                background-color: $baby-powder;
                top: 120%;
                display: none;
                padding: 8px;
                position: absolute;
                width: min-content;
                box-shadow: $elevation-floating;
                border-radius: 16px;

                &.active {
                    display: flex;
                    flex-direction: column;
                }

                .item {
                    white-space: nowrap;
                    font-weight: 600;
                    padding: 8px 20px;
                    text-align: center;
                    border-radius: 8px;
                    text-decoration: none;
                    color: $color-text;

                    &:hover {
                        background-color: $color-gray-roboflow-200;
                    }
                }
            }
        }

        &.router-link-active,
        &:has(.router-link-active),
        &.active {
            color: $color-text-rev;
            background-color: $color-black-cosmicore-900;

            &.red {
                background-color: $g-colorRed100;
            }
        }
    }

    .search {
        background-color: $color-gray-roboflow-200;
        height: 48px;
        border-radius: 24px;
        padding: 0px 8px 0px 16px;
        flex-grow: 1;
        display: flex;
        gap: 10px;
        position: relative;
        margin-inline: 10px;
        @include md(true) {
            display: none;
        }
        .icon {
            @include flex-center;

            svg {
                color: $color-text-icon-subtle;
            }
        }

        input {
            all: unset;
            height: 100%;
            width: 100%;
        }

        .results-list {
            position: absolute;
            top: 100%;
            background-color: $baby-powder;
            left: 0;
            width: 100%;
            min-height: 400px;
            border-radius: 0px 0px 24px 24px;
            padding: 16px;
        }
    }

    .button {
        height: 48px;
        width: 48px;
        @include flex-center;
        border-radius: 50%;
        background-color: transparent;
        transition: background-color 0.2s;
        color: $color-gray-roboflow-500;
        cursor: pointer;

        svg {
            height: 24px;
            width: 24px;
        }

        &:hover {
            background-color: $color-gray-roboflow-200;
        }

        &.menu {
            &.mouseDown {
                scale: 0.9;
            }

            transition: 0.1s scale;
            height: 24px;
            width: 24px;

            svg {
                height: 14px;
                width: 14px;
            }
        }
    }

    .options {
        display: flex;
        position: absolute;
        right: 0;
        margin: 8px;
        top: 60px;
        max-width: 360px;
        width: 100%;
        box-shadow: $elevation-floating;
        min-height: 40px;
        min-width: 180px;
        padding: 8px;
        background-color: $baby-powder;
        border-radius: 16px;

        .items {
            width: 100%;
            display: flex;
            flex-direction: column;

            .item {
                border-radius: 8px;
                padding: 8px;
                font-weight: 600;
                cursor: pointer;

                &:hover {
                    background-color: $color-gray-roboflow-200;
                }
            }
        }
    }
}
</style>
