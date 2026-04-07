import sys
import os

# Fix module path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

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


# ---------------- BACKGROUND RUNNER ---------------- #

def background_runner():
    from inference import run
    time.sleep(3)  # wait for server to be fully ready

    print("🔥 STARTING INFERENCE...")
    run()
    print("🔥 INFERENCE DONE")

    # 🔥 KEEP PROCESS ALIVE (CRITICAL FOR HF)
    while True:
        time.sleep(60)


# 🔥 START THREAD IMMEDIATELY (NOT lifespan)
threading.Thread(target=background_runner, daemon=False).start()