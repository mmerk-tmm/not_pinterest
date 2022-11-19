<template>
    <form class="settings-selection" ref="form">
        <h1>Общедоступный профиль</h1>
        <div class="picture-editor">
            <SelectImage @changed="updatePic" :pictureUrl="picture" name="userPicture" ref="selectPic" />
            <div class="picture-editor-content">
                <FormField :borderRadius="10" name="first_name" placeholder="Имя" v-model="firstName" offMargin>
                    <span :class="['count', { wrong: firstNameLenght < 0 }]">{{ firstNameLenght }}</span>
                </FormField>
                <FormField :borderRadius="10" name="last_name" placeholder="Фамилия" v-model="lastName" offMargin />
            </div>
        </div>
        <FormTextArea class="description" name="description" label="Описание" placeholder="Расскажите свою историю"
            v-model="description" :rows="5" offMargin :paddingRight="35" :maxLength="VITE_MAX_DESCRIPTION_LENGTH">
            <span :class="['count', { wrong: descriptionLenghtLimit < 0 }]" v-if="descriptionLenghtLimit">
                {{ descriptionLenghtLimit }}
            </span>
        </FormTextArea>
        <FormField :borderRadius="10" name="site" label="Веб-сайт"
            placeholder="Добавьте ссылку для привлечения трафика на свой сайт" v-model="site" offMargin />
        <FormField :borderRadius="10" name="username" label="Имя пользователя" v-model="userName"
            placeholder="И пусть это имя войдет в историю..." offMargin notEmpty />
        <div :class="['button', { active: dataChanged }, { wrong: fieldsWrong }]" @click="save">Сохранить</div>
        <div class="button">Сбросить</div>
    </form>
</template>
<script>
import SelectImage from './SelectImage.vue';
import FormField from './FormField.vue';
import FormTextArea from './FormTextArea.vue';
import { useAuthStore } from '../stores/auth';
import handleError from '../composables/errors';
import { useToast } from "vue-toastification";
import { storeToRefs } from 'pinia';
import { Role } from '../helpers/roles.js';
import { HTTP } from '../http-common.vue';
export default {
    setup() {
        const { userData, userRole } = storeToRefs(useAuthStore());
        const { setUserData, logout, getMe } = useAuthStore();
        const toast = useToast();
        const { VITE_MAX_FIRSTNAME_LENGTH, VITE_MAX_LASTNAME_LENGTH, VITE_MAX_DESCRIPTION_LENGTH } = import.meta.env;
        return {
            userData,
            toast,
            setUserData,
            logout,
            getMe,
            Role,
            userRole,
            VITE_MAX_FIRSTNAME_LENGTH,
            VITE_MAX_LASTNAME_LENGTH,
            VITE_MAX_DESCRIPTION_LENGTH
        }
    },
    components: {
        SelectImage,
        FormField,
        FormTextArea
    },
    data() {
        return {
            firstName: this.userData?.first_name,
            lastName: this.userData?.last_name,
            mounted: false,
            remove_picture: false,
            original_image: null,
            file_changed: false,
            fileChanged: false,
            picture: this.userData?.picture,
            description: this.userData?.description,
            site: this.userData?.site,
            userName: this.userData?.username,
        }
    },
    mounted() {
        this.mounted = true;
        this.getMe();
    },
    watch: {
        userData(data) {
            if (!data) return
            const { first_name, last_name, username, site, picture, description } = data;
            this.firstName = first_name;
            this.lastName = last_name;
            this.original_image = picture;
            this.picture = picture;
            this.description = description;
            this.site = site;
            this.userName = username;
        }
    },
    computed: {
        avatarIsEmpty() {
            if (!this.userData) return true
            return !Boolean(this.userData.picture)
        },
        dataChanged() {
            if (!this.userData) return
            if (this.fieldsWrong) return
            return this.userData.first_name !== this.firstName || this.userData.last_name !== this.lastName || this.userData.description !== this.description || this.userData.site !== this.site || this.userData.username !== this.userName || this.file_changed
        },
        fieldsWrong() {
            return this.lastNameLenght < 0 || this.firstNameLenght < 0
        },
        lastNameLenght() {
            if (!this.lastName) return
            return this.VITE_MAX_LASTNAME_LENGTH - this.lastName?.length
        },
        firstNameLenght() {
            if (!this.firstName) return
            return this.VITE_MAX_FIRSTNAME_LENGTH - this.firstName?.length
        },
        descriptionLenghtLimit() {
            let lenght = this.description?.length;
            if (!lenght) return
            return this.VITE_MAX_DESCRIPTION_LENGTH - lenght
        },
    },
    methods: {
        detelePicture() {
            this.$refs.selectPic.detelePicture();
            this.remove_picture = true;
            this.file_changed = true;
        },
        updatePic(target) {
            this.file_changed = true;
            if (!this.file_changed) return
            let file = target.files;
            this.fileChanged = file !== this.userData.picture;
        },
        save() {
            if (this.fieldsWrong) return
            if (this.dataChanged) {
                const form = this.$refs.form;
                if (!form) return
                let data = new FormData(form);
                data.append('remove_picture', this.remove_picture);
                HTTP.put('me', data)
                    .then((response) => {
                        this.remove_picture = false;
                        this.file_changed = false;
                        this.setUserData(response.data);
                    })
                    .catch((error) => {
                        this.toast.error(handleError(error, 'При обновлении профиля произошла ошибка').message)
                    });
            }
        }
    },

}
</script>
<style lang="scss" scoped>
.settings-selection {
    .picture-editor {
        margin-top: 10px;
        display: grid;
        grid-template-columns: 95px 1fr;
        gap: 10px;

        .picture-editor-content {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
    }

    .description {
        position: relative;

        .count {
            position: absolute;
            right: 0px;
            bottom: 8px;
        }
    }

    .button {
        padding: 10px;
        border-radius: 10px;
        background-color: var(--color-gray-roboflow-300);
        text-align: center;

        &.wrong {
            background-color: var(--rose-madder);
        }

        &.active {
            background: black;
            color: white;
            cursor: pointer;
        }
    }
}
</style>