from fastapi import FastAPI
from typing import Dict

app = FastAPI()

env = None

@app.on_event("startup")
def init_env():
    global env
    try:
        from env.environment import EmailEnv
        env = EmailEnv()
        print("✅ EmailEnv initialized")
    except Exception as e:
        print("❌ Failed to initialize EmailEnv:", str(e))
        env = None


@app.get("/")
def home():
    return {"status": "API is running"}


@app.post("/reset")
def reset():
    if env is None:
        return {"error": "Env not initialized"}

    try:
        obs = env.reset()
        return {
            "observation": obs.dict(),
            "reward": 0.0,
            "done": False,
            "info": {}
        }
    except Exception as e:
        return {"error": str(e)}


@app.post("/step")
def step(action: Dict):
    if env is None:
        return {"error": "Env not initialized"}

    try:
        obs, reward, done, info = env.step(action)
        return {
            "observation": obs.dict(),
            "reward": reward,
            "done": done,
            "info": info
        }
    except Exception as e:
        return {"error": str(e)}


@app.get("/state")
def state():
    if env is None:
        return {"error": "Env not initialized"}

    try:
        return env.state()
    except Exception as e:
        return {"error": str(e)}