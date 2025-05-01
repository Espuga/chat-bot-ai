import { defineStore } from 'pinia'
import { i18n } from '../i18n/i18n';

export const configStore = defineStore('config', {
  state: () => ({
    title: ""
  }),

  actions: {

    async changeLanguage(idiom) {
      i18n.global.locale.value = idiom
    },

    getTitle() {
      return this.title;
    },
    setTitle(title) {
      this.title = title
    }
  }
})


