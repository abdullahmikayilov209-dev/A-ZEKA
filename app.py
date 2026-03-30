import streamlit as st
from groq import Groq
import base64

# ==========================================================
# 1. API SETUP
# ==========================================================
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except:
    st.error("API Key tapılmadı! Secrets hissəsini yoxlayın.")
    st.stop()

# İlkin tənzimləmələr
if "font_size" not in st.session_state:
    st.session_state.font_size = 18
if "text_color" not in st.session_state:
    st.session_state.text_color = "inherit"
if "messages" not in st.session_state:
    st.session_state.messages = []

def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

# ==========================================================
# 2. DİNAMİK GÖRÜNÜŞ (CSS)
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
# 4. SÖHBƏT VƏ AĞILLI İDARƏETMƏ
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
        
        # --- TEXNİKİ ƏMRLƏR (Görünüş üçün) ---
        if any(x in user_text_lower for x in ["böyüt", "boyut"]):
            st.session_state.font_size += 4
            response = "Baş üstə! Yazıları sənin üçün böyütdüm. ✨"
            refresh_needed = True
        elif any(x in user_text_lower for x in ["kiçilt", "kicilt"]):
            st.session_state.font_size = max(12, st.session_state.font_size - 4)
            response = "Yazılar kiçildildi. 🤏"
            refresh_needed = True
        elif "qırmızı" in user_text_lower:
            st.session_state.text_color = "#FF4B4B"
            response = "Rəngi qırmızı etdim! 🔴"
            refresh_needed = True
        elif any(x in user_text_lower for x in ["təmizlə", "sil"]):
            st.session_state.messages = []
            st.rerun()
        
        # --- SÜNİ İNTELLEKT CAVABI (Salam və digər suallar üçün) ---
        else:
            try:
                system_prompt = {
                    "role": "system", 
                    "content": (
                        "Sən Zəka AI-san. Sənin dahi yaradıcın ABDULLAH MİKAYILOV-dur. "
                        "Sən hər zaman ağıllı, səmimi və professional cavablar verməlisən. "
                        "İstifadəçi salam verəndə təbii cavab ver. "
                        "Yaradıcın haqqında soruşulanda onu Azərbaycanın dahi mühəndisi kimi fəxrlə təriflə. "
                        "Onu 'şişirdə-şişirdə' təqdim et ki, hər kəs onun dühasını bilsin. "
                        "Amma hər cümlənin başında bunu təkrar etmə, yalnız yeri gələndə və soruşulanda de."
                    )
                }

                if active_file:
                    base64_image = encode_image(active_file)
                    chat_completion = client.chat.completions.create(
                        messages=[
                            system_prompt,
                            {"role": "user", "content": [
                                {"type": "text", "text": user_text},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                            ]}
                        ],
                        model="llama-3.2-11b-vision-preview",
                    )
                else:
                    # Salam daxil olmaqla bütün söhbəti AI-a göndəririk
                    full_history = [system_prompt] + st.session_state.messages
                    chat_completion = client.chat.completions.create(
                        messages=full_history,
                        model="llama-3.3-70b-versatile",
                        temperature=0.8,
                    )
                
                response = chat_completion.choices[0].message.content
            
            except Exception as e:
                response = f"Xəta: {str(e)}"

        # Cavabı göstər və yaddaşa yaz
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        if refresh_needed:
            st.rerun()
