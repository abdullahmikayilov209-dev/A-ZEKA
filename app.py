import streamlit as st
from groq import Groq
import base64
import re
import random

# ==========================================================
# 1. GLOBAL CORE SETUP
# ==========================================================
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except:
    st.error("Kritik Xəta: API açarı tapılmadı.")
    st.stop()

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

# Mesaj tarixçəsini göstər
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================================
# 3. INPUT VƏ MƏNTİQ
# ==========================================================
prompt = st.chat_input("Mesajınızı yazın...", accept_file=True)

if prompt:
    user_text = prompt.text
    user_text_lower = user_text.lower().strip() 
    active_file = prompt.files[0] if prompt.files else None
    
    # İstifadəçi mesajını əlavə et
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.write(user_text)

    with st.chat_message("assistant"):
        # Status panelini yalnız analiz zamanı göstəririk
        with st.status("🚀 Analiz edilir...", expanded=False) as status:
            st.write("Datanın strukturu yoxlanılır...")
            if any(k in user_text_lower for k in ["import", "def", "class"]):
                st.write("Kod aşkarlandı, Abdullahın debug protokolu aktivdir.")
            status.update(label="Analiz Tamamlandı", state="complete")

        response = ""

        # 1. Xüsusi Reaksiyalar
        if "abdullah" in user_text_lower and ("kim" in user_text_lower):
            response = "🛡️ **GİRİŞ:** Memar Abdullah Mikayılov tanındı. Sistem tam nəzarətinizdədir."
        elif user_text_lower in ["salam", "sağ ol", "merhaba"]:
            response = "Salam! Zəka Ultra xidmətinizdədir. Nə kömək edə bilərəm?"
        
        # 2. Riyazi Analiz
        math_pattern = re.sub(r'[^0-9+\-*/(). ]', '', user_text)
        if not response and len(math_pattern) > 2 and any(op in user_text for op in "+-*/"):
            try:
                res_val = eval(math_pattern)
                response = f"🎯 **NƏTİCƏ:** `{user_text}` = **{res_val}**"
            except: pass

        # 3. Əsas AI Modulu (Əgər cavab yuxarıda tapılmadısa)
        if not response:
            try:
                system_instruction = "Sən ZƏKA ULTRA-san. Yaradıcın Abdullah Mikayılovdur. İL 2026. Professional və dəqiq ol."
                
                if active_file:
                    base64_image = encode_image(active_file)
                    chat_completion = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": system_instruction},
                            {"role": "user", "content": [{"type": "text", "text": user_text}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}]}
                        ],
                        model="llama-3.2-11b-vision-preview",
                    )
                else:
                    # Tarixçəni sistem təlimatı ilə birləşdir
                    msgs = [{"role": "system", "content": system_instruction}] + st.session_state.messages
                    chat_completion = client.chat.completions.create(
                        messages=msgs,
                        model="llama-3.3-70b-versatile",
                        temperature=0.3,
                    )
                response = chat_completion.choices[0].message.content
            except Exception as e:
                response = f"⚠️ Sistem xətası: {str(e)}"

        # Cavabı ekrana yaz və yaddaşa at
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
