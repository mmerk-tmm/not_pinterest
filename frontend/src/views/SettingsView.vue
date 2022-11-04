<template>
    <div class="settings-container">
        <aside>
            <router-link to="/settings/edit-profile" class="selection">Общедоступный профиль</router-link>
            <router-link to="/settings/personal-information" class="selection">Персональные данные</router-link>
            <router-link to="/settings/account-settings" class="selection">Управление аккаунтом</router-link>
            <router-link to="/edit/history" class="selection">Настроить ленту</router-link>
        </aside>
        <div class="content">
            <router-view></router-view>
        </div>
    </div>
</template>
<script>
export default {
    mounted() {
        if (this.$route.fullPath === "/settings") {
            this.$router.push("/settings/edit-profile")
        }
    }
}
</script>
<style lang="scss">
.settings-container {
    margin-top: 40px;
    display: grid;
    grid-template-columns: 200px 1fr;
    padding-left: 20px;
    padding-right: 20px;

    aside {
        display: flex;
        flex-direction: column;
        gap: 8px;

        .selection {
            border-radius: 8px;
            padding: 8px;
            text-decoration: none;
            color: var(--color-text);
            text-align: left;
            word-wrap: break-word;
            font-weight: 600;
            position: relative;

            &:hover {
                background-color: rgba($color: #000000, $alpha: 0.06);
            }

            &.router-link-active {
                &::after {
                    position: absolute;
                    left: 8px;
                    content: '';
                    background-color: var(--color-text);
                    width: calc(100% - 16px);
                    bottom: 0px;
                    height: 3px;
                    border-radius: 5px;
                }
            }


        }
    }

    .content {
        display: flex;
        flex-direction: column;
        align-items: center;

        .settings-selection {
            width: min(100vh, 488px);
            display: flex;
            gap: 8px;
            flex-direction: column;
            background-color: var(--color-gray-roboflow-200);
            padding: 10px;
            border-radius: 20px;

            h1 {
                font-weight: 600;
                text-align: center;
                font-size: x-large;
            }
            .detail {
                margin-top: 8px;
            }
        }
    }
}
</style>