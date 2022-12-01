<template>
    <div class="settings-selection">
        <h1>Персональные данные</h1>
        <div class="detail">
            Отредактируйте основные личные сведения, чтобы улучшить рекомендации. Эта информация является
            конфиденциальной и не будет отображаться в вашем общедоступном профиле.
        </div>
        <div class="formkit-outer personal-information">
            <div class="formkit-wrapper">
                <label class="formkit-label">Пол</label>
                <div class="select-gender">
                    <label class="item-wrapper" for="male">
                        <div class="item">
                            <input id="male" name="gender" type="radio" value="male" v-model="gender">
                        </div>
                        <div class="text">Мужской</div>
                    </label>
                    <label class="item-wrapper" for="female">
                        <div class="item">
                            <input id="female" name="gender" type="radio" value="female" v-model="gender">
                        </div>
                        <div class="text">Женский</div>
                    </label>
                    <label class="item-wrapper" for="unspecified">
                        <div class="item">
                            <input id="unspecified" name="gender" type="radio" value="unspecified" v-model="gender">
                        </div>
                        <div class="text">Другой</div>
                    </label>
                </div>
            </div>
            <FormField :border-radius="10" placeholder="Введите свой гендер" off-margin v-model="unspecifiedGender"
                v-if="gender === 'unspecified'" />
            <div :class="['send-unspecified-gender', { active: ButtonActive }]" @click="send">Отправить</div>
        </div>
    </div>
</template>
<script>
import { HTTP } from '../../http-common.vue';
import FormField from '../FormField.vue';
import { useToast } from "vue-toastification";
import { handleAxiosError } from '../../composables/errors';
export default {
    setup() {
        const toast = useToast();
        return { toast }
    },
    data() {
        return {
            gender: null,
            unspecifiedGender: '',
            watchChange: false,
            originalGender: null,
        }
    },
    mounted() {
        this.getGender();
    },
    computed: {
        ButtonActive() {
            return this.gender !== 'unspecified' ? this.originalGender !== this.gender : this.unspecifiedGender?.length > 0 && this.originalGender !== this.unspecifiedGender
        }
    },
    components: { FormField },
    watch: {
        handleUnspecifiedButton() {
            if (!this.unspecifiedButtonActive) return
            this.send();
        },
        gender(value) {
            this.unspecifiedGender = this.originalGender;
        }
    },
    methods: {
        send() {
            HTTP.put('personal-information', { gender: this.gender === 'unspecified' ? this.unspecifiedGender : this.gender })
                .then(response => {
                    this.originalGender = response.data.gender;
                })
                .catch((error) => {
                    this.toast.error(handleAxiosError(error, 'При персональных данных произошла ошибка').message)
                });
        },
        getGender() {
            HTTP.get('personal-information', { validateStatus: false })
                .then(response => {
                    const gender = response?.data?.gender;
                    this.originalGender = gender;
                    if (['male', 'female'].includes(gender)) {
                        this.gender = gender;
                    } else {
                        this.gender = 'unspecified';
                        this.unspecifiedGender = gender;
                    }
                })
                .catch((error) => {
                    this.toast.error(handleError(error, 'При персональных данных произошла ошибка').message)
                });
        }
    }
}
</script>
<style lang="scss">
@use '@/assets/styles/helpers';
@use '@/assets/styles/components';

.personal-information {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-bottom: 0px;

    .send-unspecified-gender {
        @include components.button;
    }

    .select-gender {
        display: flex;
        gap: 10px;

        .item-wrapper {
            @include helpers.flex-center;
            gap: 5px;

            .item {
                border: 2px solid var(--color-gray-roboflow-400);
                border-radius: 50%;
                height: 24px;
                width: 24px;

                input {
                    opacity: 0;
                }

                &:has(input:checked) {
                    border: 8px solid black;
                }
            }
        }
    }
}
</style>