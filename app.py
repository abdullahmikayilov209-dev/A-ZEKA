import streamlit as st
from groq import Groq

# API açarını Secrets-dən götürürük
try:
    api_key = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.error("Xəta: GROQ_API_KEY tapılmadı!")
    st.stop()

client = Groq(api_key=api_key)

# --- BÜTÜN "ARTIQLIQLARI" SİLƏN VƏ "+" QOYAN CSS ---
st.markdown("""
    <style>
    /* 1. O böyük "Drag and Drop" yazısını və çərçivəni tamamilə yox edirik */
    [data-testid="stFileUploader"] section {
        padding: 0 !important;
        border: none !important;
        background-color: transparent !important;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    /* 2. "Browse files" yazısını və digər yazıları gizlədirik */
    [data-testid="stFileUploader"] label, 
    [data-testid="stFileUploader"] small,
    [data-testid="text-ui-internal"] {
        display: none !important;
    }

    /* 3. Düyməni balaca "+" şəklinə salırıq və sual qutusunun içinə (sola) qoyuruq */
    [data-testid="stFileUploader"] {
        position: fixed;
        bottom: 34px; /* Qutunun tam mərkəzi */
        left: 55px;   /* Sol künc */
        width: 30px !important;
        z-index: 10000;
    }

    [data-testid="stFileUploader"] button {
        background-color: transparent !important;
        border: none !important;
        color: #5f6368 !important;
        font-size: 24px !important;
        font-weight: 300 !important;
        width: 30px !important;
        height: 30px !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    /* Düymənin içinə "+" yazısını məcburi qoyuruq */
    [data-testid="stFileUploader"] button::after {
        content: "+" !important;
        visibility: visible;
    }
    
    [data-testid="stFileUploader"] button div {
        display: none !important; /* Orijinal yazını gizlət */
    }

    /* 4. Sual qutusundakı yazını bir az sağa çəkirik ki, "+" ilə üst-üstə düşməsin */
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

# Bu həmin "+" düyməsidir. Artıq o böyük qutu görünməyəcək.
uploaded_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'])

if uploaded_file:
    st.toast("Şəkil yükləndi!", icon="📸")

# Sual qutusu
if prompt := st.chat_input("Sualınızı bura yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.text(prompt)

    with st.chat_message("assistant"):
        model = "llama-3.2-11b-vision-preview" if uploaded_file else "llama-3.3-70b-versatile"
        chat_completion = client.chat.completions.create(
            messages=[{"role": "system", "content": "Sən Zəka AI-san."}] + st.session_state.messages,
            model=model,
        )
        response = chat_completion.choices[0].message.content
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
