# Chat Bot

An AI-powered chatbot platform built using Python and Vue 3, featuring file uploads, persistent conversation history with MongoDB, and integration with the Mistral language model via Ollama.

## ✨ Features

- 🧠 Chat interface powered by the Mistral language model via Ollama
- 🗂 Upload files for contextual Q&A with the chatbot
- 💾 Persistent chat and file data storage using MongoDB
- ⚡ REST API backend built with Python
- 🖥 Modern frontend using Vue 3 and Vite

## 🗂 Project Structure

```
chat-bot/ 
├── chatbot-ai/ # Python backend: API, AI integration, MongoDB logic
└── chatbot-web/ # Vue 3 frontend: UI, chat interface, file uploads
```

## 🔧 Technologies Used

- **Frontend:** Vue 3, Vite
- **Backend:** Python, FastAPI (or Flask if used)
- **Database:** MongoDB
- **AI Model:** Mistral via Ollama
- **File Upload & Contextual Q&A**

## 🚀 Getting Started

### Prerequisites

- Node.js (v16+)
- Python (v3.8+)
- MongoDB
- Ollama with Mistral model installed

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/chat-bot.git
cd chat-bot
```

### 2. Backend Setup (`chatbot-ai`)

```bash
cd chatbot-ai
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Make sure you have MongoDB running:

```bash
docker run -d --name mongodb -p 27017:27017 -e MONGO_INITDB_ROOT_USERNAME=admin -e MONGO_INITDB_ROOT_PASSWORD=admin mongo
```

Also Ollama installed with the Mistral model:

```bash
ollama pull mistral
```

Start the API server:

```bash
python3 main.py
```

### 3. Frontend Setup (`chatbot-web`)

```bash
cd ../chatbot-web
npm install
npm run dev
```

### 4. Access the App

Navigate to: `http://localhost:5173`
Make sure the backend is running and properly connected.

## 📁 File Upload & Contextual AI

Uploaded files are processed and stored in MongoDB. The AI model uses this data to provide answers based on your documents, simulating a RAG (Retrieval-Augmented Generation) workflow.

## 📬 API Endpoints

Example endpoints (adjust as needed):

- `POST /chat`: Send a message to the AI
- `GET /messages`: Fetch chat history
- `POST /upload`: Upload files

## 📄 License

MIT License. See `LICENSE` file for details.
