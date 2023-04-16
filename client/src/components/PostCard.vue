<script setup lang="ts">
import { onMounted, ref } from "vue";
import { createClient } from "@supabase/supabase-js";

const url = import.meta.env.VITE_SUPABASE_URL;
const key = import.meta.env.VITE_SUPABASE_KEY;
const supabase = createClient(url, key);

const friends = ref([]);
const selectedFriend = ref("");
const getFollow = async () => {
  friends.value = [];
  const data = await supabase
    .from("Friend")
    .select("id, follower_email, established, rejected")
    .eq("follow_email", sessionStorage.getItem("email"));
  for (const d of data.data) {
    if (d.established && !d.rejected) {
      const user = await supabase
        .from("User")
        .select("user_name")
        .eq("email", d.follower_email);
      const name = user.data[0].user_name;
      console.log(friends.value);
      friends.value.push(d.follower_email);
    }
  }
};

const getFollower = async () => {
  const data = await supabase
    .from("Friend")
    .select("id, follow_email, established, rejected")
    .eq("follower_email", sessionStorage.getItem("email"));
  for (const d of data.data) {
    if (d.established && !d.rejected) {
      const user = await supabase
        .from("User")
        .select("user_name")
        .eq("email", d.follow_email);
      const name = user.data[0].user_name;
      console.log(friends.value);
      friends.value.push(d.follow_email);
    }
  }
};

onMounted(() => {
  getFollow();
  getFollower();
  console.log(friends.value);
});

const due_date = ref("");
const deadline = ref("");
const onInputDue = () => {
  due_date.value = due_date.value.replace(/\D/g, "");
  const year = due_date.value.substring(0, 4);
  const month = due_date.value.substring(4, 6);
  const day = due_date.value.substring(6, 8);
  if (due_date.value.length >= 7) {
    due_date.value = `${year}-${month}-${day}`;
  } else if (due_date.value.length >= 5) {
    due_date.value = `${year}-${month}${day}`;
  } else {
    due_date.value = `${year}${month}${day}`;
  }
};
const onInputDead = () => {
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

const amount = ref();
const note = ref("");

const registerPayment = async () => {
  console.log(new Date(deadline.value));
  console.log(new Date(due_date.value));
  console.log(selectedFriend);
  await supabase.from("Transaction").insert({
    amount: amount.value,
    memo: note.value,
    limit_date: new Date(deadline.value),
    due_date: new Date(due_date.value),
    lender_id: sessionStorage.getItem("email"),
    borrower_id: selectedFriend.value,
  });
};
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
          <v-select v-model="selectedFriend" :items="friends" label="フレンド" variant="outlined"
            prepend-icon="mdi-account-multiple"></v-select>
          <v-form v-model="valid">
            <v-text-field v-model="due_date" @input="onInputDue" label="貸した日(YYYY-MM-DD)" placeholder="YYYY-MM-DD"
              maxlength="10" variant="outlined" prepend-icon="mdi-calendar">
            </v-text-field>
            <v-text-field v-model="deadline" @input="onInputDead" label="締切日(YYYY-MM-DD)" placeholder="YYYY-MM-DD"
              maxlength="10" variant="outlined" prepend-icon="mdi-calendar">
            </v-text-field>
            <v-text-field type="number" v-model="amount" prepend-icon="mdi-currency-jpy" label="金額" variant="outlined"
              required />
            <v-textarea label="メモ" v-model="note" auto-grow variant="outlined" rows="3" row-height="25" shaped
              prepend-icon="mdi-note"></v-textarea>
            <v-card-actions class="justify-center pa-3">
              <v-btn @click="registerPayment" :disabled="!valid" color="pink accent-2" class="font-weight-bold text-h6"
                flat>
                登録
              </v-btn>
            </v-card-actions>
          </v-form>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>
