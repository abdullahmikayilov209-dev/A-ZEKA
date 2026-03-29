import streamlit as st
from groq import Groq

# API setup
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except:
    st.error("API Key tapılmadı!")
    st.stop()

# --- BÜTÜN ARTIQ YAZILARI SİLƏN VƏ "+" QOYAN CSS ---
st.markdown("""
    <style>
    /* 1. Sual qutusunun içini (sol tərəfi) boşaldırıq */
    .stChatInputContainer textarea {
        padding-left: 50px !important;
    }

    /* 2. O böyük eybəcər qutunu (Uploader) tamamilə görünməz edirik */
    [data-testid="stFileUploader"] {
        position: fixed;
        bottom: 33px !important; 
        left: 45px !important;
        width: 35px !important;
        z-index: 1000000 !important;
    }

    /* 3. "Drag and drop", "Browse files", "Limit 200MB" - bunların HAMISINI silirik */
    [data-testid="stFileUploader"] section {
        padding: 0 !important;
        border: none !important;
        background: transparent !important;
    }
    
    /* Bütün yazıları məcburi gizlət */
    [data-testid="stFileUploader"] label, 
    [data-testid="stFileUploader"] small,
    [data-testid="stFileUploaderText"],
    .st-emotion-cache-1ae8k9d, 
    .st-emotion-cache-9ycgxx {
        display: none !important;
    }

    /* 4. Orijinal düyməni sadəcə balaca bir "+" simvolu edirik */
    [data-testid="stFileUploader"] button {
        background-color: transparent !important;
        border: none !important;
        color: #5f6368 !important;
        font-size: 35px !important; /* Artı işarəsinin ölçüsü */
        font-weight: 200 !important;
        width: 32px !important;
        height: 32px !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        box-shadow: none !important;
    }

    /* "Browse files" yazısını silib yerinə "+" yazırıq */
    [data-testid="stFileUploader"] button div {
        display: none !important;
    }
    [data-testid="stFileUploader"] button::after {
        content: "+" !important;
        visibility: visible !important;
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

# BU O BALACA "+". ARTIQ NƏ "DROP", NƏ DƏ "BROWSE" YAZISI GÖRÜNMƏYƏCƏK.
uploaded_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'])

if uploaded_file:
    st.toast("Şəkil seçildi!")

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
