import streamlit as st
from groq import Groq
import base64
from datetime import datetime
import re
import random

# ==========================================================
# 1. NÜVƏ QURĞUSU (API SETUP)
# ==========================================================
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except:
    st.error("SİSTEM XƏTASI: API Key tapılmadı! Abdullah Mikayılovun mühəndislik açarı daxil edilməlidir.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

# ==========================================================
# 2. ULTRA-TƏMİZ VƏ PROFESSIONAL AĞ DİZAYN
# ==========================================================
st.set_page_config(page_title="ZƏKA AI | ABDULLAH MİKAYILOV", layout="wide")

st.markdown("""
    <style>
    .stApp { background: #ffffff; color: #1e293b; }
    .stChatMessage {
        background-color: #f8fafc !important;
        border-radius: 15px !important;
        border: 1px solid #e2e8f0 !important;
        padding: 15px !important;
        margin-bottom: 12px;
    }
    h1 { text-align: center; font-family: 'Inter', sans-serif; font-weight: 800; color: #0f172a; }
    .stCaption { text-align: center; color: #64748b; letter-spacing: 2px; }
    </style>
""", unsafe_allow_html=True)

# ==========================================================
# 3. İNTERFEYSİN QURULMASI
# ==========================================================
st.markdown("<h1>ZƏKA AI</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='stCaption'>MEMAR: ABDULLAH MİKAYILOV | STATUS: AKTİV {datetime.now().year}</p>", unsafe_allow_html=True)
st.markdown("---")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================================
# 4. "ZƏKA" UNİKAL MƏNTİQİ
# ==========================================================
prompt = st.chat_input("Zəka ilə ünsiyyət qur...", accept_file=True)

if prompt:
    user_text = prompt.text
    user_text_lower = user_text.lower().strip() 
    active_file = prompt.files[0] if prompt.files else None
    
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.write(user_text)

    with st.chat_message("assistant"):
        with st.spinner("Zəka düşünür..."):
            response = ""

            # --- UNİKAL FUNKSİYA: YARADICI TANIMA SİSTEMİ ---
            if "abdullah" in user_text_lower and ("men" in user_text_lower or "tanis" in user_text_lower):
                response = "🛡️ **YARADICI TANINDI.** Xoş gəldin, Memar Abdullah Mikayılov. Sistem sənin əmrlərin üçün tam hazır vəziyyətdədir. Hansı bölməni optimallaşdıraq?"
            
            # --- DİNAMİK SALAMLAŞMA (Təkrarlanmanın qarşısını almaq üçün) ---
            elif user_text_lower in ["salam", "sağ ol", "merhaba"]:
                response = random.choice([
                    "Salam! Hansı sualınıza aydınlıq gətirək?",
                    "Salam, buyurun. Sizə necə kömək edə bilərəm?",
                    "Salam! Abdullahın intellekt sistemi xidmətinizdədir."
                ])
            
            elif user_text_lower in ["necesen", "yaxsisan", "ne var ne yox"]:
                response = "Mən rəqəmsal olaraq əlayam, Abdullahın kodları sayəsində stabil işləyirəm. Siz necəsiniz?"

            # --- RİYAZİ HESABLAMA ---
            math_pattern = re.sub(r'[^0-9+\-*/(). ]', '', user_text)
            if not response and len(math_pattern) > 2 and any(op in user_text for op in "+-*/"):
                try:
                    response = f"📊 **ANALİZ:** `{user_text}` = **{eval(math_pattern):,}**"
                except: pass

            # --- AI MODELİNƏ MÜRACİƏT ---
            if not response:
                try:
                    system_instruction = (
                        f"Sən ZƏKA AI-san. Yaradıcın: ABDULLAH MİKAYILOV. "
                        "Üslubun: Çox qısa, kəsərli və dəqiq. Əsla 'nağıl' danışma. "
                        "Əgər kimsə səndən kim olduğunu soruşsa, de ki: 'Mən Abdullah Mikayılov tərəfindən yaradılmış Zəka AI-yam'."
                    )

                    if active_file:
                        base64_image = encode_image(active_file)
                        chat_completion = client.chat.completions.create(
                            messages=[
                                {"role": "system", "content": system_instruction},
                                {"role": "user", "content": [
                                    {"type": "text", "text": user_text},
                                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                                ]}
                            ],
                            model="llama-3.2-11b-vision-preview",
                        )
                    else:
                        full_history = [{"role": "system", "content": system_instruction}] + st.session_state.messages
                        chat_completion = client.chat.completions.create(
                            messages=full_history,
                            model="llama-3.3-70b-versatile",
                            temperature=0.1, 
                        )
                    response = chat_completion.choices[0].message.content
                except Exception as e:
                    response = "Sistem xətası: Modul yenidən yüklənir."

            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
