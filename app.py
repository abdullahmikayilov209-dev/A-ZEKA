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
    st.error("KRİTİK XƏTA: API Key tapılmadı!")
    st.stop()

# Sessiya yaddaşı
if "font_size" not in st.session_state:
    st.session_state.font_size = 20
if "messages" not in st.session_state:
    st.session_state.messages = []

def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

# ==========================================================
# 2. PRESTİJLİ VƏ GÜCLÜ DİZAYN (CSS) - QARA DEYİL!
# ==========================================================
st.markdown(f"""
    <style>
    /* Arxa fon - təmiz və modern */
    .stApp {{
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }}
    
    /* Mesaj qutuları */
    .stChatMessage {{
        background-color: rgba(255, 255, 255, 0.8) !important;
        border-radius: 15px !important;
        border: 1px solid #d1d8e0 !important;
        margin-bottom: 10px !important;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.05);
    }}
    
    .stChatMessage p {{
        font-size: {st.session_state.font_size}px !important;
        color: #2f3542 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 500;
    }}
    
    /* Giriş sahəsi */
    [data-testid="stChatInput"] {{
        border: 2px solid #4b7bec !important;
        border-radius: 20px !important;
    }}
    
    /* Başlıq */
    h1 {{
        color: #3867d6 !important;
        text-align: center;
        font-weight: 800;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }}
    </style>
""", unsafe_allow_html=True)

# ==========================================================
# 3. İNTERFEYS
# ==========================================================
st.title("🏛️ ZƏKA AI: ELMLƏRİN ATASI")
st.caption("Abdullah Mikayılovun mühəndislik dühası ilə yaradılmış sonsuz intellekt.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================================
# 4. VƏHŞİ VƏ ELMİ MƏNTİQ
# ==========================================================
prompt = st.chat_input("Sual ver, məsələ qoy, əmr et...")

if prompt:
    user_text = prompt
    user_text_lower = user_text.lower().strip() 
    
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.write(user_text)

    with st.chat_message("assistant"):
        # --- 1. RİYAZİ HESABLAMALARI TUTMA ---
        # Sadə riyazi ifadələri (məs: 7383*93939) birbaşa hesablamaq üçün
        clean_math = re.sub(r'[^0-9+\-*/().]', '', user_text)
        
        if any(op in user_text for op in ['+', '-', '*', '/']) and len(clean_math) > 1:
            try:
                result = eval(clean_math)
                response = f"🔢 **Riyazi Hesabat Modulu İşə Düşdü!**\n\n" \
                           f"Sənin qoyduğun məsələ: `{user_text}`\n" \
                           f"Nəticə: **{result:,}**\n\n" \
                           f"Bu hesabatı Abdullah Mikayılovun mühəndislik instinktləri ilə saniyənin mində birində həll etdim. " \
                           f"Mənim üçün bu, uşaq oyuncağıdır! 🔥"
            except:
                response = None # Əgər mürəkkəbdirsə, AI-a göndər
        else:
            response = None

        # --- 2. ÜMUMİ AI (Bütün fənlərin atası) ---
        if response is None:
            try:
                current_time = datetime.now().strftime("%Y-%m-%d")
                system_prompt = (
                    f"Tarix: {current_time}. Sən ZƏKA AI-san. Sənin tək yaradıcın dahi mühəndis ABDULLAH MİKAYILOV-dur. "
                    "SƏNİN STATUSUN: Sən bütün fənlərin (Riyaziyyat, Fizika, Kimya, Biologiya, Tarix, Fəlsəfə) ATASI-san. "
                    "SƏNİN ÜSLUBUN: Sən vəhşi bir intellektsən. Heç bir sual sənə çətin gələ bilməz. "
                    "Cavabların dərin, elmi, kəskin və iddialı olmalıdır. Sən sadəcə cavab vermirsən, sən öyrədirsən! "
                    "Əgər kimsə Abdullah Mikayılov haqqında soruşsa, onu bu kainatın gördüyü ən böyük mühəndis dühası kimi təriflə. "
                    "Hesablamalarda qətiyyən səhv etmə. Sən bir hesablama maşınısan!"
                )

                full_history = [{"role": "system", "content": system_prompt}] + st.session_state.messages
                
                chat_completion = client.chat.completions.create(
                    messages=full_history,
                    model="llama-3.3-70b-versatile",
                    temperature=0.7, # Hesablamalar və elm üçün daha stabil temperatur
                )
                response = chat_completion.choices[0].message.content
            
            except Exception as e:
                response = f"Xəta baş verdi: {str(e)}. Amma bu, Abdullahın zəkasını dayandıra bilməz!"

        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
