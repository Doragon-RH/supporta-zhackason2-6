<script setup lang="ts">
import { computed, ref } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";

const router = useRouter();

const friends = ["test01", "test02"];

const deadline = ref("");
const onInput = () => {
  deadline.value = deadline.value.replace(/\D/g, "");
  const year = deadline.value.substring(0, 4);
  const month = deadline.value.substring(4, 6);
  const day = deadline.value.substring(6, 8);
  if (deadline.value.length >= 7) {
    deadline.value = `${year}-${month}-${day}`;
  } else if (deadline.value.length >= 5) {
    deadline.value = `${year}-${month}${day}`;
  } else {
    deadline.value = `${year}${month}${day}`;
  }
};

const valid = ref(false);

const user_id = ref("");
const emailRules = [
  (v: string) => !!v || "Emailを入力してください",
  (v: string) => /\S+@\S+.\S+/.test(v) || "有効なEmailを入力してください",
  (v: string) => 6 <= v.length || "6文字以上で入力してください",
];
</script>
<template>
  <v-row align-content="center">
    <v-col align="center">
      <v-card max-width="600px" min-width="450px" style="width: 100%">
        <v-card-title class="text-pink-darken-4 font-weight-bold pa-5">
          RECORD PAYMENT
        </v-card-title>
        <v-divider />
        <v-card-text class="pa-5">
          <v-select :items="friends" label="フレンド" variant="outlined" prepend-icon="mdi-account-multiple"></v-select>
          <v-form v-model="valid">
            <v-text-field v-model="deadline" @input="onInput" label="日付(YYYY-MM-DD)" placeholder="YYYY-MM-DD"
              maxlength="10" variant="outlined" prepend-icon="mdi-calendar">
            </v-text-field>
            <v-text-field :rules="emailRules" v-model="user_id" prepend-icon="mdi-currency-jpy" label="金額"
              variant="outlined" required />
            <v-textarea label="メモ" auto-grow variant="outlined" rows="3" row-height="25" shaped
              prepend-icon="mdi-note"></v-textarea>
            <v-card-actions class="justify-center pa-3">
              <v-btn to="/profile/register" @click="registerAccount" :disabled="!valid" color="pink accent-2"
                class="font-weight-bold text-h6" flat>
                登録
              </v-btn>
            </v-card-actions>
          </v-form>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>
