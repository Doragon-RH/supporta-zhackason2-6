<script setup lang="ts">
import { ref } from "vue";

const loaded = ref(false);
const loading = ref(false);

const onClick = () => {
  loading.value = true;

  setTimeout(() => {
    loading.value = false;
    loaded.value = true;
  }, 2000);
};

const tab = ref("申請中");
const tabs = ["申請中", "未承認", "承認済み"];

const applications = ref([
  { user_name: "山田太郎", user_id: "yamada_taro" },
  { user_name: "田中次郎", user_id: "tanaka_jiro" },
]);
const deleteApplication = (index: number) => {
  applications.value.splice(index, 1);
};

const unApproved = ref([
  { user_name: "山田太郎", user_id: "yamada_taro" },
  { user_name: "田中次郎", user_id: "tanaka_jiro" },
]);
const approve = (index: number) => {
  unApproved.value.splice(index, 1);
};
const reject = (index: number) => {
  unApproved.value.splice(index, 1);
};

const friends = ref([
  { user_name: "山田太郎", user_id: "yamada_taro" },
  { user_name: "田中次郎", user_id: "tanaka_jiro" },
]);
const deleteFriend = (index: number) => {
  friends.value.splice(index, 1);
};
</script>
<template>
  <v-card max-width="600px" min-width="350px" style="width: 60%">
    <v-card-title class="text-pink-darken-4 font-weight-bold pa-5">
      FRIEND
    </v-card-title>
    <v-card-text>
      <div style="width: 80%">
        <v-text-field
          :loading="loading"
          variant="outlined"
          label="ユーザIDを入力"
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
            {{ user.user_name }} (@{{ user.user_id }})
          </p>
          <v-spacer></v-spacer>
          <v-btn
            @click="deleteApplication(index)"
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
            {{ user.user_name }} (@{{ user.user_id }})
          </p>
          <v-spacer></v-spacer>
          <v-btn
            @click="approve(index)"
            color="green-darken-2"
            variant="outlined"
            style="margin-top: 12px; margin-right: 20px"
          >
            承認
          </v-btn>
          <v-btn
            @click="reject(index)"
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
            <v-icon size="64" icon="mdi-account-circle" />
          </v-avatar>
          <p class="text-h6" style="padding-top: 15px; padding-left: 5px">
            {{ user.user_name }} (@{{ user.user_id }})
          </p>
          <v-spacer></v-spacer>
          <v-btn
            @click="deleteFriend(index)"
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
</template>
<style></style>
