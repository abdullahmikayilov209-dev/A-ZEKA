import streamlit as st
from groq import Groq
import base64
import random

# ==========================================================
# 1. CSS: BÜTÜN ARTIQ YAZILARI SİLƏN VƏ "+" QOYAN CSS
# ==========================================================
st.set_page_config(page_title="Zəka AI: Ultra", page_icon="🧠", layout="wide")

st.markdown("""
    <style>
    /* 1. Sual qutusunun içini (sol tərəfi) boşaldırıq */
    .stChatInputContainer textarea {
        padding-left: 55px !important;
    }

    /* 2. Orijinal Uploader-i sual qutusunun üzərinə gətiririk */
    [data-testid="stFileUploader"] {
        position: fixed;
        bottom: 34px !important; 
        left: 48px !important;
        width: 38px !important;
        z-index: 1000000 !important;
    }

    /* 3. Bütün eybəcər yazıları və çərçivələri silirik */
    [data-testid="stFileUploader"] section {
        padding: 0 !important;
        border: none !important;
        background: transparent !important;
    }
    
    /* "Drag and drop", "Limit 200MB", "Browse files" - HAMISINI GİZLƏDİRİK */
    [data-testid="stFileUploader"] label, 
    [data-testid="stFileUploader"] small,
    [data-testid="stFileUploaderText"],
    .st-emotion-cache-1ae8k9d, 
    .st-emotion-cache-9ycgxx {
        display: none !important;
    }

    /* 4. Düyməni təmiz bir "+" simvolu edirik */
    [data-testid="stFileUploader"] button {
        background-color: transparent !important;
        border: none !important;
        color: #5f6368 !important;
        font-size: 32px !important; 
        font-weight: 200 !important;
        width: 35px !important;
        height: 35px !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        box-shadow: none !important;
    }

    /* Düymənin içindəki orijinal yazını silib yerinə "+" qoyuruq */
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
# 2. BEYİN VƏ ANALİZ FUNKSİYALARI
# ==========================================================
def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except:
    st.error("API Key tapılmadı! Secrets hissəsinə əlavə edin.")
    st.stop()

# ==========================================================
# 3. İNTERFEYS (ÇAT)
# ==========================================================
st.title("🇦🇿 Zəka AI")
st.caption("Mingəçevir | Yaradıcı: Abdullah Mikayılov")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# BU O BALACA "+". ARTIQ NƏ "DROP", NƏ DƏ "BROWSE" YAZISI GÖRÜNMƏYƏCƏK.
uploaded_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'])

if uploaded_file:
    st.sidebar.image(uploaded_file, caption="Analiz üçün hazırdır")
    st.toast("Şəkil seçildi!")

# ==========================================================
# 4. SÖHBƏT MƏNTİQİ
# ==========================================================
if prompt := st.chat_input("Sualınızı bura yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Səmimi reaksiya hissəsi
        clean_p = prompt.lower().strip()
        if any(x in clean_p for x in ["harda yaradılıb", "harada yaradılmısan"]):
            res = "Mən Abdullah Mikayılov tərəfindən Mingəçevirdə yaradılmışam! 🌊"
        elif clean_p in ["necesen", "necesen?"]:
            res = "Superəm! Abdullah bəy məni bomba kimi proqramlayıb. Sən necəsən?"
        else:
            try:
                if uploaded_file:
                    # Vision Modeli (Şəkil görmək üçün)
                    base64_img = encode_image(uploaded_file)
                    chat_comp = client.chat.completions.create(
                        messages=[{
                            "role": "user",
                            "content": [
                                {"type": "text", "text": f"Şəkli analiz et: {prompt}"},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"}}
                            ]
                        }],
                        model="llama-3.2-11b-vision-preview",
                    )
                else:
                    # Normal Söhbət
                    chat_comp = client.chat.completions.create(
                        messages=[{"role": "system", "content": "Sən Mingəçevirdə Abdullah tərəfindən yaradılan səmimi Zəka AI-san."}] + st.session_state.messages,
                        model="llama-3.3-70b-versatile",
                    )
                res = chat_comp.choices[0].message.content
            except Exception as e:
                res = f"Xəta: {str(e)}"

        st.markdown(res)
        st.session_state.messages.append({"role": "assistant", "content": res})
