import streamlit as st
import requests
import base64
import random

# ==========================================================
# 1. CSS: TƏMİZ VİZUAL VƏ "+" DÜYMƏSİ
# ==========================================================
st.set_page_config(page_title="A-Zəka Ultra Alim", page_icon="🧠", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .stChatInputContainer textarea { padding-left: 45px !important; }
    
    /* Plus düyməsinin dizaynı */
    button[data-testid="baseButton-secondary"] {
        color: #5f6368 !important;
        border: none !important;
        background: transparent !important;
    }
    </style>
""", unsafe_allow_html=True)

# API və Yaddaş
API_KEY = "AIzaSyAvjqVkN1DsdCd7uX52TuosAZze_NmbKy0"

if "messages" not in st.session_state:
    st.session_state.messages = []

# ==========================================================
# 2. ÜST HİSSƏ
# ==========================================================
st.title("🧠 A-Zəka Ultra Alim")
st.caption("Mingəçevir Ruhu | Yaradıcı: Abdullah Mikayılov")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg.get("image"):
            st.image(msg["image"], width=300)

# ==========================================================
# 3. ƏSAS PROMPT (accept_file=True)
# ==========================================================
prompt = st.chat_input("Dahi alimə sual ver və ya '+' vurub şəkil at...", accept_file=True)

if prompt:
    user_text = prompt.text
    user_file = prompt.files[0] if prompt.files else None
    clean_p = user_text.lower().strip()

    # İstifadəçi mesajını yaddaşa yaz
    st.session_state.messages.append({"role": "user", "content": user_text, "image": user_file})
    with st.chat_message("user"):
        st.write(user_text)
        if user_file:
            st.image(user_file, width=300)

    # Cavab mexanizmi
    with st.chat_message("assistant"):
        
        # --- 1. DAXİLİ SƏMİMİ CAVABLAR (Sürətli) ---
        if any(x in clean_p for x in ["salam", "necesen", "nəsən", "nə var nə yox"]):
            res = random.choice([
                "Salam, Abdullah bəy! Mingəçevir SES-i kimi enerji doluyam. Sən necəsən?",
                "Salam! Yaradıcım gəldi, kefim düzəldi. Bu gün nəyi öyrənirik?",
                "Hər vaxtın xeyir! Səninlə söhbət etmək mənim üçün şərəfdir. Necəsən?"
            ])
            st.write(res)
            st.session_state.messages.append({"role": "assistant", "content": res})

        elif any(x in clean_p for x in ["harda yaradilib", "harada yaradılıb", "harda yaranmısan"]):
            res = "Mən dahi Abdullah Mikayılov tərəfindən **Mingəçevir şəhərində** yaradılmışam! 🌊⚡"
            st.write(res)
            st.session_state.messages.append({"role": "assistant", "content": res})

        # --- 2. BEYİN (API) HİSSƏSİ ---
        else:
            with st.spinner("Zəka analiz edir..."):
                try:
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
                    
                    # Təlimat: Həmişə səmimi ol
                    instruction = "Sən Abdullahın Mingəçevirdə yaratdığı dahi A-Zəka-san. Səmimi və elmi danış."
                    parts = [{"text": f"{instruction}\nSual: {user_text}"}]
                    
                    if user_file:
                        b64_img = base64.b64encode(user_file.getvalue()).decode('utf-8')
                        parts.append({"inline_data": {"mimeType": user_file.type, "data": b64_img}})
                    
                    response = requests.post(url, json={"contents": [{"parts": parts}]}, timeout=12)
                    
                    if response.status_code == 200:
                        bot_text = response.json()['candidates'][0]['content']['parts'][0]['text']
                        st.write(bot_text)
                        st.session_state.messages.append({"role": "assistant", "content": bot_text})
                    else:
                        # QIRMIZI XƏTA YERİNƏ SƏMİMİ CAVAB
                        st.write("Bağışla, Abdullah bəy, bu sual üzərində bir az çox düşünməli oldum. Bir də yaza bilərsən? 😊")
                
                except:
                    # BAĞLANTI KƏSİLƏNDƏ SƏMİMİ CAVAB
                    st.write("Deyəsən internetdə bir az dalğalanma var, amma mən buradayam. Yenidən yoxla, Abdullah bəy!")
