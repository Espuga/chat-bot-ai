# 📘 API Documentation

This document describes the REST API provided by the backend service of the **Chat Bot** project. The API is built with Flask and communicates with MongoDB and the Mistral model via Ollama.

---

## 🔗 Base URL

`http://localhost:5000`

---

## 📁 Chat Endpoints

### 🔍 GET `/chats`

Fetch all existing chats.

**Response:**

```json
[
  {
    "_id": "chat_id_1",
    "name": "Project Assistant",
    "loading": false,
    "timestamp": "Tue, 22 Apr 2025 17:50:44 GMT"
  },
  ...
]
```

---

### ➕ POST `/chats`

Create a new chat.

**Request:**

```json
{
  "name": "My New Chat"
}
```

**Response:**

```json

{
  "_id": "chat_id_2",
  "name": "My New Chat",
  "loading": false,
  "timestamp": "Tue, 22 Apr 2025 17:50:44 GMT"
}
```

### ❌ DELETE `/chats/<chat_id>`

Delete a chat by ID.

**Response:**

```json
{
  "message": "Chat deleted successfully"
}
```

## 💬 Message Endpoints

### 🔍 GET `/chats/<chat_id>/messages`

Get all messages in a chat, along with a loading status.

**Response:**

```json
{
  "loading": false,
  "messages": [
    {
      "_id": "message_id_1",
      "chat_id": "chat_id_1",
      "role": "user",
      "message": "Hello",
      "timestamp": "Tue, 22 Apr 2025 17:50:50 GMT"
    },
    {
      "_id": "message_id_2",
      "chat_id": "chat_id_1",
      "role": "assistant",
      "message": "Hi there! How can I help you?",
      "timestamp": "Tue, 22 Apr 2025 17:50:50 GMT"
    }
  ]
}
```

### ➕ POST `/chats/<chat_id>/messages`

Send a new message to the chatbot. This triggers a response from the AI model and stores both messages in the database.

**Request:**

```json
{
  "message": "Tell me about the uploaded files."
}
```

**Response:**

```json
{
    "_id": "message_id_2",
    "chat_id": "chat_id_1",
    "role": "assistant",
    "message": "Hi there! How can I help you?",
    "timestamp": "Tue, 22 Apr 2025 17:50:50 GMT"
}
```

## 📄 Info/File Upload Endpoints

### 🔍 GET `/info`

Retrieve metadata and contents of all uploaded files.

**Response:**

```json
[
  {
    "_id": "info_id_1",
    "filename": "data.txt",
    "text": "Project schedule and goals for Q4...",
    "timestamp": "Tue, 22 Apr 2025 17:49:23 GMT"
  },
  ...
]
```

### ➕ POST `/info`

Upload a new text file (used as reference/context for AI answers).

**Form Data:**

- `file`: File (text/plain, pdf)

**Response:**

```json
{
  "_id": "info_id_2",
  "filename": "notes.txt",
  "text": "Meeting notes and action items...",
  "timestamp": "Tue, 22 Apr 2025 17:49:23 GMT"
}
```

### ❌ DELETE `/info/<info_id>`

Delete an uploaded file/info entry by ID.

**Response:**

```json
{
  "message": "Info deleted successfully"
}
```

## ⚙️ Notes

- The chatbot uses all uploaded info texts to build a context for each chat message.
- Messages are stored per chat and include both user and assistant roles.
- The AI model used is Mistral, queried via Ollama.
