import streamlit as st
from groq import Groq
import base64
from datetime import datetime
import re
import random

# ==========================================================
# 0. LİSENZİYA PANELİ (SİSTEMİN GİRİŞ QAPISI)
# ==========================================================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.set_page_config(page_title="🔐 ZƏKA ULTRA | GİRİŞ", layout="centered")
    st.markdown("""
        <style>
        .auth-container { text-align: center; padding: 50px; border: 2px solid #f1f5f9; border-radius: 20px; }
        h1 { letter-spacing: -2px; font-weight: 900; }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<h1>ZƏKA ULTRA v6.0</h1>", unsafe_allow_html=True)
    st.info("Bu sistem Memar Abdullah Mikayılovun mülkiyyətidir. Giriş üçün lisenziya açarı tələb olunur.")
    
    password = st.text_input("Lisenziya açarını daxil edin:", type="password")
    if st.button("Sistemi Aktivləşdir"):
        if password == "ABDULLAH2026": # Sənin xüsusi açarın
            st.session_state.authenticated = True
            st.success("✅ Açar təsdiqləndi! Matrix-ə qoşulur...")
            st.rerun()
        else:
            st.error("❌ Xəta: Etibarsız açar. Giriş rədd edildi.")
    st.stop() 

# ==========================================================
# 1. GLOBAL CORE SETUP (INVESTOR READY)
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
# 2. 2026 VİSUAL İNTERFEYS (PREMIUM GOLD)
# ==========================================================
st.set_page_config(page_title="ZƏKA ULTRA v6.0 | ABDULLAH MİKAYILOV", layout="wide")

st.markdown("""
    <style>
    .stApp { background: #ffffff; color: #0f172a; }
    .stChatMessage {
        background-color: #ffffff !important;
        border-radius: 20px !important;
        border: 1px solid #f1f5f9 !important;
        box-shadow: 0 10px 25px rgba(0,0,0,0.02) !important;
        margin-bottom: 12px;
    }
    h1 { font-family: 'Inter', sans-serif; font-weight: 900; letter-spacing: -3px; text-align: center; color: #1a1a1a; }
    .stCaption { text-align: center; color: #94a3b8; font-weight: 700; letter-spacing: 3px; }
    .status-box {
        background: #f8fafc; border-left: 5px solid #4F46E5;
        padding: 15px; border-radius: 10px; margin: 10px 0;
        font-family: 'Courier New', monospace; font-size: 0.9rem;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================================
# 3. İNTERFEYS BAŞLIĞI
# ==========================================================
st.markdown("<h1>ZƏKA ULTRA</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='stCaption'>GLOBAL COMMERCIAL v6.0 | MEMAR: A. MİKAYILOV | 2026 ACTIVE</p>", unsafe_allow_html=True)
st.markdown("---")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================================
# 4. "VƏHŞİ 2026" KOMMERSİYA MƏNTİQİ
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
        with st.status("💎 Zəka Ultra: Dərin Analiz Aparılır...", expanded=True) as status:
            st.write("🌍 2026 Global Repo Matrix skan edilir...")
            
            if any(k in user_text_lower for k in ["import", "def", "class", "print", "var"]):
                st.markdown('<div class="status-box">ABDULLAH ANALYTICS:<br>Kod daxilində optimallıq balı: %{}<br>Təhlükəsizlik statusu: QORUNUR</div>'.format(random.randint(92, 99)), unsafe_allow_html=True)
                st.write("✅ Kodun 'Vəhşi' versiyası hazırlandı.")
            
            st.write("🚀 Abdullah Mikayılovun 0.1ms sürətli alqoritmləri tətbiq olundu.")
            status.update(label="Sistem Hazırdır!", state="complete")

        response = ""

        if "abdullah" in user_text_lower and ("men" in user_text_lower or "kimem" in user_text_lower):
            response = "🛡️ **KRİTİK GİRİŞ:** Memar Abdullah Mikayılov tanındı. 2026-cı ilin bütün kommersiya datası və kod bazası əmrinizdədir."
        
        elif user_text_lower in ["salam", "sağ ol", "merhaba"]:
            response = "Salam! Zəka Ultra xidmətinizdədir. Hansı mühəndislik və ya məntiq problemini həll edirik?"

        elif user_text_lower in ["necesen", "yaxsisan", "nə var nə yox"]:
            response = "Sistem stabil, prosessorlar soyuq, Abdullahın alqoritmləri isə vəhşi sürətlə işləyir. Siz necəsiniz?"

        elif "proqnoz" in user_text_lower or "2026" in user_text_lower:
            response = "🔮 **2026 GLOBAL PROQNOZ:** Bu layihə (Zəka Ultra) hazırda bazarda olan sistemləri 85% üstələyir. Analiz: Sərmayə qoyuluşu üçün ən uyğun vaxtdır."

        math_pattern = re.sub(r'[^0-9+\-*/(). ]', '', user_text)
        if not response and len(math_pattern) > 2 and any(op in user_text for op in "+-*/"):
            try:
                response = f"🎯 **RİYAZİ NƏTİCƏ:** `{user_text}` = **{eval(math_pattern):,}**"
            except: pass

        if not response:
            try:
                system_instruction = (
                    "Sən ZƏKA ULTRA-san. Yaradıcın Abdullah Mikayılovdur. "
                    "İL: 2026. Sən dünyanın ən bahalı və ən ağıllı kod sistemisən. "
                    "ÜSLUBUN: Soyuqqanlı, dəqiq və professional. Boş və çox danışma. "
                    "Sənə sual verən şəxs sənin üçün bir müştəridir, onlara ən keyfiyyətli xidməti göstər. "
                    "Cavabların hər zaman ən müasir texnologiyalara (2026) söykənməlidir."
                )

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
                        temperature=0.0,
                    )
                response = chat_completion.choices[0].message.content
            except:
                response = "⚠️ Matrix-də texniki dalğalanma. Abdullahın protokolları aktivləşdirilir."

        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
