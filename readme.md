# TELEGRAM RAG BOT
- This project is a Telgream chatbot built using Python and implements RAG pipeline
## Architecture
- User logs in (Telegram)
- Telegram bot
- User query (/ask)
- Embedding model(MiniLM)
- FAISS vector search(replaced SQLite)
- Context+PRompt
- Ollama(Mistral LLM)
- Generates answer
## Setup:
- Install :
    - python-telegram-bot sentence-transformers faiss-cpu ollama
    - Pull the model-ollama pull mistral
- In telegram, Create a new bot from BotFather and generate a API token
## Work flow
- Import the libraries
- Create telegram commands(/start, /ask, /help)
- Load the docs  and split into smaller chunks
- Each chunk is converted into embeddings
- Embeddings are stored in FAISS index
- On query:
  - Query is embedded
  - Top-k similar chunks are retrieved
  - Context is built
  - Prompt is sent to LLM (Mistral via Ollama)
- LLM generates an answer

# You can test the bot in telegram:
- username= @Aneesha_rag_bot

## Demo vedio of the bot is uploaded

