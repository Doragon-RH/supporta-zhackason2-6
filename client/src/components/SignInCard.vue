<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";
import { createClient } from "@supabase/supabase-js";

const url = import.meta.env.VITE_SUPABASE_URL;
const key = import.meta.env.VITE_SUPABASE_KEY;
const supabase = createClient(url, key);

const router = useRouter();

const valid = ref(false);

const email = ref("");
const emailRules = [
  (v: string) => !!v || "Emailを入力してください",
  (v: string) => /\S+@\S+.\S+/.test(v) || "有効なEmailを入力してください",
  (v: string) => 6 <= v.length || "6文字以上で入力してください",
];

const showPassword = ref(false);
const password = ref("");
const passwordRules = [
  (v: string) => !!v || "パスワードを入力してください",
  (v: string) => 7 <= v.length || "8文字以上で入力してください",
];

const signIn = async () => {
  await axios
    .post("/auth/signin", {
      email: email.value,
      password: password.value,
    })
    .then(async (res) => {
      sessionStorage.setItem("user_id", res.data.user_id);
      sessionStorage.setItem("email", res.data.email);
      const { data, error } = await supabase
        .from("User")
        .select("user_name")
        .eq("user_id", res.data.user_id);
      if (!error) {
        sessionStorage.setItem("user_name", data[0].user_name);
      }
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
      SIGN IN
    </v-card-title>
    <v-divider />
    <v-card-text class="pa-5">
      <v-form v-model="valid">
        <v-text-field
          :rules="emailRules"
          v-model="email"
          prepend-icon="mdi-email"
          label="メールアドレス"
          variant="outlined"
          required
          style="padding-right: 40px"
        />
        <v-text-field
          @click:append="showPassword = !showPassword"
          v-bind:type="showPassword ? 'text' : 'password'"
          v-bind:append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
          v-model="password"
          :rules="passwordRules"
          prepend-icon="mdi-lock"
          label="パスワード"
          variant="outlined"
          required
        />
        <v-card-actions class="justify-center pa-3">
          <v-btn
            @click="signIn"
            :disabled="!valid"
            color="pink accent-2"
            class="font-weight-bold text-h6"
            flat
          >
            サインイン
          </v-btn>
        </v-card-actions>
      </v-form>
    </v-card-text>
    <v-divider />
    <p class="text-center" style="padding-top: 20px; padding-bottom: 20px">
      アカウントを<br />お持ちでない方は<router-link to="/signup"
        >こちら
      </router-link>
      <br />
    </p>
  </v-card>
</template>
