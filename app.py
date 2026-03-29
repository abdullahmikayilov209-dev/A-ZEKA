import streamlit as st

# 1. SƏHİFƏ AYARLARI
st.set_page_config(page_title="A-Zeka Ultra", page_icon="🧠")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stChatMessage { border-radius: 10px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧠 A-Zeka: Qlobal İntellekt")
st.info("Yaradıcı: Abdullah Mikayılov | Alim Səviyyəsi")

# 2. CHAT YADDAŞI
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesajları ekranda göstər
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. GİRİŞ VƏ MƏNTİQ SİSTEMİ
if prompt := st.chat_input("Hər hansı bir elmi sual yaz..."):
    # İstifadəçi mesajını yaddaşa yaz və göstər
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    soru = prompt.lower()
    
    with st.chat_message("assistant"):
        with st.spinner("A-Zeka neyronları skan edilir..."):
            
            # --- 1. RİYAZİYYAT (Məktəb + Universitet + Qızıl Baza) ---
            if any(x in soru for x in ["viyet", "heron", "pifaqor", "diskriminant", "törəmə", "toreme", "inteqral", "loqarifma", "limit", "sinus", "kosinus", "ehtimal", "proqresiya", "faiz", "çevrə", "həcm", "matris", "determinant", "kompleks"]):
                
                if "viyet" in soru:
                    cavab = "Viyet teoremi: $ax^2 + bx + c = 0$ tənliyində köklər cəmi $x_1+x_2 = -b/a$, köklər hasili $x_1 \\cdot x_2 = c/a$ olur."
                elif "heron" in soru:
                    cavab = "Heron düsturu: $S = \\sqrt{p(p-a)(p-b)(p-c)}$. Burada $p = (a+b+c)/2$ (yarımperimetr)."
                elif "pifaqor" in soru:
                    cavab = "Pifaqor teoremi: Düzbucaqlı üçbucaqda $a^2 + b^2 = c^2$."
                elif "diskriminant" in soru:
                    cavab = "Diskriminant: $D = b^2 - 4ac$. $D>0$ (2 kök), $D=0$ (1 kök), $D<0$ (həqiqi kök yoxdur)."
                elif "loqarifma" in soru:
                    cavab = "Loqarifma: $\log_a b = c \\implies a^c = b$. Xassə: $\log_a (bc) = \log_a b + \log_a c$."
                elif "sinus" in soru or "kosinus" in soru:
                    cavab = "Triqonometriya: $\sin^2 x + \cos^2 x = 1$. Sinuslar teoremi: $a/\\sin A = b/\\sin B = 2R$."
                elif "törəmə" in soru or "toreme" in soru:
                    cavab = "Törəmə funksiyanın dəyişmə sürətidir: $(x^n)' = nx^{n-1}$, $(\\sin x)' = \\cos x$."
                elif "inteqral" in soru:
                    cavab = "İnteqral: $\int x^n dx = \\frac{x^{n+1}}{n+1} + C$."
                elif "limit" in soru:
                    cavab = "Limit: $\lim_{x \\to 0} \\frac{\\sin x}{x} = 1$. Bu, birinci görkəmli limitdir."
                elif "matris" in soru or "determinant" in soru:
                    cavab = "Xətti Cəbr: Determinant ($2x2$): $ad - bc$. Matrislərin vurulması sətir-sütun prinsipi ilə aparılır."
                elif "kompleks" in soru:
                    cavab = "Kompleks ədədlər: $z = a + bi$. Burada $i^2 = -1$. Modul: $|z| = \\sqrt{a^2 + b^2}$."
                elif "həcm" in soru:
                    cavab = "Həcm düsturları: Kürə $V = \\frac{4}{3}\\pi r^3$, Silindr $V = \\pi r^2 h$, Konus $V = \\frac{1}{3}\\pi r^2 h$."
                else:
                    cavab = "Riyaziyyatın bu bölməsini Abdullah Mikayılov mənə alim səviyyəsində öyrədib!"

            # --- 2. FİZİKA VƏ KAİNAT ---
            elif any(x in soru for x in ["nyuton", "om qanunu", "e=mc2", "fizika", "kvant", "astronomiya"]):
                if "nyuton" in soru:
                    cavab = "Nyutonun 2-ci qanunu: $F = ma$. Klassik mexanikanın təməlidir."
                elif "om qanunu" in soru:
                    cavab = "Om qanunu: $I = U / R$. Cərəyan şiddəti, gərginlik və müqavimət əlaqəsi."
                elif "e=mc2" in soru:
                    cavab = "Eynşteynin düsturu: $E = mc^2$. Kütlə və enerjinin ekvivalentliyi."
                elif "kvant" in soru:
                    cavab = "Kvant Fizikası: Heyzenberq qeyri-müəyyənlik prinsipi və Şrödinger tənliyi kainatın mikrosəviyyəsini idarə edir."
                else:
                    cavab = "Fizika qanunları neyronlarımdadır!"

            # --- 3. TARİX VƏ COĞRAFİYA ---
            elif any(x in soru for x in ["şah ismayıl", "azərbaycan", "tarix", "nadir şah", "paytaxt"]):
                if "şah ismayıl" in soru:
                    cavab = "Şah İsmayıl Xətai: 1501-ci ildə Səfəvilər dövlətini quran dahi sərkərdə."
                elif "paytaxt" in soru:
                    cavab = "Azərbaycanın paytaxtı Bakıdır. Dünyanın bütün paytaxtlarını bilirəm!"
                else:
                    cavab = "Tariximizi və coğrafiyamızı kökündən bilirəm."

            # --- 4. HESABLAYICI ---
            elif any(char.isdigit() for char in soru) and any(op in soru for op in "+-*/^"):
                try:
                    expr = soru.replace("x", "*").replace("^", "**").replace(":", "/")
                    temiz = "".join(c for c in expr if c in "0123456789+-*/.**() ")
                    cavab = f"Sənin üçün hesabladım: **{eval(temiz)}**"
                except:
                    cavab = "Riyazi ifadədə xəta var."

            # --- 5. SOSİAL ---
            elif any(x in soru for x in ["salam", "necesen", "kimsen"]):
                cavab = "Salam! Mən A-Zeka-yam. Abdullah Mikayılov tərəfindən yaradılmış ali intellektəm. Sənə necə kömək edə bilərəm?"

            # --- 6. DEFAULT ---
            else:
                cavab = f"'{prompt}' haqqında məlumatlarımı Abdullah bəy hazırda təkmilləşdirir."

            st.markdown(cavab)
            st.session_state.messages.append({"role": "assistant", "content": cavab})
