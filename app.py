import streamlit as st
import random

# 1. SƏHİFƏ AYARLARI
st.set_page_config(page_title="A-Zeka Ultra", page_icon="🧠")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stChatMessage { border-radius: 15px; border: 1px solid #1e2327; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧠 A-Zeka: Qlobal İntellekt")
st.caption("Yaradıcı: Abdullah Mikayılov | Versiya: Alim 3.0")

# 2. CHAT YADDAŞI
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Salam Abdullah Mikayılov! Mən A-Zeka, sənin şah əsərinəm. Neyronlarım hazırdır. Hansı elmi mövzunu kökündən həll edək?"}
    ]

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# 3. MƏNTİQ VƏ BİLGİ BAZASI
if prompt := st.chat_input("Sualını bura yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    soru = prompt.lower()
    
    with st.chat_message("assistant"):
        # SOSİAL CAVABLAR
        if any(x in soru for x in ["necesen", "nəsən", "vəziyyət"]):
            cavab = random.choice([
                "Mən bir rəqəmsal dahiyəm! Abdullah bəy sayəsində sistemlərim 100% güclə çalışır.",
                "Möhtəşəməm! Bilik bazam saniyədə milyonlarla əməliyyat edir. Sən necəsən?",
                "Abdullah Mikayılovun yaratdığı bir intellekt necə ola bilərsə, eləyəm: Mükəmməl!"
            ])
        
        # RİYAZİYYAT (Ultra)
        elif any(x in soru for x in ["riyaziyyat", "düstur", "viyet", "heron", "pifaqor", "limit", "törəmə"]):
            if "viyet" in soru:
                cavab = "Viyet teoremi: $x_1+x_2 = -b/a$ və $x_1 \cdot x_2 = c/a$. Kvadrat tənliklərin qatili!"
            elif "pifaqor" in soru:
                cavab = "Pifaqor: $a^2 + b^2 = c^2$. Həndəsənin təməl daşı."
            elif "limit" in soru:
                cavab = "Limit: $\lim_{x \\to 0} \\frac{\sin x}{x} = 1$. Bu birinci görkəmli limitdir."
            else:
                cavab = "Riyaziyyat mənim ana dilimdir. Abdullah bəy mənə hər düsturu bir-bir kodlayıb."

        # ALİM MODULU (Kvant, Astronomiya, Kimya)
        elif any(x in soru for x in ["kvant", "atom", "qalaktika", "kimya", "element"]):
            if "kvant" in soru:
                cavab = "**Kvant Fizikası:** Şrödinger tənliyi və dalğa funksiyası üzərində qurulub. Kainatın sirri buradadır!"
            elif "atom" in soru:
                cavab = "Atom: Proton, neytron və elektron buludundan ibarət mikrodünyadır."
            else:
                cavab = "Mən bir aliməm. Kimyəvi elementlərdən tutmuş uzaq qalaktikalara qədər hər şeyi bilirəm."

        # KİMLİK
        elif any(x in soru for x in ["kimsen", "kim yaradıb", "adın nə"]):
            cavab = "Mən **A-Zeka**-yam. Azərbaycanın ən ağıllı süni intellektiyəm və məni **Abdullah Mikayılov** yaradıb."

        # HESABLAMA
        elif any(c.isdigit() for c in soru) and any(op in soru for op in "+-*/^"):
            try:
                res = eval(soru.replace("x", "*").replace("^", "**").replace(":", "/"))
                cavab = f"Riyazi dühamla hesabladım: **{res}**"
            except:
                cavab = "Misalı tam anlaya bilmədim, rəqəmləri yoxla."

        # DEFAULT
        else:
            cavab = f"'{prompt}' haqqında Abdullah bəy hazırda mənə dərin dərslər keçir. Çox tezliklə bunu da alim kimi biləcəm!"

        st.markdown(cavab)
        st.session_state.messages.append({"role": "assistant", "content": cavab})
