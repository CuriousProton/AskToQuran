import streamlit as st
#from dotenv import load_dotenv
import os
from groq import Groq
import sys
import chromadb
import pandas as pd

# Load environment variables
#load_dotenv()

# Load ChromaDB
CHROMA_DATA_PATH = 'Quran/'
COLLECTION_NAME = "quran_separate_verses_v3"
client_db = chromadb.PersistentClient(path=CHROMA_DATA_PATH)
collection = client_db.get_collection(COLLECTION_NAME)

# Load Quranic verses DataFrame
quran_df = pd.read_csv('Quran.csv')  # Ensure this file is correctly loaded

def get_context(query, n_results: int, n_expanded_verses=1):
    """Retrieves relevant verses and expands the context around them."""
    
    # Query the vector database
    query_results = collection.query(query_texts=query, n_results=n_results)

    # Extract matched verses and their IDs
    answers = query_results["documents"]
    verse_nos_list = query_results["ids"]

    final_context = []

    # Expand context for each verse found
    for v in verse_nos_list:
        for verse_id in v:
            try:
                # Extract numeric ID (e.g., 'id6216' → 6216)
                verse_index = int(verse_id.lstrip('id'))  

                # Ensure valid index range
                start_idx = max(0, verse_index - n_expanded_verses)
                end_idx = min(len(quran_df), verse_index + n_expanded_verses)

                # Extract expanded context safely
                expanded_context = quran_df['Ayat'].iloc[start_idx:end_idx].tolist()
                final_context.append(expanded_context)

            except (ValueError, IndexError) as e:
                print(f"Skipping verse {verse_id} due to error: {e}")

    return {"context": answers, "expanded_context": final_context}

# Initialize Groq API client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class RAGAgent:
    def __init__(self, client: Groq, system: str = "", max_history: int = 5) -> None:
        """
        Initializes the RAG agent.

        :param client: Groq API client instance.
        :param system: System message to define assistant behavior.
        :param max_history: Maximum number of historical exchanges to keep.
        """
        self.client = client
        self.system = system
        self.max_history = max_history  # Limit conversation length
        self.messages = [{"role": "system", "content": system}] if system else []

    def __call__(self, user_message: str, context: str = ""):
        """
        Handles user input while incorporating retrieved context.
        Returns both the assistant's response and the retrieved context.
        """

        # Modify system message instead of appending new ones
        system_instruction = f"""Use the following information to answer the user's question:
        
        Context: {context}
        
        Important: If the context is irrelevant, respond with "Sorry! I do not know."
        """

        if self.messages and self.messages[0]["role"] == "system":
            self.messages[0]["content"] = system_instruction  # Update system message
        else:
            self.messages.insert(0, {"role": "system", "content": system_instruction})

        # Add user message
        self.messages.append({"role": "user", "content": user_message})

        # Generate response
        result = self.execute()

        # Store assistant's response in conversation history
        self.messages.append({"role": "assistant", "content": result})

        # Trim old messages if history exceeds max limit
        self.trim_history()

        # Return both the response and the retrieved context
        return {"response": result, "context": context}

    def execute(self):
        """
        Sends chat messages to the Groq API and retrieves the response.
        """
        try:
            completion = self.client.chat.completions.create(
                model="llama3-70b-8192",
                messages=self.messages
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Error: {e}"

    def trim_history(self):
        """
        Limits the message history to prevent exceeding token limits.
        Keeps the latest 'max_history' exchanges.
        """
        system_message = self.messages[0]  # Preserve system message
        self.messages = [system_message] + self.messages[-(self.max_history * 2):]

# Ensure the agent instance persists in Streamlit
if "agent" not in st.session_state:
    st.session_state.agent = RAGAgent(client, system="You are an AI assistant that only responds based on provided knowledge.")

# Streamlit UI
st.title("📖 Quranic RAG Chatbot")

# User Input
user_input = st.text_input("Ask a question:", placeholder="What does the Quran say about patience?")

if user_input:
    # Retrieve context from ChromaDB
    context_data = get_context(user_input, n_results=3)

    # Get assistant response and context
    output = st.session_state.agent(user_input, context_data["expanded_context"])

    # Display Response
    st.subheader("🤖 Assistant's Response:")
    st.write(output["response"])

    # Display Retrieved Context
    st.subheader("📜 Retrieved Context:")
    st.write("\n".join(["\n".join(c) for c in output["context"]]))  # Format for readability
