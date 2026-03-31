import streamlit as st
import google.generativeai as genai # Groq yerinə Gemini kitabxanası
from PIL import Image # Şəkilləri emal etmək üçün
import re

# ==========================================================
# 1. GLOBAL CORE SETUP (NEW GEMINI VISION ENGINE)
# ==========================================================
# DİQQƏT: Gemini API açarını Streamlit Secrets-ə əlavə et (GEMINI_API_KEY)
# Lokalda işləyirsənsə, .streamlit/secrets.toml faylına yaz.
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    
    # Şəkil analizi üçün ən yeni və güclü model
    vision_model = genai.GenerativeModel('gemini-1.5-flash-latest')
    # Yalnız mətn üçün model
    text_model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("Kritik Xəta: Gemini API açarı (GEMINI_API_KEY) tapılmadı.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

# ==========================================================
# 2. PREMIUM VİSUAL İNTERFEYS (2026 STANDARDI)
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
st.markdown("<p class='stCaption'>GLOBAL v6.0 | MEMAR: A. MİKAYILOV | GEMINI POWERED</p>", unsafe_allow_html=True)
st.markdown("---")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================================
# 3. INPUT VƏ MƏNTİQ (O İSTƏDİYİN + İKONASI BURDADIR)
# ==========================================================
prompt = st.chat_input("Mesajınızı yazın...", accept_file=True)

if prompt:
    user_text = prompt.text if prompt.text else "Bu şəkildə nə var?"
    active_file = prompt.files[0] if prompt.files else None
    
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.write(user_text)

    with st.chat_message("assistant"):
        with st.status("🚀 Zəka Ultra Analiz Edir...", expanded=False) as status:
            if active_file:
                st.write("🖼️ Şəkil emal olunur (Gemini Vision)...")
            st.write("🧠 Neyron şəbəkə aktivləşdirilir...")
            status.update(label="Analiz Tamamlandı!", state="complete")

        response = ""
        user_text_lower = user_text.lower().strip()

        # 1. MEMAR TANINMA SİSTEMİ
        if "abdullah" in user_text_lower and ("kim" in user_text_lower):
            response = "🛡️ **GİRİŞ:** Memar Abdullah Mikayılov tanındı. Zəka Ultra tam əmrinizdədir."
        
        # 2. RİYAZİ ANALİZ SİSTEMİ
        math_pattern = re.sub(r'[^0-9+\-*/(). ]', '', user_text)
        if not response and len(math_pattern) > 2 and any(op in user_text for op in "+-*/"):
            try:
                response = f"🎯 **RİYAZİ NƏTİCƏ:** `{user_text}` = **{eval(math_pattern)}**"
            except: pass

        # 3. ƏSAS GEMINI AI CORE (HƏLL YOLU)
        if not response:
            try:
                # Sistem təlimatı
                system_instruction = (
                    "Sən ZƏKA ULTRA-san. Yaradıcın Abdullah Mikayılovdur. İL 2026. "
                    "Soyuqqanlı, dəqiq və professional ol. Şəkilləri və mətnləri "
                    "vəhşi bir sürətlə analiz edirsən."
                )
                
                if active_file:
                    # GEMINI VISION REQUEST (HEÇ VAXT ÇÖKMÜR)
                    img = Image.open(active_file)
                    # Təlimatı və sualı bir yerdə göndəririk
                    chat_completion = vision_model.generate_content([system_instruction, user_text, img])
                else:
                    # GEMINI TEXT REQUEST
                    # Tarixçəni sistem təlimatı ilə birləşdir
                    msgs = [{"role": "user", "content": system_instruction}] + st.session_state.messages
                    # Sadələşdirilmiş text request (generate_content daha stabil işləyir)
                    chat_completion = text_model.generate_content(msgs)
                
                response = chat_completion.text
            except Exception as e:
                response = f"⚠️ **Sistem Xətası:** Zəka Ultra serverlə bağlana bilmədi. Detal: {str(e)}"

        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
