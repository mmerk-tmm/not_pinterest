<template>
    <header :class="{ onShadow: !searchFocused }">
        <router-link class="link" to="/">Главная</router-link>
        <div class="link dropdown" @click.self="createToggle = !createToggle" v-on-click-outside="closeDropdown">
            Создать
            <FontAwesomeIcon icon="chevron-down" />
            <div :class="['list', { active: createToggle }]">
                <router-link class="item" to="/new-idea">Создать идею</router-link>
                <router-link class="item" to="/new-art">Создать арт</router-link>
            </div>
        </div>
        <div class="search">
            <div class="icon" v-if="!searchFocused">
                <FontAwesomeIcon icon="magnifying-glass" />
            </div>
            <input placeholder="Поиск" type="text" @focus="searchFocused = true" @blur="searchFocused = false">
            <div class="results-list" v-if="searchFocused">
                adsasdasd
            </div>
        </div>
        <div class="button">
            <FontAwesomeIcon icon="bell" />
        </div>
        <router-link to="/settings" class="button">
            <FontAwesomeIcon icon="user" />
        </router-link>
        <div :class="['button', 'menu', { mouseDown: menuButtonPushed }], { active: optionsOpen }"
            @click="optionsOpen = !optionsOpen" @mousedown="menuButtonPushed = true"
            @mouseup="menuButtonPushed = false">
            <FontAwesomeIcon icon="chevron-down" />
        </div>
        <div class="options" v-if="optionsOpen">
            <div class="items">
                <div class="item">Настройки</div>
                <div class="item">Настройки</div>
                <div class="item">Настройки</div>
                <div class="item">Настройки</div>
                <div class="item">Настройки</div>
                <div class="item">Настройки</div>
            </div>
        </div>
    </header>
</template>
<script>
import { library } from '@fortawesome/fontawesome-svg-core';
import { faChevronDown, faMagnifyingGlass, faBell, faUser } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
library.add(faChevronDown, faMagnifyingGlass, faBell, faUser);
import { vOnClickOutside } from "@vueuse/components";

export default {
    components: { FontAwesomeIcon },
    data() {
        return {
            createToggle: false,
            searchFocused: false,
            menuButtonPushed: false,
            optionsOpen: false,
        }
    },
    methods: {
        closeDropdown() {
            if (this.createToggle) {
                this.createToggle = false;
            }
        }
    },
    watch: {
        searchFocused(value) {
            console.log(value)
            this.$emit('searchOpened', value)
        }
    },
    directives: {
        OnClickOutside: vOnClickOutside,
    },
}
</script>
<style lang="scss">
@use '@/assets/styles/helpers';

header {
    height: 80px;
    display: flex;
    align-items: center;
    padding: 4px 16px;
    z-index: 99;
    position: relative;

    // &.onShadow {
    //     box-shadow: var(--shadow);
    // }

    .link {
        height: 48px;
        min-width: 60px;
        border-radius: 24px;
        @include helpers.flex-center;
        color: var(--color-text);
        padding-inline: 15px;
        text-decoration: none;
        font-weight: 600;
        gap: 5px;

        svg {
            width: 15px;
            height: 15px;
        }

        &.dropdown {
            user-select: none;
            position: relative;

            .list {
                background-color: var(--baby-powder);
                top: 120%;
                display: none;
                padding: 8px;
                position: absolute;
                width: min-content;
                box-shadow: var(--elevation-floating);
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
                    color: var(--color-text);

                    &:hover {
                        background-color: var(--color-gray-roboflow-200);
                    }
                }
            }
        }

        &.router-link-active,
        &:has(.router-link-active) {
            color: var(--color-text-rev);
            background-color: var(--color-black-cosmicore-900);
        }
    }

    .search {
        background-color: var(--color-gray-roboflow-200);
        height: 48px;
        border-radius: 24px;
        padding: 0px 8px 0px 16px;
        flex-grow: 1;
        display: flex;
        gap: 10px;
        position: relative;
        margin-inline: 10px;

        .icon {
            @include helpers.flex-center;

            svg {
                color: var(--color-text-icon-subtle)
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
            background-color: var(--baby-powder);
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
        @include helpers.flex-center;
        border-radius: 50%;
        background-color: transparent;
        transition: background-color .2s;
        color: var(--color-gray-roboflow-500);

        svg {
            height: 24px;
            width: 24px;
        }

        &:hover {
            background-color: var(--color-gray-roboflow-200);
        }

        &.menu {
            &.mouseDown {
                scale: 0.9;
            }

            transition: 0.1s scale;
            height: 24px;
            width: 24px;

            cursor: pointer;

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
        box-shadow: var(--elevation-floating);
        min-height: 40px;
        min-width: 180px;
        padding: 8px;
        background-color: var(--baby-powder);
        border-radius: 16px;

        .items {
            width: 100%;
            display: flex;
            flex-direction: column;

            .item {
                border-radius: 8px;
                padding: 8px;
                font-family: var(--font-family-default-latin);
                font-weight: 600;

                &:hover {
                    background-color: var(--color-gray-roboflow-200);
                }
            }
        }
    }
}
</style>