from fastapi import FastAPI, Body
from email_openenv.environment import EmailOpenEnv
from email_openenv.models import ActionRequest

app = FastAPI()
env = EmailOpenEnv()


# ROOT
@app.get("/")
def root():
    return {"status": "API is running"}


# RESET (FIXED ✅ — optional body)
@app.post("/reset")
def reset(payload: dict = Body(default={})):
    return env.reset(**payload)


# STEP
@app.post("/step")
def step(action: ActionRequest):
    return env.step(action.dict())


# STATE
@app.get("/state")
def state():
    return env.state