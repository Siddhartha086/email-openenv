from fastapi import FastAPI, Body
from email_openenv.environment import EmailOpenEnv
from email_openenv.models import ActionRequest

app = FastAPI()
env = EmailOpenEnv()


# ROOT
@app.get("/")
def root():
    return {"status": "API is running"}


# RESET
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


# 🔥 REQUIRED FOR VALIDATOR
def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()