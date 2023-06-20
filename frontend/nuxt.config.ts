// https://nuxt.com/docs/api/configuration/nuxt-config

export default defineNuxtConfig({
    modules: [
        "nuxt-icon",
        "@element-plus/nuxt",
        "@nuxtjs/tailwindcss",
        "@nuxtjs/google-fonts",
        "@pinia/nuxt",
        "@vueuse/nuxt",
        "nuxt-typed-router",
        "nuxt-viewport",
    ],
    ssr: true,
    viewport: {
        breakpoints: {
            xs: 360,
            sm: 576,
            md: 768,
            lg: 992,
            xl: 1200,
        },
    },
    nuxtTypedRouter: {
        strict: true,
    },
    googleFonts: {
        families: {
            "Open+Sans": true,
        },
        download: true,
    },
    plugins: [
        { src: "~/plugins/autoAnimatePlugin.js", mode: `client` },
        { src: "~/plugins/refreshToken.js", mode: `client` },
        { src: "~/plugins/vue-toastification.js", mode: `client` },
        { src: "~/plugins/api.js" },
    ],
    nitro: {
        devProxy: {
            "/api": {
                target: "http://localhost:8000/api",
                changeOrigin: true,
                prependPath: true,
                cookieDomainRewrite: false,
            },
            "/api/docs": {
                target: "http://localhost:8000/docs",
                changeOrigin: true,
                prependPath: true,
            },
        },
    },
    css: ["@/assets/styles/global.scss"],
    vite: {
        css: {
            preprocessorOptions: {
                scss: {
                    additionalData: [
                        '@use "@/assets/styles/_colors.scss" as *;',
                        '@use "@/assets/styles/helpers.scss" as *;',
                        '@use "@/assets/styles/breakpoints.scss" as *;',
                        '@use "@/assets/styles/components.scss" as *;',
                    ].join(""),
                },
            },
        },
    },
    runtimeConfig: {
        public: {
            MAX_FIRSTNAME_LENGTH: Number(process.env.VITE_MAX_FIRSTNAME_LENGTH),
            MAX_LASTNAME_LENGTH: Number(process.env.VITE_MAX_LASTNAME_LENGTH),
            MAX_PASSWORD_LENGTH: Number(process.env.VITE_MAX_PASSWORD_LENGTH),
            MIN_PASSWORD_LENGTH: Number(process.env.VITE_MIN_PASSWORD_LENGTH),
            MIN_LOGIN_LENGTH: Number(process.env.VITE_MIN_LOGIN_LENGTH),
            MAX_LOGIN_LENGTH: Number(process.env.VITE_MAX_LOGIN_LENGTH),
            LOGIN_REGEX: process.env.VITE_LOGIN_REGEX,
            MAX_DESCRIPTION_LENGTH: Number(
                process.env.VITE_MAX_DESCRIPTION_LENGTH
            ),
            MAX_SITE_LENGTH: Number(process.env.VITE_MAX_SITE_LENGTH),
            MAX_GENDER_LENGTH: Number(process.env.VITE_MAX_GENDER_LENGTH),
            DATE_FORMAT: process.env.VITE_DATE_FORMAT,
            MAX_IDEA_NAME_LENGTH: Number(process.env.VITE_MAX_IDEA_NAME_LENGTH),
            MIN_IDEA_NAME_LENGTH: Number(process.env.VITE_MIN_IDEA_NAME_LENGTH),
            MAX_IDEA_DESCRIPTION_LENGTH: Number(
                process.env.VITE_MAX_IDEA_DESCRIPTION_LENGTH
            ),
            MAX_POST_NAME_LENGTH: Number(process.env.VITE_MAX_POST_NAME_LENGTH),
            MIN_POST_NAME_LENGTH: Number(process.env.VITE_MIN_POST_NAME_LENGTH),
            MAX_POST_DESCRIPTION_LENGTH: Number(
                process.env.VITE_MAX_POST_DESCRIPTION_LENGTH
            ),
            MAX_POST_COMMENT_LENGTH: Number(
                process.env.VITE_MAX_POST_COMMENT_LENGTH
            ),
            MIN_POST_COMMENT_LENGTH: Number(
                process.env.VITE_MIN_POST_COMMENT_LENGTH
            ),
            MAX_KEYWORD_NAME_LENGTH: Number(
                process.env.VITE_MAX_KEYWORD_NAME_LENGTH
            ),
            MIN_KEYWORD_NAME_LENGTH: Number(
                process.env.VITE_MIN_KEYWORD_NAME_LENGTH
            ),
        },
    },
});
