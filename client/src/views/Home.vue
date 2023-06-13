<script setup lang="ts">
import { dialogStore } from "@/stores";
import { computed } from "vue";
import ChartCanvas from "/src/components/ChartCanvas.vue";
import Friend from "/src/components/Friend.vue";
import ProfileCard from "/src/components/ProfileCard.vue";
import PostCard from "/src/components/PostCard.vue";

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
</script>
<template>
  <v-dialog v-model="showNoticeDialog" width="auto"> </v-dialog>
  <v-dialog v-model="showPostDialog" width="auto">
    <PostCard />
  </v-dialog>
  <v-dialog v-model="showFriendDialog" width="auto">
    <Friend />
  </v-dialog>
  <v-dialog v-model="showProfileDialog" width="auto">
    <ProfileCard />
  </v-dialog>
  <div style="height: 150px" />
  <ChartCanvas />
</template>
