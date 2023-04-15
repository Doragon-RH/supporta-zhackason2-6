<script setup lang="ts">
import { ref } from "vue";
import axios from "axios";
import { createClient } from "@supabase/supabase-js";
import { decode } from "base64-arraybuffer";

const url = import.meta.env.VITE_SUPABASE_URL;
const key = import.meta.env.VITE_SUPABASE_KEY;
const supabase = createClient(url, key);

const email = sessionStorage.getItem("email");

const image_data_url = ref();
const image_url = sessionStorage.getItem("image_url");
if (image_url) {
  const image_data = supabase.storage.from("Images").getPublicUrl(image_url);
  image_data_url.value = image_data.data.publicUrl;
}

const uploadImg = ref();
const fl = ref();
const handleImageUpload = (event: any) => {
  const file = event.target.files[0];
  fl.value = file;
  const reader = new FileReader();
  reader.onload = () => {
    uploadImg.value = reader.result;
  };
  reader.readAsDataURL(file);
};

const selectImgType = ref(sessionStorage.getItem("face_pattern"));
const selectImage = (type: string) => {
  selectImgType.value = type;
};

const valid = ref(false);

const user_id = sessionStorage.getItem("user_id");

const user_name = ref(sessionStorage.getItem("user_name"));
const nameRules = [
  (v: string) => !!v || "ユーザ名を入力してください",
  (v: string) => 6 <= v.length || "6文字以上で入力してください",
];

const updateProfile = async () => {
  if (uploadImg.value) {
    const exist_image = sessionStorage.getItem("image_id");
    const img = uploadImg.value.split(",")[1];
    const path = ref("");
    const error = ref();
    if (exist_image) {
      const data = await supabase.storage
        .from("Images")
        .update(`Origin/${user_id}.png`, decode(img));
      path.value = data.data?.path;
      error.value = data.error;
    } else {
      const data = await supabase.storage
        .from("Images")
        .upload(`Origin/${user_id}.png`, decode(img));
      path.value = data.data?.path;
      error.value = data.error;
    }
    console.log(path.value);

    await supabase
      .from("Image")
      .insert({ user_id: user_id, origin_path: path.value });
    const i_data = await supabase.from("Image").select().eq("user_id", user_id);
    if (!i_data.error) {
      sessionStorage.setItem("image_id", i_data.data[0].id);
      sessionStorage.setItem("image_url", i_data.data[0].origin_path);
    }
  }
  const error = await supabase
    .from("User")
    .update({
      user_name: user_name.value,
      image_id: sessionStorage.getItem("image_id"),
      face_pattern: selectImgType.value,
      updated_at: new Date(),
    })
    .eq("user_id", user_id);
  sessionStorage.setItem("user_name", user_name.value);
  sessionStorage.setItem("face_pattern", selectImgType.value);

  console.log(error);
};
</script>
<template>
  <v-row align-content="center">
    <v-col align="center">
      <v-card max-width="600px" min-width="450px" style="width: 100%">
        <v-card-title class="text-pink-darken-4 font-weight-bold pa-5">
          PROFILE
        </v-card-title>
        <p class="text-subtitle-1">Email : {{ email }}</p>
        <div style="text-align: center">
          <v-avatar size="128">
            <v-img v-if="uploadImg" :src="uploadImg" />
            <v-img v-else-if="image_data_url" :src="image_data_url" />
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
              disabled
              v-model="user_id"
              prepend-icon="mdi-account"
              label="ユーザID"
              variant="outlined"
              required
            />
            <v-text-field
              v-model="user_name"
              :rules="nameRules"
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
                @click="updateProfile"
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
    </v-col>
  </v-row>
</template>
<style>
.notSelected {
  opacity: 0.5;
}
</style>
