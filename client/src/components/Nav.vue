<template>
  <v-app-bar height="100" color="pink accent-3" flat>
    <v-img height="80" src="/src/assets/logo_title.png"></v-img>
    <v-spacer></v-spacer>
    <v-spacer></v-spacer>
    <v-btn class="btns" size="48">
      <v-icon size="48">mdi-bell</v-icon>
    </v-btn>
    <v-btn class="btns" size="48">
      <v-icon size="48">mdi-plus-circle</v-icon>
    </v-btn>
    <v-btn class="btns" size="48">
      <v-icon size="48">mdi-account-multiple</v-icon>
    </v-btn>
    <v-btn class="btns" size="48">
      <v-icon size="48">mdi-account-edit</v-icon>
    </v-btn>
    <v-btn class="btns" size="48">
      <v-icon size="48">mdi-logout</v-icon>
    </v-btn>
  </v-app-bar>
</template>
<style>
.btns {
  margin-right: 20px;
}
</style>
