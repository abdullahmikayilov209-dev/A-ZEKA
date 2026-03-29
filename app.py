import streamlit as st
from groq import Groq

# API açarını Secrets-dən götürürük
try:
    api_key = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.error("Xəta: GROQ_API_KEY tapılmadı! Zəhmət olmasa Secrets bölməsinə əlavə edin.")
    st.stop()

client = Groq(api_key=api_key)

# Səhifənin başlığı
st.set_page_config(page_title="Zəka AI", page_icon="🇦🇿")
st.title("🇦🇿 Milli Süni İntellekt")
st.subheader("Səmimi və Ağıllı Köməkçi")

# Yaddaş və Sistem Təlimatı
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system", 
            "content": """Sən səmimi və ağıllı bir köməkçisən. Adın Zəka AI-dır. 
            TƏLİMATLAR:
            1. Salamlaşanda qısa və səmimi ol (Məs: 'Salam! Buyur, nə sualın var?').
            2. Yalnız sual soruşulanda ətraflı cavab ver.
            3. Həmişə Azərbaycan dilində danış.
            4. Riyazi düstur yazmırsansa, dollar ($) işarəsindən istifadə etmə ki, ekranda səhv görünməsin."""
        }
    ]

# Əvvəlki mesajları göstər
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# İstifadəçi girişi
if prompt := st.chat_input("Sualınızı bura yazın..."):
    # İstifadəçi mesajını yaddaşa əlavə et
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Cavabın generasiyası
    with st.chat_message("assistant"):
        try:
            chat_completion = client.chat.completions.create(
                messages=st.session_state.messages,
                model="llama-3.3-70b-versatile",
                temperature=0.7,
            )
            response = chat_completion.choices[0].message.content
            
            # Cavabı ekrana çıxar və yaddaşa yaz
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Xəta baş verdi: {str(e)}")
