<template>
    <header>
        <template v-if="logined">
            <nuxt-link class="link home" to="/">
                <span v-if="$viewport.isGreaterOrEquals('md')">Главная</span>
                <Icon name="mdi:home" v-else />
            </nuxt-link>
            <div
                class="link dropdown"
                @click="createToggle = !createToggle"
                ref="createToggleref"
            >
                Создать
                <Icon name="mdi:chevron-down" />
                <div :class="['list', { active: createToggle }]">
                    <nuxt-link
                        class="item"
                        to="/ideas/new"
                        @click.prevent="createToggle = false"
                    >
                        Создать идею
                    </nuxt-link>
                    <nuxt-link
                        class="item"
                        to="/arts/new"
                        @click.prevent="createToggle = false"
                    >
                        Создать арт
                    </nuxt-link>
                </div>
            </div>
            <nuxt-link class="link" to="/ideas">Идеи</nuxt-link>
            <div
                class="button"
                @click="searchActive = true"
                v-if="$viewport.isLessThan('lg')"
            >
                <Icon name="mdi:magnify" />
            </div>
            <div
                class="search-bg"
                @click="
                    searchActive = false;
                    createToggle = false;
                "
                v-if="searchFocused || searchActive || createToggle"
            />
            <div
                :class="[
                    'search',
                    {
                        focused: search && searchFocused && searchActive,
                    },
                ]"
                v-if="$viewport.isGreaterOrEquals('lg') || searchActive"
            >
                <div
                    class="icon"
                    v-if="$viewport.isGreaterOrEquals('lg') && !searchFocused"
                >
                    <Icon name="mdi:magnify" />
                </div>

                <input
                    placeholder="Поиск"
                    type="text"
                    @focus="searchFocused = true"
                    v-model="search"
                    @blur="searchFocused = false"
                />
                <template v-if="search">
                    <client-only>
                        <div class="results-list" v-auto-animate>
                            <SearchItem
                                v-for="item in results"
                                :item="item"
                                @select="
                                    search = '';
                                    searchActive = false;
                                "
                            />
                            <div class="empty" v-if="!results.length">
                                Ничего не найдено
                            </div>
                        </div>
                    </client-only>
                </template>
            </div>
            <nuxt-link
                class="button avatar"
                :to="{ name: 'user-id', params: { id: userData.id } }"
            >
                <img
                    :src="userData.picture"
                    alt="avatar"
                    v-if="userData.picture"
                />
                <Icon name="material-symbols:person" v-else />
            </nuxt-link>
            <div class="button" @click="logout">
                <Icon name="material-symbols:logout" />
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
import { storeToRefs } from "pinia";
import { Service } from "@/client";
const authStore = useAuthStore();
const { logined, userData } = storeToRefs(authStore);
const { $toast } = useNuxtApp();

const logout = () => {
    authStore.logout();
    $toast.success("Вы вышли из аккаунта");
};

const searchFocused = ref(false);
const createToggle = ref(false);
const route = useRoute();
watch(
    () => route.name,
    () => {
        searchActive.value = false;
        createToggle.value = false;
    }
);

const search = ref("");
const results = ref([]);
const searchActive = ref(false);
watch(search, async (value) => {
    if (value.length < 1) {
        results.value = [];
        return;
    }
    results.value = await Service.searchAllApiV1SearchGet(value);
});
watch(searchActive, (value) => {
    search.value = "";
});
</script>
<style lang="scss">
.search-bg {
    content: "";
    position: fixed;
    inset: 0;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: -1;

    @include md {
        display: none;
    }
}
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

        &.home {
            svg {
                width: 24px;
                height: 24px;
            }
        }

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
        isolation: isolate;
        z-index: 1;

        @include md(true) {
            position: fixed;
            background-color: $color-gray-roboflow-100;
            width: 100%;
            left: 0;
            right: 0;
            margin-inline: 0;
            border-radius: 0px;
            top: 0;
            padding: 0px 16px;
            height: 70px;
        }
        box-shadow: $elevation-floating;
        &.focused {
            @include md {
                border-radius: 24px 24px 0px 0px;
            }
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
            min-height: 200px;
            border-radius: 0px 0px 24px 24px;
            padding: 16px;
            box-shadow: $elevation-floating;
            display: flex;
            flex-direction: column;
            gap: 10px;

            .empty {
                @include flex-center;
                height: 100%;
            }
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
