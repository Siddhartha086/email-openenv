import sys
import os
import threading
import time

# Fix module path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import FastAPI
from email_openenv.environment import EmailOpenEnv
from email_openenv.models import ActionRequest


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

    time.sleep(3)  # allow server to start

    print("🔥 STARTING INFERENCE...")
    try:
        run()
    except Exception as e:
        print(f"[ERROR] inference failed: {e}")

    print("🔥 INFERENCE DONE")

    # keep container alive (HF requirement)
    while True:
        time.sleep(60)


# ---------------- ENTRYPOINT (🔥 REQUIRED) ---------------- #

def main():
    import uvicorn

    # start background thread ONLY when running as main
    threading.Thread(target=background_runner, daemon=True).start()

    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()