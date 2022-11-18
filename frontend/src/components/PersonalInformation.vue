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
            <FormField :border-radius="10" placeholder="Введите свой гендер" v-if="gender === 'unspecified'"
                off-margin />
        </div>

    </div>
</template>
<script>
import FormField from './FormField.vue';

export default {
    data() {
        return {
            gender: '',
        }
    },
    components: { FormField }
}
</script>
<style lang="scss">
@use '@/assets/styles/helpers';

.personal-information {
    display: flex;
    flex-direction: column;
    gap: 10px;

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