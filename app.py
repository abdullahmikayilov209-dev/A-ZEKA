import streamlit as st
from groq import Groq

# API açarını Secrets-dən götürürük
try:
    api_key = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.error("Xəta: GROQ_API_KEY tapılmadı!")
    st.stop()

client = Groq(api_key=api_key)

st.set_page_config(page_title="Zəka AI", page_icon="🇦🇿")
st.title("🇦🇿 Milli Süni İntellekt")

# Yaddaş tənzimləməsi
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesajları göstərərkən səninkini "SADƏ MƏTN", AI-nınkını "MARKDOWN" kimi göstəririk
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "user":
            # Sənin yazdığın o uzun kəsrlər burada xarab olmayacaq:
            st.text(message["content"])
        else:
            # AI-nın cavabı normal qaydada (markdown) görünəcək
            st.markdown(message["content"])

# Giriş hissəsi
if prompt := st.chat_input("Sualınızı və ya misalı bura yazın..."):
    # İstifadəçi mesajını yaddaşa əlavə et
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        # Sənin yazdığını ekranda "sadə mətn" kimi göstəririk ki, dağılmasın
        st.text(prompt)

    with st.chat_message("assistant"):
        try:
            # Sistem təlimatını buraya əlavə edirik ki, hər dəfə oxusun
            full_messages = [
                {"role": "system", "content": "Sən Zəka AI-san. Səmimi ol və riyazi misalları addım-addım Azərbaycan dilində izah et."}
            ] + st.session_state.messages

            chat_completion = client.chat.completions.create(
                messages=full_messages,
                model="llama-3.3-70b-versatile",
                temperature=0.2,
            )
            response = chat_completion.choices[0].message.content
            
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Xəta: {str(e)}")
