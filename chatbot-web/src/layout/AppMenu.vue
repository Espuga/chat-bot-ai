<script setup>
import { computed, onMounted, ref } from "vue";
import router from "../router/router";
import { useI18n } from 'vue-i18n';

import axios from "axios";
import FilesView from "../views/config/Files.vue";

const { t } = useI18n();
const emit = defineEmits(['showMenu'])

const items = ref([])
const classe = "bg-bluegray-50 border-round-lg shadow-1"
const visibleNewChat = ref(false)
const newChatTitle = ref("")
const selectedId = ref(null);

const handleDelete = () => {
  if (selectedId.value) {
    axios.delete("http://localhost:5000/chats/" + selectedId.value)
      .then((res) => {
        items.value = items.value.filter(item => String(item._id) !== String(selectedId.value))
        selectedId.value = null
      }).catch((err) => {
        console.error(err)
      })
  }
}

const menu = ref();
const contextMenuItems = ref([
  {
    label: 'Delete',
    icon: 'pi pi-fw pi-trash',
    command: handleDelete
  }
]);

const onRightClick = (event, id) => {
  selectedId.value = id;
  menu.value.show(event);
};

// invalid
const invalidNewChatTitle = ref(false)

const getClass = (r) => {
  if (r == router.currentRoute.value.path) {
    return classe
  }
  return ""
}

const createChat = () => {
  if(!newChatTitle.value || newChatTitle.value.length < 1) {
    invalidNewChatTitle.value = true
    return
  }
  invalidNewChatTitle.value = false
  axios.post("http://localhost:5000/chats", { name: newChatTitle.value })
    .then((res) => {
      items.value.push({
        label: res.data.name,
        command: () => { router.push("/chat/" + res.data._id) },
        class: getClass("/chat/" + res.data._id)
      })
      router.push("/chat/" + res.data._id)
      visibleNewChat.value = false
    }).catch((err) => {
      console.error(err)
    })
}


onMounted(() => {
  axios.get("http://localhost:5000/chats")
    .then((res) => {
      res.data.forEach((chat) => {
        items.value.push({
          _id: chat._id,
          label: chat.name,
          command: () => { router.push("/chat/" + chat._id) },
          class: getClass("/chat/" + chat._id)
        })
      })
    }).catch((err) => {
      console.error(err)
    })
})


// gestionar fitxers
const visibleConfig = ref(false)
const showConfig = () => {
  visibleConfig.value = !visibleConfig.value
}

</script>

<template>
  <div class="p-2 shadow-2">

    <div class="mb-2 flex flex-row gap-2">
      <Button icon="pi pi-plus" class="w-full p-button-rounded p-button-outlined" @click="visibleNewChat = true" label="New Chat" />
      <Button icon="pi pi-cog" class="px-3 p-button-rounded p-button-outlined" @click="showConfig" label="" />
    </div>

    <div v-for="item in items" :key="item.label" @contextmenu="onRightClick($event, item._id)"  class="flex flex-column gap-1">
      <div :class="item.class" @click="item.command" 
        class="p-2 cursor-pointer hover:bg-bluegray-100 transition-colors duration-200 ease-in-out">
        {{ item.label }}
      </div>
    </div>
    <ContextMenu ref="menu" :model="contextMenuItems">
      <template #item="{ item, props }">
          <a v-ripple class="flex items-center" v-bind="props.action">
              <span :class="item.icon" />
              <span class="ml-2">{{ item.label }}</span>
              <i v-if="item.items" class="pi pi-angle-right ml-auto"></i>
          </a>
      </template>
    </ContextMenu>

    <!-- New Chat Dialog -->
    <Dialog v-model:visible="visibleNewChat" modal header="New Chat" :style="{ width: '25rem' }">
      <div class="flex flex-column gap-2">
        <InputText autofocus v-model="newChatTitle" :invalid="invalidNewChatTitle" placeholder="Title" @keyup.enter="createChat" />
        <Button label="Create" icon="pi pi-save" @click="createChat" class="p-button-rounded p-button-outlined" />
      </div>
    </Dialog>

    <!-- Config Dialog -->
    <Dialog v-model:visible="visibleConfig" modal :draggable="false" header="Configuration" :style="{ width: '70rem' }" :pt="{
      header: { class: 'pb-0' },
    }">
      <div class="flex flex-row gap-2">
        
        <!-- Menu -->
        <div class="flex col-2 flex-column align-items-start gap-2">
          <h3 class="m-0 text-2xl">Menu</h3>
        </div>

        <!-- Menu view -->
        <FilesView :pt="{
          root: { class: 'col-10 border-noround border-none' },
          list: { class: 'gap-1 w-full' }
        }" />

      </div>
    </Dialog>

  </div>
</template>