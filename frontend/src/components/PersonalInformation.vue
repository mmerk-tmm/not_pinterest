<template>
    <div class="settings-selection">
        <h1>Персональные данные</h1>
        <div class="detail">
            Отредактируйте основные личные сведения, чтобы улучшить рекомендации. Эта информация является
            конфиденциальной и не будет отображаться в вашем общедоступном профиле.
        </div>
        <div class="formkit-outer" data-family="text" data-type="text">
            <div class="formkit-wrapper">
                <label class="formkit-label">Пол</label>
                <div class="select-gender">
                    <label class="item-wrapper" for="male">
                        <div class="item">
                            <input class="M8E MIw e43 xpn ac9 BG7" id="male" name="gender" type="radio" value="male">
                        </div>
                        <div class="text">Мужской</div>
                    </label>
                    <label class="item-wrapper" for="female">
                        <div class="item">
                            <input class="M8E MIw e43 xpn ac9 BG7" id="female" name="gender" type="radio"
                                value="female">
                        </div>
                        <div class="text">Женский</div>
                    </label>
                    <label class="item-wrapper" for="unspecified">
                        <div class="item">
                            <input class="M8E MIw e43 xpn ac9 BG7" id="unspecified" name="gender" type="radio"
                                value="unspecified">
                        </div>
                        <div class="text">Другой</div>
                    </label>

                </div>
            </div>
        </div>

    </div>
</template>
<style lang="scss">
@use '@/assets/styles/helpers';

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
</style>