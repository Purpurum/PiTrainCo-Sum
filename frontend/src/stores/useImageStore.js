import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useImageStore = defineStore('image', () => {
    const image = ref(null)
    const imageURL = ref(null)
    const result = ref(null)
    const isLoading = ref(false)

    const hasImage = computed(() => {
        return Boolean(image.value)
    })

    const hasResult = computed(() => {
        return Boolean(imageURL.value) && !isLoading.value && Boolean(result.value)
    })

    const resultJSON = computed(() => {
        if (!result.value) return ''
        const tabSize = document.documentElement.clientWidth > 700 ? 4 : 2
        return JSON.stringify(result.value, null, tabSize)
    })

    const actualImageWidth = computed(() => {
        if (!hasResult.value) return
        return result.value.numbers?.at(0)?.img_width
    })

    const actualImageHeight = computed(() => {
        if (!hasResult.value) return
        return result.value.numbers?.at(0)?.img_height
    })

    function startLoading() {
        isLoading.value = true
    }

    function stopLoading() {
        isLoading.value = false
    }

    function setImage(img) {
        image.value = img
        renderImage(img.file)
    }

    function setResult(res) {
        result.value = res
    }

    function renderImage(file) {
        const fileReader = new FileReader()

        fileReader.onload = () => {
            imageURL.value = fileReader.result
        }

        fileReader.readAsDataURL(file)
    }

    function reset() {
        image.value = null
        imageURL.value = null
        result.value = null
        isLoading.value = false
    }

    return {
        image,
        imageURL,
        isLoading,
        hasResult,
        setImage,
        hasImage,
        startLoading,
        stopLoading,
        result,
        resultJSON,
        setResult,
        actualImageWidth,
        actualImageHeight,
        reset
    }
})
