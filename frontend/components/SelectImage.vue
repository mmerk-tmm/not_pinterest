<template>
    <div :class="['select-image', { empty: !picture }]">
        <Icon name="material-symbols:image" v-if="!picture" />
        <img :src="picture" v-else />
        <div class="edit-area">
            <div class="edit-area-container">
                <Icon name="material-symbols:image" v-if="picture" />
                <div class="edit-area-text">выбрать файл</div>
                <input
                    type="file"
                    :name="name"
                    ref="fileupload"
                    :accept="acceptedFormats"
                    @change="previewFiles"
                />
            </div>
        </div>
    </div>
</template>
<script>
import { useToast } from "vue-toastification";
export default {
    setup() {
        const toast = useToast();
        return {
            toast,
        };
    },
    props: {
        pictureUrl: String,
        name: String,
        blockColor: String,
    },
    emits: ["changed"],
    data() {
        return {
            picture: this.pictureUrl,
            acceptedFormats: ".jpg, .jpeg, .png",
            target: null,
            defaultColor: "var(--color-text)",
        };
    },
    watch: {
        pictureUrl(value) {
            this.picture = value;
        },
    },
    computed: {
        color() {
            return this.blockColor || this.defaultColor;
        },
    },
    methods: {
        previewFiles(event) {
            let file = event.target.files;
            if (!(file && file[0])) {
                this.detelePicture();
                return;
            }
            this.target = file;
            var fileName = file[0].name;
            var idxDot = fileName.lastIndexOf(".") + 1;
            var extFile = fileName
                .substr(idxDot, fileName.length)
                .toLowerCase();
            let extentions = this.acceptedFormats
                .split(", ")
                .map((el) => el.replace(".", ""));
            if (!extentions.includes(extFile)) {
                this.toast(`Поддерживаемые форматы ${this.acceptedFormats}`);
                this.toast.error("Формат изображения не поддерживанется");
                this.detelePicture();
                return;
            }
            let reader = new FileReader();
            reader.onload = (e) => {
                this.picture = e.target.result;
            };
            reader.readAsDataURL(file[0]);
            this.$emit("changed", this.$refs.fileupload);
        },
        detelePicture() {
            this.$refs.fileupload.value = null;
            this.picture = null;
            this.target = null;
        },
    },
};
</script>
<style lang="scss">
.select-image {
    aspect-ratio: 1;
    position: relative;
    overflow: hidden;
    border-radius: 8px;
    isolation: isolate;
    transition: 2s filter, 2s opacity;

    img {
        object-fit: cover;
        width: 100%;
        height: 100%;
    }

    &.empty {
        @include flex-center;
        overflow: hidden;
        border: 2px dashed transparent;

        border-color: v-bind(color);

        svg {
            width: 40%;
            height: 40%;
            transition: 0.2s opacity;
            color: v-bind(color);
        }
    }

    &:hover {
        .edit-area {
            opacity: 1;
        }

        &.empty {
            svg {
                opacity: 0.5;
            }
        }

        img {
            filter: blur(3px);
        }
    }

    .edit-area {
        transition: opacity 0.2s;
        @include flex-center;
        flex-direction: column;
        position: absolute;
        inset: 0;
        opacity: 0;
        isolation: isolate;

        .edit-area-container {
            z-index: 2;
            position: absolute;
            inset: 0;
            @include flex-center;
            flex-direction: column;
            background-color: rgba($color: #000000, $alpha: 0.3);
            padding: 5px;
            aspect-ratio: 1;

            svg {
                width: 25%;
                height: 25%;
                margin-bottom: 5%;
                z-index: 2;
                opacity: 1;
            }

            .edit-area-text {
                z-index: 2;
                text-align: center;
            }
        }

        input {
            position: absolute;
            inset: 0;
            z-index: 3;
            opacity: 0;
            cursor: pointer;
        }

        &::after {
            content: "";
            position: absolute;
            inset: 0;
            background-color: $color-gray-roboflow-100;
            opacity: 0.5;
            z-index: 1;
        }
    }
}
</style>
