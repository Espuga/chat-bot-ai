<script setup>
import { ref } from 'vue';
import { useI18n } from 'vue-i18n';
import { configStore } from '../stores/configStore';

const config = configStore();
const { t } = useI18n();

const opUser = ref();
const opIdioms = ref();

const toggle = (event) => {
  opUser.value.toggle(event)
}
const toggleIdiom = (event) => {
  opIdioms.value.toggle(event)
}

</script>

<template>
  <!-- <div class="shadow-2 py-3 px-4 flex flex-row justify-content-between align-items-center border-round-2xl"> -->
  <div class="shadow-2 py-3 px-4 flex flex-row justify-content-between align-items-center">
    <div class="flex flex-row align-items-center gap-2">
      <h1 class="m-0 text-3xl">Chat Bot</h1>
    </div>

    <div>
      <span class="font-bold text-3xl text-900">{{ t(config.getTitle()) }}</span>
    </div>

    <div class="flex flex-row justify-content-center align-items-center gap-3">
      <p class="text-xl m-0 p-0">{{ t('hi') }} <span class="font-bold">Marc</span>!</p>
      <i class="pi pi-user text-2xl cursor-pointer hover:text-800" @click="toggle"></i>
      <Popover ref="opUser">
        <div class="flex flex-column mx-2">
          <div class="flex flex-row justify-content-center align-items-center gap-2 cursor-pointer hover:text-800" >
            <i class="pi pi-sign-out text-xl"></i>
            <p class="text-lg m-0">{{ t('log_out') }}</p>
          </div>
        </div>
      </Popover>

      <!-- Change Language -->
      <i class="pi pi-globe text-2xl cursor-pointer hover:text-800" @click="toggleIdiom">
        <Popover ref="opIdioms">
          <div class="flex flex-column mx-2 gap-2">
            <!-- English -->
            <div class="flex flex-row align-items-center gap-2 cursor-pointer hover:text-800"
              @click="config.changeLanguage('en')">
              <img src="/img/idioms/en.png" alt="Catalan idiom" width="20px" />
              <p class="text-lg m-0">English</p>
            </div>
            <!-- <div class="flex flex-row align-items-center gap-2 cursor-pointer hover:text-700" @click="config.changeLanguage('ca')">
            <img src="/img/idioms/cat.png" alt="Catalan idiom" width="20px" />
            <p class="text-lg m-0">Català</p>
          </div> -->
          </div>
        </Popover>
      </i>
    </div>
  </div>
</template>