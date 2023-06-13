<script setup lang="ts">
import Nav from "/src/components/Nav.vue";
</script>

<template>
  <v-app class="bg-grey-lighten-4">
    <Nav />
    <v-row align-content="center">
      <v-col align="center">
        <router-view />
      </v-col>
    </v-row>
  </v-app>
</template>

<style scoped></style>
