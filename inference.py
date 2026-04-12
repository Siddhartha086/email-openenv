import os
import requests
from typing import Dict
from openai import OpenAI

# ===== ENV =====
API_BASE = os.environ.get("API_BASE_URL", "http://127.0.0.1:8000")
MODEL = os.environ.get("MODEL_NAME", "gpt-4o-mini")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
HF_TOKEN = os.environ.get("HF_TOKEN")

client = OpenAI(api_key=OPENAI_API_KEY)


# ===== HEADERS =====
def get_headers():
    headers = {"Content-Type": "application/json"}
    if HF_TOKEN:
        headers["Authorization"] = f"Bearer {HF_TOKEN}"
    return headers


# ===== ENV =====
def reset_env(task: str) -> Dict:
    r = requests.post(
        f"{API_BASE}/reset",
        json={"task": task},
        headers=get_headers()
    )
    r.raise_for_status()
    data = r.json()
    print(f"[RESET] {data}")
    return data


def step_env(payload: Dict) -> Dict:
    r = requests.post(
        f"{API_BASE}/step",
        json=payload,
        headers=get_headers()
    )
    if not r.ok:
        print(f"[HTTP {r.status_code}] {r.json()}")
        r.raise_for_status()
    return r.json()


# ===== CLASSIFIER =====
def classify_email(email: str) -> str:
    email = email.lower()
    if "payment" in email and ("failed" in email or "deducted" in email):
        return "payment_issue"
    if "refund" in email:
        return "refund_request"
    if "bill" in email:
        return "billing_problem"
    if "complaint" in email:
        return "complaint"
    return "general_query"


# ===== ROUTER =====
def route_email(category: str) -> str:
    routing = {
        "payment_issue": "billing_team",
        "refund_request": "billing_team",
        "billing_problem": "billing_team",
        "complaint": "escalation_team",
        "general_query": "support_team",
    }
    return routing.get(category, "support_team")


# ===== RESPONSE GENERATOR =====
def generate_response(email: str, category: str) -> str:
    res = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a professional customer support agent. "
                    "Write a concise, empathetic, helpful reply. "
                    "No subject lines or placeholders. Just the email body."
                )
            },
            {
                "role": "user",
                "content": f"Customer email: {email}\nCategory: {category}\nWrite a support response:"
            }
        ],
        temperature=0.2,
    )
    return res.choices[0].message.content.strip()


# ===== AGENT =====
def run_agent(task: str):
    print(f"\n{'='*50}")
    print(f"[START] task={task}")
    print(f"{'='*50}")

    obs = reset_env(task)
    category = None

    for step in range(20):
        observation = obs.get("observation", obs)
        email = observation.get("email_content", "")
        actions = observation.get("available_actions", [])
        stage = observation.get("current_stage", "unknown")
        last_error = observation.get("last_action_error")

        print(f"\n[STEP {step}] stage={stage} actions={actions}")
        if last_error:
            print(f"[LAST ERROR] {last_error}")

        if not actions:
            print("[DONE] No more actions")
            break

        # ===== CLASSIFY =====
        if "classify" in actions:
            category = classify_email(email)
            print(f"[ACTION] classify → {category}")
            payload = {
                "type": "classify",
                "action": "classify",
                "label": category
            }

        # ===== ROUTE =====
        elif "route" in actions:
            if not category:
                category = classify_email(email)
            team = route_email(category)
            print(f"[ACTION] route → {team}")
            payload = {
                "type": "route",
                "action": "route",
                "team": team
            }

        # ===== REPLY =====
        elif "reply" in actions:
            if not category:
                category = classify_email(email)
            response = generate_response(email, category)
            print(f"[ACTION] reply → {response[:80]}...")
            payload = {
                "type": "reply",
                "action": "reply",
                "response": response
            }

        # ===== RESPOND =====
        elif "respond" in actions:
            if not category:
                category = classify_email(email)
            response = generate_response(email, category)
            print(f"[ACTION] respond → {response[:80]}...")
            payload = {
                "type": "respond",
                "action": "respond",
                "response": response
            }

        # ===== ESCALATE =====
        elif "escalate" in actions:
            print(f"[ACTION] escalate")
            payload = {
                "type": "escalate",
                "action": "escalate"
            }

        # ===== RESOLVE =====
        elif "resolve" in actions:
            print(f"[ACTION] resolve")
            payload = {
                "type": "resolve",
                "action": "resolve"
            }

        # ===== FALLBACK =====
        else:
            action = actions[0]
            print(f"[ACTION] fallback → {action}")
            payload = {
                "type": action,
                "action": action
            }

        obs = step_env(payload)
        reward = obs.get("reward", 0)
        done = obs.get("done", False)
        print(f"[RESULT] reward={reward} done={done}")

        if done:
            print(f"[COMPLETE] Final reward={reward}")
            break

    else:
        print("[TIMEOUT] Max steps reached")


# ===== MAIN =====
if __name__ == "__main__":
    for task in ["easy", "medium", "hard"]:
        run_agent(task)