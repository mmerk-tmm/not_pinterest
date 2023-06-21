module.exports = {
    apps: [
        {
            name: "not-pinterest-frontend",
            port: "4010",
            exec_mode: "cluster",
            instances: "max",
            script: "./.output/server/index.mjs",
        },
    ],
};
