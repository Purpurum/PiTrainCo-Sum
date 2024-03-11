<script setup>
import TheMain from '@/components/TheMain.vue'
import UploadImageModal from '@/components/UploadImageModal.vue'

import { useImageStore } from '@/stores/useImageStore'

const imageStore = useImageStore()
</script>

<template>
    <div class="home-view">
        <TheMain />
        <UploadImageModal v-if="!imageStore.hasResult" />
    </div>
</template>

<style>
.home-view {
    padding: 25px;
}

@media (max-width: 600px) {
    .home-view {
        padding: 10px;
    }
}
</style>
