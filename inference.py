import requests

BASE = "https://sidtheslayer-email-openenv-agent.hf.space"


def run():
    r = requests.post(f"{BASE}/reset")
    data = r.json()

    obs = data["observation"]
    done = False
    total_reward = 0

    while not done:
        action_type = obs["available_actions"][0]
        action = {"type": action_type}

        if action_type == "classify":
            action["label"] = "billing"

        elif action_type == "route":
            action["department"] = "billing"

        elif action_type == "reply":
            action["response"] = "We are resolving your issue"

        r = requests.post(f"{BASE}/step", json=action)
        data = r.json()

        obs = data["observation"]
        reward = data["reward"]
        done = data["done"]

        total_reward += reward

    print("FINAL SCORE:", total_reward)


if __name__ == "__main__":
    run()