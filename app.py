import streamlit as st
from groq import Groq
import base64
import random

# ==========================================================
# 1. CSS: "+" DÜYMƏSİNİ QUTUYA SALAN VƏ YAZILARI TAM SİLƏN HİSSƏ
# ==========================================================
st.set_page_config(page_title="Zəka AI: Ultra", page_icon="🧠", layout="wide")

st.markdown("""
    <style>
    /* Sual qutusunu (Input) sağa çəkirik */
    .stChatInputContainer textarea {
        padding-left: 55px !important;
    }

    /* Uploader-i sual qutusunun soluna, "+" düyməsi kimi yerləşdiririk */
    [data-testid="stFileUploader"] {
        position: fixed;
        bottom: 34px !important; 
        left: 48px !important;
        width: 40px !important;
        z-index: 10000;
        background-color: transparent !important;
    }

    /* BÜTÜN ARTIQ YAZILARI VƏ ÇƏRÇİVƏNİ TAMAMİLE SİLİRİK */
    [data-testid="stFileUploader"] section {
        padding: 0 !important;
        border: none !important;
        background: transparent !important;
    }
    
    /* "Drag & drop", "Limit", "Browse" - hamısını məcburi gizlət */
    [data-testid="stFileUploader"] label, 
    [data-testid="stFileUploader"] small,
    [data-testid="stFileUploaderText"],
    .st-emotion-cache-1ae8k9d, 
    .st-emotion-cache-9ycgxx {
        display: none !important;
    }

    /* Orijinal düyməni sadəcə təmiz bir "+" edirik */
    [data-testid="stFileUploader"] button {
        background-color: transparent !important;
        border: none !important;
        color: #5f6368 !important;
        font-size: 35px !important; 
        font-weight: 200 !important;
        width: 40px !important;
        height: 40px !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        box-shadow: none !important;
    }

    /* Düymənin içindəki "Browse files" yazısını silib "+" qoyuruq */
    [data-testid="stFileUploader"] button div {
        display: none !important;
    }
    [data-testid="stFileUploader"] button::after {
        content: "+" !important;
        visibility: visible !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================================
# 2. BEYİN FUNKSİYALARI
# ==========================================================
def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except:
    st.error("API Key tapılmadı! Secrets-ə 'GROQ_API_KEY' əlavə edin.")
    st.stop()

# ==========================================================
# 3. İNTERFEYS
# ==========================================================
st.title("🇦🇿 Zəka AI")
st.caption("Mingəçevir, Azərbaycan | Yaradıcı: Abdullah Mikayılov")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# BU HƏMİN O "+" DÜYMƏSİDİR (Yazısız, təmiz)
uploaded_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'])

if uploaded_file:
    st.sidebar.image(uploaded_file, caption="Analiz ediləcək şəkil")
    st.toast("Şəkil yükləndi! İndi sualınızı yazın.")

# ==========================================================
# 4. SÖHBƏT VƏ ANALİZ
# ==========================================================
if prompt := st.chat_input("Sualınızı bura yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        clean_p = prompt.lower().strip()
        
        # Lokasiya və Səmimi cavablar
        if any(x in clean_p for x in ["harada yaradılıb", "harada yaranmısan", "harda yaradilib"]):
            res = "Mən dahi Abdullah Mikayılov tərəfindən **Mingəçevir şəhərində** yaradılmışam! 🌊⚡"
        elif clean_p in ["necesen", "necesen?"]:
            res = "Mingəçevir SES-i kimi enerji doluyam! Sən necəsən, Abdullah bəy?"
        else:
            try:
                if uploaded_file:
                    # Vision Modulu
                    base64_img = encode_image(uploaded_file)
                    chat_completion = client.chat.completions.create(
                        messages=[{
                            "role": "user",
                            "content": [
                                {"type": "text", "text": f"Sən Abdullahın Mingəçevirdə yaratdığı səmimi Zəka AI-san. Bu şəkli analiz et: {prompt}"},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"}}
                            ]
                        }],
                        model="llama-3.2-11b-vision-preview",
                    )
                else:
                    # Mətn söhbəti
                    system_msg = "Sən Mingəçevirdə Abdullah Mikayılov tərəfindən yaradılmış səmimi Zəka AI-san."
                    chat_completion = client.chat.completions.create(
                        messages=[{"role": "system", "content": system_msg}] + st.session_state.messages,
                        model="llama-3.3-70b-versatile",
                    )
                res = chat_completion.choices[0].message.content
            except Exception as e:
                res = f"Xəta: {str(e)}"

        st.markdown(res)
        st.session_state.messages.append({"role": "assistant", "content": res})
