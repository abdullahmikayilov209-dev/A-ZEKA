import streamlit as st
from groq import Groq
import base64

# ==========================================================
# 1. API SETUP VƏ İLKİN AYARLAR
# ==========================================================
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except:
    st.error("API Key tapılmadı!")
    st.stop()

# Yazı ölçüsü və rəngi yaddaşda saxlayırıq
if "font_size" not in st.session_state:
    st.session_state.font_size = 18
if "text_color" not in st.session_state:
    st.session_state.text_color = "inherit" # Standart rəng

def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

# ==========================================================
# 2. DİNAMİK GÖRÜNÜŞ (CSS)
# ==========================================================
# Bu hissə botun əmrlərinə görə dəyişir
st.markdown(f"""
    <style>
    .stChatMessage p {{
        font-size: {st.session_state.font_size}px !important;
        color: {st.session_state.text_color} !important;
    }}
    </style>
""", unsafe_allow_html=True)

# ==========================================================
# 3. İNTERFEYS
# ==========================================================
st.title("🇦🇿 Zəka AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesajları göstər
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ==========================================================
# 4. SÖHBƏT VƏ AĞILLI İDARƏETMƏ
# ==========================================================
prompt = st.chat_input("Sual ver və ya 'yazını böyüt' de...", accept_file=True)

if prompt:
    user_text = prompt.text
    user_text_lower = user_text.lower() # Analiz üçün kiçik hərf
    active_file = prompt.files[0] if prompt.files else None
    
    # --- İNTELLEKTUAL ƏMR ANALİZİ ---
    refresh_needed = False
    
    if "böyüt" in user_text_lower or "boyut" in user_text_lower:
        st.session_state.font_size += 4
        refresh_needed = True
    elif "kiçilt" in user_text_lower or "kicilt" in user_text_lower:
        st.session_state.font_size = max(12, st.session_state.font_size - 4)
        refresh_needed = True
    elif "qırmızı" in user_text_lower:
        st.session_state.text_color = "#FF4B4B"
        refresh_needed = True
    elif "sıfırla" in user_text_lower or "sifirla" in user_text_lower:
        st.session_state.font_size = 18
        st.session_state.text_color = "inherit"
        refresh_needed = True
    elif "mesajları sil" in user_text_lower or "təmizlə" in user_text_lower:
        st.session_state.messages = []
        st.rerun()

    if refresh_needed:
        st.toast("Görünüş yeniləndi! ✨")

    # Mesajı yaddaşa əlavə et
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.write(user_text)

    with st.chat_message("assistant"):
        try:
            system_prompt = (
                "Sən Zəka AI-san. Üslubun Gemini kimidir: səmimi, konkret və ağıllı. "
                "İstifadəçi sənə 'yazını böyüt', 'rəngi dəyiş' və ya 'sil' kimi əmrlər verəndə, "
                "onlara bu əmri yerinə yetirdiyini səmimi şəkildə bildir. "
                "Məsələn: 'Baş üstə, yazıları sənin üçün böyütdüm!' və ya 'Bütün mesajları təmizləyirəm.' "
                "Artıq söz danışma, nağıl eləmə."
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
                chat_completion = client.chat.completions.create(
                    messages=[{"role": "system", "content": system_prompt}] + st.session_state.messages,
                    model="llama-3.3-70b-versatile",
                )
            
            response = chat_completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            if refresh_needed: # CSS dəyişikliyini tətbiq etmək üçün
                st.rerun()
        
        except Exception as e:
            st.error(f"Xəta: {str(e)}")
