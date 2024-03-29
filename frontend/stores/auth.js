import { defineStore } from "pinia";
import { Service } from "@/client";

export const useAuthStore = defineStore({
    id: "auth",
    state: () => ({
        logined: false,
        userData: null,
    }),
    getters: {
        fullName() {
            let name = [this.userData.first_name, this.userData.last_name].join(
                " "
            );
            if (name.trim() === "") {
                name = this.userData.username;
            }
            return name;
        },
        isAdmin() {
            return this.userData?.is_superuser === true;
        },
    },
    actions: {
        setUserData(data) {
            if (data) {
                this.userData = data;
            }
        },
        logout() {
            this.logined = false;
            this.userData = null;
        },
        async refresh() {
            try {
                await Service.refreshApiV1AuthRefreshPost();
            } catch (error) {
                this.logout();
            }
        },
        async getUserData() {
            try {
                const userData = await Service.getUserInfoApiV1UsersMeGet();
                this.userData = userData;
                this.logined = true;
                return userData;
            } catch (error) {
                this.logout();
            }
        },
        async logoutRequest() {
            try {
                await Service.logoutApiV1AuthLogoutDelete();
            } catch (error) {}

            this.logout();
        },
        async loginRequest(username, password) {
            this.logined = false;
            try {
                const userData = await Service.loginApiV1AuthLoginPost({
                    username: username,
                    password: password,
                });
                this.userData = userData;
                this.logined = true;
            } catch (error) {
                this.logout();
                return error;
            }
        },
        async registerRequest(username, password, first_name, last_name) {
            this.logined = false;
            try {
                const userData =
                    await Service.createUserSignupApiV1AuthSignupPost({
                        username: username,
                        password: password,
                        first_name,
                        last_name,
                    });
                this.userData = userData;
                this.logined = true;
            } catch (error) {
                this.logout();
                return error;
            }
        },
        init() {
            this.refresh();
            setInterval(() => {
                if (this.logined) {
                    this.refresh();
                }
            }, 1000 * 60 * 5);
        },
    },
});
