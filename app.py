import streamlit as st
from groq import Groq

# API açarını Secrets-dən götürürük
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except:
    st.error("Xəta: GROQ_API_KEY tapılmadı!")
    st.stop()

# --- ƏN SON VƏ DƏQİQ CSS (GEMINI ÜSLUBU) ---
st.markdown("""
    <style>
    /* 1. Sual qutusunu tənzimləyirik */
    .stChatInputContainer {
        padding-left: 40px !important;
    }
    .stChatInputContainer textarea {
        padding-left: 45px !important;
        border-radius: 25px !important;
    }

    /* 2. O böyük eybəcər qutunu (Uploader) tamamilə gizlədirik */
    [data-testid="stFileUploader"] {
        position: fixed;
        bottom: 34px !important;
        left: 45px !important;
        width: 35px !important;
        z-index: 100000;
    }
    
    /* Qutunun daxilindəki bütün yazıları və çərçivələri silirik */
    [data-testid="stFileUploader"] section {
        padding: 0 !important;
        border: none !important;
        background: transparent !important;
    }
    [data-testid="stFileUploader"] label, 
    [data-testid="stFileUploader"] small,
    [data-testid="stFileUploaderText"] {
        display: none !important;
    }

    /* 3. Sadəcə balaca "+" düyməsini düzəldirik */
    [data-testid="stFileUploader"] button {
        border-radius: 50% !important;
        width: 30px !important;
        height: 30px !important;
        background-color: transparent !important;
        border: none !important;
        color: #5f6368 !important;
        font-size: 30px !important;
        font-weight: 200 !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }

    /* Düymənin içinə məcburi "+" qoyuruq */
    [data-testid="stFileUploader"] button div {
        display: none !important;
    }
    [data-testid="stFileUploader"] button::after {
        content: "+" !important;
        visibility: visible !important;
        display: block !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🇦🇿 Zəka AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesajları göstər
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Sənin istədiyin o balaca "+" düyməsi
uploaded_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'])

if uploaded_file:
    st.toast("Şəkil yükləndi!")

# Sual qutusu
if prompt := st.chat_input("Sualınızı bura yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        # Şəkil varsa Vision modeli, yoxsa normal model
        model = "llama-3.2-11b-vision-preview" if uploaded_file else "llama-3.3-70b-versatile"
        chat_completion = client.chat.completions.create(
            messages=[{"role": "system", "content": "Sən Zəka AI-san."}] + st.session_state.messages,
            model=model,
        )
        response = chat_completion.choices[0].message.content
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
