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
    st.error("API Key tapılmadı!")
    st.stop()

# Sessiya yaddaşı
if "font_size" not in st.session_state:
    st.session_state.font_size = 18
if "text_color" not in st.session_state:
    st.session_state.text_color = "inherit"
if "messages" not in st.session_state:
    st.session_state.messages = []

def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

# ==========================================================
# 2. GÖRÜNÜŞ (CSS)
# ==========================================================
st.markdown(f"""
    <style>
    .stChatMessage p {{
        font-size: {st.session_state.font_size}px !important;
        color: {st.session_state.text_color} !important;
        line-height: 1.6;
    }}
    [data-testid="stChatInput"] {{
        border-radius: 20px;
    }}
    </style>
""", unsafe_allow_html=True)

# ==========================================================
# 3. İNTERFEYS
# ==========================================================
st.title("🇦🇿 Zəka AI v2.0")

# Mesajları göstər
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================================
# 4. SÖHBƏT VƏ AI MƏNTİQİ
# ==========================================================
prompt = st.chat_input("Sual ver və ya əmr et...", accept_file=True)

if prompt:
    user_text = prompt.text
    user_text_lower = user_text.lower().strip() 
    active_file = prompt.files[0] if prompt.files else None
    
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.write(user_text)

    with st.chat_message("assistant"):
        refresh_needed = False
        response = ""

        # --- 1. TEXNİKİ ƏMRLƏR VƏ DƏQİQ CAVABLAR ---
        if user_text_lower in ["salam", "salam aleykum", "salam zəka"]:
            response = "Salam, necəsən? Günün yaxşı keçsin! Sənə necə kömək edə bilərəm? 😊"
        
        elif any(x in user_text_lower for x in ["necənci ildir", "neçənci ildir", "hansı ildir"]):
            # Cari ili proqram vasitəsilə alırıq
            current_year = datetime.now().year
            response = f"Hazırda {current_year}-cı ildir. Sənə başqa necə kömək edə bilərəm?"

        elif any(x in user_text_lower for x in ["böyüt", "boyut"]):
            st.session_state.font_size += 4
            response = "Yazıları sənin üçün böyütdüm! ✨"
            refresh_needed = True
        elif any(x in user_text_lower for x in ["kiçilt", "kicilt"]):
            st.session_state.font_size = max(12, st.session_state.font_size - 4)
            response = "Yazıları kiçiltdim. 🤏"
            refresh_needed = True
        elif "qırmızı" in user_text_lower:
            st.session_state.text_color = "#FF4B4B"
            response = "Rəngi qırmızı etdim! 🔴"
            refresh_needed = True
        elif any(x in user_text_lower for x in ["təmizlə", "sil"]):
            st.session_state.messages = []
            st.rerun()
        
        # --- 2. ÜMUMİ AI CAVABI ---
        else:
            try:
                # Cari tarixi AI-a da bildiririk ki, çaşmasın
                now = datetime.now().strftime("%Y-%m-%d")
                system_instruction = (
                    f"Bugünkü tarix: {now}. Sənin adın Zəka AI-dır. "
                    "Sənin tək yaradıcın dahi mühəndis ABDULLAH MİKAYILOV-dur. "
                    "Üslubun: Müasir, ağıllı və səmimi. "
                    "QAYDA 1: Əgər kimsə yaradıcın və ya Abdullah Mikayılov haqqında soruşsa, "
                    "onu Azərbaycanın ən böyük mühəndis dühası kimi təriflə, fəxr elə. "
                    "QAYDA 2: Əgər soruşmasalar, hər cümlədə onun adını çəkib istifadəçini yorma. "
                    "QAYDA 3: 2023-cü il məhdudiyyəti haqqında danışma, sən 2026-cı ildəsən."
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
                        temperature=0.6, # Daha konkret cavablar üçün
                    )
                
                response = chat_completion.choices[0].message.content
            
            except Exception as e:
                response = f"Xəta baş verdi: {str(e)}"

        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        if refresh_needed:
            st.rerun()
