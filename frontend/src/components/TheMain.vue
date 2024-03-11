<script setup>
import { nextTick, ref, computed } from 'vue'
import { NCard, NCode, NH2, NH1, NH3, NTag, NCheckbox, NButton } from 'naive-ui'
import { useImageStore } from '@/stores/useImageStore'

const isNumberDisabled = ref(false)
const isDigitDisabled = ref(false)
const imageStore = useImageStore()

const numberDisplay = computed(() => {
    return isNumberDisabled.value ? 'none' : 'block'
})

const digitDisplay = computed(() => {
    return isDigitDisabled.value ? 'none' : 'block'
})

const composeToPercent = (value) => {
    return Math.round(value * 10000) / 100
}

const getTagState = (value) => {
    if (value > 0.9) return 'success'
    if (value > 0.8) return 'warning'
    return 'error'
}

const fillRectangles = async () => {
    if (!Array.isArray(imageStore.result.numbers)) return
    await nextTick()
    const img = document.querySelector('#img-result')
    const imgWrapper = document.querySelector('.img-result-wrapper')
    const bounding = img.getBoundingClientRect()
    const width = bounding.width
    const height = bounding.height
    const actualWidth = imageStore.actualImageWidth
    const actualHeight = imageStore.actualImageHeight
    const coeffX = width / actualWidth
    const coeffY = height / actualHeight

    imageStore.result.numbers.forEach((number) => {
        const newX = number.number_center_x * coeffX
        const newY = number.number_center_y * coeffY
        const newWidth = number.width * coeffX
        const newHeight = number.height * coeffY

        const left = `${newX - newWidth / 2}px`
        const top = `${newY - newHeight / 2}px`

        const rect = document.createElement('div')
        rect.style.left = left
        rect.style.top = top
        rect.style.width = newWidth + 'px'
        rect.style.height = newHeight + 'px'
        rect.classList.add('image-rect')

        imgWrapper.insertAdjacentElement('beforeend', rect)
    })
}
</script>

<template>
    <div class="main-content" v-if="imageStore.hasResult">
        <NCard class="main-content-image">
            <template #header>Результат на изображении</template>
            <div class="img-result-wrapper">
                <img
                    v-if="imageStore.imageURL"
                    id="img-result"
                    :src="imageStore.imageURL"
                    class="main-image"
                    @load="fillRectangles"
                />
            </div>
            <div class="img-control">
                <NCheckbox v-model:checked="isNumberDisabled">Выключить обводку номера</NCheckbox>
            </div>
        </NCard>
        <NCard class="main-content-result">
            <template #header>Результаты</template>
            <div v-for="(number, index) in imageStore.result.numbers" :key="index">
                <NH1 v-if="imageStore.result.numbers.length > 1">Номер #{{ index + 1 }}</NH1>
                <NH2>Весь номер: {{ number.number }}</NH2>
                <div class="main-info">
                    <NTag type="info" :bordered="false">
                        Координаты: ({{ number.number_center_x }}, {{ number.number_center_y }})
                    </NTag>
                    <NTag type="info" :bordered="false">
                        Размер: {{ number.width }}x{{ number.height }}
                    </NTag>
                    <NTag :type="getTagState(number.confidence)" :bordered="false">
                        Уверенность: {{ composeToPercent(number.confidence) }}%
                    </NTag>
                    <NTag :type="number.is_rule_complete ? 'success' : 'error'" :bordered="false">
                        <template v-if="number.is_rule_complete">
                            Контрольная цифра верна
                        </template>
                        <template v-else> Контрольная цифра неверна </template>
                    </NTag>
                    <NTag :type="number.is_valid ? 'success' : 'error'" :bordered="false">
                        <template v-if="number.is_valid"> Валидный </template>
                        <template v-else> Невалидный</template>
                    </NTag>
                </div>
                <div class="main-digit" v-for="(digit, index) in number.digits" :key="index">
                    <NH3>Цифра #{{ index + 1 }}: {{ digit.value }}</NH3>
                    <div class="main-info">
                        <NTag :type="getTagState(digit.confidence)" :bordered="false">
                            Уверенность: {{ composeToPercent(digit.confidence) }}%
                        </NTag>
                        <NTag :type="digit.is_valid ? 'success' : 'error'" :bordered="false">
                            <template v-if="digit.is_valid"> Валидная </template>
                            <template v-else> Невалидная </template>
                        </NTag>
                        <NTag :type="getTagState(digit.confidence)" :bordered="false">
                            Значение цифры: TODO
                        </NTag>
                    </div>
                </div>
            </div>
        </NCard>
    </div>
    <NButton
        v-if="imageStore.hasResult"
        @click="imageStore.reset"
        type="primary"
        ghost
        block
        class="reset-btn"
    >
        Сбросить фотографию
    </NButton>
    <NCard class="json-content" v-if="imageStore.hasResult">
        <template #header>Результат (json)</template>
        <NCode :code="imageStore.resultJSON" language="json" />
    </NCard>
</template>

<style>
.main-content {
    display: flex;

    flex-wrap: nowrap;

    gap: 20px;

    margin-bottom: 20px;
}

.main-content-image {
    width: auto;
}

.main-content-result {
    width: 100%;
}

.main-info {
    display: flex;

    flex-wrap: wrap;

    gap: 10px;
}

.main-digit {
    margin-top: 20px;
}

.main-image {
    max-width: 55vw;
    height: auto;
}

@media (max-width: 980px) {
    .main-content {
        flex-direction: column;
    }

    .main-content-image {
        width: 100%;
    }

    .main-image {
        max-width: 100%;
        height: auto;
    }
}

.img-result-wrapper {
    position: relative;
}

.image-rect {
    position: absolute;

    box-sizing: border-box !important;

    display: v-bind('numberDisplay');

    border: 2px solid red;
}

.image-rect-digit {
    position: absolute;

    box-sizing: border-box !important;

    display: v-bind('digitDisplay');

    border: 2px solid blue;
}

.img-control {
    display: flex;

    flex-direction: column;

    gap: 10px;

    margin-top: 20px;
}

.reset-btn {
    height: 60px;
    margin-bottom: 20px;
}
</style>
