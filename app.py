import streamlit as st
import requests
import base64

# ==========================================================
# 1. CSS: st.chat_input-un daxili "+" düyməsini düzəldirik
# ==========================================================
st.set_page_config(page_title="A-Zəka Ultra Alim", page_icon="🧠", layout="wide")

st.markdown("""
    <style>
    /* Sual qutusunun fonu və yazısı */
    .stChatInputContainer {
        background-color: transparent !important;
    }
    
    /* Streamlit-in daxili yükləmə düyməsini (clippit) "+" simvoluna çeviririk */
    [data-testid="stChatInputSubmit"] {
        color: #5f6368 !important;
    }

    /* Sol tərəfdəki o balaca "+" düyməsinin dizaynı */
    button[data-testid="baseButton-secondary"] {
        border: none !important;
        background-color: transparent !important;
        font-size: 25px !important;
        color: #5f6368 !important;
    }
    
    /* "Drag and drop" yazısını və digər artıqları bu funksiyada Streamlit özü gizlədir, 
       biz sadəcə rəngləri və səmimiyyəti qoruyuruq */
    </style>
""", unsafe_allow_html=True)

# ==========================================================
# 2. API VƏ YADDAŞ
# ==========================================================
API_KEY = "AIzaSyAvjqVkN1DsdCd7uX52TuosAZze_NmbKy0"

if "messages" not in st.session_state:
    st.session_state.messages = []

# ==========================================================
# 3. İNTERFEYS
# ==========================================================
st.title("🧠 A-Zəka Ultra Alim")
st.markdown(f"**Yaradıcı:** Abdullah Mikayılov | **Məkan:** Mingəçevir 🌊")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if "image" in msg and msg["image"]:
            st.image(msg["image"], width=300)

# ==========================================================
# 4. SƏNİN İSTƏDİYİN O PROMPT (accept_file=True ilə)
# ==========================================================
prompt = st.chat_input("Dahi alimə sual ver və ya '+' vurub şəkil at...", accept_file=True)

if prompt:
    user_text = prompt.text
    # Birdən çox şəkil ola bilər, biz birincini götürürük
    user_file = prompt.files[0] if prompt.files else None

    # Mesajı yaddaşa əlavə et
    st.session_state.messages.append({"role": "user", "content": user_text, "image": user_file})
    
    with st.chat_message("user"):
        st.write(user_text)
        if user_file:
            st.image(user_file, width=300)

    with st.chat_message("assistant"):
        # Mingəçevir və Yaradıcı haqqında xüsusi məntiq
        clean_p = user_text.lower().strip()
        if any(x in clean_p for x in ["harada yaradılıb", "harada yaranmısan", "harda yaradilib"]):
            bot_text = "Mən dahi Abdullah Mikayılov tərəfindən Azərbaycanın energetika mərkəzi olan **Mingəçevir şəhərində** yaradılmışam! 🌊⚡"
            st.write(bot_text)
            st.session_state.messages.append({"role": "assistant", "content": bot_text})
        else:
            with st.spinner("A-Zəka analiz edir..."):
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
                
                system_instruction = "Sən 'A-Zəka'-san. Səni Mingəçevirdə Abdullah Mikayılov yaradıb. Çox səmimi və dahi alimsən."
                parts = [{"text": f"{system_instruction}\n\nİstifadəçi sualı: {user_text}"}]
                
                if user_file:
                    b64_image = base64.b64encode(user_file.getvalue()).decode('utf-8')
                    parts.append({
                        "inline_data": {
                            "mimeType": user_file.type,
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
                        st.error("API Xətası. VPN-i yoxla.")
                except Exception as e:
                    st.error(f"Bağlantı xətası: {e}")
