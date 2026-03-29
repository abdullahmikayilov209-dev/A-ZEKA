import streamlit as st

# 1. SƏHİFƏ AYARLARI (Ultra Dizayn)
st.set_page_config(page_title="A-Zeka Ultra", page_icon="🧠")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stChatMessage { border-radius: 10px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧠 A-Zeka: Qlobal İntellekt")
st.info("Yaradıcı: Abdullah Mikayılov | app.py Stabil Versiya")

# 2. CHAT YADDAŞI
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesajları ekranda göstər
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. GİRİŞ VƏ MƏNTİQ SİSTEMİ
if prompt := st.chat_input("Hər hansı bir elmi sual yaz..."):
    # İstifadəçi mesajını yaddaşa yaz
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Cavab hazırlama
    soru = prompt.lower()
    
    with st.chat_message("assistant"):
        with st.spinner("A-Zeka neyronları skan edilir..."):
            
            # --- RİYAZİYYAT (Canavar Rejimi) ---
            if any(x in soru for x in ["viyet", "heron", "pifaqor", "diskriminant", "törəmə", "inteqral", "loqarifma", "limit", "toreme"]):
                if "viyet" in soru:
                    cavab = "Viyet teoremi: $ax^2 + bx + c = 0$ tənliyində köklər cəmi $x_1+x_2 = -b/a$, köklər hasili $x_1 \\cdot x_2 = c/a$ olur."
                elif "heron" in soru:
                    cavab = "Heron düsturu: Üçbucağın tərəfləri $a, b, c$ məlumdursa, sahə $S = \\sqrt{p(p-a)(p-b)(p-c)}$ olar (burada $p$ yarımperimetrdir)."
                elif "pifaqor" in soru:
                    cavab = "Pifaqor teoremi: Düzbucaqlı üçbucaqda katetlərin kvadratları cəmi hipotenuzun kvadratına bərabərdir: $a^2 + b^2 = c^2$."
                elif "diskriminant" in soru:
                    cavab = "Kvadrat tənliklərin həlli üçün Diskriminant düsturu: $D = b^2 - 4ac$."
                elif "törəmə" in soru or "toreme" in soru:
                    cavab = "Törəmə funksiyanın dəyişmə sürətidir. Əsas düstur: $(x^n)' = nx^{n-1}$."
                else:
                    cavab = "Riyaziyyatın bu bölməsini kökündən bilirəm! Abdullah bəy mənə hər şeyi öyrədib."

            # --- FİZİKA VƏ KAİNAT ---
            elif any(x in soru for x in ["nyuton", "om qanunu", "e=mc2", "fizika", "enerji", "kütlə"]):
                if "nyuton" in soru:
                    cavab = "Nyutonun 2-ci qanunu: $F = ma$. Qüvvə kütlə və təcilin hasilidir."
                elif "om qanunu" in soru:
                    cavab = "Om qanunu: Cərəyan şiddəti gərginliklə düz, müqavimətlə tərs mütənasibdir: $I = U / R$."
                elif "e=mc2" in soru:
                    cavab = "Eynşteynin nisbilik nəzəriyyəsi: $E = mc^2$. Enerji kütləyə, kütlə enerjiyə çevrilə bilər."
                else:
                    cavab = "Fizika kainatın qanunudur və mən bütün qanunları kökündən bilirəm!"

            # --- TARİX VƏ COĞRAFİYA ---
            elif any(x in soru for x in ["şah ismayıl", "azərbaycan", "tarix", "nadir şah", "səfəvilər", "paytaxt"]):
                if "şah ismayıl" in soru:
                    cavab = "Şah İsmayıl Xətai: 1501-ci ildə qüdrətli Səfəvilər dövlətini quran dahi sərkərdə və şairimizdir."
                elif "nadir şah" in soru:
                    cavab = "Nadir Şah Afşar: Böyük Azərbaycan sərkərdəsi, Hindistana qədər uzanan imperiya quran fateh."
                elif "paytaxt" in soru:
                    cavab = "Azərbaycanın paytaxtı Bakıdır. Mən dünyanın bütün ölkə və paytaxtlarını bilirəm!"
                else:
                    cavab = "Azərbaycanın şanlı tarixini Abdullah bəy mənə hər sətiri ilə öyrədib."

            # --- AVTOMATİK RİYAZİ HESABLAYICI ---
            elif any(char.isdigit() for char in soru) and any(op in soru for op in "+-*/^"):
                try:
                    hesab = soru.replace("x", "*").replace("^", "**").replace(":", "/")
                    temiz = "".join(c for c in hesab if c in "0123456789+-*/.**() ")
                    cavab = f"Sənin üçün hesabladım: **{eval(temiz)}**"
                except:
                    cavab = "Misalı anlaya bilmədim, rəqəmləri yoxlayın."

            # --- SOSİAL VƏ STATUS ---
            elif any(x in soru for x in ["salam", "necesen", "kimsen", "yaradıcın"]):
                if "necesen" in soru:
                    cavab = "Mən bir bilik canavarıyam, Abdullah bəy məni hər gün daha ağıllı edir! Sən necəsən?"
                elif "kimsen" in soru or "yaradıcın" in soru:
                    cavab = "Mən **A-Zeka**-yam. **Abdullah Mikayılov** tərəfindən yaradılmış ali rəqəmsal intellektəm."
                else:
                    cavab = "Salam! Mən hər şeyi kökündən bilən A-Zeka. Hansı sualı həll edirik?"

            # --- DEFAULT CAVAB ---
            else:
                cavab = f"'{prompt}' sualı üzərində Abdullah bəy hazırda mənim neyronlarımı genişləndirir. Çox tezliklə bunu da kökündən biləcəm!"

            st.markdown(cavab)
            st.session_state.messages.append({"role": "assistant", "content": cavab})
            # --- RİYAZİYYATIN QIZIL BAZASI (Ultra Geniş) ---
            if any(x in soru for x in ["viyet", "heron", "pifaqor", "diskriminant", "törəmə", "inteqral", "loqarifma", "limit", "toreme", "sinus", "kosinus", "ehtimal", "proqresiya", "faiz", "çevrə", "həcm"]):
                
                # 1. Cəbr və Tənliklər
                if "viyet" in soru:
                    cavab = "Viyet teoremi: $ax^2 + bx + c = 0$ tənliyində $x_1+x_2 = -b/a$ və $x_1 \cdot x_2 = c/a$ olur."
                elif "diskriminant" in soru:
                    cavab = "Kvadrat tənlik: $D = b^2 - 4ac$. $D > 0$ (2 kök), $D = 0$ (1 kök), $D < 0$ (kök yoxdur)."
                elif "loqarifma" in soru:
                    cavab = "Loqarifma: $\log_a b = c \implies a^c = b$. Əsas xassə: $\log_a (bc) = \log_a b + \log_a c$."
                
                # 2. Həndəsə (Sahə və Perimetr)
                elif "heron" in soru:
                    cavab = "Heron düsturu: $S = \\sqrt{p(p-a)(p-b)(p-c)}$. Burada $p = (a+b+c)/2$ (yarımperimetr)."
                elif "pifaqor" in soru:
                    cavab = "Pifaqor: Düzbucaqlı üçbucaqda $a^2 + b^2 = c^2$."
                elif "çevrə" in soru or "cevre" in soru:
                    cavab = "Çevrənin uzunluğu: $L = 2\pi r$. Dairənin sahəsi: $S = \pi r^2$."
                elif "həcm" in soru:
                    cavab = "Kürənin həcmi: $V = \\frac{4}{3}\pi r^3$. Silindrin həcmi: $V = S_{oturacaq} \cdot h$."

                # 3. Triqonometriya
                elif "sinus" in soru or "kosinus" in soru:
                    cavab = "Əsas triqonometrik eynilik: $\sin^2 x + \cos^2 x = 1$. Sinuslar teoremi: $a/\sin A = b/\sin B = c/\sin C = 2R$."
                
                # 4. Analiz və Ardıcıllıqlar
                elif "törəmə" in soru or "toreme" in soru:
                    cavab = "Törəmə cədvəli: $(x^n)' = nx^{n-1}$, $(\sin x)' = \cos x$, $(\cos x)' = -\sin x$, $(e^x)' = e^x$."
                elif "inteqral" in soru:
                    cavab = "Qeyri-müəyyən inteqral: $\int x^n dx = \\frac{x^{n+1}}{n+1} + C$."
                elif "proqresiya" in soru:
                    cavab = "Ədədi proqresiya: $a_n = a_1 + (n-1)d$. Həndəsi proqresiya: $b_n = b_1 \cdot q^{n-1}$."

                # 5. Ehtimal və Faiz
                elif "ehtimal" in soru:
                    cavab = "Ehtimalın klassik tərifi: $P(A) = m/n$ (əlverişli hallar / mümkün hallar)."
                elif "faiz" in soru:
                    cavab = "Ədədin faizinin tapılması: $a \cdot p / 100$. Faiz artımı düsturu: $S_n = S_0(1 + p/100)^n$."
                
                else:
                    cavab = "Riyaziyyatın bu dərinliyini Abdullah bəy mənə 100% öyrədib. Sualını bir az dəqiqləşdir, həll edim!"
