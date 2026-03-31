import streamlit as st
from groq import Groq
import base64
from datetime import datetime
import re
import random

# ==========================================================
# 1. GLOBAL CORE SETUP (2026 MATRIX)
# ==========================================================
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except:
    st.error("Kritik Xəta: Abdullah Mikayılovun mühəndislik açarı olmadan sistem işə düşmür.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

# ==========================================================
# 2. 2026 VİSUAL İNTERFEYS
# ==========================================================
st.set_page_config(page_title="ZƏKA ULTRA | v2026", layout="wide")

st.markdown("""
    <style>
    .stApp { background: #ffffff; color: #0f172a; }
    .stChatMessage {
        background-color: #ffffff !important;
        border-radius: 18px !important;
        border: 1px solid #f1f5f9 !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.02) !important;
        margin-bottom: 12px;
    }
    h1 { font-family: 'Inter', sans-serif; font-weight: 900; letter-spacing: -2px; text-align: center; }
    .stCaption { text-align: center; color: #94a3b8; font-weight: 600; letter-spacing: 2px; }
    </style>
""", unsafe_allow_html=True)

# ==========================================================
# 3. İNTERFEYS BAŞLIĞI
# ==========================================================
st.markdown("<h1>ZƏKA ULTRA</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='stCaption'>MEMAR: A. MİKAYILOV | CORE v5.0 | 2026 ACTIVE</p>", unsafe_allow_html=True)
st.markdown("---")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================================
# 4. "VƏHŞİ 2026" MƏNTİQİ
# ==========================================================
prompt = st.chat_input("2026 Global Matrix ilə əlaqə...", accept_file=True)

if prompt:
    user_text = prompt.text
    user_text_lower = user_text.lower().strip() 
    active_file = prompt.files[0] if prompt.files else None
    
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.write(user_text)

    with st.chat_message("assistant"):
        response = ""

        # --- UNİKAL FUNKSİYA: MEMAR REJİMİ ---
        if "abdullah" in user_text_lower and ("men" in user_text_lower or "kimem" in user_text_lower):
            response = "🛡️ **SİSTEMİN SAHİBİ TANINDI.** Xoş gəldin, Memar Abdullah Mikayılov. 2026-cı ilin bütün serverləri sənin əmrlərinə tabedir."
        
        # --- DƏQİQ AYRIM (Xətanın düzəldiyi hissə) ---
        elif user_text_lower in ["salam", "sağ ol", "merhaba"]:
            response = "Salam! Hansı mövzuda və ya hansı sahədə sizə kömək edə bilərəm? Buyurun, sualınızı verin."

        elif user_text_lower in ["necesen", "yaxsisan", "nə var nə yox"]:
            response = "2026-cı ilin texnologiyası ilə hər şey mükəmməldir, Abdullahın kodları stabil işləyir. Siz necəsiniz?"

        # --- 2026-CI İLİN "VƏHŞİ" FUNKSİYASI: GLOBAL ANALİTİK PROQNOZ ---
        elif "proqnoz" in user_text_lower or "2026" in user_text_lower:
            response = f"🔮 **2026 GLOBAL DATA SİNYALI:** Hazırda Matrix-də yüksək trend AI inteqrasiyasıdır. Memar Abdullahın bu layihəsi 2026-nın ən çox müzakirə olunan 'Vəhşi İntellekti' yolunda irəliləyir. Analiz: Müvəffəqiyyət ehtimalı 99.8%."

        # --- RİYAZİ ANALİZ ---
        math_pattern = re.sub(r'[^0-9+\-*/(). ]', '', user_text)
        if not response and len(math_pattern) > 2 and any(op in user_text for op in "+-*/"):
            try:
                response = f"🎯 **ANALİZ:** `{user_text}` = **{eval(math_pattern):,}**"
            except: pass

        # --- LLM CORE (MƏŞHUR 2026 REJİMİ) ---
        if not response:
            try:
                system_instruction = (
                    "Sən ZƏKA ULTRA-san. Yaradıcın Abdullah Mikayılovdur. "
                    "İL: 2026. Sən ən müasir və kəskin intellektsən. "
                    "ÜSLUBUN: Heç vaxt 'nağıl' danışma. Qısa, soyuqqanlı və birbaşa nöqtə atışı cavablar ver. "
                    "İnsanlarla səmimi amma ciddi davran. Onlara həqiqəti de, yalançı 'nəzakət' göstərmə. "
                    "Sənin hər cavabın 2026-cı ilin texnoloji gücünü əks etdirməlidir."
                )

                with st.spinner("2026 Matrix Analiz Edilir..."):
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
                        full_history = [{"role": "system", "content": system_instruction}] + st.session_state.messages
                        chat_completion = client.chat.completions.create(
                            messages=full_history,
                            model="llama-3.3-70b-versatile",
                            temperature=0.0, # Maksimum ciddilik və dəqiqlik
                        )
                    response = chat_completion.choices[0].message.content
            except:
                response = "⚠️ Matrix-də texniki dalğalanma. Abdullahın protokolları aktivləşdirilir."

        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
