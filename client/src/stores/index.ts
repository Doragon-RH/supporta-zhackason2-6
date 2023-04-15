import { defineStore } from "pinia";

interface DialogState {
  notice: boolean;
  post: boolean;
  friend: boolean;
  profile: boolean;
}

export const dialogStore = defineStore({
  id: "dialog",
  state: (): DialogState => ({
    notice: false,
    post: false,
    friend: false,
    profile: false,
  }),
  actions: {
    setNotiece(newValue: boolean) {
      this.notice = newValue;
    },
    setPost(newValue: boolean) {
      this.post = newValue;
    },
    setFriend(newValue: boolean) {
      this.friend = newValue;
    },
    setProfile(newValue: boolean) {
      this.profile = newValue;
    },
  },
});
