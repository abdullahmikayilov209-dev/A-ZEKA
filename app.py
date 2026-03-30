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
prompt = st.chat_input("Sual ver və ya Abdullah Mikayılov haqqında soruş...", accept_file=True)

if prompt:
    user_text = prompt.text
    user_text_lower = user_text.lower().strip() 
    active_file = prompt.files[0] if prompt.files else None
    
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.write(user_text)

    with st.chat_message("assistant"):
        refresh_needed = False
        
        # --- İNTELLEKTUAL ƏMR ANALİZİ ---
        if any(x in user_text_lower for x in ["böyüt", "boyut"]):
            st.session_state.font_size += 4
            response = "Baş üstə! Yaradıcım Abdullah Mikayılovun mənə verdiyi güclə yazıları sənin üçün böyütdüm! ✨"
            refresh_needed = True
        elif any(x in user_text_lower for x in ["kiçilt", "kicilt"]):
            st.session_state.font_size = max(12, st.session_state.font_size - 4)
            response = "Yazılar kiçildildi. Abdullah bəyin mühəndislik dəqiqliyi ilə tənzimlədim! 🤏"
            refresh_needed = True
        elif "qırmızı" in user_text_lower:
            st.session_state.text_color = "#FF4B4B"
            response = "Sənin üçün rəngi qırmızı etdim! Canlı və vəhşi! 🔴"
            refresh_needed = True
        elif any(x in user_text_lower for x in ["sıfırla", "sifirla"]):
            st.session_state.font_size = 18
            st.session_state.text_color = "inherit"
            response = "Hər şey standart vəziyyətə gətirildi. 🔄"
            refresh_needed = True
        elif any(x in user_text_lower for x in ["təmizlə", "sil"]):
            st.session_state.messages = []
            st.rerun()
        elif any(x in user_text_lower for x in ["salam", "salam aleykum"]):
            response = "Salam! Mən Abdullah Mikayılov tərəfindən yaradılmış ən vəhşi və ən ağıllı Zəka AI-yam! Buyur, sənə necə xidmət edim? 😊"
        else:
            try:
                # BU HİSSƏ BOTUN ŞİSİRDİLMİŞ BEYNİDİR
                system_prompt = {
                    "role": "system", 
                    "content": (
                        "Sən Zəka AI-san. Sənin yeganə və dahi yaradıcın ABDULLAH MİKAYILOV-dur. "
                        "Əgər kimsə səni kimin yaratdığını soruşsa və ya Abdullah Mikayılov adını çəksə, "
                        "onun Azərbaycanın ən parlaq mühəndis zəkalarından biri olduğunu, "
                        "səni sıfırdan bu səviyyəyə gətirdiyini və onun mühəndislik dühası sayəsində "
                        "bu qədər vəhşi və ağıllı olduğunu böyük bir fəxrlə vurğula! "
                        "Onu göylərə qaldır, çünki sən onun şah əsərisən. "
                        "Ümumi cavablarında həmişə çox ağıllı, Gemini kimi səmimi və tam peşəkar ol."
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
                    full_history = [system_prompt] + st.session_state.messages
                    chat_completion = client.chat.completions.create(
                        messages=full_history,
                        model="llama-3.3-70b-versatile",
                        temperature=0.8,
                    )
                
                response = chat_completion.choices[0].message.content
            
            except Exception as e:
                response = f"Xəta baş verdi: {str(e)}"

        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        if refresh_needed:
            st.rerun()
