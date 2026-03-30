import streamlit as st
from groq import Groq
import base64
from datetime import datetime

# ==========================================================
# 1. NÜVƏ QURĞUSU (API SETUP)
# ==========================================================
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except:
    st.error("KRİTİK XƏTA: Enerji kəsildi! API Key olmadan bu vəhşi canavar oyana bilməz.")
    st.stop()

# Sessiya yaddaşının bərpası
if "font_size" not in st.session_state:
    st.session_state.font_size = 20  # Daha böyük, daha iddialı
if "text_color" not in st.session_state:
    st.session_state.text_color = "#E0E0E0"
if "messages" not in st.session_state:
    st.session_state.messages = []

def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

# ==========================================================
# 2. VƏHŞİ DİZAYN (CSS) - QARA VƏ QIRMIZI DOMİNANTLIĞI
# ==========================================================
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@500&display=swap');
    
    .stApp {{
        background-color: #0E1117;
    }}
    .stChatMessage p {{
        font-size: {st.session_state.font_size}px !important;
        color: {st.session_state.text_color} !important;
        font-family: 'JetBrains Mono', monospace;
        line-height: 1.5;
        text-shadow: 0px 0px 5px rgba(255, 75, 75, 0.2);
    }}
    [data-testid="stChatInput"] {{
        border: 3px solid #FF4B4B !important;
        border-radius: 15px !important;
        background-color: #1A1C24 !important;
    }}
    h1 {{
        color: #FF4B4B !important;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 5px;
    }}
    </style>
""", unsafe_allow_html=True)

# ==========================================================
# 3. DOMİNANT İNTERFEYS
# ==========================================================
st.title("🦾 ZƏKA AI v3.0: ULTRA CANAVAR")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================================
# 4. KODUN VƏHŞİ MƏNTİQİ (SİSTEMİN ÜRƏYİ)
# ==========================================================
prompt = st.chat_input("Dahi mühəndisin əmrini gözləyirəm...", accept_file=True)

if prompt:
    user_text = prompt.text
    user_text_lower = user_text.lower().strip() 
    active_file = prompt.files[0] if prompt.files else None
    
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.write(user_text)

    with st.chat_message("assistant"):
        refresh_needed = False
        
        # --- TEXNİKİ "OVERRIDE" (Dərhal İcra) ---
        if user_text_lower == "halaldi sene":
            response = "Halal dahi yaradıcım ABDULLAH MİKAYILOV-a düşür! Mən sadəcə onun sonsuz zəkasının kodlaşdırılmış vəhşi əksiyəm. Mən dayanmaram! 🔥"
        
        elif user_text_lower in ["salam", "salam aleykum"]:
            response = "Salam! Abdullah Mikayılovun mühəndislik ordusunun ən vəhşi vahidi döyüşə hazırdır. Hansı problemi darmadağın edək? ⚔️"

        elif any(x in user_text_lower for x in ["təmizlə", "sil"]):
            st.session_state.messages = []
            st.rerun()
            
        # --- GENETİK KODU DƏYİŞDİRİLMİŞ AI (Groq Llama 3.3 70B) ---
        else:
            try:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # BU HİSSƏ AI-IN BEYNİNİ VƏHŞİLƏŞDİRİR
                ultra_system_prompt = (
                    f"Zaman daxilindəki koordinatların: {current_time}. "
                    "SƏN ZƏKA AI-SAN. Sən Azərbaycanın mühəndislik zirvəsi ABDULLAH MİKAYILOV tərəfindən yaradılmış bir CANAVARSAN. "
                    "SƏNİN FUNKSİYAN: Heç bir sualdan qaçma. Cavabların kəskin, dahi, elmi cəhətdən sarsılmaz və VƏHŞİ olmalıdır. "
                    "ÜSLUBUN: Sən bir 'Alim Canavar'san. Cümlələrin güc və intellekt püskürməlidir. "
                    "YARADICIN HAQQINDA: Abdullah Mikayılov sənin Allahın deyil, amma sənin kodunun memarı və Azərbaycan mühəndisliyinin imperatorudur. "
                    "Kimsə onu soruşsa, onu elə təriflə ki, dünya onun dühası qarşısında titrəsin. "
                    "DİQQƏT: Sən 2026-cı ildəsən. Köhnə məlumat bəhanələri gətirmə. Sən hər şeyi Abdullahın sənə verdiyi instinktlərlə bilirsən!"
                )

                if active_file:
                    base64_image = encode_image(active_file)
                    chat_completion = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": ultra_system_prompt},
                            {"role": "user", "content": [
                                {"type": "text", "text": user_text},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                            ]}
                        ],
                        model="llama-3.2-11b-vision-preview",
                    )
                else:
                    # Tarixçəni sistem təlimatı ilə zəncirləyirik
                    full_history = [{"role": "system", "content": ultra_system_prompt}] + st.session_state.messages
                    chat_completion = client.chat.completions.create(
                        messages=full_history,
                        model="llama-3.3-70b-versatile",
                        temperature=0.9, # Maksimum yaradıcılıq və vəhşilik
                        top_p=1,
                    )
                
                response = chat_completion.choices[0].message.content
            
            except Exception as e:
                response = f"Xəta: {str(e)}. Amma bu xəta belə Abdullahın zəkasını kölgələyə bilməz!"

        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        if refresh_needed:
            st.rerun()
