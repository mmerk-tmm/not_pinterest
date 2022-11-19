<template>
    <Teleport to="#modal">
        <Transition name="modal">
            <div class="modal-bg" v-if="active" @click.self="closeModal">
                <div class="modal">
                    <div class="messages">
                        <div :class="['message', { error: message.error }]" v-for="message in messages">
                            {{ message.text }}
                        </div>
                    </div>
                    <div class="headline">
                        <div class="text">{{ headline }}</div>
                        <div class="close-button" @click="closeModal">
                            <FontAwesomeIcon icon="fa-x" />
                        </div>
                    </div>
                    <div class="modal-content" v-if="text">
                        {{ text }}
                    </div>
                    <slot></slot>
                    <div class="modal-buttons">
                        <div :class="['button', { loading: yesLoading }]" v-if="yesButton" @click="$emit('yes')">
                            <span v-if="!yesLoading">Да</span>
                            <FontAwesomeIcon icon="fa-spinner" v-else />
                        </div>
                        <div class="button" v-if="noButton" @click="$emit('no')">Нет</div>
                        <div :class="['button', 'custom', { active: buttonActive }]" v-if="buttonText"
                            @[buttonActive&&`click`]="$emit('buttonClick')">{{ buttonText }}</div>
                    </div>
                </div>
            </div>
        </Transition>
    </Teleport>
</template>
<script>
import { library } from '@fortawesome/fontawesome-svg-core';
import { faX, faSpinner } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
library.add(faX, faSpinner);

export default {
    props: {
        active: Boolean,
        headline: String,
        text: String,
        yesButton: Boolean,
        yesLoading: Boolean,
        noButton: Boolean,
        buttonText: String,
        buttonActive: Boolean,
        messages: Array,
    },
    emits: ['close', 'yes', 'no', 'buttonClick'],
    methods: {
        closeModal() {
            this.$emit('close');
        }
    },
    components: { FontAwesomeIcon }
}
</script>
<style lang="scss">
@use '@/assets/styles/helpers';
@use '@/assets/styles/components';

.modal-enter-active,
.modal-leave-active {
    transition: all 0.25s ease;
}

.modal-enter-from,
.modal-leave-to {
    opacity: 0;
}


.modal-bg {
    position: absolute;
    inset: 0;
    background-color: rgba($color: #000000, $alpha: 0.5);
    @include helpers.flex-center;
    z-index: 99;

    .modal {
        background-color: var(--baby-powder);
        min-width: 400px;
        padding: 10px;
        border-radius: 20px;
        display: flex;
        flex-direction: column;
        gap: 10px;
        position: relative;

        .messages {
            position: absolute;
            bottom: calc(100% + 10px);
            width: 100%;
            left: 0;
            display: flex;
            flex-direction: column;
            gap: 5px;

            .message {
                border-radius: 10px;
                background-color: var(--baby-powder);
                padding: 10px;
                position: relative;
                isolation: isolate;
                overflow: hidden;
                text-align: center;

                &.error {
                    &::after {
                        content: '';
                        background-color: rgba($color: red, $alpha: 0.2);
                        position: absolute;
                        inset: 0;
                        z-index: -1;
                    }
                }
            }
        }

        .headline {
            display: flex;
            margin-bottom: 10px;
            @include helpers.flex-center;

            .text {
                flex-grow: 1;
                text-align: center;
                font-size: 18px;
            }

            .close-button {
                @include components.button;
                color: var(--color-text);
                border-radius: 15px;
                padding: 8px;
                background-color: var(--color-gray-roboflow-300);

                &:hover {
                    background-color: var(--color-gray-roboflow-400);
                }

                svg {
                    width: 15px;
                    height: 15px;
                }
            }
        }

        .modal-content {
            padding: 10px;
        }

        .modal-buttons {
            display: flex;
            gap: 5px;

            .button {
                @include components.button;
                background-color: var(--color-text);
                color: var(--color-text-rev);
                flex-grow: 1;
                text-align: center;
                padding: 5px;
                border-radius: 10px;

                &.custom {
                    padding: 10px;
                    color: var(--color-text);
                    background-color: var(--g-colorGray150);

                    &.active {
                        color: var(--color-text-rev);
                        background-color: var(--color-text);
                    }
                }
            }
        }
    }
}
</style>