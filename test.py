import requests
import time

BASE = "https://sidtheslayer-email-openenv-agent.hf.space"


def pretty_print(step, data):
    print(f"\n===== {step.upper()} =====")
    print("RAW:", data)

    obs = data.get("observation", {})
    print("Stage:", obs.get("current_stage"))
    print("History:", obs.get("history"))
    print("Available Actions:", obs.get("available_actions"))
    print("Reward:", data.get("reward"))
    print("Done:", data.get("done"))


def test_flow():
    print("🚀 Starting End-to-End Test...\n")

    # RESET
    r = requests.post(f"{BASE}/reset")
    data = r.json()
    pretty_print("reset", data)

    done = False
    total_reward = 0

    while not done:
        action_type = data["observation"]["available_actions"][0]

        action = {"type": action_type}

        if action_type == "classify":
            action["label"] = "billing"

        elif action_type == "route":
            action["department"] = "billing"

        elif action_type == "reply":
            action["response"] = "We are resolving your issue"

        print(f"\n➡️ Sending action: {action}")

        # ✅ IMPORTANT FIX (NO "action" wrapper)
        r = requests.post(f"{BASE}/step", json=action)

        data = r.json()
        pretty_print("step", data)

        total_reward += data.get("reward", 0)
        done = data.get("done", False)

        time.sleep(0.5)

    print("\n🎯 FINAL RESULT")
    print("Total Reward:", total_reward)


if __name__ == "__main__":
    test_flow()