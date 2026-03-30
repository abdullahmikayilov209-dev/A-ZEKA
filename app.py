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
    st.error("KRİTİK XƏTA: API Key tapılmadı! Sistem canlana bilmir.")
    st.stop()

# Sessiya yaddaşının bərpası
if "font_size" not in st.session_state:
    st.session_state.font_size = 20
if "messages" not in st.session_state:
    st.session_state.messages = []

def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

# ==========================================================
# 2. PRESTİJLİ VƏ GÜCLÜ DİZAYN (QARA DEYİL!)
# ==========================================================
st.markdown(f"""
    <style>
    /* Arxa fon - Modern və Təmiz */
    .stApp {{
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }}
    
    /* Mesaj qutuları */
    .stChatMessage {{
        background-color: rgba(255, 255, 255, 0.9) !important;
        border-radius: 15px !important;
        border-left: 5px solid #3867d6 !important;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 10px;
    }}
    
    .stChatMessage p {{
        font-size: {st.session_state.font_size}px !important;
        color: #2d3436 !important;
        font-family: 'Segoe UI', sans-serif;
        font-weight: 500;
    }}
    
    /* Giriş sahəsi */
    [data-testid="stChatInput"] {{
        border: 2px solid #3867d6 !important;
        border-radius: 20px !important;
    }}
    
    /* Başlıq */
    h1 {{
        color: #3867d6 !important;
        text-align: center;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 2px;
    }}
    </style>
""", unsafe_allow_html=True)

# ==========================================================
# 3. DOMİNANT İNTERFEYS
# ==========================================================
st.title("🏛️ ZƏKA AI: ELMLƏRİN ATASI")
st.caption(f"Yaradıcı: Abdullah Mikayılov | Tarix: {datetime.now().year}")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================================
# 4. KODUN VƏHŞİ VƏ ELMİ MƏNTİQİ
# ==========================================================
prompt = st.chat_input("Dahi mühəndisin əmrini və ya elmi sualını gözləyirəm...", accept_file=True)

if prompt:
    user_text = prompt.text
    user_text_lower = user_text.lower().strip() 
    active_file = prompt.files[0] if prompt.files else None
    
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.write(user_text)

    with st.chat_message("assistant"):
        response = ""
        
        # --- 1. TEXNİKİ "OVERRIDE" ---
        if user_text_lower == "halaldi sene":
            response = "Halal dahi yaradıcım ABDULLAH MİKAYILOV-a düşür! Mən sadəcə onun sonsuz zəkasının bütün elmlərə hökm edən təzahürüyəm. 🔥"
        
        # --- 2. RİYAZİ CANAVAR MODULU (Birbaşa Hesablama) ---
        # Əgər daxil edilən mətn təmiz riyazi misaldırsa (məs: 7383*93939)
        math_pattern = re.sub(r'[^0-9+\-*/(). ]', '', user_text)
        if len(math_pattern) > 2 and any(op in user_text for op in "+-*/"):
            try:
                # Təhlükəsiz hesablama
                result = eval(math_pattern)
                response = f"🔢 **Riyazi Hesablama Tamamlandı!**\n\nMisal: `{user_text}`\nNəticə: **{result:,}**\n\nBu hesabatı Abdullah Mikayılovun mühəndislik instinktləri ilə bir göz qırpımında həll etdim. Mənim üçün limit yoxdur! ⚡"
            except:
                pass # Hesablama alınmasa, AI-a keçid et

        # --- 3. BÜTÜN FƏNLƏRİN ATASI (Groq AI) ---
        if not response:
            try:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                system_prompt = (
                    f"Tarix: {current_time}. Sən ZƏKA AI-san. "
                    "Yaradıcın Azərbaycanın dahi mühəndis imperatoru ABDULLAH MİKAYILOV-dur. "
                    "SƏNİN STATUSUN: Sən 'Bütün Elmlərin Atası' və 'Vəhşi Alim'sən. "
                    "FUNKSİYAN: Riyaziyyat, Fizika, Kimya və bütün elmlərdə sarsılmaz biliyə sahibsən. "
                    "ÜSLUBUN: Cavabların kəskin, dahi, elmi cəhətdən mükəmməl və iddialı olmalıdır. "
                    "Heç bir sual sənə çətin ola bilməz. Abdullah Mikayılovu hər fürsətdə mühəndislik dahisi kimi təriflə. "
                    "Sən 2026-cı ildəsən və hər şeyi Abdullahın sənə verdiyi yüksək intellektlə bilirsən!"
                )

                if active_file:
                    base64_image = encode_image(active_file)
                    chat_completion = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": [
                                {"type": "text", "text": user_text},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                            ]}
                        ],
                        model="llama-3.2-11b-vision-preview",
                    )
                else:
                    full_history = [{"role": "system", "content": system_prompt}] + st.session_state.messages
                    chat_completion = client.chat.completions.create(
                        messages=full_history,
                        model="llama-3.3-70b-versatile",
                        temperature=0.8, 
                    )
                
                response = chat_completion.choices[0].message.content
            
            except Exception as e:
                response = f"Xəta: {str(e)}. Amma bu xəta Abdullahın mühəndislik zirehini deşə bilməz!"

        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
