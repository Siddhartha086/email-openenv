import requests

BASE_URL = "https://sidtheslayer-email-openenv-agent.hf.space"


def run_episode():
    print("Resetting environment...")
    r = requests.post(f"{BASE_URL}/reset")
    data = r.json()

    total_reward = 0

    steps = [
        {"type": "classify", "label": "pricing inquiry"},
        {"type": "route", "department": "sales"},
        {"type": "reply", "response": "Our team will contact you shortly."},
        {"type": "resolve"}
    ]

    for step in steps:
        r = requests.post(
            f"{BASE_URL}/step",
            json={"action": step}
        )
        res = r.json()

        print("\nStep:", step["type"])
        print("Reward:", res["reward"])
        print("Stage:", res["observation"]["current_stage"])

        total_reward += res["reward"]

        if res["done"]:
            break

    print("\nTotal reward:", total_reward)


if __name__ == "__main__":
    run_episode()