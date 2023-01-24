<template>
  <div class="new-art-wrapper">
    <div class="new-art-container">
      <div class="editor">
        <div class="column">
          <SelectImage block-color="var(--color-gray-roboflow-600)" />
        </div>
        <div class="column">
          <div class="art-info">
            <FormField
              label="В лентах видны только первые 40 символов"
              placeholder="Добавьте название арта"
              :border-radius="10"
              off-margin
            />
            <FormField
              placeholder="Ссылка на первоначальный источник"
              :border-radius="10"
              off-margin
              label="Пользователь сможет перейти на оригинальную страницу с изображением"
            />
            <div class="info-buttons">
              <div class="info-button">Выбрать тему</div>
            </div>
          </div>
        </div>
      </div>
      <FormTextArea
        placeholder="Добавьте описание арта"
        label="Когда люди нажимают на изображение они видят 50 первых символов"
      />
      <TopicSelector />
      <div class="buttons">
        <div class="save-button">Сохранить</div>
      </div>
    </div>
  </div>
</template>
<style lang="scss">
@use "@/assets/styles/helpers";
@use "@/assets/styles/components";

.new-art-wrapper {
  padding: 16px 0px;
  justify-content: center;
  display: flex;

  .new-art-container {
    padding: 20px;
    display: flex;
    flex-direction: column;
    width: 100%;
    gap: 10px;
    max-width: 750px;
    border-radius: 20px;
    background-color: var(--color-gray-roboflow-200);

    .buttons {
      display: flex;
      justify-content: right;
      gap: 10px;

      .save-button {
        background-color: var(--g-colorRed100);
        padding: 10px;
        border-radius: 10px;
        color: white;
        font-weight: 600;
        cursor: pointer;

        &:hover {
          background-color: var(--g-colorRed0);
        }
      }
    }

    .editor {
      display: grid;
      grid-template-columns: 200px 1fr;
      gap: 10px;

      .column {
        display: flex;
        flex-direction: column;
        gap: 10px;

        .art-info {
          display: flex;
          flex-direction: column;
          gap: 10px;

          .info-buttons {
            display: flex;
            gap: 10px;

            .info-button {
              @include components.button;
            }
          }
        }
      }
    }
  }
}
</style>
<script>
import SelectImage from "../components/SelectImage.vue";
import FormField from "../components/FormField.vue";
import FormTextArea from "../components/FormTextArea.vue";
import TopicSelector from "../components/topicSelector/index.vue";
export default {
  components: { SelectImage, FormField, FormTextArea, TopicSelector },
};
</script>
