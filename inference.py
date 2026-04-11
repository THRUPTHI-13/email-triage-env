from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# ✅ Flexible input (accepts ANY fields OpenEnv sends)
class InputData(BaseModel):
    input: Optional[str] = None
    route: Optional[str] = None
    priority: Optional[int] = None

    class Config:
        extra = "allow"   # 🔥 VERY IMPORTANT (accept unknown fields)

# ✅ Required
@app.post("/reset")
def reset():
    return {"status": "ok"}

# ✅ Required
@app.post("/step")
def step(data: InputData):
    # handle different possible inputs
    user_input = data.input or data.route or "default"

    result = f"Processed: {user_input}"

    # ✅ REQUIRED FORMAT
    return {
        "output": result
    }