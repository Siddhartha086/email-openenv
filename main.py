from fastapi import FastAPI
from env.environment import EmailEnv

app = FastAPI()
env = EmailEnv()


@app.get("/")
def root():
    return {"status": "API is running"}


@app.post("/reset")
def reset():
    obs = env.reset()
    return {
        "observation": obs.dict(),
        "reward": 0.0,
        "done": False,
        "info": {}
    }


@app.post("/step")
def step(action: dict):
    # ✅ CRITICAL FIX (your main bug)
    actual_action = action.get("action", action)

    obs, reward, done, info = env.step(actual_action)

    return {
        "observation": obs,
        "reward": reward,
        "done": done,
        "info": info
    }


@app.get("/state")
def state():
    return env.state()