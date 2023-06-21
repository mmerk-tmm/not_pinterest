import { useAuthStore } from "@/stores/auth";
import { storeToRefs } from "pinia";
import { routesNames, navigateTo } from "@typed-router";
export default defineNuxtRouteMiddleware(async (context) => {
    const authStore = useAuthStore();
    const { logout, refresh, getUserData } = authStore;
    const { logined } = storeToRefs(authStore);
    if (process.server) {
        await getUserData();

        if (!logined.value) {
            logout();
            return navigateTo({ name: routesNames.login });
        }
    } else if (process.client) {
        await refresh();
        if (!logined.value) {
            return navigateTo({ name: routesNames.login });
        }
    }
});
