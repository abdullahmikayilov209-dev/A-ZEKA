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
   # İstifadəçi sualını yaddaşa əlavə edirik (Amma burada dərhal ekrana çap etmirik ki, təkrarlanmasın)
    soru = prompt.lower()
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Səhifəni yeniləyirik ki, mesajlar qaydasında görünsün
    st.rerun()

# Mesajları göstərən hissə (Bu blok if prompt-un çölündə, yuxarıda olmalıdır)
# Əgər yuxarıda artıq varsa, aşağıdakı if-in daxili məntiqinə diqqət yetir:

if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        with st.spinner("A-Zeka riyazi neyronları işə salır..."):
            son_sual = st.session_state.messages[-1]["content"].lower()
            
            # --- RİYAZİYYATIN QIZIL QAYDALARI (Sətir sayını artıran hissə) ---
            if "viyet" in son_sual:
                cavab = "Viyet teoremi: $ax^2 + bx + c = 0$ tənliyində $x_1+x_2 = -b/a$ və $x_1 \cdot x_2 = c/a$ olur."
            
            elif "heron" in son_sual:
                cavab = "Heron düsturu: $S = \\sqrt{p(p-a)(p-b)(p-c)}$. Burada $p$ yarımperimetrdir."
            
            elif "pifaqor" in son_sual:
                cavab = "Pifaqor teoremi: Düzbucaqlı üçbucaqda $a^2 + b^2 = c^2$."
            
            elif "diskriminant" in son_sual:
                cavab = "Kvadrat tənliyin həlli: $D = b^2 - 4ac$."
            
            elif "törəmə" in son_sual or "toreme" in son_sual:
                cavab = "Törəmə qaydası: $(x^n)' = nx^{n-1}$."
            
            elif "inteqral" in son_sual:
                cavab = "İnteqral qaydası: $\int x^n dx = \\frac{x^{n+1}}{n+1} + C$."
                
            elif "loqarifma" in son_sual:
                cavab = "Loqarifma: $\log_a b = c \implies a^c = b$."

            # --- RİYAZİ HESABLAYICI MODUL ---
            elif any(char.isdigit() for char in son_sual) and any(op in son_sual for op in "+-*/^"):
                try:
                    hesab = son_sual.replace("x", "*").replace("^", "**").replace(":", "/")
                    təmiz_hesab = "".join(c for c in hesab if c in "0123456789+-*/.**() ")
                    cavab = f"Hesablamanın nəticəsi: **{eval(təmiz_hesab)}**"
                except:
                    cavab = "Təəssüf ki, bu mürəkkəb misalı həll edə bilmədim. Rəqəmləri yoxlayın."

            # --- DİGƏR CAVABLAR ---
            elif "necesen" in son_sual:
                cavab = "Mən rəqəmsal zəkayam, Abdullah bəy mənə yeni qaydalar öyrətdikcə daha yaxşı oluram!"
            
            elif "salam" in son_sual:
                cavab = "Salam! Mən A-Zeka. Hansı elmi mövzunu araşdırırıq?"

            else:
                cavab = "Bu mövzunu hələ mükəmməl bilmirəm, amma 1-11-ci sinif proqramını öyrənməyə davam edirəm!"

            st.markdown(cavab)
            st.session_state.messages.append({"role": "assistant", "content": cavab})
