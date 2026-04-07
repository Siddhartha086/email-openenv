import sys
import os

# Fix module path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import uvicorn
from fastapi import FastAPI
from email_openenv.environment import EmailOpenEnv
from email_openenv.models import ActionRequest

import threading
import time

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

def run_agent_once():
    from inference import run
    time.sleep(2)
    run()

def main():
    threading.Thread(target=run_agent_once, daemon=True).start()
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()