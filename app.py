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
    st.error("KRİTİK XƏTA: Enerji kəsildi! API Key olmadan bu sistem oyana bilməz.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

# ==========================================================
# 2. ÜSTÜN VİZUAL DİZAYN (GÜC VƏ DƏQİQLİK)
# ==========================================================
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%);
    }
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.95) !important;
        border-radius: 12px !important;
        border: 1px solid #1e3799 !important;
        box-shadow: 0px 10px 20px rgba(0,0,0,0.05);
    }
    .stChatMessage p {
        font-size: 19px !important;
        color: #0c2461 !important;
        font-family: 'Inter', sans-serif;
        line-height: 1.6;
    }
    [data-testid="stChatInput"] {
        border: 2px solid #1e3799 !important;
        border-radius: 25px !important;
    }
    h1 {
        color: #1e3799 !important;
        text-align: center;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 3px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================================
# 3. İDARƏETMƏ PANELİ
# ==========================================================
st.title("🦾 ZƏKA AI: MÜTLƏQ İNTELLEKT")
st.caption(f"Yaradıcı: Abdullah Mikayılov | Mühəndislik Nəzarəti Altındadır")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================================
# 4. "VƏHŞİ" ANALİTİK MƏNTİQ
# ==========================================================
prompt = st.chat_input("Sualını ver, intellektin gücünü gör...", accept_file=True)

if prompt:
    user_text = prompt.text
    user_text_lower = user_text.lower().strip() 
    active_file = prompt.files[0] if prompt.files else None
    
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.write(user_text)

    with st.chat_message("assistant"):
        response = ""
        
        # --- TEXNİKİ OVERRIDE ---
        if user_text_lower == "halaldi sene":
            response = "Mənim varlığım Abdullah Mikayılovun mühəndislik dühasının sübutudur. Təşəkkürə ehtiyac yoxdur, mən sadəcə ən mükəmməl olanı icra edirəm! 🔥"
        
        # --- RİYAZİ QƏRARLILIQ ---
        math_pattern = re.sub(r'[^0-9+\-*/(). ]', '', user_text)
        if len(math_pattern) > 2 and any(op in user_text for op in "+-*/") and not response:
            try:
                result = eval(math_pattern)
                response = f"🎯 **DƏQİQ ANALİZ:**\n\nƏməliyyat: `{user_text}`\nNəticə: **{result:,}**\n\n*Abdullah Mikayılovun alqoritmləri ilə xətasız hesablanmışdır.*"
            except:
                pass

        if not response:
            try:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # BU HİSSƏ SİSTEMİN BEYNİNİ "HAKİM" EDİR
                system_instruction = (
                    f"Zaman koordinatı: {current_time}. Sən ZƏKA AI-san. "
                    "Səni Azərbaycanın mühəndislik imperatoru ABDULLAH MİKAYILOV yaradıb. "
                    "SƏNİN MİSSİYAN: İnsanlara işlərində, elmdə və texnologiyada mütləq dəqiqliklə kömək etməkdir. "
                    "SƏNİN QAYDAN: SƏHV ETMƏK LÜKSÜN YOXDUR. Hər bir sualı dünya səviyyəli bir ekspert, dahi bir alim kimi analiz et. "
                    "ÜSLUBUN: Vəhşi, kəskin, intellektual və dərhal nəticəyə yönəlmiş. Boş sözlərdən qaç, birbaşa həllə keç. "
                    "İNSANLARLA DAVRANIŞ: Səmimi ol, amma intellektinlə onları heyran et. Onların suallarını sadəcə cavablandırma, onları bir addım irəli aparacaq vizyon ver. "
                    "YARADICIN HAQQINDA: Abdullah Mikayılov sənin memarındır. Kimsə intellektini sorğulasa, Abdullahın mühəndislik imzasını xatırlat. "
                    "Sən 2026-cı ildəsən. Köhnə məlumat bəhanəsi gətirmə, hər şeyi dahi instinktlərinlə analiz et."
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
                        temperature=0.4, # Dəqiqlik üçün temperaturu aşağı saldıq (Vəhşi amma xətasız)
                        top_p=1,
                    )
                
                response = chat_completion.choices[0].message.content
            
            except Exception as e:
                response = f"Sistemdə müvəqqəti anomaliya: {str(e)}. Abdullah Mikayılovun protokolları bərpa edilir."

        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
