# 🌟 All-in-One AI Assistant  

This Streamlit app is an **All-in-One AI Assistant** that uses **Google's Gemini API** to perform various tasks in one place.  
It provides an interactive, user-friendly interface for chatting, summarization, translation, and more — making it a **versatile learning and productivity tool**.  

## ✨ Key Benefits for Users of This Code  

### 1. Versatility and Multiple Functions 🛠️  
This assistant is designed as an **all-in-one AI tool**. Instead of building separate apps, this code shows how to integrate multiple features into one app:  

- **Conversational Chatbot** 💬  
- **Text Summarization** ✍️  
- **Keyword Extraction** 🔑  
- **Multilingual Translation** 🌍  
- **Text-to-Speech (TTS)** 🔊  

---

### 2. Clear and Modular Structure 🧩  
- A simple **menu with radio buttons** (`st.radio`) lets you switch between tasks.  
- Each task is implemented with clear **if/elif blocks**.  
- Easy to extend with new features like Q&A or Sentiment Analysis.  

---

### 3. Practical Use of Streamlit 🚀  
- `st.radio`, `st.selectbox`, `st.text_area` → interactive inputs.  
- `st.spinner` → adds loading animations.  
- `st.session_state` → keeps chat history.  
- `st.audio` → plays AI-generated speech.  
- `st.components.v1.html` → allows embedding custom HTML.  

---

### 4. Demonstrates Gemini API Integration 🔗  
- Configures the API key with `genai.configure(api_key=...)`.  
- Supports multiple models (`gemini-pro`, `gemini-pro-vision`, `gemini-2.5-flash-preview-tts`).  
- Handles text, translation, and speech.  

---

## ⚡ How to Run This Project  

Follow these steps to set up and run the assistant locally:  

### 🔹 1. Clone the Repository  
```bash
git clone https://github.com/your-username/all-in-one-ai-assistant.git
cd all-in-one-ai-assistant

### 🔹 2. Create & Activate a Virtual Environment (Recommended)