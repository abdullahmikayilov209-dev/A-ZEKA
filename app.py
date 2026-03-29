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

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system", 
            "content": """Sən Zəka AI-san. Səmimi və ağıllı köməkçisən.
            Riyazi ifadələri və kəsrləri izah edərkən onları kod bloku içində (```) göstər ki, oxunması rahat olsun.
            Həmişə Azərbaycan dilində cavab ver."""
        }
    ]

# Mesajları göstərərkən xüsusi tənzimləmə
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            # Əgər mətndə çoxlu riyazi simvol varsa, onu qarışdırmadan göstər
            st.write(message["content"])

if prompt := st.chat_input("Sualınızı bura yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        # Sənin yazdığın o uzun kəsri olduğu kimi göstərmək üçün st.text istifadə edirik
        st.text(prompt) 

    with st.chat_message("assistant"):
        try:
            chat_completion = client.chat.completions.create(
                messages=st.session_state.messages,
                model="llama-3.3-70b-versatile",
                temperature=0.2, # Maksimum dəqiqlik
            )
            response = chat_completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Xəta: {str(e)}")
