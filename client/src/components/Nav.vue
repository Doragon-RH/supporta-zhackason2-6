<script setup lang="ts">
import { dialogStore } from "@/stores";
import { computed } from "vue";
import { useRouter } from "vue-router";

const store = dialogStore();
const showNoticeDialog = computed({
  get: () => store.notice,
  set: (newValue) => store.setNotiece(newValue),
});
const showPostDialog = computed({
  get: () => store.post,
  set: (newValue) => store.setPost(newValue),
});
const showFriendDialog = computed({
  get: () => store.friend,
  set: (newValue) => store.setFriend(newValue),
});
const showProfileDialog = computed({
  get: () => store.profile,
  set: (newValue) => store.setProfile(newValue),
});

const router = useRouter();

const signOut = () => {
  sessionStorage.removeItem("user_id");
  sessionStorage.removeItem("email");
  router.push("/signin");
};
</script>
<template>
  <v-app-bar height="100" color="pink accent-3" flat>
    <router-link to="/">
      <img style="padding-left: 20px" height="80" src="/src/assets/logo_title.png" />
    </router-link>
    <v-spacer></v-spacer>
    <v-spacer></v-spacer>
    <v-btn class="btns" size="48" @click="showNoticeDialog = true">
      <v-icon size="48">mdi-bell</v-icon>
    </v-btn>
    <v-btn class="btns" size="48" @click="showPostDialog = true">
      <v-icon size="48">mdi-plus-circle</v-icon>
    </v-btn>
    <v-btn class="btns" size="48" @click="showFriendDialog = true">
      <v-icon size="48">mdi-account-multiple</v-icon>
    </v-btn>
    <v-btn class="btns" size="48" @click="showProfileDialog = true">
      <v-icon size="48">mdi-account-edit</v-icon>
    </v-btn>
    <v-btn class="btns" size="48" @click="signOut">
      <v-icon size="48">mdi-logout</v-icon>
    </v-btn>
  </v-app-bar>
</template>
<style>
.btns {
  margin-right: 20px;
}
</style>
