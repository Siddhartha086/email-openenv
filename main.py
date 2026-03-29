from fastapi import FastAPI, Body
from env.environment import EmailEnv

app = FastAPI()

env = EmailEnv()

@app.post("/reset")
def reset():
    obs = env.reset()
    return {
        "observation": obs.dict() if hasattr(obs, "dict") else obs,
        "reward": 0.0,
        "done": False,
        "info": {}
    }

@app.post("/step")
def step(action: dict = Body(...)):
    obs, reward, done, info = env.step(action)
    return {
        "observation": obs.dict() if hasattr(obs, "dict") else obs,
        "reward": reward,
        "done": done,
        "info": info
    }

@app.get("/state")
def state():
    return env.state()