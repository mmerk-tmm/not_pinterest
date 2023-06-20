import { Service } from "@/client";
export const useKeywordSearch = () => {
    const searchText = ref("");
    const keywords = ref([]);
    const cache = reactive({});
    const getKeywords = async (text) => {
        try {
            if (Object.hasOwn(cache, text)) {
                keywords.value = cache[text];
                return;
            }
            if (!text) return [];
            const data = await Service.searchKeywordApiV1KeywordsSearchGet(
                text
            );
            keywords.value = data;
            cache[text] = data;
        } catch (error) {
            console.log("Произошла ошибка при поиске");
            keywords.value = [];
        }
    };
    const clearSearch = () => {
        searchText.value = "";
        keywords.value = [];
    };
    watch(searchText, getKeywords);
    return { searchText, keywords, clearSearch };
};
