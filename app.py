import streamlit as st
from groq import Groq

# API açarını Secrets-dən götürürük
try:
    api_key = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.error("Xəta: GROQ_API_KEY tapılmadı!")
    st.stop()

client = Groq(api_key=api_key)

# --- "+" DÜYMƏSİNİ QUTUNUN İÇİNƏ MƏCBURİ YERLƏŞDİRƏN CSS ---
st.markdown("""
    <style>
    /* 1. Fayl yükləmə qutusunu tamamilə kiçik bir "+" düyməsinə çeviririk */
    .stFileUploader {
        position: fixed;
        bottom: 35px !important; /* Çat qutusunun hündürlüyünə tam uyğun */
        left: 45px !important;   /* Sola yapışdırırıq */
        width: 40px !important;
        z-index: 1000000 !important;
    }
    
    /* Düymənin daxili elementlərini gizlədirik */
    .stFileUploader section {
        padding: 0 !important;
        border: none !important;
        background-color: transparent !important;
    }
    
    .stFileUploader label {
        display: none !important;
    }

    /* "Browse files" düyməsini dairəvi "+" düyməsi edirik */
    .stFileUploader button {
        border-radius: 50% !important;
        width: 35px !important;
        height: 35px !important;
        background-color: #f0f2f6 !important; /* Gemini-dəki kimi açıq boz */
        border: 1px solid #d1d1d1 !important;
        color: #333 !important;
        font-size: 22px !important;
        font-weight: 300 !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
    }

    /* Düymənin içindəki orijinal yazını silib "+" yazırıq */
    .stFileUploader button div {
        display: none !important;
    }
    .stFileUploader button::before {
        content: "+" !important;
    }

    /* 2. Sual qutusunu (Input) düyməyə görə tənzimləyirik */
    .stChatInputContainer {
        padding-left: 60px !important; /* Yazı düymənin altından başlamasın */
    }
    
    .stChatInputContainer textarea {
        background-color: #ffffff !important;
        border-radius: 25px !important;
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
    # Şəkil yüklənəndə çat ekranında kiçik bildiriş
    st.toast("📷 Şəkil əlavə edildi!", icon="✅")

# Sual qutusu
if prompt := st.chat_input("Sualınızı bura yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.text(prompt)

    with st.chat_message("assistant"):
        try:
            # Model seçimi
            model = "llama-3.2-11b-vision-preview" if uploaded_file else "llama-3.3-70b-versatile"
            
            chat_completion = client.chat.completions.create(
                messages=[{"role": "system", "content": "Sən səmimi Zəka AI-san."}] + st.session_state.messages,
                model=model,
            )
            response = chat_completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Xəta: {e}")
