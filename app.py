import sys
import os

# Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import FastAPI
from email_openenv.environment import EmailOpenEnv
from email_openenv.models import ActionRequest

app = FastAPI()
env = EmailOpenEnv()


# -------- ROOT --------
@app.get("/")
def root():
    return {"status": "API is running"}


# -------- RESET --------
@app.post("/reset")
def reset():
    return env.reset()


# -------- STEP --------
@app.post("/step")
def step(action: ActionRequest):
    return env.step(action.dict())


# -------- STATE --------
@app.get("/state")
def state():
    return env.state