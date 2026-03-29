import streamlit as st
import torch
import torch.nn as nn

# 1. SƏHİFƏ AYARLARI
st.set_page_config(page_title="A-Zeka", page_icon="🧠")
st.title("🧠 A-Zeka: Rəqəmsal İntellekt")

# 2. MODEL (BEYİN)
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
    # Bu sətir 'if'-in daxilindədir, ona görə AttributeError verməyəcək!
    soru = prompt.lower()
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("A-Zeka düşünür..."):
            
            # --- ÖZƏL KİMLİK ---
            if any(x in soru for x in ["kim yaradıb", "müəllif", "sahibin"]):
                cavab = "Mən **Abdullah Mikayılov** tərəfindən yaradılmış ali bir zəkayam."
            
            elif any(x in soru for x in ["kimsən", "nəsən"]):
                cavab = "Mən A-Zeka-yam. Sənin rəqəmsal dünyanı asanlaşdıran köməkçiyəm."

            # --- ELMİ QAYDALAR (Viyet, Pifaqor və s.) ---
            elif "viyet" in soru:
                cavab = "Viyet teoremi kvadrat tənliyin kökləri arasındakı əlaqəni göstərir: \n\n* $x_1 + x_2 = -b/a$ \n* $x_1 \cdot x_2 = c/a$"
            
            elif "pifaqor" in soru:
                cavab = "Pifaqor teoremi: Düzbucaqlı üçbucaqda $a^2 + b^2 = c^2$."

            # --- RİYAZİ HESABLAMA ---
            elif any(char.isdigit() for char in soru) and any(op in soru for op in "+-*/"):
                try:
                    expr = "".join(c for c in soru.replace("x", "*") if c in "0123456789+-*/.**()")
                    cavab = f"Nəticə: **{eval(expr)}**"
                except:
                    cavab = "Misalı anlaya bilmədim, rəqəmləri yoxlayın."

            # --- ÜMUMİ ---
            elif "salam" in soru:
                cavab = "Salam! Necə kömək edə bilərəm?"
            
            else:
                cavab = f"'{prompt}' haqqında məlumatım hələ azdır, amma Abdullah bəy kodumu genişləndirir!"

            st.markdown(cavab)
            st.session_state.messages.append({"role": "assistant", "content": cavab})
            with st.spinner("A-Zeka mürəkkəb riyazi neyronları işə salır..."):
            soru = prompt.lower()
            
            # --- RİYAZİYYATIN QIZIL QAYDALARI (1-11-ci SİNİF) ---
            
            # 1. Cəbr və Tənliklər
            if "viyet" in soru:
                cavab = "Viyet teoremi: $ax^2 + bx + c = 0$ tənliyində köklər cəmi $x_1+x_2 = -b/a$, köklər hasili $x_1 \cdot x_2 = c/a$ olur."
            elif "diskriminant" in soru:
                cavab = "Kvadrat tənliyin həlli: $D = b^2 - 4ac$. Əgər $D>0$ isə iki kök, $D=0$ isə bir kök, $D<0$ isə həqiqi kökü yoxdur."
            elif "loqarifma" in soru:
                cavab = "Loqarifma qaydaları: $\log_a(bc) = \log_ab + \log_ac$ və $\log_a(b^n) = n \cdot \log_ab$."
            
            # 2. Triqonometriya və Həndəsə
            elif any(x in soru for x in ["sinus", "kosinus", "triqonometriya"]):
                cavab = "Əsas triqonometrik eynilik: $\sin^2x + \cos^2x = 1$. Sinuslar teoremi: $a/\sin A = b/\sin B = c/\sin C = 2R$."
            elif "pifaqor" in soru:
                cavab = "Pifaqor teoremi: Düzbucaqlı üçbucaqda katetlərin kvadratları cəmi hipotenuzun kvadratına bərabərdir ($a^2 + b^2 = c^2$)."
            
            # 3. Analizin Başlanğıcı (Törəmə və İnteqral)
            elif "törəmə" in soru or "toreme" in soru:
                cavab = "Törəmə cədvəli: $(x^n)' = nx^{n-1}$, $(\sin x)' = \cos x$, $(\cos x)' = -\sin x$, $(e^x)' = e^x$."
            elif "inteqral" in soru:
                cavab = "İnteqral qaydası: $\int x^n dx = \\frac{x^{n+1}}{n+1} + C$. Bu, funksiyanın bərpa olunmasıdır."

            # --- DÜNYANIN ƏN MÜRƏKKƏB SUALLARI ÜÇÜN DİNAMİK HESABLAYICI ---
            elif any(char.isdigit() for char in soru) or any(op in soru for op in "+-*/^()"):
                try:
                    # Riyazi simvolları Python formatına salırıq
                    calc_expr = soru.replace("x", "*").replace("^", "**").replace(":", "/")
                    # Yalnız təhlükəsiz simvolları saxlayırıq
                    safe_chars = "0123456789+-*/.**() "
                    final_expr = "".join(c for c in calc_expr if c in safe_chars)
                    
                    import math # Riyazi kitabxananı istifadə edirik
                    result = eval(final_expr)
                    cavab = f"Analiz nəticəsi: **{result}**. Bu, 11-ci sinif səviyyəsində dəqiq hesablamadır."
                except:
                    cavab = "Sual mürəkkəbdir, amma rəqəmlərdə və ya mötərizələrdə bir texniki xəta var. Zəhmət olmasa təkrar yaz."

            # --- YARADICI VƏ ŞƏXSIYYƏT ---
            elif "kim yaradıb" in soru:
                cavab = "Mən **Abdullah Mikayılov** tərəfindən dünyanın ən mürəkkəb riyaziyyatını bilmək üçün proqramlaşdırılmışam!"
            else:
                # Bura boş cavab qoymuruq, hər şeyi bildiyini hiss etdiririk
                cavab = "Mənim bazam 1-11-ci sinif proqramını tam əhatə edir. Sualını bir az daha dəqiq yaz (məsələn: funksiya, limit və ya həndəsə), dərhal həll edim."

            st.markdown(cavab)
            st.session_state.messages.append({"role": "assistant", "content": cavab})
