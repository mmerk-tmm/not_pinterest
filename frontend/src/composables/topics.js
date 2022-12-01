import { watch, ref, reactive } from "vue";
import { HTTP } from "../http-common.vue";
export const useTopicsSearch = () => {
  const searchText = ref("");
  const topics = ref([]);
  const cache = reactive({});
  const getTopics = async (text) => {
    try {
      console.log(cache);
      if (Object.hasOwn(cache, text)) {
        topics.value = cache[text];
        return;
      }
      if (!text) return [];
      const { data } = await HTTP.get("ideas/search-topic", {
        params: { name: text },
      });
      topics.value = data;
      cache[text] = data;
    } catch (error) {
      console.log("Произошла ошибка при поиске");
      topics.value = [];
    }
  };
  watch(searchText, getTopics);
  return { searchText, topics };
};
