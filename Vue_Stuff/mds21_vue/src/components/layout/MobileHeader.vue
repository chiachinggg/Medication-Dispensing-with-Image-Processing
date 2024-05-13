<template>
  <FlexRow class="w-100 py-3 justify-content-between">
    <FlexCol>
      <FlexRow
        ><button type="button" class="btn btn-mds">
          <span style="color: yellow; font-weight: bold">FYP</span> MDS21
        </button></FlexRow
      >
    </FlexCol>
    <FlexCol class="justify-content-center" @click="handleAboutUs()">
      <FlexRow class="header">About Us</FlexRow>
    </FlexCol>
    <FlexCol class="justify-content-center"><FlexRow class="header">FAQs</FlexRow></FlexCol>
    <FlexCol class="justify-content-center pe-2"
      ><FlexRow class="header">Bug Report</FlexRow></FlexCol
    >
  </FlexRow>
</template>
<script setup>
import FlexCol from '@/components/layout/FlexCol.vue'
import FlexRow from '@/components/layout/FlexRow.vue'
</script>
<style scoped>
.btn-mds {
  background-color: #0c513f;
  color: white;
  text-align: center;
  border-radius: 30px;
  padding: 1rem;
}

.header {
  cursor: pointer;
  font-size: 0.8rem;
  font-weight: bold;
}
</style>
