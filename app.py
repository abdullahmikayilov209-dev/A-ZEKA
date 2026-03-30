import streamlit as st
from groq import Groq
import base64

# ==========================================================
# 1. CSS: ŞƏKİLDƏKİ KİMİ TƏMİZ "+" DÜYMƏSİ (YAZISIZ)
# ==========================================================
st.set_page_config(page_title="Zəka AI", page_icon="🧠", layout="wide")

st.markdown("""
    <style>
    /* Sual qutusunu tənzimləyirik */
    .stChatInputContainer textarea {
        padding-left: 50px !important;
    }

    /* Uploader-i tamamilə "yox" edirik, amma funksiyası qalır */
    [data-testid="stFileUploader"] {
        position: fixed;
        bottom: 34px !important; 
        left: 48px !important;
        width: 35px !important;
        z-index: 10000;
    }

    /* Bütün o "Drag and Drop", "Browse", "200MB" yazılarını silirik */
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

    /* Orijinal düyməni sadəcə balaca bir "+" simvoluna çeviririk */
    [data-testid="stFileUploader"] button {
        background-color: transparent !important;
        border: none !important;
        color: #5f6368 !important;
        font-size: 32px !important; 
        width: 35px !important;
        height: 35px !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        box-shadow: none !important;
    }

    /* Düymənin içindəki yazını silib yerinə təmiz "+" qoyuruq */
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
# 2. BEYİN (API VƏ ANALİZ)
# ==========================================================
def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except:
    st.error("API Key tapılmadı!")
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

# BU O "+" DÜYMƏSİDİR (Heç bir yazı görünmür)
uploaded_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'])

if uploaded_file:
    st.sidebar.image(uploaded_file, caption="Analiz üçün şəkil seçildi")

# ==========================================================
# 4. SÖHBƏT VƏ VISION MƏNTİQİ
# ==========================================================
if prompt := st.chat_input("Sualınızı yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Səmimi reaksiya
        clean_p = prompt.lower().strip()
        if any(x in clean_p for x in ["harada yaradılıb", "harada yaranmısan"]):
            res = "Mən dahi Abdullah Mikayılov tərəfindən **Mingəçevirdə** yaradılmışam! 🌊"
        else:
            try:
                if uploaded_file:
                    base64_img = encode_image(uploaded_file)
                    chat_comp = client.chat.completions.create(
                        messages=[{
                            "role": "user",
                            "content": [
                                {"type": "text", "text": f"Mən Abdullahın yaratdığı Zəka AI-yam. Analiz et: {prompt}"},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"}}
                            ]
                        }],
                        model="llama-3.2-11b-vision-preview",
                    )
                else:
                    chat_comp = client.chat.completions.create(
                        messages=[{"role": "system", "content": "Sən Mingəçevirdə Abdullah tərəfindən yaradılan səmimi Zəka AI-san."}] + st.session_state.messages,
                        model="llama-3.3-70b-versatile",
                    )
                res = chat_comp.choices[0].message.content
            except Exception as e:
                res = f"Xəta: {str(e)}"

        st.markdown(res)
        st.session_state.messages.append({"role": "assistant", "content": res})
