<template>
    <header>
        <router-link class="link" to="/">Главная</router-link>
        <div class="link dropdown" @click.self="createToggle = !createToggle" v-on-click-outside="closeDropdown">
            Создать
            <FontAwesomeIcon icon="chevron-down" />
            <div :class="['list', { active: createToggle }]">
                <router-link class="item" to="">Создать идею</router-link>
                <router-link class="item" to="">Создать арт</router-link>
            </div>
        </div>
        <div class="search">
            <div class="icon" v-if="!searchFocused">
                <FontAwesomeIcon icon="magnifying-glass" />
            </div>
            <input placeholder="Поиск" type="text" @focus="searchFocused = true" @blur="searchFocused = false">
        </div>
        <div class="button">
            <FontAwesomeIcon icon="bell" />
        </div>
    </header>
</template>
<script>
import { library } from '@fortawesome/fontawesome-svg-core';
import { faChevronDown, faMagnifyingGlass, faBell } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
library.add(faChevronDown, faMagnifyingGlass, faBell);
import { vOnClickOutside } from "@vueuse/components";

export default {
    components: { FontAwesomeIcon },
    data() {
        return {
            createToggle: false,
            searchFocused: false,
        }
    },
    methods: {
        closeDropdown() {
            console.log('asdas')
            if (this.createToggle) {
                this.createToggle = false;
            }
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
    box-shadow: var(--shadow);
    padding: 4px 16px;
    gap: 5px;

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

        &.router-link-active {
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
    }

    .button {
        height: 48px;
        width: 48px;
        @include helpers.flex-center;
        border-radius: 50%;
        background-color: transparent;
        transition: background-color .2s;

        svg {
            height: 24px;
            width: 24px;
        }

        &:hover {
            background-color: var(--color-gray-roboflow-200);
        }
    }
}
</style>