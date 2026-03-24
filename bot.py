from telegram.ext import ApplicationBuilder, CommandHandler
import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import faiss
import ollama

# Load a model
model=SentenceTransformer('all-MiniLM-L6-v2')

#load token
load_dotenv()
TOKEN= os.getenv("TELEGRAM_BOT_TOKEN")

# Load  and chunk docs
def load_documents():
    chunks=[]
    for file in os.listdir("data"):
        with open(f"data/{file}", "r", encoding="utf-8") as f:
            text=f.read()

            #splitting into chunks
            parts=text.split("\n")

            for part in parts:
                if part.strip():
                    chunks.append(part)
    return chunks

# convert the docs into emebdddings
def create_embeddings(docs):
    embeddings=model.encode(docs)
    return embeddings

# Store in a vector data base-faiss index
def create_index(embeddings):
    dimension = len(embeddings[0])
    index=faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index

# Search function(embedds the query and searches fo similar chunks)
def search(query,docs,index):
    query_embedding=model.encode([query])
    D,I =index.search(query_embedding, k=2)
    if D[0][0] > 1.0:
        return ["Kindly, ask relevant questions"]
    results=[docs[i] for i in I[0]]
    return results

# Create response generater using ollama
def generate_answer(query,context_chunks):
    context="\n".join(context_chunks)

    prompt= f"""
    Answer the question based on the context below.PermissionErrorContext:
    {context}

    Question:
    {query}

    Give a short and clear answer """
    response =ollama.chat(
        model='phi3',
        messages=[{"role":"user","content":prompt}]
    )
    return response ['message']['content']

# Telegram commands
# Start command
async def start(update,context):
    await update.message.reply_text("Hi,I am Aneesha's Bot")

# Ask command
async def ask(update,context):
    query= " ".join(context.args)

    if not query:
        await update.message.reply_text("Please type after /ask")
        return
    
    results=search(query,documents,index)
    answer = generate_answer(query,results)
    if not results:
        await update.message.reply_text("No results")
        return
    
    response="\n\n".join(results[ :2])
    await update.message.reply_text(answer)   

# Help command
async def help(update,context):
    await update.message.reply_text("Commands:\n"
                                    "/ask <question> - Ask something\n"
                                    "/help - Show this message")

#Creating bot
def main():
    global documents, index

    print("Loading docs....")
    documents= load_documents()

    print("Creating embeddings....")
    emeddings=create_embeddings(documents)

    print("Building index....")
    index= create_index(emeddings)


    app=ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start",start))
    app.add_handler(CommandHandler("ask",ask))
    app.add_handler(CommandHandler("help",help))
    

    print("Bot is running")
    app.run_polling()

# Run
if __name__=="__main__":
    main()


