from fastapi import FastAPI
from server.email_env_environment import EmailEnvironment
from models import EmailAction

app = FastAPI()
env = EmailEnvironment()


@app.get("/")
def root():
    return {"message": "Email Triage Environment Running 🚀"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/reset")
def reset():
    obs = env.reset()
    return obs.model_dump()


@app.post("/step")
def step(action: EmailAction):
    obs = env.step(action)
    return obs.model_dump()


@app.get("/state")
def state():
    return {
        "episode_id": env.state.episode_id,
        "step_count": env.state.step_count,
    }


# 🔥 REQUIRED FOR OPENENV
def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=8000)


# 🔥 REQUIRED ENTRY POINT
if __name__ == "__main__":
    main()