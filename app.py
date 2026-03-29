import os
from groq import Groq
from dotenv import load_dotenv

# .env faylındakı məlumatları yükləyirik
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)

def ai_assistant():
    print("🚀 Süni İntellekt Hazırdır! (Çıxmaq üçün 'exit' yazın)\n")
    
    messages = [
        {"role": "system", "content": "Sən ağıllı və köməkçil bir süni intellektsən."}
    ]

    while True:
        user_input = input("Siz: ")
        
        if user_input.lower() == 'exit':
            break
            
        messages.append({"role": "user", "content": user_input})

        try:
            chat_completion = client.chat.completions.create(
                messages=messages,
                model="llama-3.3-70b-versatile",
            )

            ai_response = chat_completion.choices[0].message.content
            print(f"\nAI: {ai_response}\n")
            print("-" * 30)
            
            messages.append({"role": "assistant", "content": ai_response})

        except Exception as e:
            print(f"Xəta: {e}")

if __name__ == "__main__":
    ai_assistant()
