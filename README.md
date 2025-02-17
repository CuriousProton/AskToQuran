# 📖 Quranic RAG Chatbot

A **Retrieval-Augmented Generation (RAG) chatbot** that answers questions based on the **Quran** using **ChromaDB** for vector search and **Groq API** for AI-generated responses.

---

## 🚀 Features
✅ **Retrieves Quranic verses** using vector search (ChromaDB)  
✅ **Expands context** to include relevant surrounding verses  
✅ **AI-powered responses** using the Groq Llama3-70B model  
✅ **Streamlit UI** for an interactive chat experience  
✅ **Memory retention** for multi-turn conversations  

---

## 📂 Project Structure
```
quran_rag_app/
│── app.py                 # Main Streamlit app
│── requirements.txt        # Dependencies
│── quran_data.csv          # Quranic verses data
│── .env                    # Environment variables (Optional)
│── README.md               # Project description
│── chroma_db/              # ChromaDB storage (if using local persistence)
```

---

## 🛠 Installation
### **1️⃣ Clone the repository**
```bash
git clone https://github.com/CuriousProton/AskToQuran/quran-rag-chatbot.git
cd quran-rag-chatbot
```

### **2️⃣ Create a virtual environment (optional, but recommended)**
```bash
python -m venv venv
source venv/bin/activate   # For Mac/Linux
venv\Scripts\activate      # For Windows
```

### **3️⃣ Install dependencies**
```bash
pip install -r requirements.txt
```

### **4️⃣ Set up environment variables**  
Create a `.env` file and add your **Groq API key**:
```
GROQ_API_KEY=your-secret-api-key
```

---

## 🚀 Running the App Locally
```bash
streamlit run app.py
```
Then, open your browser and go to **`http://localhost:8501/`**

---

## 🌍 Deploying on Streamlit Cloud
### **1️⃣ Push your code to GitHub**
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

### **2️⃣ Deploy on Streamlit**
1. Go to **[Streamlit Cloud](https://share.streamlit.io/)**
2. Click **"New App"** and select your GitHub repo
3. Set:
   - **Branch:** `main`
   - **Main file:** `app.py`
4. Add API keys under **Advanced Settings → Secrets**
5. Click **"Deploy"** 🚀

Your app will be live at:
```
https://your-username-your-app.streamlit.app
```

---

## 📌 Usage
1. Enter your **question** in the text input.
2. The app retrieves relevant **Quranic verses**.
3. AI generates a **context-aware response**.
4. Retrieved context is displayed below the response.

---

## 📜 Example Queries
❓ *What does the Quran say about patience?*  
❓ *What are the teachings on charity?*  
❓ *Tell me about the importance of prayer.*  

---

## 📧 Contact
For any issues or improvements, feel free to open an **issue** or **pull request** in the repository.

---

### ⭐ If you find this project useful, consider giving it a **star** on GitHub!

