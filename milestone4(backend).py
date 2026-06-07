from fastapi import FastAPI
from pydantic import BaseModel
import openai

app = FastAPI()

class TextRequest(BaseModel):
    text: str
    style_prompt: str = "an engaging audiobook style"
    api_key: str

@app.post("/rewrite")
def rewrite_text(req: TextRequest):
    openai.api_key = req.api_key
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert audiobook narrator."},
                {"role": "user", "content": f"Rewrite the following text in {req.style_prompt}:\n\n{req.text}"}
            ],
        )
        return {"rewritten_text": response.choices[0].message.content.strip()}
    except Exception as e:
        return {"error": str(e)}
