<template>
    <el-input v-bind="$attrs" v-model="value">
        <template #suffix>
            <span
                :class="[
                    'el-input__count',
                    { disabled: !showWordLimit || !value },
                ]"
                v-if="showWordLimit"
            >
                <span class="el-input__count-inner">
                    <span
                        :class="[
                            'current-length',
                            { warning: value.length < props.minLength },
                        ]"
                        >{{ value.length }}</span
                    >
                    /
                    <span class="max-length">{{ maxLength }}</span>
                </span>
            </span>
        </template>
    </el-input>
</template>
<script setup>
const props = defineProps({
    modelValue: {
        type: String,
        default: "",
    },
    height: {
        type: String,
        default: "40px",
    },
    append: {
        type: String,
        default: "",
    },
    showWordLimit: {
        type: Boolean,
        default: false,
    },
    minLength: {
        type: Number,
        default: 0,
    },
    maxLength: {
        type: Number,
        default: 0,
    },
});
const height = ref(props.height);
const value = ref(props.modelValue);
const showWordLimit = ref(props.showWordLimit);
const emit = defineEmits(["update:modelValue"]);
watch(value, (val) => {
    if (props.maxLength && val.length > props.maxLength) {
        value.value = val.slice(0, props.maxLength);
    }
    emit("update:modelValue", val);
});
</script>
<style lang="scss">
.el-input {
    // --el-input-bg-color: var(--app-input-bg, #{$secondary-bg});
    // --el-fill-color-blank: var(--app-input-bg, #{$secondary-bg});
    // --el-input-border-color: var(--app-input-border, #{$quaternary-text});
    // --el-input-hover-border-color: var(
    //     --app-input-hover-border,
    //     #{$tertiary-text}
    // );
    // --el-input-focus-border-color: var(--app-input-focus-border, #{$accent});
    // --el-input-text-color: var(--app-input-text, #{$primary-text});
    // --el-input-border-radius: var(--app-input-border-radius, 10px);
    --el-input-height: v-bind(height);

    .el-input__count {
        opacity: 1;
        &.disabled {
            opacity: 0;
        }
        .el-input__count-inner {
            .current-length {
                &.warning {
                    color: #{$g-colorRed100};
                }
            }
        }
    }
}
</style>
