import streamlit as st
from groq import Groq
import base64
import re

# ==========================================================
# 1. GLOBAL CORE SETUP (NEW 2026 STABLE MODELS)
# ==========================================================
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except:
    st.error("Kritik Xəta: API açarı tapılmadı.")
    st.stop()

# DİQQƏT: Groq-un ən son stabil vision modeli budur:
# Əgər yenə xəta versə, bura 'llama-3.2-90b-vision-preview' yazaraq yoxla.
VISION_MODEL_NAME = "llama-3.2-11b-vision-preview" 
TEXT_MODEL_NAME = "llama-3.3-70b-versatile"

if "messages" not in st.session_state:
    st.session_state.messages = []

def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

# ==========================================================
# 2. VİSUAL İNTERFEYS
# ==========================================================
st.set_page_config(page_title="ZƏKA ULTRA v6.0", layout="wide")

st.markdown("""
    <style>
    .stApp { background: #ffffff; color: #0f172a; }
    .stChatMessage {
        background-color: #ffffff !important;
        border-radius: 15px !important;
        border: 1px solid #f1f5f9 !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
    }
    h1 { text-align: center; color: #1a1a1a; font-weight: 900; }
    .stCaption { text-align: center; color: #94a3b8; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>ZƏKA ULTRA</h1>", unsafe_allow_html=True)
st.markdown("<p class='stCaption'>GLOBAL v6.0 | MEMAR: A. MİKAYILOV</p>", unsafe_allow_html=True)
st.markdown("---")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================================
# 3. INPUT VƏ MƏNTİQ
# ==========================================================
prompt = st.chat_input("Mesajınızı yazın...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Bu şəkli analiz et."
    active_file = prompt.files[0] if prompt.files else None
    
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.write(user_text)

    with st.chat_message("assistant"):
        with st.status("🚀 Zəka Ultra Analiz Edir...", expanded=False) as status:
            st.write("Mühərrik işə düşdü...")
            status.update(label="Analiz Tamamlandı!", state="complete")

        response = ""
        user_text_lower = user_text.lower().strip()

        # Xüsusi Reaksiyalar (Riyaziyyat və Memar Tanınması)
        if "abdullah" in user_text_lower:
            response = "🛡️ **SİSTEM MESAJI:** Memar Abdullah Mikayılov tanındı. Xoş gəldiniz."
        
        math_pattern = re.sub(r'[^0-9+\-*/(). ]', '', user_text)
        if not response and len(math_pattern) > 2 and any(op in user_text for op in "+-*/"):
            try:
                response = f"🎯 **RİYAZİ NƏTİCƏ:** `{user_text}` = **{eval(math_pattern)}**"
            except: pass

        # Əsas AI Modulu
        if not response:
            try:
                system_instruction = "Sən ZƏKA ULTRA-san. Yaradıcın Abdullah Mikayılovdur. İL 2026."
                
                if active_file:
                    base64_image = encode_image(active_file)
                    # VISION REQUEST
                    chat_completion = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": system_instruction},
                            {"role": "user", "content": [
                                {"type": "text", "text": user_text},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                            ]}
                        ],
                        model=VISION_MODEL_NAME,
                    )
                else:
                    # TEXT ONLY REQUEST
                    msgs = [{"role": "system", "content": system_instruction}] + st.session_state.messages
                    chat_completion = client.chat.completions.create(
                        messages=msgs,
                        model=TEXT_MODEL_NAME,
                    )
                response = chat_completion.choices[0].message.content
            except Exception as e:
                response = f"⚠️ **Sistem Xətası:** Groq hazırda Vision modelini yeniləyir. Zəhmət olmasa 5 dəqiqə sonra yenidən yoxlayın. (Xəta kodu: {str(e)})"

        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
