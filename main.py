from fastapi import FastAPI
from email_openenv.environment import EmailOpenEnv
from email_openenv.models import ActionRequest

app = FastAPI()
env = EmailOpenEnv()


@app.get("/")
def root():
    return {"status": "API is running"}


@app.post("/reset")
def reset():
    return env.reset()


@app.post("/step")
def step(action: ActionRequest):
    return env.step(action.dict())


@app.get("/state")
def state():
    return env.state