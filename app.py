import streamlit as st
from groq import Groq
import base64

# API tənzimləmələri
try:
    api_key = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.error("API Key tapılmadı!")
    st.stop()

client = Groq(api_key=api_key)

# --- CSS HİYLƏSİ (Düyməni qutunun yanına qoymaq üçün) ---
st.markdown("""
    <style>
    /* Fayl yükləmə qutusunu kiçik bir düymə kimi göstəririk */
    .stFileUploader {
        min-width: 0px !important;
        width: 45px !important;
        position: fixed;
        bottom: 42px;
        left: 10%; /* Ekranın ölçüsünə görə tənzimlənir */
        z-index: 1000;
    }
    .stFileUploader section {
        padding: 0 !important;
        border: none !important;
    }
    .stFileUploader label {
        display: none !important;
    }
    /* Çat qutusunun özü */
    .stChatInputContainer {
        padding-left: 50px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🇦🇿 Zəka AI")

# Yaddaş
if "messages" not in st.session_state:
    st.session_state.messages = []

# Fayl yükləmə (O həmin "+" düyməsi rolunda)
uploaded_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'], key="plus_button")

if uploaded_file:
    st.sidebar.image(uploaded_file, caption="Yüklənən şəkil", width=150)
    st.sidebar.success("Şəkil hazırdır!")

# Mesajlar
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "user":
            st.text(message["content"])
        else:
            st.markdown(message["content"])

# Sual qutusu
if prompt := st.chat_input("Sualınızı bura yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.text(prompt)

    with st.chat_message("assistant"):
        try:
            # Əgər şəkil varsa Vision modelini işlədirik
            model = "llama-3.2-11b-vision-preview" if uploaded_file else "llama-3.3-70b-versatile"
            
            chat_completion = client.chat.completions.create(
                messages=[{"role": "system", "content": "Sən Zəka AI-san. Azərbaycan dilində cavab ver."}] + st.session_state.messages,
                model=model,
            )
            response = chat_completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Xəta: {e}")
