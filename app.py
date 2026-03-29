import streamlit as st
from groq import Groq

# API setup
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except:
    st.error("API Key tapılmadı!")
    st.stop()

# --- GEMINI STİLİ: BÜYÜK QUTUNU SİLİB "+" QOYAN KOD ---
st.markdown("""
    <style>
    /* 1. Sual qutusunu (Chat Input) tənzimləyirik */
    [data-testid="stChatInput"] {
        padding-left: 50px !important;
    }
    
    [data-testid="stChatInput"] textarea {
        border-radius: 25px !important;
        padding-left: 45px !important;
    }

    /* 2. O böyük eybəcər qutunu (Drag and Drop) tamamilə gizlədirik */
    [data-testid="stFileUploader"] {
        position: fixed;
        bottom: 34px; /* Qutunun daxilinə tam otursun */
        left: 42px;   
        width: 35px !important;
        z-index: 99999;
    }

    /* Bütün artıq yazıları və çərçivələri silirik */
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

    /* 3. Sadəcə balaca "+" düyməsini saxlayırıq */
    [data-testid="stFileUploader"] button {
        border-radius: 50% !important;
        width: 32px !important;
        height: 32px !important;
        background-color: transparent !important;
        border: none !important;
        color: #5f6368 !important;
        font-size: 30px !important;
        font-weight: 200 !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }

    /* Düymənin içinə "+" işarəsini məcburi qoyuruq */
    [data-testid="stFileUploader"] button::after {
        content: "+" !important;
        visibility: visible !important;
    }
    
    [data-testid="stFileUploader"] button div {
        display: none !important; /* Orijinal yazını gizlət */
    }
    </style>
""", unsafe_allow_html=True)

st.title("🇦🇿 Zəka AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesajlar
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Sənin istədiyin o balaca "+" düyməsi budur:
uploaded_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'])

if uploaded_file:
    st.toast("Şəkil yükləndi!")

# Sual qutusu
if prompt := st.chat_input("Sualınızı bura yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        model = "llama-3.2-11b-vision-preview" if uploaded_file else "llama-3.3-70b-versatile"
        chat_completion = client.chat.completions.create(
            messages=[{"role": "system", "content": "Sən Zəka AI-san."}] + st.session_state.messages,
            model=model,
        )
        response = chat_completion.choices[0].message.content
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
