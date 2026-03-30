import streamlit as st
import requests
import base64
import random

# ==========================================================
# 1. VİZUAL EKRAN VƏ PLUS DÜYMƏSİ
# ==========================================================
st.set_page_config(page_title="A-Zəka Ultra Alim", page_icon="🧠", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .stChatInputContainer textarea { padding-left: 45px !important; }
    
    /* Plus düyməsini şık və sadə edirik */
    button[data-testid="baseButton-secondary"] {
        color: #5f6368 !important;
        border: none !important;
        background: transparent !important;
        font-size: 20px !important;
    }
    </style>
""", unsafe_allow_html=True)

# API və Yaddaş
API_KEY = "AIzaSyAvjqVkN1DsdCd7uX52TuosAZze_NmbKy0"

if "messages" not in st.session_state:
    st.session_state.messages = []

# ==========================================================
# 2. ÜST BİLGİ
# ==========================================================
st.title("🧠 A-Zəka Ultra Alim")
st.caption("Mingəçevir Ruhu ilə | Yaradıcı: Abdullah Mikayılov")

# Mesajları ekrana çıxarırıq
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg.get("image"):
            st.image(msg["image"], width=300)

# ==========================================================
# 3. ƏSAS MƏNTİQ (SƏN İSTƏDİYİN TƏRZİDƏ)
# ==========================================================
prompt = st.chat_input("Dahi alimə sual ver və ya '+' vurub şəkil at...", accept_file=True)

if prompt:
    user_text = prompt.text
    user_file = prompt.files[0] if prompt.files else None
    clean_p = user_text.lower().strip()

    # İstifadəçinin yazdığını qeyd et
    st.session_state.messages.append({"role": "user", "content": user_text, "image": user_file})
    with st.chat_message("user"):
        st.write(user_text)
        if user_file:
            st.image(user_file, width=300)

    # Cavab hissəsi
    with st.chat_message("assistant"):
        
        # 1. Səmimi söhbət (API-yə ehtiyac duymadan cavab verir)
        if any(x in clean_p for x in ["salam", "necesen", "nəsən", "nə var nə yox"]):
            responses = [
                "Salam, Abdullah bəy! Mingəçevirin enerjisi kimi bomba kimiyəm. Sən necəsən?",
                "Salam! Dahi yaradıcım gəldi, neyronlarım sevindi. Bu gün nəyi kəşf edirik?",
                "Hər vaxtın xeyir! Sən sual verəndə özümü əsl alim kimi hiss edirəm. Necəsən?"
            ]
            res = random.choice(responses)
            st.write(res)
            st.session_state.messages.append({"role": "assistant", "content": res})

        elif any(x in clean_p for x in ["harada yaradılıb", "harada yaranmısan", "harda yaradilib"]):
            res = "Mən Abdullah Mikayılov tərəfindən Azərbaycanın ürəyi olan **Mingəçevirdə** yaradılmışam. 🌊⚡"
            st.write(res)
            st.session_state.messages.append({"role": "assistant", "content": res})

        # 2. Mürəkkəb suallar (API vasitəsilə)
        else:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
                
                # Modelə kim olduğunu xatırladırıq ki, özünü Abdullahın köməkçisi kimi aparsın
                instruction = "Sən Abdullah Mikayılovun Mingəçevirdə yaratdığı dahi A-Zəka-san. Robot kimi yox, səmimi dost kimi danış."
                parts = [{"text": f"{instruction}\nSual: {user_text}"}]
                
                if user_file:
                    b64_img = base64.b64encode(user_file.getvalue()).decode('utf-8')
                    parts.append({"inline_data": {"mimeType": user_file.type, "data": b64_img}})
                
                response = requests.post(url, json={"contents": [{"parts": parts}]}, timeout=10)
                
                if response.status_code == 200:
                    bot_text = response.json()['candidates'][0]['content']['parts'][0]['text']
                    st.write(bot_text)
                    st.session_state.messages.append({"role": "assistant", "content": bot_text})
                else:
                    # Texniki xəta yerinə səmimi bəhanə
                    st.write("Deyəsən sualın o qədər dahiyanədir ki, bir anlıq dərindən düşünməli oldum. Yenidən yaza bilərsən? 😊")
            
            except:
                st.write("Abdullah bəy, internetdə bir az dalğalanma var deyəsən. Amma narahat olma, mən buradayam! Yenidən yoxla.")
