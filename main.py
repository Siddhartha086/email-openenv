from fastapi import FastAPI
from pydantic import BaseModel

from email_openenv.env.environment import EmailOpenEnv

app = FastAPI()
env = EmailOpenEnv()


class ActionRequest(BaseModel):
    action: dict


@app.get("/")
def root():
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
def step(req: ActionRequest):
    obs, reward, done, info = env.step(req.action)
    return {
        "observation": obs,
        "reward": reward,
        "done": done,
        "info": info
    }


@app.get("/state")
def state():
    return env.state()