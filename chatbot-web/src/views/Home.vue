<script setup>
import { ref, watch, nextTick } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";

const route = useRoute();
const messages = ref([]);
const newMessage = ref('');
const loadingMessage = ref(false);
const messagesEnd = ref(null); // Ref for the scroll container

const loadingMessageString = {message: 'Loading...', role: 'assistant'};

const getMessages = (chatId) => {
  axios.get(`http://localhost:5000/chats/${chatId}/messages`)
    .then((response) => {
      messages.value = response.data.messages;
      if(response.data.loading) {
        messages.value.push(loadingMessageString);
      }
      scrollToBottom();  // Scroll to bottom after loading messages
    })
    .catch((error) => {
      console.error("Error fetching messages:", error);
    });
};

const sendMessage = () => {
  if (loadingMessage.value) return;
  if (!newMessage.value.trim()) return;
  const chatId = route.params.id;
  messages.value.push({
    message: newMessage.value,
    role: 'user'
  });
  let messageToSend = newMessage.value;
  newMessage.value = '';
  loadingMessage.value = true;
  messages.value.push(loadingMessageString); // Add loading message to the chat
  scrollToBottom();  // Scroll to bottom after adding loading message
  axios.post(`http://localhost:5000/chats/${chatId}/messages`, {
    message: messageToSend
  })
    .then((res) => {
      // Remove loading message after receiving response
      const index = messages.value.findIndex(msg => msg.message === loadingMessageString.message && msg.role === loadingMessageString.role);
      if (index !== -1) {
        messages.value.splice(index, 1); // Remove loading message
      }
      loadingMessage.value = false;
      messages.value.push(res.data);
      scrollToBottom();  // Scroll to bottom after sending the message
    })
    .catch((err) => {
      loadingMessage.value = false;
      console.error("Error sending message:", err);
    });
};

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesEnd.value) {
      messagesEnd.value.scrollIntoView({ behavior: 'smooth' });
    }
  });
};

watch(
  () => route.params.id,
  (chatId) => {
    if (chatId) {
      getMessages(chatId);
    }
  },
  { immediate: true }
);

</script>

<template>
  <div class="flex flex-column h-full">
    <!-- Scrollable message area -->
    <div class="flex-1 overflow-y-auto p-3">
      <div
        v-for="message in messages"
        :key="message._id"
        class="flex mb-2"
        :class="{
          'justify-content-end': message.role === 'user',
          'justify-content-start': message.role === 'assistant'
        }"
      >
        <div
          :class="{
            'bg-bluegray-50 text-right': message.role === 'user',
            'bg-bluegray-100 text-left': message.role === 'assistant'
          }"
          class="border-round-lg shadow-1 p-3 max-w-30rem"
        >
          <p class="m-0">{{ message.message }}</p>
        </div>
      </div>
      <!-- This is the element that will be scrolled to the bottom -->
      <div ref="messagesEnd"></div>
    </div>

    <!-- Input fixed at bottom of this area -->
    <div class="p-3 border-top-1 surface-border flex gap-2 align-items-center bg-white">
      <InputText
        v-model="newMessage"
        placeholder="Type a message..."
        class="flex-1"
        @keyup.enter="sendMessage"
      />
      <Button :disabled="loadingMessage" icon="pi pi-send" label="Send" @click="sendMessage" class="p-button-rounded p-button-outlined" />
    </div>
  </div>
</template>
