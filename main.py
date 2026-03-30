from fastapi import FastAPI
from env.environment import EmailEnv

app = FastAPI()
env = EmailEnv()


@app.get("/")
def home():
    return {"status": "API is running"}


@app.post("/reset")
def reset():
    obs = env.reset()
    return {
        "observation": obs,
        "reward": 0.0,
        "done": False,
        "info": {}
    }


@app.post("/step")
def step(action: dict):
    # 🔥 IMPORTANT FIX: extract inner action
    obs, reward, done, info = env.step(action.get("action", {}))

    return {
        "observation": obs,
        "reward": reward,
        "done": done,
        "info": info
    }


@app.get("/state")
def state():
    return env.state()