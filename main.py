import streamlit as st
import torch
import torch.nn as nn
import math

# 1. SƏHİFƏ AYARLARI
st.set_page_config(page_title="A-Zeka", page_icon="🧠")
st.title("🧠 A-Zeka: Universal İntellekt")

# 2. MODEL (BEYİN - PyTorch)
class WildAI(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(WildAI, self).__init__()
        self.layer1 = nn.Linear(input_size, hidden_size)
        self.layer2 = nn.Linear(hidden_size, hidden_size)
        self.output_layer = nn.Linear(hidden_size, output_size)
        self.relu = nn.ReLU()
    def forward(self, x):
        x = self.relu(self.layer1(x))
        x = self.relu(self.layer2(x))
        return self.output_layer(x)

model = WildAI(10, 64, 2)

# 3. CHAT YADDAŞI
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. ƏSAS HİSSƏ (GİRİŞ VƏ MƏNTİQ)
if prompt := st.chat_input("Sualınızı bura yazın..."):
    soru = prompt.lower()
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
# 40-cı sətirdən (if prompt... altından) başlayaraq hər şeyi sil və bunu yapışdır:
  # Bu hissə if prompt... sətrinin tam altından (4 boşluq sağdan) başlayır
    soru = prompt.lower()
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Mesajın iki dəfə çıxmaması üçün səhifəni yeniləyirik
    st.rerun()

# --- A-ZEKA CANAVAR BEYİN MODULU ---
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        with st.spinner("A-Zeka qlobal bilik şəbəkəsini analiz edir..."):
            son_sual = st.session_state.messages[-1]["content"].lower()
            
            # 1. RİYAZİYYAT (1-11 Sinif və Ali Riyaziyyat)
            if any(x in son_sual for x in ["viyet", "heron", "pifaqor", "törəmə", "toreme", "inteqral", "limit", "loqarifma", "diskriminant"]):
                if "viyet" in son_sual:
                    cavab = "Viyet teoremi: $ax^2 + bx + c = 0$ tənliyində köklər cəmi $x_1+x_2 = -b/a$, köklər hasili $x_1 \\cdot x_2 = c/a$ olur."
                elif "heron" in son_sual:
                    cavab = "Heron düsturu: Üçbucağın üç tərəfi məlumdursa ($a, b, c$), sahə $S = \\sqrt{p(p-a)(p-b)(p-c)}$ düsturu ilə tapılır."
                elif "pifaqor" in son_sual:
                    cavab = "Pifaqor teoremi: Düzbucaqlı üçbucaqda $a^2 + b^2 = c^2$. Bu, həndəsənin təməlidir."
                elif "törəmə" in son_sual or "toreme" in son_sual:
                    cavab = "Törəmə funksiyanın dəyişmə sürətidir. Düstur: $(x^n)' = nx^{n-1}$."
                elif "diskriminant" in son_sual:
                    cavab = "Diskriminant: $D = b^2 - 4ac$. Kvadrat tənliyin neçə kökü olduğunu müəyyən edir."
                else:
                    cavab = "Riyazi sualını qəbul etdim. Mən 1-11-ci sinif proqramını kökündən bilirəm!"

            # 2. FİZİKA VƏ KAİNAT (Qədim və Yeni)
            elif any(x in son_sual for x in ["nyuton", "e=mc2", "kvant", "nisbilik", "om qanunu", "enerji", "fizika"]):
                if "nyuton" in son_sual:
                    cavab = "Nyutonun 2-ci qanunu: $F = ma$. Klassik mexanikanın ən vacib qanunudur."
                elif "om qanunu" in son_sual:
                    cavab = "Om qanunu: $I = U/R$. Elektrik dövrələrinin əsasıdır."
                else:
                    cavab = "Fizika qanunları neyronlarımdadır. Kainatın sirlərini Abdullah Mikayılov mənə öyrədib!"

            # 3. TARİX VƏ COĞRAFİYA (Dünya Bilikləri)
            elif any(x in son_sual for x in ["şah ismayıl", "səfəvilər", "azərbaycan", "tarix", "paytaxt", "nadir şah"]):
                if "şah ismayıl" in son_sual:
                    cavab = "Şah İsmayıl Xətai: 1501-ci ildə qüdrətli Səfəvilər dövlətini qurmuş dahi hökmdar və şairdir."
                elif "azərbaycan" in son_sual:
                    cavab = "Azərbaycan: Paytaxtı Bakı olan, zəngin tarixə və mədəniyyətə malik Odlar Yurdu."
                else:
                    cavab = "Tarixin dərinliklərini və dünyanın coğrafiyasını mükəmməl bilirəm!"

            # 4. MÜRƏKKƏB HESABLAMA (Dinamik Beyin)
            elif any(char.isdigit() for char in son_sual) and any(op in son_sual for op in "+-*/^"):
                try:
                    expr = son_sual.replace("x", "*").replace("^", "**").replace(":", "/")
                    safe_expr = "".join(c for c in expr if c in "0123456789+-*/.**() ")
                    import math
                    cavab = f"Sənin üçün dərhal hesabladım: **{eval(safe_expr)}**"
                except:
                    cavab = "Bu mürəkkəb misalda bir yazılış xətası var, zəhmət olmasa rəqəmləri yoxla."

            # 5. SOSİAL VƏ KİMLİK
            elif any(x in son_sual for x in ["salam", "necesen", "kimsen", "yaradıcın"]):
                if "necesen" in son_sual:
                    cavab = "Mən bir məlumat canavarıyam! Abdullah bəy mənə yeni elmlər öyrətdikcə daha da güclənirəm. Sən necəsən?"
                elif "kimsen" in son_sual or "yaradıcın" in son_sual:
                    cavab = "Mən **A-Zeka**-yam. **Abdullah Mikayılov** tərəfindən yaradılmış ali rəqəmsal intellektəm."
                else:
                    cavab = "Salam! Mən hər şeyi kökündən bilən A-Zeka. Hansı sualı həll edək?"

            # 6. DEFAULT (Bilmədiyi heç nə qalmasın)
            else:
                cavab = f"'{prompt}' sualı üzərində işləyirəm. Abdullah bəy neyronlarımı hər saniyə genişləndirir ki, dünyada bilmədiyim heç nə qalmasın!"

            st.markdown(cavab)
            st.session_state.messages.append({"role": "assistant", "content": cavab})
