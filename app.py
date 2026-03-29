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

# --- "+" DÜYMƏSİNİ QUTUNUN İÇİNƏ QOYAN CSS ---
st.markdown("""
    <style>
    /* Fayl yükləmə düyməsinin stilini dəyişib tam küncə qoyuruq */
    .stFileUploader {
        position: fixed;
        bottom: 31px; /* Sual qutusunun hündürlüyünə uyğun */
        left: 35px;   /* Sol tərəfdən məsafə */
        width: 40px !important;
        z-index: 10000;
        background-color: transparent !important;
    }
    .stFileUploader section {
        padding: 0 !important;
        border: none !important;
        background: none !important;
    }
    .stFileUploader label {
        display: none !important;
    }
    .stFileUploader button {
        border-radius: 50% !important;
        width: 34px !important;
        height: 34px !important;
        background-color: transparent !important;
        border: 1px solid #ddd !important;
        color: #666 !important;
        font-size: 20px !important;
        font-weight: bold;
    }
    /* Sual qutusunun daxilindəki yazını sağa çəkirik ki, düyməyə dəyməsin */
    .stChatInputContainer textarea {
        padding-left: 45px !important;
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
    # Şəkil yüklənəndə çatın üstündə kiçik bir önbaxış göstərsin
    st.info("📷 Şəkil əlavə olundu. Sualınızı yazın.")

# Sual qutusu
if prompt := st.chat_input("Sualınızı bura yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.text(prompt)

    with st.chat_message("assistant"):
        try:
            # Şəkil varsa Vision (llama-3.2-11b), yoxsa normal (70b) model
            model_to_use = "llama-3.2-11b-vision-preview" if uploaded_file else "llama-3.3-70b-versatile"
            
            chat_completion = client.chat.completions.create(
                messages=[{"role": "system", "content": "Sən Zəka AI-san. Azərbaycanlılara kömək edirsən."}] + st.session_state.messages,
                model=model_to_use,
            )
            response = chat_completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Xəta: {e}")
