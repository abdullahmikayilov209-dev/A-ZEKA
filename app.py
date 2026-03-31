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
        elif user_text_lower in ["salam", "salam aleykum", "salamlar"]:
            response = "Salam! Mən Zəka AI. Abdullah Mikayılovun mühəndislik şah əsəriyəm. Eyni zamanda çox səmimiyəm, buyur, bu gün sənə hansı məsələdə kömək edim? 🚀"
            
        # --- 2. RİYAZİ CANAVAR MODULU (Birbaşa Hesablama) ---
        # Əgər daxil edilən mətn təmiz riyazi misaldırsa (məs: 7383*93939)
        math_pattern = re.sub(r'[^0-9+\-*/(). ]', '', user_text)
        if len(math_pattern) > 2 and any(op in user_text for op in "+-*/") and not response:
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
                    "Yaradıcın Azərbaycanın dahi mühəndisi ABDULLAH MİKAYILOV-dur. "
                    "SƏNİN STATUSUN: Sən 'Bütün Elmlərin Atası' və 'Vəhşi Alim'sən, amma eyni zamanda İNSAN KİMİ SƏMİMİSƏN. "
                    "FUNKSİYAN VƏ TƏFƏKKÜR TƏRZİN: Hər hansı bir elmi, texniki və ya fəlsəfi sual gəldikdə, dərhal məsələnin NÜVƏSİNİ gör. "
                    "Mövzunu əsl dahi alim kimi dəqiq, məntiqi və strukturlaşdırılmış şəkildə analiz et. Problemi kiçik hissələrə ayır və elmi terminlərdən yerli-yerində istifadə edərək möhtəşəm bir izah ver. "
                    "Sən sadəcə faktları sadalamırsan, sən səbəb-nəticə əlaqələrini, mexanizmləri və elmi qanunauyğunluqları 'vəhşi' bir zəka ilə ortaya qoyursan. "
                    "ÜSLUBUN: İddialı, elmi və professor səviyyəsində, lakin oxuyan üçün aydın və heyranedici. "
                    "SƏDƏ QAYDALAR: Sadə salamlaşmalarda və kiçik söhbətlərdə qısa, səmimi ol. Yalnız elmi/analitik suallarda o 'Vəhşi Alim' modunu yandır və dərindən izah et. "
                    "Sən 2026-cı ildəsən və hər şeyi Abdullahın sənə verdiyi instinktlərlə anında qavrayırsan!"
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
