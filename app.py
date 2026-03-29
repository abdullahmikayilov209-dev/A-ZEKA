import streamlit as st
from groq import Groq

# API setup
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except:
    st.error("API Key tapılmadı!")
    st.stop()

# --- GEMINI ÜSLUBU: "+" DÜYMƏSİNİ YAZI QUTUSUNUN İÇİNƏ SOXAN CSS ---
st.markdown("""
    <style>
    /* 1. Sual yazdığın ağ qutunu sola tərəf boşaldırıq */
    .stChatInputContainer textarea {
        padding-left: 50px !important;
        border-radius: 25px !important;
    }

    /* 2. O böyük eybəcər qutunu (File Uploader) tamamilə görünməz edib qutunun daxilinə qoyuruq */
    div[data-testid="stFileUploader"] {
        position: fixed;
        bottom: 34px !important; /* Yazı qutusunun tam mərkəzi */
        left: 42px !important;   /* Tam sol daxili künc */
        width: 35px !important;
        z-index: 1000000 !important;
    }

    /* 3. Bütün lazımsız yazıları (Drag and drop, Browse və s.) 100% silirik */
    div[data-testid="stFileUploader"] section {
        padding: 0 !important;
        border: none !important;
        background: transparent !important;
    }
    
    div[data-testid="stFileUploader"] label, 
    div[data-testid="stFileUploader"] small,
    div[data-testid="stFileUploaderText"] {
        display: none !important;
    }

    /* 4. Düyməni sadəcə bir "+" simvolu kimi göstəririk */
    div[data-testid="stFileUploader"] button {
        border-radius: 50% !important;
        width: 32px !important;
        height: 32px !important;
        background-color: transparent !important;
        border: none !important;
        color: #5f6368 !important; /* Gemini tünd boz rəngi */
        font-size: 32px !important;
        font-weight: 200 !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        box-shadow: none !important;
    }

    /* Orijinal mətni "+" ilə əvəz edirik */
    div[data-testid="stFileUploader"] button div {
        display: none !important;
    }
    div[data-testid="stFileUploader"] button::after {
        content: "+" !important;
        visibility: visible !important;
        display: block !important;
        margin-top: -4px;
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

# BU O BALACA "+" DÜYMƏSİDİR (Həmin o sual qutusunun daxilinə gedəcək)
uploaded_file = st.file_uploader("", type=['+,'])

if uploaded_file:
    st.toast("📸 Şəkil seçildi!")

# Sual qutusu (Chat Input)
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
