import streamlit as st
from groq import Groq

# API setup
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except:
    st.error("API Key tapılmadı!")
    st.stop()

# --- GEMINI ÜSLUBU: BÖYÜK QUTUNU SİLİB "+" QOYAN CSS ---
st.markdown("""
    <style>
    /* 1. Sual qutusunu (Chat Input) tənzimləyirik */
    [data-testid="stChatInput"] {
        padding-left: 50px !important;
    }
    
    [data-testid="stChatInput"] textarea {
        border-radius: 25px !important;
        padding-left: 45px !important;
        background-color: #ffffff !important;
    }

    /* 2. O böyük 'Drag and Drop' qutusunu tamamilə 'öldürürük' */
    [data-testid="stFileUploader"] {
        position: fixed;
        bottom: 34px; /* Qutunun hündürlüyünə tam uyğun */
        left: 42px;   /* Sol tərəfə yapışdır */
        width: 35px !important;
        z-index: 99999;
        padding: 0 !important;
    }

    /* Bütün çərçivələri və yazıları gizlət */
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

    /* 3. 'Browse files' düyməsini balaca '+' edirik */
    [data-testid="stFileUploader"] button {
        border-radius: 50% !important;
        width: 32px !important;
        height: 32px !important;
        background-color: transparent !important;
        border: none !important;
        color: #5f6368 !important; /* Gemini rəngi */
        font-size: 30px !important;
        font-weight: 200 !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        box-shadow: none !important;
        margin: 0 !important;
    }

    /* Düymənin içinə məcburi '+' qoyuruq */
    [data-testid="stFileUploader"] button::after {
        content: "+" !important;
        visibility: visible;
        position: absolute;
    }
    
    /* Orijinal yazını gizlət */
    [data-testid="stFileUploader"] button div {
        display: none !important;
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

# BU O BALACA "+" DÜYMƏSİDİR
uploaded_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'])

if uploaded_file:
    st.sidebar.image(uploaded_file, caption="Yüklənən şəkil", width=100)
    st.toast("Şəkil hazırdır!")

# Sual qutusu
if prompt := st.chat_input("Sualınızı bura yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.text(prompt)

    with st.chat_message("assistant"):
        # Şəkil varsa Vision modeli, yoxsa normal
        model = "llama-3.2-11b-vision-preview" if uploaded_file else "llama-3.3-70b-versatile"
        
        chat_completion = client.chat.completions.create(
            messages=[{"role": "system", "content": "Sən səmimi Zəka AI-san."}] + st.session_state.messages,
            model=model,
        )
        response = chat_completion.choices[0].message.content
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
