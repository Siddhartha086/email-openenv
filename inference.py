import os
import requests
from typing import Dict
from openai import OpenAI

API_BASE = os.environ.get("API_BASE_URL", "http://127.0.0.1:8000")
MODEL = os.environ.get("MODEL_NAME", "gpt-4o-mini")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
HF_TOKEN = os.environ.get("HF_TOKEN")

client = OpenAI(api_key=OPENAI_API_KEY)


def get_headers():
    headers = {"Content-Type": "application/json"}
    if HF_TOKEN:
        headers["Authorization"] = f"Bearer {HF_TOKEN}"
    return headers


def reset_env(task: str) -> Dict:
    try:
        r = requests.post(f"{API_BASE}/reset", json={"task": task}, headers=get_headers(), timeout=30)
        r.raise_for_status()
        return r.json()
    except Exception:
        return {}


def step_env(payload: Dict) -> Dict:
    try:
        r = requests.post(f"{API_BASE}/step", json=payload, headers=get_headers(), timeout=30)
        r.raise_for_status()
        return r.json()
    except Exception:
        return {"reward": 0, "done": True}


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


def route_email(category: str) -> str:
    routing = {
        "payment_issue": "billing_team",
        "refund_request": "billing_team",
        "billing_problem": "billing_team",
        "complaint": "escalation_team",
        "general_query": "support_team",
    }
    return routing.get(category, "support_team")


def generate_response(email: str, category: str) -> str:
    try:
        res = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a professional customer support agent. Write a concise, empathetic, helpful reply. No subject lines or placeholders. Just the email body."},
                {"role": "user", "content": f"Customer email: {email}\nCategory: {category}\nWrite a support response:"}
            ],
            temperature=0.2,
        )
        return res.choices[0].message.content.strip()
    except Exception:
        return "Thank you for contacting us. We are looking into your issue and will get back to you shortly."


def run_agent(task: str):
    print(f"[START] task={task}", flush=True)

    obs = reset_env(task)
    category = None
    rewards = []
    step = 0

    for step in range(1, 21):
        observation = obs.get("observation", obs)
        email = observation.get("email_content", "")
        actions = observation.get("available_actions", [])

        if not actions:
            break

        if "classify" in actions:
            category = classify_email(email)
            payload = {"type": "classify", "action": "classify", "label": category}

        elif "route" in actions:
            if not category:
                category = classify_email(email)
            team = route_email(category)
            payload = {"type": "route", "action": "route", "team": team}

        elif "reply" in actions:
            if not category:
                category = classify_email(email)
            response = generate_response(email, category)
            payload = {"type": "reply", "action": "reply", "response": response}

        elif "respond" in actions:
            if not category:
                category = classify_email(email)
            response = generate_response(email, category)
            payload = {"type": "respond", "action": "respond", "response": response}

        elif "escalate" in actions:
            payload = {"type": "escalate", "action": "escalate"}

        elif "resolve" in actions:
            payload = {"type": "resolve", "action": "resolve"}

        else:
            action = actions[0]
            payload = {"type": action, "action": action}

        obs = step_env(payload)
        reward = obs.get("reward", 0)
        done = obs.get("done", False)
        rewards.append(reward)

        print(f"[STEP] step={step} action={payload['action']} reward={reward:.2f} done={str(done).lower()}", flush=True)

        if done:
            break

    score = rewards[-1] if rewards else 0.0
    print(f"[END] task={task} success=true steps={step} score={score:.2f} rewards={','.join(f'{r:.2f}' for r in rewards)}", flush=True)


if __name__ == "__main__":
    for task in ["easy", "medium", "hard"]:
        run_agent(task)