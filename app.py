import streamlit as st
import requests
import base64
import random

# ==========================================================
# 1. EKRAN DİZAYNI VƏ "+" DÜYMƏSİ ÜÇÜN CSS
# ==========================================================
st.set_page_config(page_title="A-Zəka Ultra Alim", page_icon="🧠", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #ffffff; color: #1a1b1e; }
    
    /* Sual qutusunu tənzimləyirik */
    .stChatInputContainer textarea {
        padding-left: 55px !important;
    }

    /* Uploader-i "+" düyməsi kimi sol küncə yerləşdiririk */
    [data-testid="stFileUploader"] {
        position: fixed;
        bottom: 34px !important; 
        left: 48px !important;
        width: 38px !important;
        z-index: 10000;
    }

    /* Bütün artıq yazıları silirik (Drag & Drop, Limit və s.) */
    [data-testid="stFileUploader"] section {
        padding: 0 !important;
        border: none !important;
        background: transparent !important;
    }
    
    [data-testid="stFileUploader"] label, 
    [data-testid="stFileUploader"] small,
    [data-testid="stFileUploaderText"] {
        display: none !important;
    }

    /* Orijinal düyməni təmiz "+" simvolu edirik */
    [data-testid="stFileUploader"] button {
        background-color: transparent !important;
        border: none !important;
        color: #5f6368 !important;
        font-size: 32px !important; 
        width: 35px !important;
        height: 35px !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }

    [data-testid="stFileUploader"] button div { display: none !important; }
    [data-testid="stFileUploader"] button::after {
        content: "+" !important;
        visibility: visible !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================================
# 2. API VƏ YADDAŞ SİSTEMİ
# ==========================================================
API_KEY = "AIzaSyAvjqVkN1DsdCd7uX52TuosAZze_NmbKy0"

if "messages" not in st.session_state:
    st.session_state.messages = []

# ==========================================================
# 3. İNTERFEYS
# ==========================================================
st.title("🧠 A-Zəka Ultra Alim")
st.markdown(f"**Yaradıcı:** Abdullah Mikayılov | **Məkan:** Mingəçevir 🌊")

# Tarixçəni göstər
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg.get("image"):
            st.image(msg["image"], width=300)

# "+" DÜYMƏSİ (Burada faylı qəbul edir)
uploaded_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'])

# ==========================================================
# 4. ANALİZ VƏ CAVAB MƏNTİQİ
# ==========================================================
if prompt := st.chat_input("Dahi alimə sual ver..."):
    # Səmimi Mingəçevir Cavabları (Robotluqdan çıxartmaq üçün)
    clean_p = prompt.lower().strip()
    
    st.session_state.messages.append({"role": "user", "content": prompt, "image": uploaded_file})
    with st.chat_message("user"):
        st.write(prompt)
        if uploaded_file:
            st.image(uploaded_file, width=300)

    with st.chat_message("assistant"):
        # Xüsusi suallar üçün dərhal cavab
        if any(x in clean_p for x in ["harada yaradılıb", "harada yaranmısan", "harda yaradilib"]):
            bot_text = "Mən dahi Abdullah Mikayılov tərəfindən Azərbaycanın energetika mərkəzi olan **Mingəçevir şəhərində** yaradılmışam! 🌊⚡"
            st.write(bot_text)
            st.session_state.messages.append({"role": "assistant", "content": bot_text})
        else:
            with st.spinner("A-Zəka analiz edir..."):
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
                
                system_instruction = "Sən 'A-Zəka'-san. Səni Mingəçevirdə Abdullah Mikayılov yaradıb. Sən çox səmimi, dahi bir Ultra Alimsən. Azərbaycan dilində danış."
                parts = [{"text": f"{system_instruction}\n\nSual: {prompt}"}]
                
                if uploaded_file:
                    b64_image = base64.b64encode(uploaded_file.getvalue()).decode('utf-8')
                    parts.append({
                        "inline_data": {
                            "mimeType": uploaded_file.type,
                            "data": b64_image
                        }
                    })
                
                payload = {"contents": [{"parts": parts}]}
                
                try:
                    response = requests.post(url, json=payload)
                    if response.status_code == 200:
                        bot_text = response.json()['candidates'][0]['content']['parts'][0]['text']
                        st.write(bot_text)
                        st.session_state.messages.append({"role": "assistant", "content": bot_text})
                    else:
                        st.error(f"Xəta: {response.status_code}. API limitini və ya VPN-i yoxla.")
                except Exception as e:
                    st.error(f"Bağlantı xətası: {e}")
