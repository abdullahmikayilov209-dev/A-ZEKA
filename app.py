import streamlit as st
from groq import Groq
import base64
import re

# ==========================================================
# 1. GLOBAL CORE SETUP (2026 STABLE)
# ==========================================================
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except:
    st.error("Kritik Xəta: API açarı (GROQ_API_KEY) Streamlit Secrets-də tapılmadı.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

# ==========================================================
# 2. PREMIUM VİSUAL İNTERFEYS
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
    h1 { text-align: center; color: #1a1a1a; font-weight: 900; letter-spacing: -1px; }
    .stCaption { text-align: center; color: #94a3b8; font-weight: 600; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>ZƏKA ULTRA</h1>", unsafe_allow_html=True)
st.markdown("<p class='stCaption'>GLOBAL v6.0 | MEMAR: A. MİKAYILOV | 2026 VISION ENABLED</p>", unsafe_allow_html=True)
st.markdown("---")

# Mesaj tarixçəsini göstər
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================================
# 3. MƏNTİQ VƏ VISION MODULU
# ==========================================================
prompt = st.chat_input("Mesajınızı yazın və ya şəkil əlavə edin...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Bu şəkli analiz et."
    user_text_lower = user_text.lower().strip() 
    active_file = prompt.files[0] if prompt.files else None
    
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.write(user_text)

    with st.chat_message("assistant"):
        with st.status("🚀 Zəka Ultra Analiz Edir...", expanded=False) as status:
            if active_file:
                st.write("🖼️ Şəkil emal olunur (Base64)...")
            st.write("🧠 Neyron şəbəkə aktivləşdirilir...")
            status.update(label="Analiz Tamamlandı!", state="complete")

        response = ""

        # 1. MEMAR TANINMA SİSTEMİ
        if "abdullah" in user_text_lower and ("kim" in user_text_lower):
            response = "🛡️ **GİRİŞ TƏSDİQLƏNDİ:** Memar Abdullah Mikayılov. Sistem tam gücü ilə xidmətinizdədir."
        
        # 2. RİYAZİ ANALİZ SİSTEMİ
        math_pattern = re.sub(r'[^0-9+\-*/(). ]', '', user_text)
        if not response and len(math_pattern) > 2 and any(op in user_text for op in "+-*/"):
            try:
                response = f"🎯 **NƏTİCƏ:** `{user_text}` = **{eval(math_pattern)}**"
            except: pass

        # 3. ƏSAS AI CORE (VISION & TEXT)
        if not response:
            try:
                system_instruction = "Sən ZƏKA ULTRA-san. Yaradıcın Abdullah Mikayılovdur. İL 2026. Dünyanın ən sürətli və ağıllı sistemisən."
                
                if active_file:
                    # YENİLƏNMİŞ MODEL: llama-3.2-90b-vision-preview
                    base64_image = encode_image(active_file)
                    chat_completion = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": system_instruction},
                            {"role": "user", "content": [
                                {"type": "text", "text": user_text},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                            ]}
                        ],
                        model="llama-3.2-90b-vision-preview", # Ən yeni vision modeli
                        temperature=0.2
                    )
                else:
                    msgs = [{"role": "system", "content": system_instruction}] + st.session_state.messages
                    chat_completion = client.chat.completions.create(
                        messages=msgs,
                        model="llama-3.3-70b-versatile",
                        temperature=0.3,
                    )
                response = chat_completion.choices[0].message.content
            except Exception as e:
                response = f"⚠️ **Sistem Xətası:** {str(e)}"

        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
