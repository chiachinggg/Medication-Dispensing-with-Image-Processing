<template>
  <div class="d-flex flex-column" :class="props.utils">
    <slot></slot>
  </div>
</template>
<script setup>
import { defineProps } from 'vue'
const props = defineProps({
  utils: {
    type: String
  }
})
</script>
