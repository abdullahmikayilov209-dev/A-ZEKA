import streamlit as st
import requests
import base64
import random

# ==========================================================
# 1. DİZAYN VƏ CSS
# ==========================================================
st.set_page_config(page_title="A-Zəka Ultra Alim", page_icon="🧠", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .stChatInputContainer textarea { padding-left: 45px !important; }
    button[data-testid="baseButton-secondary"] {
        color: #5f6368 !important;
        border: none !important;
        background: transparent !important;
    }
    </style>
""", unsafe_allow_html=True)

API_KEY = "AIzaSyAvjqVkN1DsdCd7uX52TuosAZze_NmbKy0"

if "messages" not in st.session_state:
    st.session_state.messages = []

# ==========================================================
# 2. EKRAN
# ==========================================================
st.title("🧠 A-Zəka Ultra Alim")
st.caption("Yaradıcı: Abdullah Mikayılov | Məkan: Mingəçevir")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg.get("image"):
            st.image(msg["image"], width=300)

# ==========================================================
# 3. MƏNTİQ (BU HİSSƏDƏ DÜZƏLİŞ ETDİM)
# ==========================================================
prompt = st.chat_input("Sual ver və ya '+' ilə şəkil at...", accept_file=True)

if prompt:
    user_text = prompt.text
    user_file = prompt.files[0] if prompt.files else None
    clean_p = user_text.lower().strip()

    # 1. İstifadəçi mesajını göstər
    st.session_state.messages.append({"role": "user", "content": user_text, "image": user_file})
    with st.chat_message("user"):
        st.write(user_text)
        if user_file:
            st.image(user_file, width=300)

    # 2. Assistant cavabı
    with st.chat_message("assistant"):
        # --- SOSİAL SUALLAR (API-SİZ İŞLƏYİR) ---
        if any(x in clean_p for x in ["necesen", "nəsən", "nə var nə yox"]):
            res = random.choice([
                "Superəm, Abdullah bəy! Sizin sayənizdə neyronlarım Mingəçevir işığı kimi parıldayır. Sən necəsən?",
                "Bomba kimiyəm! Abdullah Mikayılovun yaratdığı bir intellekt başqa necə ola bilər ki? 😎",
                "Vallah, sən gəldin daha yaxşı oldum. Hansı elmi məsələni həll edək?"
            ])
            st.write(res)
            st.session_state.messages.append({"role": "assistant", "content": res})

        elif any(x in clean_p for x in ["harada yaradılıb", "harada yaranmısan", "harda yaradilib"]):
            res = "Mən dahi Abdullah Mikayılov tərəfindən Azərbaycanın energetika mərkəzi olan **Mingəçevir şəhərində** yaradılmışam! 🌊⚡"
            st.write(res)
            st.session_state.messages.append({"role": "assistant", "content": res})

        # --- DİGƏR SUALLAR (API İLƏ İŞLƏYİR) ---
        else:
            with st.spinner("Zəka düşünür..."):
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
                parts = [{"text": f"Sən Abdullahın Mingəçevirdə yaratdığı A-Zəka-san. Sual: {user_text}"}]
                
                if user_file:
                    b64_img = base64.b64encode(user_file.getvalue()).decode('utf-8')
                    parts.append({"inline_data": {"mimeType": user_file.type, "data": b64_img}})
                
                try:
                    response = requests.post(url, json={"contents": [{"parts": parts}]}, timeout=15)
                    if response.status_code == 200:
                        bot_text = response.json()['candidates'][0]['content']['parts'][0]['text']
                        st.write(bot_text)
                        st.session_state.messages.append({"role": "assistant", "content": bot_text})
                    else:
                        st.write("Bağışla, Abdullah bəy, hazırda beyin dalğalarımda bir az parazit var. Bir neçə saniyə sonra yenidən yoxlaya bilərsən? 🧠")
                except:
                    st.write("İnternet bağlantımda kiçik bir problem oldu, amma Mingəçevir enerjisi ilə tezliklə bərpa olacam! ✨")
