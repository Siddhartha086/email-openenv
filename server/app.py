import uvicorn
from fastapi import FastAPI
from email_openenv.environment import EmailOpenEnv
from email_openenv.models import ActionRequest

import threading
import time

app = FastAPI()
env = EmailOpenEnv()

# ---------------- API ---------------- #

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

# ---------------- INFERENCE RUNNER ---------------- #

def run_agent_once():
    from inference import run
    time.sleep(2)  # wait for server to be ready
    run()

# ---------------- START ---------------- #

def main():
    # Run agent ONLY ONCE in background
    threading.Thread(target=run_agent_once, daemon=True).start()

    # Start API server
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()