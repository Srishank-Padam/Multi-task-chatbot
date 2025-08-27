import streamlit as st
import google.generativeai as genai
import os
import base64
import wave
import io
import streamlit.components.v1 as components
from dotenv import load_dotenv

# --- Configuration ---

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")


# --- Page Navigation ---
# Using a query parameter to handle page navigation
if 'page' not in st.query_params:
    st.query_params['page'] = 'Welcome'

page = st.query_params['page']

if page == "Welcome":
    # --- Display the custom HTML welcome page ---
    try:
        # Use components.html to embed the animated HTML page
        # The encoding is specified to prevent a UnicodeDecodeError
        with open("welcome_animated.html", "r", encoding="utf-8") as f:
            html_code = f.read()
        components.html(html_code, height=700, scrolling=True)
    except FileNotFoundError:
        st.error("Error: The 'welcome_animated.html' file was not found. Please make sure it's in the same directory as your Python script.")
        st.markdown("""
        ### Fallback Welcome Page
        Welcome to the ✨ AI Chatbot!
        This application showcases powerful NLP capabilities using the latest AI models.
        """)

elif page == "AI Chatbot":
    # Set up Streamlit page configuration for the chatbot page
    st.title("🧠 AI Chatbot")
    st.markdown("This chatbot uses the Google Gemini API for various NLP tasks like Q&A, summarization, and keyword extraction.")

    # Main content area
    st.subheader("Choose a task")
    task = st.radio(
        "Select an NLP task:",
        ("Chatbot (Multi-turn)", "Summarize Paragraph", "Extract Keywords", "Multilingual Translation", "Text-to-Speech"),
        horizontal=True
    )

    try:
        # Check if a valid API key is available before proceeding
        if not api_key:
            st.error("Please provide a valid API Key to use the application.")
        else:
            genai.configure(api_key=api_key)

            # --- Handle Different Tasks ---
            if task == "Chatbot (Multi-turn)":
                st.subheader("Start your conversation:")
                
                # Initialize chat history in session state
                if "messages" not in st.session_state:
                    st.session_state.messages = []
                
                # Display chat messages from history
                for message in st.session_state.messages:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])

                # Accept user input
                if prompt := st.chat_input("What is up?"):
                    # Add user message to chat history
                    st.session_state.messages.append({"role": "user", "content": prompt})
                    # Display user message in chat message container
                    with st.chat_message("user"):
                        st.markdown(prompt)

                    # Generate a response
                    with st.chat_message("assistant"):
                        with st.spinner("Thinking..."):
                            # Use the conversation history for the model
                            model = genai.GenerativeModel('gemini-2.0-flash')
                            try:
                                response = model.generate_content(prompt)
                                st.markdown(response.text)
                            except Exception as e:
                                st.error(f"An error occurred: {e}")
                                st.markdown("The error might be due to a quota limit. Please wait and try again.")
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": response.text})

            # The other tasks are still single-turn, so they use a text area and button
            else:
                user_input = st.text_area(f"Enter your text for '{task}':", height=200, placeholder="Type your text here...")

                if task == "Multilingual Translation":
                    languages = ["English", "Spanish", "French", "German", "Japanese", "Chinese"]
                    target_language = st.selectbox("Select Target Language", languages)

                if st.button("Generate Response"):
                    if not user_input:
                        st.error("Please enter some text.")
                    else:
                        if task == "Summarize Paragraph":
                            model = genai.GenerativeModel('gemini-2.0-flash')
                            with st.spinner("Generating summary..."):
                                prompt = f"Summarize the following text in a concise and clear manner: {user_input}"
                                response = model.generate_content(prompt)
                                st.subheader("Response:")
                                st.write(response.text)

                        elif task == "Extract Keywords":
                            model = genai.GenerativeModel('gemini-2.0-flash')
                            with st.spinner("Extracting keywords..."):
                                prompt = f"Extract the most relevant keywords from the following text and list them, separated by commas: {user_input}"
                                response = model.generate_content(prompt)
                                st.subheader("Response:")
                                st.write(response.text)
                        
                        elif task == "Multilingual Translation":
                            model = genai.GenerativeModel('gemini-2.0-flash')
                            with st.spinner(f"Translating to {target_language}..."):
                                prompt = f"Translate the following text to {target_language}: {user_input}"
                                response = model.generate_content(prompt)
                                st.subheader(f"Translation to {target_language}:")
                                st.write(response.text)

                        elif task == "Text-to-Speech":
                            with st.spinner("Generating audio..."):
                                model = genai.GenerativeModel(model_name="gemini-2.5-flash-preview-tts")
                                
                                response = model.generate_content(
                                    contents=[{'parts': [{'text': user_input}]}],
                                    generation_config=genai.GenerationConfig(
                                        response_modalities=["AUDIO"],
                                        speech_config={"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": "Kore"}}}
                                    )
                                )
                                
                                if response.candidates and response.candidates[0].content.parts and response.candidates[0].content.parts[0].inline_data:
                                    audio_data_b64 = response.candidates[0].content.parts[0].inline_data.data
                                    audio_data = base64.b64decode(audio_data_b64)
                                    
                                    wav_file = io.BytesIO()
                                    with wave.open(wav_file, 'wb') as wf:
                                        wf.setnchannels(1)
                                        wf.setsampwidth(2)
                                        wf.setframerate(16000)
                                        wf.writeframes(audio_data)
                                    
                                    wav_file.seek(0)
                                    st.subheader("Play Audio:")
                                    st.audio(wav_file, format="audio/wav")
                                else:
                                    st.error("Failed to generate audio. Please try again.")

    except Exception as e:
        st.error(f"An error occurred: {e}")
