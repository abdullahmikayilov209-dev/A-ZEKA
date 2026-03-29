import streamlit as st
from groq import Groq
import PIL.Image # Şəkillərlə işləmək üçün

# API açarını Secrets-dən götürürük
try:
    api_key = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.error("Xəta: GROQ_API_KEY tapılmadı!")
    st.stop()

client = Groq(api_key=api_key)

st.set_page_config(page_title="Zəka AI", page_icon="🇦🇿", layout="wide")

# SOL PANEL (Sidebar) - Şəkil yükləmək üçün "+" funksiyası burada olacaq
with st.sidebar:
    st.title("➕ Seçimlər")
    uploaded_file = st.file_uploader("Sualın şəklini çək və ya yüklə", type=['png', 'jpg', 'jpeg'])
    if uploaded_file:
        image = PIL.Image.open(uploaded_file)
        st.image(image, caption='Yüklənən şəkil', use_container_width=True)
        st.success("Şəkil yükləndi! İndi sualınızı yazın.")

st.title("🇦🇿 Zəka AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesajları göstər
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "user":
            st.text(message["content"])
        else:
            st.markdown(message["content"])

# Giriş hissəsi
if prompt := st.chat_input("Sualınızı yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.text(prompt)

    with st.chat_message("assistant"):
        try:
            # Əgər şəkil yüklənibsə, Sİ-yə şəkli təsvir etməyi tapşırırıq
            # QEYD: Groq Vision üçün model adını dəyişməliyik (məsələn: llama-3.2-11b-vision-preview)
            
            model_name = "llama-3.3-70b-versatile"
            system_msg = "Sən Zəka AI-san. Riyazi misalları və sualları Azərbaycan dilində dəqiq həll edirsən."
            
            if uploaded_file:
                system_msg += " İstifadəçi həmçinin bir şəkil yükləyib. Şəkildəki məlumatları nəzərə al."

            chat_completion = client.chat.completions.create(
                messages=[{"role": "system", "content": system_msg}] + st.session_state.messages,
                model=model_name,
                temperature=0.2,
            )
            
            response = chat_completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Xəta: {str(e)}")
