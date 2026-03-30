import streamlit as st
from groq import Groq
import base64

# ==========================================================
# 1. API SETUP
# ==========================================================
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except:
    st.error("API Key tapılmadı!")
    st.stop()

# İlkin tənzimləmələr
if "font_size" not in st.session_state:
    st.session_state.font_size = 18
if "text_color" not in st.session_state:
    st.session_state.text_color = "inherit"
if "messages" not in st.session_state:
    st.session_state.messages = []

def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

# ==========================================================
# 2. DİNAMİK GÖRÜNÜŞ (CSS)
# ==========================================================
st.markdown(f"""
    <style>
    .stChatMessage p {{
        font-size: {st.session_state.font_size}px !important;
        color: {st.session_state.text_color} !important;
        line-height: 1.6;
    }}
    /* Sual qutusundakı "+" düyməsini qəşəngləşdiririk */
    [data-testid="stChatInput"] {{
        border-radius: 20px;
    }}
    </style>
""", unsafe_allow_html=True)

# ==========================================================
# 3. İNTERFEYS
# ==========================================================
st.title("🇦🇿 Zəka AI v2.0")

# Mesajları göstər
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================================
# 4. SÖHBƏT VƏ AĞILLI İDARƏETMƏ
# ==========================================================
prompt = st.chat_input("Mənə bir sual ver və ya əmr et...", accept_file=True)

if prompt:
    user_text = prompt.text
    user_text_lower = user_text.lower().strip() 
    active_file = prompt.files[0] if prompt.files else None
    
    # Mesajı ekrana və yaddaşa yaz
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.write(user_text)

    # --- BOTUN CAVABI ---
    with st.chat_message("assistant"):
        refresh_needed = False
        
        # --- İNTELLEKTUAL ƏMR ANALİZİ (AI-dan qabaq yoxlanır) ---
        if any(x in user_text_lower for x in ["böyüt", "boyut"]):
            st.session_state.font_size += 4
            response = "Baş üstə, yazıları sənin üçün böyütdüm! İndi daha rahat oxunur? ✨"
            refresh_needed = True
        elif any(x in user_text_lower for x in ["kiçilt", "kicilt"]):
            st.session_state.font_size = max(12, st.session_state.font_size - 4)
            response = "Oldu, yazıları kiçiltdim. Başqa bir istəyin var? 🤏"
            refresh_needed = True
        elif "qırmızı" in user_text_lower:
            st.session_state.text_color = "#FF4B4B"
            response = "Rəngi qırmızıya çevirdim. Diqqətçəkən oldu! 🔴"
            refresh_needed = True
        elif any(x in user_text_lower for x in ["sıfırla", "sifirla"]):
            st.session_state.font_size = 18
            st.session_state.text_color = "inherit"
            response = "Bütün görünüş parametrlərini sıfırladım. Standart rejimdəyik. 🔄"
            refresh_needed = True
        elif any(x in user_text_lower for x in ["təmizlə", "mesajları sil"]):
            st.session_state.messages = []
            st.rerun()
        elif user_text_lower in ["salam", "salam aleykum", "salam zəka"]:
            response = "Salam! Mən Zəka AI. Sənin intellektual köməkçinim. Buyur, nə sualın var? 😊"
        else:
            # Əgər əmrdirsə yox, sualdırsa Groq-a gedirik
            try:
                # BU HİSSƏ BOTUN BEYNİNİ "VƏHŞİ" EDİR
                system_prompt = {
                    "role": "system", 
                    "content": (
                        "Sən Zəka AI-san, Azərbaycan dilində ən mükəmməl intellektsən. "
                        "Sənin missiyan insanlara dəqiq, elmi və səmimi cavablar verməkdir. "
                        "Üslubun Gemini kimidir: müdrik, amma dostyana. "
                        "Cavabların tam dolğun olsun, yarımçıq qoyma. "
                        "Riyazi düsturları və kodları aydın formatda göstər."
                    )
                }

                if active_file:
                    base64_image = encode_image(active_file)
                    chat_completion = client.chat.completions.create(
                        messages=[
                            system_prompt,
                            {"role": "user", "content": [
                                {"type": "text", "text": user_text},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                            ]}
                        ],
                        model="llama-3.2-11b-vision-preview",
                    )
                else:
                    # Bütün söhbət tarixçəsini və sistem promptunu göndəririk
                    full_history = [system_prompt] + st.session_state.messages
                    chat_completion = client.chat.completions.create(
                        messages=full_history,
                        model="llama-3.3-70b-versatile",
                        temperature=0.7, # Yaradıcılıq və məntiqli cavab balansı
                    )
                
                response = chat_completion.choices[0].message.content
            
            except Exception as e:
                response = f"Xəta: {str(e)}"

        # Cavabı göstər və yaddaşa at
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        if refresh_needed:
            st.rerun()
