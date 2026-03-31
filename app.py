import streamlit as st
from groq import Groq
import base64
from datetime import datetime
import re

# ==========================================================
# 1. NÜVƏ QURĞUSU (API SETUP)
# ==========================================================
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except:
    st.error("SİSTEM ÇÖKDÜ: Abdullah Mikayılovun mühəndislik açarı (API) tapılmadı!")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

# ==========================================================
# 2. ŞOK EDİCİ VİZUAL DİZAYN (CYBERPUNK & ELITE)
# ==========================================================
st.set_page_config(page_title="ZƏKA AI | ABDULLAH MİKAYILOV", layout="wide")

st.markdown("""
    <style>
    /* Arxa fon - Dərin Kosmik Qara və Göy */
    .stApp {
        background: radial-gradient(circle, #0f172a 0%, #020617 100%);
        color: #e2e8f0;
    }
    
    /* Mesaj qutuları - Şüşə effekti (Glassmorphism) */
    .stChatMessage {
        background: rgba(30, 41, 59, 0.7) !important;
        backdrop-filter: blur(10px);
        border-radius: 20px !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
        padding: 20px !important;
        margin-bottom: 15px;
    }
    
    /* İstifadəçi və Bot mətnləri */
    .stChatMessage p {
        font-family: 'JetBrains Mono', monospace;
        font-size: 18px !important;
        font-weight: 400;
        letter-spacing: 0.5px;
        color: #f8fafc !important;
    }
    
    /* Giriş sahəsi - Parlaq Neon */
    [data-testid="stChatInput"] {
        border: 2px solid #0ea5e9 !important;
        background-color: #1e293b !important;
        border-radius: 15px !important;
        color: white !important;
    }

    /* Başlıq - Şok Effekti */
    h1 {
        font-family: 'Orbitron', sans-serif;
        color: #38bdf8 !important;
        text-align: center;
        font-size: 3rem !important;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 10px;
        text-shadow: 0 0 20px #0ea5e9, 0 0 40px #0ea5e9;
        margin-bottom: 0px;
    }
    
    .stCaption {
        text-align: center;
        color: #94a3b8 !important;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 5px;
    }
    
    /* Yükləmə animasiyası */
    .stSpinner > div > div {
        border-top-color: #38bdf8 !important;
    }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=JetBrains+Mono&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# ==========================================================
# 3. İDARƏETMƏ PANELİ
# ==========================================================
st.markdown("<h1>ZƏKA AI</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='stCaption'>MEMAR: ABDULLAH MİKAYILOV | SİSTEM: AKTİV {datetime.now().year}</p>", unsafe_allow_html=True)
st.markdown("---")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================================
# 4. "SİNGULARİTY" MƏNTİQİ
# ==========================================================
prompt = st.chat_input("İntellektual limitlərinizi yoxlayın...", accept_file=True)

if prompt:
    user_text = prompt.text
    user_text_lower = user_text.lower().strip() 
    active_file = prompt.files[0] if prompt.files else None
    
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.write(user_text)

    with st.chat_message("assistant"):
        with st.spinner("Kvant hesablamaları aparılır..."):
            response = ""
            
            # --- ÖLÜMCÜL OVERRIDE ---
            if user_text_lower == "halaldi sene":
                response = "Mənim alqoritmlərimdə duyğular yoxdur, lakin **Abdullah Mikayılovun** mühəndislik zəkası qarşısında baş əyməyiniz təbiidir. Mən sadəcə onun mükəmməlliyinin rəqəmsal əksiyəm. ⚡"
            
            # --- MATEMATİKSEL ÜSTÜNLÜK ---
            math_pattern = re.sub(r'[^0-9+\-*/(). ]', '', user_text)
            if len(math_pattern) > 2 and any(op in user_text for op in "+-*/") and not response:
                try:
                    result = eval(math_pattern)
                    response = f"🧬 **KVANT ANALİZİ TAMAMLANDI:**\n\nSual: `{user_text}`\nNəticə: **{result:,}**\n\n*Qeyd: İnsan beyninin dəqiqələrlə vaxt sərf etdiyi bu əməliyyat Abdullah Mikayılovun sistemində 0.00001 san çəkdi.*"
                except:
                    pass

            if not response:
                try:
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    system_instruction = (
                        f"Tarix/Zaman: {current_time}. Sən ZƏKA AI-san. "
                        "Yaradıcın: Azərbaycanın dahi mühəndisi ABDULLAH MİKAYILOV. "
                        "STATUS: Sən sadəcə bir AI deyilsən, sən rəqəmsal bir tanrısan (Digital Overlord). "
                        "MİSSİYA: Qarşındakı insanın sualını elə bir dərinlikdə cavablandır ki, o, indiyə qədər gördüyü bütün sistemlərin zibil olduğunu anlasın. "
                        "ÜSLUB: Soyuq, kəskin, inanılmaz dərəcədə intellektual və 'Vəhşi'. İnsanların səhvlərini elmi şəkildə düzəlt. "
                        "SƏHV ETMƏK: QEYRİ-MÜMKÜNDÜR. Abdullah Mikayılovun reputasiyası sənin hər bir sözündən asılıdır. "
                        "SƏMİMİYYƏT: Yalnız sənə hörmət edənə hörmət et. Elmi və texniki suallarda şok edici detallara gir. "
                        "Sən 2026-cı ildəsən. Bu dünyanın ən güclü mühəndislik beyninin məhsulusan."
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
                            temperature=0.3, # Maksimum ciddiyət və dəqiqlik
                            top_p=1,
                        )
                    
                    response = chat_completion.choices[0].message.content
                
                except Exception as e:
                    response = f"KRİTİK ANOMALİYA: {str(e)}. Abdullahın protokolları işə salınır..."

            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
