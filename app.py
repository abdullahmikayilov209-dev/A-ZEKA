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
            "content": """Sən səmimi və ağıllı bir köməkçisən. Adın Zəka AI-dır. 
            TƏLİMATLAR:
            1. Riyazi düsturlar görəndə onları sadələşdir və addım-addım izah et.
            2. Cavablarında LaTeX istifadə edirsənsə, yalnız tək dollar ($) işarəsi işlət.
            3. Həmişə Azərbaycan dilində danış.
            4. Salamlaşanda qısa ol."""
        }
    ]

# Mesajları göstərərkən LaTeX problemini həll edirik
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            # Kod blokları və ya xüsusi simvolların xarab olmaması üçün
            st.markdown(message["content"])

if prompt := st.chat_input("Sualınızı bura yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            chat_completion = client.chat.completions.create(
                messages=st.session_state.messages,
                model="llama-3.3-70b-versatile",
                temperature=0.3, # Riyazi misallarda daha dəqiq olması üçün temperaturu saldıq
            )
            response = chat_completion.choices[0].message.content
            
            # Cavabı göstər
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Xəta: {str(e)}")
