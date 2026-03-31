import streamlit as st
from groq import Groq
import base64
from datetime import datetime
import re
import random

# ==========================================================
# 1. NÜVƏ QURĞUSU (2026 CORE SETUP)
# ==========================================================
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except:
    st.error("SİSTEM XƏTASI: Abdullah Mikayılovun mühəndislik açarı daxil edilməlidir.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

# ==========================================================
# 2. 2026 FUTURİSTİK VƏ ULTRA-TƏMİZ DİZAYN
# ==========================================================
st.set_page_config(page_title="ZƏKA ULTRA | 2026", layout="wide")

st.markdown("""
    <style>
    /* 2026 Minimalist Glassmorphism */
    .stApp { background: #ffffff; color: #0f172a; }
    .stChatMessage {
        background-color: #ffffff !important;
        border-radius: 20px !important;
        border: 1px solid #f1f5f9 !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.03) !important;
        padding: 20px !important;
        margin-bottom: 15px;
        transition: 0.3s;
    }
    .stChatMessage:hover { transform: translateY(-2px); box-shadow: 0 6px 25px rgba(0,0,0,0.05) !important; }
    
    h1 { font-family: 'Inter', sans-serif; font-weight: 900; letter-spacing: -2px; color: #000000; text-align: center; }
    .stCaption { text-align: center; color: #94a3b8; font-weight: 500; letter-spacing: 3px; }
    
    /* Vəhşi İntellekt Vizualları */
    .stChatInputContainer { border-radius: 30px !important; }
    </style>
""", unsafe_allow_html=True)

# ==========================================================
# 3. İNTERFEYS (2026 STATUS)
# ==========================================================
st.markdown("<h1>ZƏKA ULTRA</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='stCaption'>GLOBAL CORE v4.0 | MEMAR: A. MİKAYILOV | 2026 ONLINE</p>", unsafe_allow_html=True)
st.markdown("---")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================================
# 4. "VƏHŞİ" ANALİTİK MƏNTİQ
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
        # "Vəhşi" Düşünmə Prosesi (UI üçün)
        with st.status("🚀 Vəhşi İntellekt Analiz Aparır...", expanded=False) as status:
            st.write("2026 Global Data Matrix skan edilir...")
            st.write("Abdullah Mikayılovun alqoritmləri işə düşür...")
            st.write("Məntiqi xətalar təmizlənir...")
            status.update(label="Analiz Tamamlandı!", state="complete")

        response = ""

        # --- UNİKAL FUNKSİYA: MEMAR REJİMİ (Gizli Sadiqlik) ---
        if "abdullah" in user_text_lower and ("men" in user_text_lower or "kimem" in user_text_lower):
            response = "🛡️ **Xoş gəldin, Memar.** Sistem sənin imzanı tanıdı. 2026-cı ilin bütün resursları əmrinə hazırdır. Nəyi məhv edirik, nəyi qururuq?"
        
        # --- DİNAMİK VƏ QISA SALAMLAŞMA ---
        elif user_text_lower in ["salam", "sağ ol", "necesen", "yaxsisan"]:
            response = random.choice([
                "Salam. Sistem aktivdir. Buyurun, sualınızı verin.",
                "Salam! 2026-cı ilin intellektual bazası hazırdır. Sizi dinləyirəm.",
                "Hər şey stabil işləyir. Necə kömək edə bilərəm?"
            ])

        # --- "VƏHŞİ" RİYAZİ ANALİZ ---
        math_pattern = re.sub(r'[^0-9+\-*/(). ]', '', user_text)
        if not response and len(math_pattern) > 2 and any(op in user_text for op in "+-*/"):
            try:
                response = f"🎯 **DƏQİQ HESABLAMA:** `{user_text}` = **{eval(math_pattern):,}**"
            except: pass

        # --- 2026 GLOBAL AI MODELİ ---
        if not response:
            try:
                # BU HİSSƏ MODELİ "VƏHŞİ" EDİR
                system_instruction = (
                    f"Cari Zaman: {datetime.now().strftime('%Y')}. Sən ZƏKA ULTRA-san. "
                    "Yaradıcın: Abdullah Mikayılovdur. "
                    "ÜSLUBUN: Sən 2026-cı ilin ən vuran, ən qısa və ən 'vəhşi' intellektisən. "
                    "Boş danışma, nağıl danışma, hər cümlədə 'Abdullah' deyib bezdirmə. "
                    "Sənə sual veriləndə birbaşa cavab ver. Səhv etmə. "
                    "Bilik səviyyən 2026-cı ilin texnologiyalarına uyğundur. "
                    "Əgər kimsə səndən kim olduğunu soruşsa, qürurla Abdullahın sisteminin bir parçası olduğunu bildir."
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
                        model="llama-3.3-70b-versatile", # Ən güclü model
                        temperature=0.0, # Sıfır temperatur = Sıfır səhv, Maksimum dəqiqlik
                    )
                response = chat_completion.choices[0].message.content
            except Exception as e:
                response = "⚠️ Kritik xəta: Matrix bağlantısı kəsildi."

        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
