<template>
  <MobileHeader></MobileHeader>
  <div v-if="step == 1 && loading == false">
    <FlexRow class="justify-content-center w-100 pt-5"
      ><div class="fs-4 fw-bold">Check your medication here:</div></FlexRow
    >
    <FlexRow class="w-100 justify-content-center pt-5 pb-5">
      <div class="img-container px-2">
        <img id="medication" src="@/assets/image.png" />
      </div>
    </FlexRow>
    <FlexRow class="pt-5">
      <FlexCol class="col-6 pe-2">
        <label for="input-file"><div class="pt-1">UPLOAD FILE</div></label>
        <input
          type="file"
          accept="image/jpeg, image/png, image/jpg"
          id="input-file"
          style="display: none"
        />
      </FlexCol>
      <FlexCol class="col-6 ps-2">
        <button class="btn btn-mds" @click="handleSubmit()">SUBMIT</button>
      </FlexCol>
    </FlexRow>
  </div>
  <div v-if="loading == true" class="d-flex h-100 mt-5 justify-content-center align-items-center">
    <FlexCol>
      <FlexRow> Image upload in progress... </FlexRow>
      <FlexRow class="justify-content-center pt-2">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </FlexRow>
    </FlexCol>
  </div>
  <div
    v-if="step == 2 && status == false && loading == false"
    class="d-flex h-100 mt-5 justify-content-center align-items-center"
  >
    <FlexCol>
      <FlexRow class="text-center">
        Image upload process has failed...<br />
        Please try again
      </FlexRow>
      <FlexRow class="justify-content-center pt-3">
        <button class="btn btn-mds" @click="handleReupload()">REUPLOAD IMAGE</button>
      </FlexRow>
    </FlexCol>
  </div>
  <div
    v-if="step == 2 && status == true && loading == false"
    class="d-flex h-100 mt-5 justify-content-center align-items-center"
  >
    <FlexCol>
      <FlexRow class="fs-2 fw-bold justify-content-center"> Results: </FlexRow>
      <FlexRow class="fs-3 fw-bold justify-content-center">Paracetamol 500g</FlexRow>
      <FlexRow class="py-4">
        <img id="medication2" :src="image.src" />
      </FlexRow>
      <FlexRow class="fs-4 fw-bold justify-content-center"> Dosage: 500mg </FlexRow>
      <FlexRow class="fs-4 fw-bold justify-content-center"> Side Effects: xxxxxx </FlexRow>
      <FlexRow class="pt-4 justify-content-center">
        <button class="btn btn-mds" @click="handleReupload()">UPLOAD A NEW IMAGE</button>
      </FlexRow>
    </FlexCol>
  </div>
</template>
<script setup>
import { ref, watch, h, computed, onMounted } from 'vue'

import FlexCol from '@/components/layout/FlexCol.vue'
import FlexRow from '@/components/layout/FlexRow.vue'
import MobileContainer from '@/components/layout/MobileContainer.vue'
import MobileHeader from '@/components/layout/MobileHeader.vue'

const image = ref(null)
const image2 = ref(null)
const inputFile = ref(null)
const status = ref(false)
const loading = ref(false)
const step = ref(1)
const imgFile = ref(null)

onMounted(() => {
  image.value = document.getElementById('medication')
  inputFile.value = document.getElementById('input-file')

  inputFile.value.addEventListener('change', function () {
    const file = inputFile.value.files[0]
    if (file) {
      image.value.src = URL.createObjectURL(file)
    }
  })
})

function setLoadingFalse() {
  loading.value = false
  step.value = 2
  status.value = false
}

function handleReupload() {
  step.value = 1
  status.value = false
  image.value.src = '@/assets/image.png'

  inputFile.value.addEventListener('change', function () {
    const file = inputFile.value.files[0]
    if (file) {
      image.value.src = URL.createObjectURL(file)
    }
  })
}

function handleSubmit() {
  loading.value = true
  setTimeout(setLoadingFalse, 5000)
}
</script>
<style scoped>
label {
  background-color: #0c513f;
  color: white;
  border: 1px solid #0c513f;
  width: 100%;
  height: 3.75rem;
  font-size: 1rem;
  padding: 0.8rem;
  border-radius: 30px;
  font-weight: bold;
  cursor: pointer;
  text-align: center;
}

.btn-mds {
  background-color: #0c513f;
  color: white;
  text-align: center;
  border-radius: 30px;
  padding: 1rem;
}

/* .img-container {
  max-width: 300px;
  max-height: 300px;
  overflow: auto;
} */

img {
  max-width: 100%;
  max-height: 400px;
  border: 2px solid black;
}
</style>
