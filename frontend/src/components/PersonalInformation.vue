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
            <template v-if="gender === 'unspecified'">
                <FormField :border-radius="10" placeholder="Введите свой гендер" off-margin
                    v-model="unspecifiedGender" />
                <div :class="['send-unspecified-gender', { active: unspecifiedButtonActive }]" @click="">dadas</div>
            </template>

        </div>

    </div>
</template>
<script>
import { HTTP } from '../http-common.vue';
import FormField from './FormField.vue';
import { useToast } from "vue-toastification";
import handleError from '../composables/errors';
export default {
    setup() {
        const toast = useToast();
        return { toast }
    },
    data() {
        return {
            gender: '',
            unspecifiedGender: '',
            gettedGender: false,
        }
    },
    mounted() {
        this.getGender();
    },
    computed: {
        unspecifiedButtonActive() {
            return this.unspecifiedGender.length > 0
        }
    },
    components: { FormField },
    watch: {
        gender(value) {
            console.log(this.gettedGender)
            if (!this.gettedGender) return
            if (value !== 'unspecified') {
                this.send();
            }
        },
        handleUnspecifiedButton() {
            if (!this.unspecifiedButtonActive) return
            this.send();
        }
    },
    methods: {
        send() {
            HTTP.put('personal-information', { gender: this.gender === 'unspecified' ? this.unspecifiedGender : this.gender })
                .then(response => {

                })
                .catch((error) => {
                    this.toast.error(handleError(error, 'При персональных данных произошла ошибка').message)
                });
        },
        getGender() {
            HTTP.get('personal-information', { validateStatus: false })
                .then(response => {
                    this.gender = response?.data?.gender;
                    this.gettedGender = true;
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