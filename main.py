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
