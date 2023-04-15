<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";

const router = useRouter();

const email = "test@example.com";

const uploadImg = ref();
const handleImageUpload = (event: any) => {
  const file = event.target.files[0];
  const reader = new FileReader();
  reader.onload = () => {
    uploadImg.value = reader.result;
  };
  reader.readAsDataURL(file);
};

const selectImgType = ref("A");
const selectImage = (type: string) => {
  selectImgType.value = type;
};

const valid = ref(false);

const user_id = ref("");
const emailRules = [
  (v: string) => !!v || "ユーザIDを入力してください",
  (v: string) => 6 <= v.length || "6文字以上で入力してください",
];

const password = ref("");
const passwordRules = [
  (v: string) => !!v || "パスワードを入力してください",
  (v: string) => 7 <= v.length || "8文字以上で入力してください",
];

const registerAccount = async () => {
  await axios
    .post("/user/signup", {
      name: user_id.value,
      password: password.value,
    })
    .then((res) => {
      sessionStorage.setItem("user_id", res.data.id);
      sessionStorage.setItem("user_name", res.data.name);
      router.push("/");
    })
    .catch((err) => {
      console.log(err);
    });
};
</script>
<template>
  <v-card max-width="600px" min-width="350px" style="width: 40%">
    <v-card-title class="text-pink-darken-4 font-weight-bold pa-5">
      PROFILE
    </v-card-title>
    <p class="text-subtitle-1">Email : {{ email }}</p>
    <div style="text-align: center">
      <v-avatar size="128">
        <v-img v-if="uploadImg" :src="uploadImg" />
        <v-icon v-else size="128" icon="mdi-account-circle" />
      </v-avatar>
      <div style="height: 20px" />
      <input
        type="file"
        @change="handleImageUpload"
        style="text-align: center"
      />
    </div>
    <div style="height: 20px" />
    <v-divider />
    <v-card-text class="pa-5">
      <v-form v-model="valid">
        <v-text-field
          :rules="emailRules"
          v-model="user_id"
          prepend-icon="mdi-account"
          label="ユーザID"
          variant="outlined"
          required
        />
        <v-text-field
          v-model="password"
          :rules="passwordRules"
          prepend-icon="mdi-card-account-details"
          label="ユーザ名"
          variant="outlined"
          required
        />
        <p class="d-flex flex-row text-subtitle-1 text-grey-darken-1">
          変形パターン
        </p>
        <div style="border: 2px solid #ccc; padding: 10px">
          <div
            :class="{ notSelected: selectImgType !== type }"
            style="display: inline-block"
            v-for="type in ['A', 'B', 'C']"
            :key="type"
            @click="selectImage(type)"
          >
            <v-avatar style="margin-right: 8px; margin-left: 8px" size="96">
              <v-img
                :src="`/src/assets/form_sample/form_sample_${type}.png`"
              ></v-img>
            </v-avatar>
          </div>
        </div>
        <v-card-actions class="justify-center pa-3">
          <v-btn
            @click="registerAccount"
            :disabled="!valid"
            color="pink accent-2"
            class="font-weight-bold text-h6"
            flat
          >
            登録
          </v-btn>
        </v-card-actions>
      </v-form>
    </v-card-text>
  </v-card>
</template>
<style>
.notSelected {
  opacity: 0.5;
}
</style>
