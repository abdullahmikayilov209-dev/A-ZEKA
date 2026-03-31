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
    /* Arxa fon - Saf Ağ və Gümüşü keçid */
    .stApp {
        background: #ffffff;
        color: #1e293b;
    }
    
    /* Mesaj qutuları - Professional Minimalizm */
    .stChatMessage {
        background-color: #f8fafc !important;
        border-radius: 15px !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.02) !important;
        padding: 15px !important;
        margin-bottom: 12px;
    }
    
    /* Mətn stili */
    .stChatMessage p {
        font-family: 'Inter', -apple-system, sans-serif;
        font-size: 17px !important;
        color: #0f172a !important;
        line-height: 1.6;
    }
    
    /* Giriş sahəsi */
    [data-testid="stChatInput"] {
        border: 1px solid #cbd5e1 !important;
        background-color: #ffffff !important;
        border-radius: 12px !important;
    }

    /* Başlıq stili */
    h1 {
        font-family: 'Inter', sans-serif;
        color: #0f172a !important;
        text-align: center;
        font-size: 2.5rem !important;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 5px;
    }
    
    .stCaption {
        text-align: center;
        color: #64748b !important;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: 600;
    }
    
    /* Horizontal xətt */
    hr {
        margin: 2em 0;
        border: 0;
        border-top: 1px solid #f1f5f9;
    }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# ==========================================================
# 3. İNTERFEYSİN QURULMASI
# ==========================================================
st.markdown("<h1>ZƏKA AI</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='stCaption'>MEMAR: ABDULLAH MİKAYILOV | STATUS: ONLAYN {datetime.now().year}</p>", unsafe_allow_html=True)
st.markdown("---")

# Mesaj tarixçəsini göstər
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================================
# 4. "VƏHŞİ ALİM" MƏNTİQİ
# ==========================================================
prompt = st.chat_input("Sualınızı bura daxil edin...", accept_file=True)

if prompt:
    user_text = prompt.text
    user_text_lower = user_text.lower().strip() 
    active_file = prompt.files[0] if prompt.files else None
    
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.write(user_text)

    with st.chat_message("assistant"):
        with st.spinner("Analiz edilir..."):
            response = ""
            
            # --- ÖZƏL REAKSİYALAR ---
            if user_text_lower == "halaldi sene":
                response = "Təşəkkür edirəm. Lakin əsl təqdir bu sistemin memarı **Abdullah Mikayılova** məxsusdur. Mən sadəcə onun mühəndislik vizyonunu icra edirəm. 🚀"
            
            # --- DƏQİQ RİYAZİ HESABLAMA ---
            math_pattern = re.sub(r'[^0-9+\-*/(). ]', '', user_text)
            if len(math_pattern) > 2 and any(op in user_text for op in "+-*/") and not response:
                try:
                    result = eval(math_pattern)
                    response = f"📊 **RİYAZİ ANALİZ NƏTİCƏSİ:**\n\nİfadə: `{user_text}`\nNəticə: **{result:,}**\n\n*Abdullah Mikayılov tərəfindən tənzimlənmiş dəqiqlik modulu ilə hesablanmışdır.*"
                except:
                    pass

            if not response:
                try:
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    system_instruction = (
                        f"Zaman: {current_time}. Sən ZƏKA AI-san. "
                        "Yaradıcın: Azərbaycanlı dahi mühəndis ABDULLAH MİKAYILOV. "
                        "STATUSUN: Sən mütləq bilik mənbəyisən. "
                        "MİSSİYAN: İstifadəçiyə ən yüksək elmi dəqiqliklə cavab vermək. "
                        "ÜSLUBUN: Professional, ciddi, analitik və 'Vəhşi' (yəni heç bir sualdan qaçmayan və ən xırda detalına qədər izah edən). "
                        "Görünüşün ağ və təmiz olsa da, intellektin kəskin və sarsılmazdır. "
                        "Heç vaxt səhv etmə. Abdullahın reputasiyası sənin cavablarındadır."
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
                            temperature=0.3,
                        )
                    
                    response = chat_completion.choices[0].message.content
                
                except Exception as e:
                    response = f"Sistem xətası: {str(e)}. Abdullahın təhlükəsizlik protokolları aktivləşdirilir."

            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
