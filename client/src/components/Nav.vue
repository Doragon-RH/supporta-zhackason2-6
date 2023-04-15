<template>
  <v-app-bar height="100" color="pink accent-3" flat>
    <router-link to="/">
      <img
        style="padding-left: 20px"
        height="80"
        src="/src/assets/logo_title.png"
      />
    </router-link>
    <v-spacer></v-spacer>
    <v-spacer></v-spacer>
    <v-btn class="btns" size="48">
      <v-icon size="48">mdi-bell</v-icon>
    </v-btn>
    <v-btn class="btns" size="48">
      <v-icon size="48">mdi-plus-circle</v-icon>
    </v-btn>
    <v-btn class="btns" size="48" to="/friend">
      <v-icon size="48">mdi-account-multiple</v-icon>
    </v-btn>
    <v-btn class="btns" size="48" to="/profile/register">
      <v-icon size="48">mdi-account-edit</v-icon>
    </v-btn>
    <v-btn class="btns" size="48" to="/signup">
      <v-icon size="48">mdi-logout</v-icon>
    </v-btn>
  </v-app-bar>
</template>
<style>
.btns {
  margin-right: 20px;
}
</style>
