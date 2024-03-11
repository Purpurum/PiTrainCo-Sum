<script setup>
import { NSpin } from 'naive-ui'
</script>

<template>
    <div class="loader">
        <NSpin size="large" :stroke-width="30" stroke="#46B379" />
    </div>
</template>

<style>
.loader {
    position: absolute;
    inset: 0;

    display: flex;

    align-items: center;
    justify-content: center;

    background-color: rgb(0 0 0 / 30%);
}
</style>
