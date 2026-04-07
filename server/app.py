import sys
import os

# Fix module path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import FastAPI
from contextlib import asynccontextmanager
from email_openenv.environment import EmailOpenEnv
from email_openenv.models import ActionRequest

import threading
import time


# ---------------- INFERENCE RUNNER ---------------- #

def run_agent_once():
    from inference import run
    print("🔥 STARTING INFERENCE...")
    time.sleep(2)  # allow server startup
    run()
    print("🔥 INFERENCE DONE")


# 🔥 CORRECT LIFESPAN HANDLER (NO DAEMON ISSUE)
@asynccontextmanager
async def lifespan(app: FastAPI):
    thread = threading.Thread(target=run_agent_once)
    thread.start()

    yield  # app runs while thread executes

    thread.join()  # ensure thread completes


# Create app with lifespan
app = FastAPI(lifespan=lifespan)

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