<template>
    <div class="settings-container">
        <aside>
            <router-link to="" class="selection">Общедоступный профиль</router-link>
            <router-link to="" class="selection">Персональные данные</router-link>
            <router-link to="" class="selection">Управление аккаунтом</router-link>
            <router-link to="" class="selection">Настроить ленту</router-link>
        </aside>
    </div>
</template>
<style lang="scss">
.settings-container {
    display: grid;
    grid-template-columns: 200px 1fr;
    padding-left: 20px;
    padding-right: 20px;

    aside {
        display: flex;
        flex-direction: column;

        .selection {
            text-decoration: none;
            color: var(--color-text);
            text-align: left;
            word-wrap: break-word;
            font-weight: 600;
            position: relative;

            &::after {
                position: absolute;
                left: 0;
                content: '';
                background-color: var(--color-text);
                width: 100%;
                bottom: -9px;
                height: 3px;
            }
        }
    }
}
</style>