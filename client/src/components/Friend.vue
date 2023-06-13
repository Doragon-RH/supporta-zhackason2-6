<script setup lang="ts">
import { createClient } from "@supabase/supabase-js";
import { onMounted, ref } from "vue";

const url = import.meta.env.VITE_SUPABASE_URL;
const key = import.meta.env.VITE_SUPABASE_KEY;
const supabase = createClient(url, key);

const email = ref("");
const emailRules = [
  (v: string) => !!v || "Emailを入力してください",
  (v: string) => /\S+@\S+.\S+/.test(v) || "有効なEmailを入力してください",
  (v: string) => 6 <= v.length || "6文字以上で入力してください",
];

const onClick = async () => {
  console.log("ok", sessionStorage.getItem("email"), email.value);
  await supabase.from("Friend").insert({
    follow_email: sessionStorage.getItem("email"),
    follower_email: email.value,
  });
  getFollow();
};

const tab = ref("申請中");
const tabs = ["申請中", "未承認", "承認済み"];

const applications = ref([]);
const deleteApplication = async (id: number) => {
  const data = await supabase
    .from("Friend")
    .update({ rejected: true })
    .eq("id", id);
  getFollow();
};

const unApproved = ref([]);
const approve = async (id: number) => {
  const data = await supabase
    .from("Friend")
    .update({ established: true })
    .eq("id", id);
  getFollower();
};
const reject = async (id: number) => {
  const data = await supabase
    .from("Friend")
    .update({ reject: true })
    .eq("id", id);
  getFollower();
};

const friends = ref([]);
const deleteFriend = async (id: number) => {
  const data = await supabase
    .from("Friend")
    .update({ reject: true })
    .eq("id", id);
  getFollow();
  getFollower();
};

const getFollow = async () => {
  applications.value = [];
  friends.value = [];
  const data = await supabase
    .from("Friend")
    .select("id, follower_email, established, rejected")
    .eq("follow_email", sessionStorage.getItem("email"));
  for (const d of data.data) {
    if (!d.established && !d.rejected) {
      const user = await supabase
        .from("User")
        .select("user_name")
        .eq("email", d.follower_email);
      const name = user.data[0].user_name;
      applications.value.push({
        id: d.id,
        user_name: name,
        email: d.follower_email,
      });
    } else if (d.established && !d.rejected) {
      const user = await supabase
        .from("User")
        .select("user_name, face_pattern, image_id")
        .eq("email", d.follower_email);
      const rand = Math.floor(Math.random() * (5 + 1 - 1)) + 1;
      const image = await supabase
        .from("Image")
        .select(`pattern${user.data[0].face_pattern}_lev${rand}_path`)
        .eq("id", user.data[0].image_id);
      const img_path =
        image.data[0][`pattern${user.data[0].face_pattern}_lev${rand}_path`];
      const url = supabase.storage.from("Images").getPublicUrl(img_path)
        .data.publicUrl;
      const name = user.data[0].user_name;
      friends.value.push({
        id: d.id,
        img_path: url,
        user_name: name,
        email: d.follower_email,
      });
    }
  }
};

const getFollower = async () => {
  unApproved.value = [];
  const data = await supabase
    .from("Friend")
    .select("id, follow_email, established, rejected")
    .eq("follower_email", sessionStorage.getItem("email"));
  for (const d of data.data) {
    if (!d.established && !d.rejected) {
      const user = await supabase
        .from("User")
        .select("user_name")
        .eq("email", d.follow_email);
      const name = user.data[0].user_name;
      unApproved.value.push({
        id: d.id,
        user_name: name,
        email: d.follow_email,
      });
    } else if (d.established && !d.rejected) {
      const user = await supabase
        .from("User")
        .select("user_name")
        .eq("email", d.follow_email);
      const name = user.data[0].user_name;
      friends.value.push({
        id: d.id,
        user_name: name,
        email: d.follow_email,
      });
    }
  }
};

onMounted(() => {
  getFollow();
  getFollower();
});
</script>
<template>
  <v-row align-content="center">
    <v-col align="center">
      <v-card max-width="600px" min-width="350px" style="width: 100%">
        <v-card-title class="text-pink-darken-4 font-weight-bold pa-5">
          FRIEND
        </v-card-title>
        <v-card-text>
          <div style="width: 80%">
            <v-text-field
              v-model="email"
              :rules="emailRules"
              variant="outlined"
              label="メールアドレスを入力"
              single-line
              hide-details
            >
              <template #append>
                <v-icon @click="onClick" size="48" style="margin-top: -12px"
                  >mdi-plus-box</v-icon
                >
              </template>
            </v-text-field>
          </div>
          <div style="height: 15px" />
          <v-tabs v-model="tab" color="pink-accent-4" align-tabs="center">
            <v-tab
              v-for="t in tabs"
              :key="t"
              :value="t"
              style="padding-left: 50px; padding-right: 50px"
            >
              <p class="font-weight-bold text-h6">{{ t }}</p>
            </v-tab>
          </v-tabs>
          <div style="height: 15px" />
          <div v-if="tab == '申請中'" style="height: 500px; overflow-y: auto">
            <div v-for="(user, index) in applications" class="d-flex flex-row">
              <v-avatar size="64">
                <v-icon size="64" icon="mdi-account-circle" />
              </v-avatar>
              <p class="text-h6" style="padding-top: 15px; padding-left: 5px">
                {{ user.user_name }} ({{ user.email }})
              </p>
              <v-spacer></v-spacer>
              <v-btn
                @click="deleteApplication(user.id)"
                color="red-darken-2"
                variant="outlined"
                style="margin-top: 12px"
              >
                取消
              </v-btn>
            </div>
          </div>
          <div v-if="tab == '未承認'" style="height: 500px; overflow-y: auto">
            <div v-for="(user, index) in unApproved" class="d-flex flex-row">
              <v-avatar size="64">
                <v-icon size="64" icon="mdi-account-circle" />
              </v-avatar>
              <p class="text-h6" style="padding-top: 15px; padding-left: 5px">
                {{ user.user_name }} ({{ user.email }})
              </p>
              <v-spacer></v-spacer>
              <v-btn
                @click="approve(user.id)"
                color="green-darken-2"
                variant="outlined"
                style="margin-top: 12px; margin-right: 20px"
              >
                承認
              </v-btn>
              <v-btn
                @click="reject(user.id)"
                color="red-darken-2"
                variant="outlined"
                style="margin-top: 12px"
              >
                拒否
              </v-btn>
            </div>
          </div>
          <div v-if="tab == '承認済み'" style="height: 500px; overflow-y: auto">
            <div v-for="(user, index) in friends" class="d-flex flex-row">
              <v-avatar size="64">
                <v-img :src="user.img_path"></v-img>
              </v-avatar>
              <p class="text-h6" style="padding-top: 15px; padding-left: 5px">
                {{ user.user_name }} ({{ user.email }})
              </p>
              <v-spacer></v-spacer>
              <v-btn
                @click="deleteFriend(user.id)"
                color="red-darken-2"
                variant="outlined"
                style="margin-top: 12px"
              >
                削除
              </v-btn>
            </div>
          </div>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>
<style></style>
