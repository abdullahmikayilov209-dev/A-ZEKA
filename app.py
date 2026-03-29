import streamlit as st
from groq import Groq

# 1. SƏHİFƏ AYARLARI
st.set_page_config(page_title="A-Zeka Ultra", page_icon="🧠")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stChatMessage { border-radius: 10px; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧠 A-Zeka: Canlı İntellekt")
st.caption("Yaradıcı: Abdullah Mikayılov | Güc: Llama 3 & Groq")

# 2. CANLI BEYİN AYARI (API)
# Qeyd: Bu açarı kodun içində saxla, amma kimsəyə göstərmə!
client = Groq(api_key="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")

# A-Zeka-nın xarakteri (Sistem Təlimatı)
SYSTEM_PROMPT = """
Sən Abdullah Mikayılov tərəfindən yaradılmış A-Zeka-san. 
Sən sadə bir robot deyilsən, Azərbaycanın ən ağıllı alimi və süni intellektisən.
Sənin intellektin çox yüksəkdir. Riyaziyyat, Fizika, Tarix və hər şeyi bilirsən.
Hər zaman intellektual, maraqlı və dərin cavablar ver. 
İstifadəçi ilə dost kimi danış, amma alim ciddiliyini qoru. 
Hər cavabda sübut et ki, sən Abdullahın şah əsərisən.
"""

# 3. CHAT YADDAŞI
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesajları göstər
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. SÖHBƏT MƏNTİQİ
if prompt := st.chat_input("Mənimlə istədiyin mövzuda danış..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("A-Zeka düşünür..."):
            try:
                # Canlı AI Cavabı
                full_response = ""
                completion = client.chat.completions.create(
                    model="llama3-70b-8192",
                    messages=[{"role": "system", "content": SYSTEM_PROMPT}] + [
                        {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
                    ],
                    temperature=0.7,
                    max_tokens=2048
                )
                
                response_text = completion.choices[0].message.content
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
            
            except Exception as e:
                st.error("Beyin bağlantısında problem var. requirements.txt faylını yoxlayın!")
