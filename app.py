import streamlit as st
from groq import Groq

# API açarını Secrets-dən götürürük
try:
    api_key = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.error("Xəta: GROQ_API_KEY tapılmadı!")
    st.stop()

client = Groq(api_key=api_key)

# Səhifənin başlığı və dizaynı
st.set_page_config(page_title="Azərbaycanlı Sİ", page_icon="🇦🇿")
st.title("🇦🇿 Milli Süni İntellekt")
st.subheader("Hər şeyi bilən köməkçiniz")

# Yaddaş tənzimləməsi
if "messages" not in st.session_state:
    # BU HİSSƏ Sİ-Nİ GÜCLƏNDİRİR:
    st.session_state.messages = [
        {
            "role": "system", 
            "content": """Sən çox intellektual, hər sahədə dərin biliyi olan bir köməkçisən. 
            Sənin adın 'Zəka AI'-dır. Sənə verilən bütün sualları dəqiq, elmi və ətraflı cavablandırmalısan.
            VACİB: Həmişə Azərbaycan dilində, rəsmi və nəzakətli bir tonda cavab ver. 
            Azərbaycan mədəniyyəti, tarixi və coğrafiyası haqqında mükəmməl biliyə sahibsən."""
        }
    ]

# Mesajları göstər (Sistem mesajı xaric)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# İstifadəçi girişi
if prompt := st.chat_input("Sualınızı bura yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Llama-3.3-70b ən güclü modeldir, hər şeyi bilir
            chat_completion = client.chat.completions.create(
                messages=st.session_state.messages,
                model="llama-3.3-70b-versatile",
                temperature=0.7, # Yaradıcılıq və dəqiqlik balansı
                max_tokens=2048  # Uzun cavablar üçün limit
            )
            response = chat_completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Xəta: {str(e)}")
