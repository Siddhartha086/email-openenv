import requests

BASE_URL = "http://localhost:7860"


def run():
    res = requests.post(f"{BASE_URL}/reset")
    data = res.json()

    done = False
    steps = 0

    while not done and steps < 10:
        obs = data["observation"]
        stage = obs["current_stage"]

        if stage == "start":
            action = {"action_type": "classify", "payload": "urgent"}
        elif stage == "classified":
            action = {"action_type": "route", "payload": "billing"}
        elif stage == "routed":
            action = {"action_type": "reply", "payload": "We are resolving your issue"}
        elif stage == "replied":
            action = {"action_type": "resolve"}
        else:
            action = {"action_type": "noop"}

        res = requests.post(f"{BASE_URL}/step", json=action)
        data = res.json()

        print("Step:", steps, "Reward:", data["reward"])
        done = data["done"]
        steps += 1


if __name__ == "__main__":
    run()