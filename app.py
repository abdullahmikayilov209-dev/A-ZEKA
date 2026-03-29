import streamlit as st
from groq import Groq
import base64

# ... (API açarı və client hissəsi eynidir)

# Şəkli oxumaq üçün köməkçi funksiya (Groq Vision üçün lazımdır)
def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode('utf-8')

# 1. Şəkil yükləmə "düyməsini" sual qutusunun üstünə qoyuruq
col1, col2 = st.columns([0.1, 0.9])
with col1:
    # Bu düymə vizual olaraq "+" funksiyasını yerinə yetirir
    uploaded_file = st.file_uploader("➕", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")

# 2. Əgər şəkil seçilibsə, onu kiçik formada göstərək ki, yer tutmasın
if uploaded_file:
    st.image(uploaded_file, width=100, caption="Yükləndi")

# 3. Sual qutusu
if prompt := st.chat_input("Sualınızı yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.text(prompt)

    with st.chat_message("assistant"):
        try:
            # ƏGƏR ŞƏKİL VARSA: Vision modelini işə salırıq
            if uploaded_file:
                base64_image = encode_image(uploaded_file)
                model_to_use = "llama-3.2-11b-vision-preview" # Şəkli görən model
                
                messages_with_image = [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                            }
                        ]
                    }
                ]
            else:
                # Şəkil yoxdursa, normal 70B modeli ilə davam edirik
                model_to_use = "llama-3.3-70b-versatile"
                messages_with_image = st.session_state.messages

            chat_completion = client.chat.completions.create(
                messages=messages_with_image,
                model=model_to_use,
                temperature=0.2,
            )
            
            response = chat_completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            st.error(f"Xəta: {str(e)}")
