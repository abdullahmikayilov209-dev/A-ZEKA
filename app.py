import streamlit as st
from groq import Groq

# Streamlit Secrets-dən API açarını götürürük
try:
    api_key = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.error("Xəta: GROQ_API_KEY tapılmadı! Zəhmət olmasa Secrets bölməsində qeyd edin.")
    st.stop()

client = Groq(api_key=api_key)

st.title("🤖 Mənim Süni İntellektim")

# Söhbət tarixçəsini yadda saxlayırıq
if "messages" not in st.session_state:
    st.session_state.messages = []

# Əvvəlki mesajları ekranda göstəririk
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# İstifadəçi nəsə yazanda
if prompt := st.chat_input("Sualınızı bura yazın..."):
    # İstifadəçi mesajını göstər və yaddaşa yaz
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Süni İntellektin cavabı
    with st.chat_message("assistant"):
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                model="llama-3.3-70b-versatile",
            )
            response = chat_completion.choices[0].message.content
            st.markdown(response)
            # Cavabı yaddaşa yaz
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Xəta baş verdi: {str(e)}")
