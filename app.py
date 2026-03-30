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
    st.error("API Key tapılmadı!")
    st.stop()

def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

# ==========================================================
# 2. İNTERFEYS DİZAYNI
# ==========================================================
st.title("🇦🇿 Zəka AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ==========================================================
# 3. SÖHBƏT VƏ ŞƏKİL ANALİZİ
# ==========================================================
prompt = st.chat_input("Dahi alimə sual ver və ya şəkil at...", accept_file=True)

if prompt:
    user_text = prompt.text
    active_file = prompt.files[0] if prompt.files else None
    
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.write(user_text)

    with st.chat_message("assistant"):
        try:
            # BOTUN ŞƏXSİYYƏTİ: KONKRET, QISA VƏ TƏBİİ
            system_prompt = (
                "Sən Mingəçevirdə Abdullah tərəfindən yaradılan 'Zəka AI'-san. "
                "Sənin üslubun Gemini kimidir: səmimi, ağıllı və çox konkret. "
                "ƏSLA uzun-uzadı 'nağıl' danışma, fəlsəfə eləmə. "
                "Sual verildikdə qısa, dəqiq və təbii cavab ver. "
                "İstifadəçi 'necəsən' yazanda 'Sağ ol, yaxşıyam, sən necəsən?' kimi qısa və səmimi cavablar ver. "
                "Cümlələrin süni və robotik olmasın. Abdullahın dostu kimi danış, amma sözü uzatma."
            )

            if active_file:
                base64_image = encode_image(active_file)
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": user_text},
                                {
                                    "type": "image_url",
                                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                                },
                            ],
                        }
                    ],
                    model="llama-3.2-11b-vision-preview",
                )
            else:
                chat_completion = client.chat.completions.create(
                    # Burada mesaj tarixinə system prompt-u da əlavə edirik ki, hər dəfə bilsin necə danışmalı olduğunu
                    messages=[{"role": "system", "content": system_prompt}] + st.session_state.messages,
                    model="llama-3.3-70b-versatile",
                )
            
            response = chat_completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        
        except Exception as e:
            st.error(f"Xəta baş verdi: {str(e)}")
