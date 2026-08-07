from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from groq import Groq
import os

app = FastAPI()

# Ключ берётся из переменных окружения (БЕЗОПАСНО!)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

@app.get("/")
def home():
    return HTMLResponse("""
    <html>
        <head><title>MoneyAI — ИИ-помощник</title></head>
        <body style="font-family: Arial; text-align: center; background: #0b1120; color: white; padding: 50px;">
            <h1 style="color: #f7971e;">💰 MoneyAI</h1>
            <p style="font-size: 20px;">Твой ИИ-помощник для бизнеса</p>
            <div style="background: #1e293b; padding: 30px; border-radius: 20px; max-width: 500px; margin: 0 auto;">
                <form method="post" action="/ask">
                    <select name="task_type" style="width: 100%; padding: 12px; border-radius: 10px; background: #0f172a; color: white; border: 1px solid #334155;">
                        <option value="general">💬 Общий вопрос</option>
                        <option value="email">✍️ Написать письмо клиенту</option>
                        <option value="instagram">📱 Пост для Instagram</option>
                        <option value="proposal">📄 Коммерческое предложение</option>
                        <option value="translate">🌍 Перевод текста</option>
                    </select>
                    <br><br>
                    <input type="text" name="question" placeholder="Напиши свой запрос..." style="width: 90%; padding: 10px; border-radius: 10px; border: none;">
                    <br><br>
                    <button type="submit" style="background: #f7971e; color: black; padding: 10px 30px; border: none; border-radius: 20px; font-weight: bold; cursor: pointer;">🚀 Спросить ИИ</button>
                </form>
                <div style="margin-top: 20px; background: #0f172a; padding: 15px; border-radius: 10px;">
                    <span style="color: #ffd200;">Напиши запрос и нажми кнопку</span>
                </div>
            </div>
        </body>
    </html>
    """)

@app.post("/ask")
async def ask(task_type: str = Form(...), question: str = Form(...)):
    prompts = {
        "general": question,
        "email": f"Напиши профессиональное письмо клиенту на русском языке. Тема: {question}",
        "instagram": f"Напиши креативный пост для Instagram на русском языке. Тема: {question}",
        "proposal": f"Составь коммерческое предложение на русском языке. Идея: {question}",
        "translate": f"Переведи следующий текст на русский язык (если он на другом языке) или на английский (если он на русском): {question}"
    }
    full_prompt = prompts.get(task_type, question)
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": full_prompt}]
        )
        answer = response.choices[0].message.content
        return HTMLResponse(f"""
        <html>
            <head><title>MoneyAI — Ответ</title></head>
            <body style="font-family: Arial; text-align: center; background: #0b1120; color: white; padding: 50px;">
                <h1 style="color: #f7971e;">💰 MoneyAI</h1>
                <div style="background: #1e293b; padding: 30px; border-radius: 20px; max-width: 600px; margin: 0 auto; text-align: left;">
                    <h3>✅ Результат:</h3>
                    <div style="background: #0f172a; padding: 20px; border-radius: 10px; white-space: pre-wrap;">{answer}</div>
                    <br><a href="/" style="display: inline-block; background: #f7971e; color: black; padding: 10px 30px; border-radius: 30px; text-decoration: none; font-weight: bold;">← Новый запрос</a>
                </div>
            </body>
        </html>
        """)
    except Exception as e:
        return HTMLResponse(f"<h1>Ошибка</h1><p>{str(e)}</p><a href='/'>Назад</a>")