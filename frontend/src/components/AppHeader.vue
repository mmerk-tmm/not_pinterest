<template>
    <header :class="{ onShadow: enableShahow }">
        <template v-if="logined">
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
            <div class="options" v-if="optionsOpen" v-on-click-outside="closeMenu">
                <div class="items">
                    <div class="item" @click="logout">Выйти</div>
                </div>
            </div>
        </template>
        <div class="not-logined" v-else>
            <div class="link active red" @click="openLoginDialog">Войти</div>
            <div class="link hovered" @click="openRegisterDialog">Регистрация</div>
            <ModalDialog :active="dialogActive"
                :headline="this.loginDialogActive ? 'Войти в аккаунт' : 'Зарегистрировать аккаунт'"
                :buttonText="this.loginDialogActive ? 'Войти' : 'Зарегистрироваться'" @close="closeDialog"
                :buttonActive="!fieldsWrong" :messages="dialogMessages" @buttonClick="buttonHandler">
                <template v-if="registerDialogActive">
                    <FormField :border-radius="borderRadius" off-margin v-model="firstName" label="Имя"
                        placeholder="Имя" />
                    <FormField :border-radius="borderRadius" off-margin v-model="lastName" label="Фамилия"
                        placeholder="Фамилия" />
                </template>
                <FormField :border-radius="borderRadius" off-margin v-model="login" label="Логин" placeholder="Логин"
                    not-empty />
                <FormField :border-radius="borderRadius" off-margin v-model="password" label="Пароль"
                    placeholder="Пароль" not-empty is-password />
            </ModalDialog>
        </div>
    </header>
</template>
<script>
import { library } from '@fortawesome/fontawesome-svg-core';
import { faChevronDown, faMagnifyingGlass, faBell, faUser } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
library.add(faChevronDown, faMagnifyingGlass, faBell, faUser);
import { vOnClickOutside } from "@vueuse/components";
import { useAuthStore } from '../stores/auth';
import handleError from '../composables/errors';
import { useToast } from "vue-toastification";
import { storeToRefs } from 'pinia';
import ModalDialog from '../components/ModalDialog.vue';
import FormField from './FormField.vue';
export default {
    components: { FontAwesomeIcon, ModalDialog, FormField },
    setup() {
        const { VITE_MIN_PASSWORD_LENGTH, VITE_MAX_LOGIN_LENGTH, VITE_MIN_LOGIN_LENGTH, VITE_MAX_FIRSTNAME_LENGTH, VITE_MAX_LASTNAME_LENGTH } = import.meta.env;
        const { logined, message } = storeToRefs(useAuthStore());
        const { loginRequest, registerRequest, clearMessage, logoutRequest } = useAuthStore();
        const toast = useToast();
        return {
            logined,
            toast,
            VITE_MIN_PASSWORD_LENGTH,
            VITE_MAX_LOGIN_LENGTH,
            VITE_MIN_LOGIN_LENGTH,
            VITE_MAX_FIRSTNAME_LENGTH,
            VITE_MAX_LASTNAME_LENGTH,
            loginRequest,
            registerRequest,
            clearMessage,
            message,
            logoutRequest
        }
    },
    data() {
        return {
            createToggle: false,
            searchFocused: false,
            menuButtonPushed: false,
            optionsOpen: false,
            loginDialogActive: false,
            registerDialogActive: false,
            login: '',
            password: '',
            firstName: '',
            lastName: '',
            borderRadius: 10,
        }
    },
    watch: {
        logined() {
            this.closeDialog();
        },
        searchFocused(value) {
            this.$emit('searchOpened', value)
        },
    },
    inject: ['scrollY'],
    methods: {
        closeDropdown() {
            if (this.createToggle) {
                this.createToggle = false;
            }
        },
        logout() {
            this.logoutRequest();
            this.closeMenu();
        },
        closeMenu() {
            this.optionsOpen = false;
        },
        closeDialog() {
            this.loginDialogActive = false;
            this.registerDialogActive = false;
            this.login = '';
            this.password = '';
            this.firstName = '';
            this.lastName = '';
            this.clearMessage();
        },
        openLoginDialog() {
            this.loginDialogActive = true;
            this.registerDialogActive = false;
        },
        openRegisterDialog() {
            this.loginDialogActive = false;
            this.registerDialogActive = true;
        },
        buttonHandler() {
            if (this.fieldsWrong) return;
            if (this.loginDialogActive) {
                this.loginRequest(this.login, this.password)
            } else {
                this.registerRequest(this.login, this.password, this.firstName, this.lastName)
            }
        }
    },
    computed: {
        fieldsWrong() {
            var isWrong = this.loginWrong || this.passwordWrong;
            if (this.registerDialogActive) {
                isWrong = isWrong || this.firstNameWrong || this.lastNameWrong
            }
            return isWrong;
        },
        dialogActive() {
            return this.loginDialogActive || this.registerDialogActive
        },
        enableShahow() {
            return this.scrollY.value > 20
        },
        loginWrong() {
            return this.login.length < this.VITE_MIN_LOGIN_LENGTH || this.login.length > this.VITE_MAX_LOGIN_LENGTH
        },
        passwordWrong() {
            return this.password.length < this.VITE_MIN_PASSWORD_LENGTH;
        },
        firstNameWrong() {
            return this.firstName.length > this.VITE_MAX_FIRSTNAME_LENGTH
        },
        lastNameWrong() {
            return this.lastName.length > this.VITE_MAX_LASTNAME_LENGTH
        },
        dialogMessages() {
            if (this.message.length !== 0) {
                return [{ error: true, text: this.message }]
            }
            var messages = [];
            if (this.login) {
                if (this.login.length < this.VITE_MIN_LOGIN_LENGTH) {
                    messages.push({ error: true, text: `Минимальная длина логина ${this.VITE_MIN_LOGIN_LENGTH} символов` })
                }
                if (this.login.length > this.VITE_MAX_LOGIN_LENGTH) {
                    messages.push({ error: true, text: `Максимальная длина логина ${this.VITE_MAX_LOGIN_LENGTH} символов` })
                }
            }
            if (this.password && this.passwordWrong) {
                messages.push({ error: true, text: `Минимальная длина пароля ${this.VITE_MIN_PASSWORD_LENGTH} символов` });
            }
            if (this.registerDialogActive) {

                if (this.firstNameWrong) {
                    messages.push({ error: true, text: `Максимальная длина имени ${this.VITE_MAX_FIRSTNAME_LENGTH} символов` })
                }
                if (this.lastNameWrong) {
                    messages.push({ error: true, text: `Максимальная длина фамилии ${this.VITE_MAX_LASTNAME_LENGTH} символов` });
                }
            }
            return messages
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
    position: fixed;
    top: 0;
    width: 100%;
    background: var(--color-background);
    transition: box-shadow .2s;

    &.onShadow {
        box-shadow: var(--shadow);
    }

    .not-logined {
        display: flex;
        gap: 5px;
        margin-left: auto;

        .hovered {
            background-color: var(--g-colorGray100);

            &:hover {
                background-color: var(--g-colorGray100Hovered);
            }
        }
    }

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
        cursor: pointer;

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
        &:has(.router-link-active),
        &.active {
            color: var(--color-text-rev);
            background-color: var(--color-black-cosmicore-900);

            &.red {
                background-color: var(--g-colorRed100);
            }
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
        cursor: pointer;

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
                cursor: pointer;

                &:hover {
                    background-color: var(--color-gray-roboflow-200);
                }
            }
        }
    }
}
</style>