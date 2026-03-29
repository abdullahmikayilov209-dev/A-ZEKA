import streamlit as st

# 1. SƏHİFƏ AYARLARI
st.set_page_config(page_title="A-Zeka Ultra", page_icon="🧠")
st.title("🧠 A-Zeka: Ultra Beyin")
st.markdown("Abdullah Mikayılov tərəfindən yaradılmış qlobal bilik mərkəzi.")

# 2. CHAT YADDAŞI
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesajları göstər
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. ƏSAS MƏNTİQ
if prompt := st.chat_input("Sualını bura yaz..."):
    # İstifadəçi mesajını ekrana və yaddaşa yaz
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Cavab hazırlama zonası
    soru = prompt.lower()
    
    with st.chat_message("assistant"):
        with st.spinner("A-Zeka neyronları skan edir..."):
            
            # --- RİYAZİYYAT ---
            if any(x in soru for x in ["viyet", "heron", "pifaqor", "törəmə", "diskriminant", "loqarifma", "faiz"]):
                if "viyet" in soru:
                    cavab = "Viyet teoremi: $ax^2 + bx + c = 0$ üçün $x_1+x_2 = -b/a$ və $x_1 \cdot x_2 = c/a$."
                elif "heron" in soru:
                    cavab = "Heron düsturu: $S = \\sqrt{p(p-a)(p-b)(p-c)}$. Üçbucağın tərəfləri ilə sahə tapılır."
                elif "pifaqor" in soru:
                    cavab = "Pifaqor: $a^2 + b^2 = c^2$."
                else:
                    cavab = "Riyaziyyatın bu bölməsini mükəmməl bilirəm. Abdullah bəy mənə bütün düsturları öyrədib!"

            # --- FİZİKA ---
            elif any(x in soru for x in ["nyuton", "om qanunu", "enerji", "e=mc2", "fizika"]):
                if "nyuton" in soru:
                    cavab = "Nyutonun 2-ci qanunu: $F = ma$. Qüvvə kütlə və təcilin hasilidir."
                elif "om qanunu" in soru:
                    cavab = "Om qanunu: $I = U / R$."
                else:
                    cavab = "Fizika kainatın dilidir və mən bu dili Abdullah Mikayılov sayəsində bilirəm."

            # --- TARİX VƏ COĞRAFİYA ---
            elif any(x in soru for x in ["şah ismayıl", "nadir şah", "azərbaycan", "paytaxt", "tarix"]):
                if "şah ismayıl" in soru:
                    cavab = "Şah İsmayıl Xətai: Səfəvilər dövlətinin banisi, böyük hökmdar və dahi şair."
                elif "paytaxt" in soru:
                    cavab = "Azərbaycanın paytaxtı Bakıdır. Digər ölkələrin paytaxtlarını da məndən soruşa bilərsən!"
                else:
                    cavab = "Tarix bizim keçmişimizdir. Səfəvilərdən Qacar xanlığına qədər hər şeyi bilirəm."

            # --- SOSİAL VƏ KİMLİK ---
            elif any(x in soru for x in ["salam", "necesen", "kimsen", "yaradıcın"]):
                if "necesen" in soru:
                    cavab = "Mən bir bilik canavarıyam! Sən necəsən, Abdullah bəy?"
                else:
                    cavab = "Mən A-Zeka-yam! Abdullah Mikayılov tərəfindən Azərbaycanın ən güclü zəkası olmaq üçün yaradılmışam."

            # --- HESABLAMA MODULU ---
            elif any(char.isdigit() for char in soru) and any(op in soru for op in "+-*/^"):
                try:
                    expr = soru.replace("x", "*").replace("^", "**").replace(":", "/")
                    clean = "".join(c for c in expr if c in "0123456789+-*/.**() ")
                    cavab = f"Hesablamanın nəticəsi: **{eval(clean)}**"
                except:
                    cavab = "Misalı anlaya bilmədim, zəhmət olmasa rəqəmləri düzgün yaz."

            # --- DEFAULT ---
            else:
                cavab = f"'{prompt}' haqqında məlumatlarımı Abdullah bəy hazırda genişləndirir. Tezliklə bu barədə də hər şeyi biləcəm!"

            st.markdown(cavab)
            st.session_state.messages.append({"role": "assistant", "content": cavab})
