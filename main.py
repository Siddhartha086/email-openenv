from fastapi import FastAPI, Request
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
async def step(request: Request):
    body = await request.json()

    # 🔥 HARD FIX (handles ANY format)
    if "action" in body:
        action = body["action"]
    else:
        action = body

    obs, reward, done, info = env.step(action)

    return {
        "observation": obs,
        "reward": reward,
        "done": done,
        "info": info
    }


@app.get("/state")
def state():
    return env.state()