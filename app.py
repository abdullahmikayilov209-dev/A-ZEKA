import streamlit as st
from groq import Groq
import base64

# ==========================================================
# 1. API SETUP
# ==========================================
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except:
    st.error("API Key tapılmadı!")
    st.stop()

# Şəkli modelin başa düşəcəyi formata salan funksiya
def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

# ==========================================================
# 2. BÜTÜN ARTIQ YAZILARI SİLƏN VƏ "+" QOYAN CSS
# ==========================================================
st.markdown("""
    <style>
    .stChatInputContainer textarea { padding-left: 50px !important; }

    [data-testid="stFileUploader"] {
        position: fixed;
        bottom: 33px !important; 
        left: 45px !important;
        width: 35px !important;
        z-index: 1000000 !important;
    }

    [data-testid="stFileUploader"] section {
        padding: 0 !important;
        border: none !important;
        background: transparent !important;
    }
    
    [data-testid="stFileUploader"] label, 
    [data-testid="stFileUploader"] small,
    [data-testid="stFileUploaderText"],
    .st-emotion-cache-1ae8k9d, 
    .st-emotion-cache-9ycgxx {
        display: none !important;
    }

    [data-testid="stFileUploader"] button {
        background-color: transparent !important;
        border: none !important;
        color: #5f6368 !important;
        font-size: 35px !important; 
        font-weight: 200 !important;
        width: 32px !important;
        height: 32px !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        box-shadow: none !important;
    }

    [data-testid="stFileUploader"] button div { display: none !important; }
    [data-testid="stFileUploader"] button::after {
        content: "+" !important;
        visibility: visible !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================================
# 3. İNTERFEYS
# ==========================================================
st.title("🇦🇿 Zəka AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# BALACA "+" DÜYMƏSİ (Köhnə yerində qalır)
uploaded_file = st.file_uploader

if uploaded_file:
    st.toast("Şəkil seçildi!")

# ==========================================================
# 4. SÖHBƏT VƏ ANALİZ (SƏN İSTƏDİYİN DƏYİŞİKLİK)
# ==========================================================
# Bura sənin istədiyin 'accept_file=True' əlavə edildi
prompt = st.chat_input("Dahi alimə sual ver və ya '+' vurub şəkil at...", accept_file=True)

if prompt:
    user_text = prompt.text
    # Həm fiteden (uploader), həm də chat_inputdan gələn faylı yoxlayırıq
    active_file = uploaded_file if uploaded_file else (prompt.files[0] if prompt.files else None)
    
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.write(user_text)

    with st.chat_message("assistant"):
        try:
            if active_file:
                # EGER SEKIL VARSA - VISION MODELI ISLEYIR
                base64_image = encode_image(active_file)
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": user_text},
                                {
                                    "type": "image_url",
                                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                                },
                            ],
                        }
                    ],
                    model="llama-3.2-11b-vision-preview",
                )
            else:
                # EGER SEKIL YOXDURSA - NORMAL SOHBET MODELI
                chat_completion = client.chat.completions.create(
                    messages=[{"role": "system", "content": "Sən Mingəçevirdə Abdullah tərəfindən yaradılan Zəka AI-san."}] + st.session_state.messages,
                    model="llama-3.3-70b-versatile",
                )
            
            response = chat_completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        
        except Exception as e:
            st.error(f"Xəta baş verdi: {str(e)}")
