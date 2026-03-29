import streamlit as st
from groq import Groq

# API setup
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except:
    st.error("Xəta: API Key tapılmadı! Secrets bölməsini yoxlayın.")
    st.stop()

# --- GEMINI ÜSLUBUNDA "+" DÜYMƏSİNİ QUTUNUN İÇİNƏ QOYAN CSS ---
st.markdown("""
    <style>
    /* 1. Sual qutusunun (Chat Input) daxili boşluğunu tənzimləyirik */
    .stChatInputContainer textarea {
        padding-left: 55px !important;
        border-radius: 25px !important;
    }

    /* 2. Fayl yükləmə düyməsini sual qutusunun daxilinə (sola) yerləşdiririk */
    [data-testid="stFileUploader"] {
        position: fixed;
        bottom: 34px !important; /* Ekranın aşağısından məsafə */
        left: 45px !important;   /* Sol tərəfdən məsafə */
        width: 35px !important;
        z-index: 1000000 !important;
    }

    /* 3. O böyük eybəcər qutunu və yazıları tamamilə gizlədirik */
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

    /* 4. Düyməni sadəcə balaca bir "+" simvoluna çeviririk */
    [data-testid="stFileUploader"] button {
        border-radius: 50% !important;
        width: 34px !important;
        height: 34px !important;
        background-color: transparent !important;
        border: none !important;
        color: #5f6368 !important; /* Gemini tünd boz rəngi */
        font-size: 32px !important;
        font-weight: 200 !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        box-shadow: none !important;
        cursor: pointer !important;
    }

    /* Orijinal mətni silib mütləq "+" qoyuruq */
    [data-testid="stFileUploader"] button div {
        display: none !important;
    }
    [data-testid="stFileUploader"] button::after {
        content: "+" !important;
        visibility: visible !important;
        display: block !important;
        margin-top: -4px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🇦🇿 Zəka AI")

# Mesaj yaddaşı
if "messages" not in st.session_state:
    st.session_state.messages = []

# Köhnə mesajları göstər
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Sənin axtardığın "+" düyməsi budur (CSS ilə qutunun daxilinə girir)
uploaded_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'])

if uploaded_file:
    st.toast("📸 Şəkil seçildi! İndi sualınızı yazın.")

# Sual qutusu (Chat Input)
if prompt := st.chat_input("Sualınızı bura yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        # Şəkil yüklənibsə Vision, yoxsa normal model
        model = "llama-3.2-11b-vision-preview" if uploaded_file else "llama-3.3-70b-versatile"
        
        try:
            chat_completion = client.chat.completions.create(
                messages=[{"role": "system", "content": "Sən Zəka AI-san."}] + st.session_state.messages,
                model=model,
            )
            response = chat_completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Xəta: {e}")
