<script setup>
import { ref } from 'vue'
import { NModal, NCard, NUpload, NButton } from 'naive-ui'
import BaseLoader from '@/components/BaseLoader.vue'
import { useImageStore } from '@/stores/useImageStore'

const isShown = ref(true)

const imageStore = useImageStore()
const errorText = ref('') 
const apiUrl = ref('http://localhost:8001/api')

const handleUpload = async ({ file }) => {
    try {
        imageStore.startLoading()
        imageStore.setImage(file)
        errorText.value = "Обработка данных"
        const formData = new FormData()
        formData.append('file', imageStore.image.file)
        const response = await fetch(apiUrl.value, {
            method: 'POST',
            body: formData
        })

        errorText.value = "Получение данных"
        const data = await response.json()

        errorText.value = "Завершение"
        imageStore.setResult(data)
        
    } catch (error) {
        errorText.value = "Возникла ошибка при обработке!"
    } finally {
        imageStore.stopLoading()
    }
}
</script>

<template>
    <NModal v-model:show="isShown" :close-on-esc="false" :mask-closable="false">
        <NCard
            style="width: 500px; height: 250px"
            title="Modal"
            :bordered="false"
            size="huge"
            role="dialog"
            aria-modal="true"
        >
            <template class="head" #header> {{ errorText || 'Загрузите фотографию для распознавания' }}</template>
            <template #default>
                <div class="upload-content">
                    <NUpload class="upload-component" :custom-request="handleUpload">
                        <NButton type="primary" size="large">Выберите изображение</NButton>
                    </NUpload>
                    <BaseLoader v-if="imageStore.isLoading" />
                </div>
            </template>
        </NCard>
    </NModal>
</template>

<style>
.upload-content {
    display: flex;

    align-items: center;

    justify-content: center;

    height: 100%;
}

.upload-component {
    display: inline-block;

    width: auto;
}

.n-upload-file-list {
    display: none;
}

.head {
    align-items: center;
    justify-content: center;
}
</style>
