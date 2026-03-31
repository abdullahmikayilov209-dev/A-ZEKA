import streamlit as st
from groq import Groq
import base64
import re

# ==========================================================
# 1. GLOBAL CORE SETUP (STABLE MODELS)
# ==========================================================
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except:
    st.error("Kritik Xəta: API açarı tapılmadı.")
    st.stop()

# Model adlarını burdan idarə edirik (Groq-un ən son stabil adları)
TEXT_MODEL = "llama-3.3-70b-versatile"
VISION_MODEL = "llama-3.2-11b-vision-preview" # Əgər bu da bağlansa, Groq panelindən yeni adı bura yazmalısan

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
    user_text = prompt.text if prompt.text else "Bu şəkildə nə var?"
    user_text_lower = user_text.lower().strip() 
    active_file = prompt.files[0] if prompt.files else None
    
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.write(user_text)

    with st.chat_message("assistant"):
        with st.status("🚀 Analiz edilir...", expanded=False) as status:
            st.write("Zəka Ultra mühərriki işə düşür...")
            status.update(label="Analiz Tamamlandı!", state="complete")

        response = ""

        # 1. Xüsusi Reaksiyalar
        if "abdullah" in user_text_lower and ("kim" in user_text_lower):
            response = "🛡️ **GİRİŞ:** Memar Abdullah Mikayılov tanındı. Sistem tam nəzarətinizdədir."
        
        # 2. Riyazi Analiz
        math_pattern = re.sub(r'[^0-9+\-*/(). ]', '', user_text)
        if not response and len(math_pattern) > 2 and any(op in user_text for op in "+-*/"):
            try:
                response = f"🎯 **NƏTİCƏ:** `{user_text}` = **{eval(math_pattern)}**"
            except: pass

        # 3. Əsas AI Modulu
        if not response:
            try:
                system_instruction = "Sən ZƏKA ULTRA-san. Yaradıcın Abdullah Mikayılovdur. İL 2026."
                
                if active_file:
                    base64_image = encode_image(active_file)
                    # DİKKAT: Əgər bu model xəta versə, deməli Groq vision dəstəyini müvəqqəti dayandırıb
                    chat_completion = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": system_instruction},
                            {"role": "user", "content": [
                                {"type": "text", "text": user_text},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                            ]}
                        ],
                        model="llama-3.2-11b-vision-preview", # Bu ən stabil variant olmalıdır
                    )
                else:
                    msgs = [{"role": "system", "content": system_instruction}] + st.session_state.messages
                    chat_completion = client.chat.completions.create(
                        messages=msgs,
                        model=TEXT_MODEL,
                        temperature=0.3,
                    )
                response = chat_completion.choices[0].message.content
            except Exception as e:
                # Əgər vision modeli işləməsə, heç olmasa mətnlə cavab ver
                response = f"⚠️ **Zəka Ultra Qeydi:** Vision modeli (şəkil analizi) hal-hazırda Groq tərəfindən yenilənir. Mətn mühərriki isə aktivdir. Xəta: {str(e)}"

        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
