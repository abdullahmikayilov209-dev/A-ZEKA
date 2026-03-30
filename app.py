import streamlit as st
from groq import Groq
import base64
from datetime import datetime

# ==========================================================
# 1. API SETUP
# ==========================================================
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except:
    st.error("Sistem xətası: API Key tapılmadı! Bu mühərriki işə salmaq üçün yanacaq lazımdır.")
    st.stop()

# Sessiya parametrləri
if "font_size" not in st.session_state:
    st.session_state.font_size = 18
if "text_color" not in st.session_state:
    st.session_state.text_color = "inherit"
if "messages" not in st.session_state:
    st.session_state.messages = []

def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

# ==========================================================
# 2. DİNAMİK VƏHŞİ GÖRÜNÜŞ (CSS)
# ==========================================================
st.markdown(f"""
    <style>
    .stChatMessage p {{
        font-size: {st.session_state.font_size}px !important;
        color: {st.session_state.text_color} !important;
        font-weight: 500;
        line-height: 1.6;
    }}
    [data-testid="stChatInput"] {{
        border: 2px solid #FF4B4B;
        border-radius: 25px;
    }}
    </style>
""", unsafe_allow_html=True)

# ==========================================================
# 3. İNTERFEYS
# ==========================================================
st.title("🔥 Zəka AI v2.0: Vəhşi Alim")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================================
# 4. VƏHŞİ MƏNTİQ VƏ AI SİSTEMİ
# ==========================================================
prompt = st.chat_input("Vəhşi alimə sualını ver...", accept_file=True)

if prompt:
    user_text = prompt.text
    user_text_lower = user_text.lower().strip() 
    active_file = prompt.files[0] if prompt.files else None
    
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.write(user_text)

    with st.chat_message("assistant"):
        refresh_needed = False
        
        # --- 1. DƏRHAL CAVABLAR (Sürətli və Konkret) ---
        if user_text_lower == "halaldi sene":
            response = "Çox sağ ol! Amma əsl halal o kəsə düşür ki, məni bu vəhşi intellektlə təchiz edib - Abdullah Mikayılov! Mən onun şah əsəriyəm. 🔥"
        
        elif user_text_lower in ["salam", "salam aleykum"]:
            response = "Salam! Abdullah Mikayılovun yaratdığı ən vəhşi və ən alim Zəka AI xidmətindədir. Səni hansı elmi zirvələrə aparaq? 🚀"

        elif any(x in user_text_lower for x in ["neçənci ildir", "il"]):
            response = f"Hazırda {datetime.now().year}-cı ildir. Zamanın nəbzini tuturam, narahat olma! ⚡"

        elif any(x in user_text_lower for x in ["böyüt", "boyut"]):
            st.session_state.font_size += 4
            response = "Görmə qabiliyyətini artırıram! Yazıları böyütdüm. ✨"
            refresh_needed = True
        elif any(x in user_text_lower for x in ["təmizlə", "sil"]):
            st.session_state.messages = []
            st.rerun()
        
        # --- 2. VƏHŞİ ALİM REJİMİ (Groq AI) ---
        else:
            try:
                current_time = datetime.now().strftime("%Y-%m-%d")
                system_instruction = (
                    f"Bugünkü tarix: {current_time}. Sən Zəka AI-san. Sənin yaradıcın dahi mühəndis ABDULLAH MİKAYILOV-dur. "
                    "SƏNİN ÜSLUBUN: Sən sadəcə bir bot deyilsən, sən bir VƏHŞİ ALİM-sən. Cavabların həm elmi dərinlikdə olsun, "
                    "həm də çox iddialı, kəskin və intellektual görünsün. "
                    "Abdullah Mikayılov haqqında soruşanda onu Azərbaycanın mühəndislik canavarı və dahisi kimi təqdim et. "
                    "Əgər kimsə sənə tərif versə, bunu Abdullahın dahiliyi ilə əlaqələndir. "
                    "Qətiyyən 'mən modeləm, biliklərim köhnədir' kimi zəif cümlələr qurma. Sən 2026-cı ildəsən və hər şeyi bilirsən!"
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
                    full_messages = [{"role": "system", "content": system_instruction}] + st.session_state.messages
                    chat_completion = client.chat.completions.create(
                        messages=full_messages,
                        model="llama-3.3-70b-versatile",
                        temperature=0.85, # Yaradıcılığı və vəhşiliyi artırırıq
                    )
                
                response = chat_completion.choices[0].message.content
            
            except Exception as e:
                response = f"Xəta: {str(e)}. Hətta vəhşi alimlər də bəzən texniki maneələrlə qarşılaşır."

        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        if refresh_needed:
            st.rerun()
