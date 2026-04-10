from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# ✅ Correct input format for OpenEnv
class InputData(BaseModel):
    input: str

# ✅ Required endpoint
@app.post("/reset")
def reset():
    return {"status": "ok"}

# ✅ Required endpoint
@app.post("/step")
def step(data: InputData):
    user_input = data.input

    # 🔥 Your logic (you can change this part later)
    result = f"You said: {user_input}"

    # ✅ VERY IMPORTANT: return format
    return {
        "output": result
    }