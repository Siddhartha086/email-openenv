import requests

BASE = "https://sidtheslayer-email-openenv-agent.hf.space"


def run():
    total_reward = 0

    print("Reset...")
    print(requests.post(f"{BASE}/reset").json())

    steps = [
        {"type": "classify", "label": "pricing inquiry"},
        {"type": "route", "department": "sales"},
        {"type": "reply", "response": "We will help you shortly."},
        {"type": "resolve"}
    ]

    for s in steps:
        res = requests.post(f"{BASE}/step", json={"action": s}).json()

        print("\nSTEP:", s["type"])
        print("Reward:", res["reward"])
        print("Stage:", res["observation"]["current_stage"])

        total_reward += res["reward"]

        if res["reward"] < 0:
            print("⚠️ Wrong step")

        if res["done"]:
            break

    print("\nTOTAL:", total_reward)


if __name__ == "__main__":
    run()