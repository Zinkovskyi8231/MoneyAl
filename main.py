from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, JSONResponse
from groq import Groq
import os

app = FastAPI()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

@app.get("/")
def home():
    return HTMLResponse("""
    <html><head><title>MoneyAI</title></head>
    <body style="background:#0b1120;color:white;text-align:center;padding:50px;font-family:Arial;">
        <h1 style="color:#f7971e;">💰 MoneyAI</h1>
        <p>Твой ИИ-помощник для бизнеса</p>
        <form method="post" action="/ask">
            <input type="text" name="question" placeholder="Напиши запрос...">
            <button type="submit">Отправить</button>
        </form>
    </body></html>
    """)

@app.post("/ask")
async def ask(question: str = Form(...), task_type: str = Form("general")):
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": question}]
        )
        return JSONResponse({"answer": response.choices[0].message.content})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
