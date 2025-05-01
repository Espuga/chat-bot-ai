<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const files = ref([]);
const fileMenu = ref();
const selectedId = ref(null);
const handleDelete = () => {
  if (selectedId.value) {
    axios.delete(`http://localhost:5000/info/${selectedId.value}`)
      .then(() => {
        files.value = files.value.filter(file => file._id !== selectedId.value);
        selectedId.value = null;
      })
      .catch((error) => {
        console.error("Error deleting file:", error);
      });
  }
};
const contextMenuItems = ref([
  {
    label: 'Delete',
    icon: 'pi pi-fw pi-trash',
    command: handleDelete
  }
]);
const visibleNewFile = ref(false);
const showNewFile = () => {
  visibleNewFile.value = !visibleNewFile.value;
};
  

const onRightClick = (event, id) => {
  selectedId.value = id;
  fileMenu.value.show(event);
};


onMounted(() => {
  axios.get("http://localhost:5000/info")
    .then((response) => {
      files.value = response.data;
    })
    .catch((error) => {
      console.error("Error fetching files:", error);
    });
})

const uploadedFile = ref(null);

const onFileSelect = (event) => {
  uploadedFile.value = event.files[0]; // Store the selected file
};

const uploadFile = () => {
  if (!uploadedFile.value) return;

  const formData = new FormData();
  formData.append("file", uploadedFile.value);

  axios.post("http://localhost:5000/info", formData, {
    headers: {
      "Content-Type": "multipart/form-data"
    }
  })
  .then((res) => {
    console.log("Upload successful:", res.data);
    visibleNewFile.value = false;
    uploadedFile.value = null;
    // files.value.insert(0, res.data);
    files.value = [res.data, ...files.value];
  })
};


</script>

<template>
  <div class="col-10">
    <div class="flex flex-row justify-content-between align-items-center mb-4">
      <h3 class="text-2xl m-0 mb-2">Files</h3>
      <Button icon="pi pi-plus" label="New File" @click="showNewFile" class="p-button-rounded p-button-outlined" />
    </div>

    <div class="flex flex-row gap-2">
      <div v-for="file in files" :key="file.name" @contextmenu="onRightClick($event, file._id)"  class="col-3 flex align-items-center gap-2 shadow-2 border-round-lg p-2">
        <i class="pi pi-file text-2xl"></i>
        <div class="flex flex-column">
          <span class="font-bold">{{ file.file_name }}</span>
        </div>
      </div>
      <ContextMenu ref="fileMenu" :model="contextMenuItems">
        <template #item="{ item, props }">
            <a v-ripple class="flex items-center" v-bind="props.action">
                <span :class="item.icon" />
                <span class="ml-2">{{ item.label }}</span>
                <i v-if="item.items" class="pi pi-angle-right ml-auto"></i>
            </a>
        </template>
      </ContextMenu>
    </div>
    <div v-if="files.length === 0" class="text-center text-gray-500">
      No files available.
    </div>

    <!-- New File Dialog -->
    <Dialog header="New File" v-model:visible="visibleNewFile" :modal="true" :closable="true">
      <div class="flex flex-column gap-2">
        <FileUpload name="file" mode="basic" accept=".pdf,.txt" :maxFileSize="104857600" 
          @select="onFileSelect" chooseLabel="Select File" uploadLabel="Upload" cancelLabel="Cancel" />
        <Button label="Save" icon="pi pi-save" @click="uploadFile" class="p-button-rounded p-button-outlined" />
      </div>
    </Dialog>

  </div>

</template>