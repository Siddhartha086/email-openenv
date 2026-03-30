import requests

BASE = "https://sidtheslayer-email-openenv-agent.hf.space"


def run():
    total_reward = 0

    print("Resetting...")
    r = requests.post(f"{BASE}/reset")
    print(r.json())

    steps = [
        {"type": "classify", "label": "pricing inquiry"},
        {"type": "route", "department": "sales"},
        {"type": "reply", "response": "We will help you shortly."},
        {"type": "resolve"}
    ]

    for s in steps:
        r = requests.post(f"{BASE}/step", json={"action": s})
        res = r.json()

        print("\nSTEP:", s["type"])
        print("Reward:", res["reward"])
        print("Stage:", res["observation"]["current_stage"])

        total_reward += res["reward"]

        if res["done"]:
            break

    print("\nTOTAL REWARD:", total_reward)


if __name__ == "__main__":
    run()