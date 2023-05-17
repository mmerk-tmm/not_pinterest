<template>
    <div class="container">
        <div class="card" v-for="link in links">
            <img :src="link.src" alt="" />
            <div class="info">
                <div class="user-info">{{ link.desc }}</div>
                <div class="desc">
                    {{ link.username }}
                </div>
            </div>
        </div>
    </div>
</template>
<script setup>
const links = [
    {
        desc: "Необъятность космоса и технического прогресса",
        username: "Star_planet",
        src: "https://media.discordapp.net/attachments/865575447811457056/1105002014758416467/unknown.png?width=1193&height=671",
    },

    {
        desc: "Тут может быть ваша реклама",
        username: "reklama.ru",
        src: "https://avatars.dzeninfra.ru/get-zen_doc/3512693/pub_5f270fb0102bf31da32cdf7a_5f2712381ea3aa309324b0a6/scale_1200",
    },

    {
        desc: "Коммисар, это ересь",
        username: "wh4k",
        src: "https://i.pinimg.com/564x/76/82/01/768201729ce1f61f8876e93a846615da.jpg",
    },

    {
        desc: "Железо снаружи железно внутри",
        username: "username",
        src: "https://i.pinimg.com/564x/dc/c1/6d/dcc16dc966b20d6882a1f60604ba42b4.jpg",
    },

    {
        desc: "Наследие Рау",
        username: "Rulf",
        src: "https://i.pinimg.com/564x/fe/37/e2/fe37e2c7c80a317141130fc3e7a79711.jpg",
    },

    {
        desc: "Бессвязный текст",
        username: "iiiooo",
        src: "https://i.pinimg.com/564x/d9/ba/e8/d9bae8502e1e4b8f1961f16dba372577.jpg",
    },

    {
        desc: "Моделирование",
        username: "Виртуоз",
        src: "https://i.pinimg.com/564x/37/2f/f9/372ff9f75ff436f87090d0f7a2d89092.jpg",
    },

    {
        desc: "Руление",
        username: "Вальтер",
        src: "https://i.pinimg.com/564x/6e/b7/f0/6eb7f08f1643df558d66f12761970e97.jpg",
    },

    {
        desc: "Педалирование",
        username: "Балор",
        src: "https://i.pinimg.com/564x/52/2a/da/522ada76330e82174af2be2f3a4bcab0.jpg",
    },

    {
        desc: "Картинка без смысла",
        username: "Асмодей",
        src: "https://i.pinimg.com/564x/a1/2f/f3/a12ff3acc9660cf5d7d4c9a4451eb872.jpg",
    },

    {
        desc: "Картинка со смыслом",
        username: "Горрум",
        src: "https://i.pinimg.com/564x/97/f9/c0/97f9c03f8933db7860d353b3e4edb7b3.jpg",
    },
];
</script>
<style lang="scss" scoped>
.container {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 10px;
    margin: auto;
    .card {
        padding: 10px;
        background-color: rgba($color: #000000, $alpha: 0.1);
        border-radius: 20px;
        display: flex;
        flex-direction: column;
        position: relative;
        isolation: isolate;

        img {
            border-radius: 20px;
            object-fit: cover;
            width: 100%;
            max-height: 200px;
        }
        .info {
            padding: 10px;
            .user-info {
                font-weight: bold;
            }
            .desc {
                text-overflow: ellipsis;

                /* Needed to make it work */
                overflow: hidden;
                white-space: nowrap;
            }
        }
    }
}
</style>
