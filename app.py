import streamlit as st
from groq import Groq
import base64

# API açarını Secrets-dən götürürük
try:
    api_key = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.error("Xəta: GROQ_API_KEY tapılmadı!")
    st.stop()

client = Groq(api_key=api_key)

# --- GÖZƏL DİZAYN ÜÇÜN CSS ---
st.markdown("""
    <style>
    /* Fayl yükləmə düyməsini balaca "+" şəklinə salırıq */
    .stFileUploader {
        position: fixed;
        bottom: 38px;
        left: 20px;
        width: 45px !important;
        z-index: 9999;
    }
    .stFileUploader section {
        padding: 0 !important;
        border: none !important;
        background: none !important;
    }
    .stFileUploader label {
        display: none !important;
    }
    /* "Browse files" yazısını gizlədib yerinə "+" qoyuruq */
    .stFileUploader button {
        border-radius: 50% !important;
        width: 40px !important;
        height: 40px !important;
        background-color: #f0f2f6 !important;
        border: 1px solid #ccc !important;
        color: #555 !important;
        font-size: 24px !important;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .stFileUploader button::after {
        content: "+";
    }
    .stFileUploader button div {
        display: none;
    }
    
    /* Çat girişini düyməyə görə bir az sağa çəkirik */
    .stChatInputContainer {
        padding-left: 55px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🇦🇿 Zəka AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesajları göstər
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "user":
            st.text(message["content"])
        else:
            st.markdown(message["content"])

# "+" Düyməsi (Fayl yükləmə)
uploaded_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'])

if uploaded_file:
    st.sidebar.image(uploaded_file, caption="Yükləndi", width=150)

# Sual qutusu
if prompt := st.chat_input("Sualınızı bura yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.text(prompt)

    with st.chat_message("assistant"):
        try:
            # Şəkil varsa Vision modelinə keçir
            model = "llama-3.2-11b-vision-preview" if uploaded_file else "llama-3.3-70b-versatile"
            
            chat_completion = client.chat.completions.create(
                messages=[{"role": "system", "content": "Sən Zəka AI-san. Səmimi ol və Azərbaycan dilində cavab ver."}] + st.session_state.messages,
                model=model,
            )
            response = chat_completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Xəta: {e}")
