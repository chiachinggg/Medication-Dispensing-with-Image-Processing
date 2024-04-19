import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useModalsStore = defineStore('modalsStore', () => {
  const popupModal = ref(null)

  return {
    popupModal
  }
})
