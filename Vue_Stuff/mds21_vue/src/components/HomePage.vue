<template>
  <MobileHeader></MobileHeader>
  <div v-if="step == 1 && !loading">
    <FlexRow class="justify-content-center w-100 pt-5"
      ><div class="fs-4 fw-bold">Check your medication here:</div></FlexRow
    >
    <FlexRow class="w-100 justify-content-center pt-5 pb-5">
      <div class="img-container px-2">
        <img ref="imgDisplay" id="medication" src="@/assets/image.png" />
      </div>
    </FlexRow>
    <FlexRow v-if="reuploadFail === true" class="w-100 justify-content-center pt-5 pb-5 text-danger">
      *No image selected, please reupload
    </FlexRow>
    <FlexRow class="pt-5">
      <FlexCol class="col-6 pe-2">
        <label for="input-file"><div class="pt-1">UPLOAD FILE</div></label>
        <input
          ref="inputFile"
          type="file"
          accept="image/jpeg, image/png, image/jpg"
          id="input-file"
          style="display: none"
          @change="inputChanged"
        />
      </FlexCol>
      <FlexCol class="col-6 ps-2">
        <button class="btn btn-mds" @click="handleSubmit()" :disabled="!tempBlobUrl">SUBMIT</button>
      </FlexCol>
    </FlexRow>
  </div>
  <div v-if="loading" class="d-flex h-100 mt-5 justify-content-center align-items-center">
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
    v-if="step == 2 && !success && !loading"
    class="d-flex h-100 mt-5 justify-content-center align-items-center"
  >
    <FlexCol>
      <FlexRow class="text-center">
        {{ errorMsg }}<br />
        Please try again
      </FlexRow>
      <FlexRow class="justify-content-center pt-3">
        <button class="btn btn-mds" @click="reupload()"data-testid="reupload-button">REUPLOAD IMAGE</button>
      </FlexRow>
    </FlexCol>
  </div>
  <div
    v-if="step == 2 && success && !loading"
    class="d-flex h-100 mt-5 justify-content-center align-items-center"
  >
    <FlexCol>
      <FlexRow class="fs-2 fw-bold justify-content-center"> Results: </FlexRow>
      <FlexRow class="fs-3 fw-bold justify-content-center">{{api}} {{ dosage }}</FlexRow>
      <FlexRow class="py-4">
        <img :src="tempBlobUrl" alt="result-image"/>
      </FlexRow>
      <FlexRow class="fs-4 fw-bold justify-content-center"> Dosage: {{ dosage }} </FlexRow>
      <FlexRow class="pt-4 justify-content-center">
        <button class="btn btn-mds" @click="reupload()">UPLOAD A NEW IMAGE</button>
      </FlexRow>
    </FlexCol>
  </div>
</template>
<script setup>
import { ref } from 'vue'
import FlexCol from '@/components/layout/FlexCol.vue'
import FlexRow from '@/components/layout/FlexRow.vue'
import MobileHeader from '@/components/layout/MobileHeader.vue'
import { storeImageToFolder } from '@/utils/api.js'

const success = ref(false)
const loading = ref(false)
const step = ref(1)
const reuploadFail = ref(false)
const reuploadText = ref(false)

const imgDisplay = ref(null)
const tempBlobUrl = ref(null)
const inputFile = ref(null)
const errorMsg = ref("")

const api = ref(null)
const dosage = ref(null)

function inputChanged() {
  reuploadText.value = true
  const file = inputFile.value.files[0]
  if (file) {
    imgDisplay.value.src = URL.createObjectURL(file)
    tempBlobUrl.value = imgDisplay.value.src
    reuploadFail.value = false
    console.log(tempBlobUrl.value)
  } else {
    imgDisplay.value.src = "@/assets/image.png"
    tempBlobUrl.value = null
    reuploadFail.value = true
  }
}

function reupload() {
  step.value = 1
  success.value = false
  tempBlobUrl.value = null
}

function handleSubmit() {
  loading.value = true
  storeImgToFolder()
}

function storeImgToFolder(){
  const file = inputFile.value.files[0]
  console.log(file.type)
  
  const reader = new FileReader()
  reader.readAsDataURL(file)
  reader.onload = function() {
    const base64 = reader.result
    storeImageToFolder(base64, file.name).then((res) => {
      loading.value = false
      step.value = 2
      if (res.error) {
        success.value = false
        errorMsg.value = res.message
      } else {
        if (res.result[0].length === 1){
          api.value = res.result[0][0]
        } else {
          api.value = res.result[0].join(', ')
        }
          
        dosage.value = res.result[1]
        success.value = true
      }
    })
  }
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
