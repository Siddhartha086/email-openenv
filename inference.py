import requests

BASE_URL = "https://sidtheslayer-email-openenv-agent.hf.space"


# 🔹 CLASSIFICATION
def classify_email(email):
    email = email.lower()

    if any(w in email for w in ["refund", "charged", "billing", "invoice", "payment", "deducted"]):
        return "billing"
    elif any(w in email for w in ["error", "bug", "issue", "login", "password", "crash"]):
        return "technical"
    elif any(w in email for w in ["complaint", "angry", "bad", "worst", "not happy"]):
        return "complaint"
    elif any(w in email for w in ["cancel", "unsubscribe", "close account"]):
        return "account"
    else:
        return "general"


# 🔹 ROUTING
def route_department(category):
    mapping = {
        "billing": "billing",
        "technical": "tech_support",
        "complaint": "escalation",
        "account": "account_management",
        "general": "general_support",
    }
    return mapping.get(category, "general_support")


# 🔹 RESPONSE GENERATION
def generate_reply(email, category):
    email = email.lower()

    if category == "billing":
        if "refund" in email or "deducted" in email:
            return "We understand your payment failed but money was deducted. Our billing team is reviewing this and will resolve it shortly."
        elif "charged" in email:
            return "We are reviewing the duplicate charge and will resolve it shortly."
        else:
            return "Our billing team is reviewing your request."

    elif category == "technical":
        if "login" in email or "password" in email:
            return "Please try resetting your password using the 'Forgot Password' option."
        else:
            return "Our technical team is investigating the issue."

    elif category == "complaint":
        return "We apologize for your experience. Your issue has been escalated."

    elif category == "account":
        return "Your account-related request is being processed."

    else:
        return "Thank you for reaching out. We are looking into your request."


# 🔹 SAFE OBS EXTRACTION
def extract_obs(data):
    return data.get("observation") or data.get("obs") or data


# 🔹 EMAIL EXTRACTION
def extract_email(obs):
    return (
        obs.get("email")
        or obs.get("email_content")
        or obs.get("input")
        or ""
    )


def run():
    total_reward = 0
    step_count = 0

    # ✅ REQUIRED START BLOCK
    print("[START] task=email_handling", flush=True)

    r = requests.post(f"{BASE_URL}/reset")
    data = r.json()

    obs = extract_obs(data)
    done = data.get("done", False)

    state = {
        "email": "",
        "category": None,
        "department": None,
    }

    while not done:
        email_text = extract_email(obs)
        if email_text:
            state["email"] = email_text

        actions = obs.get("available_actions", [])
        if not actions:
            break

        action_type = actions[0]
        action = {"type": action_type}

        if action_type == "classify":
            category = classify_email(state["email"])
            state["category"] = category
            action["label"] = category

        elif action_type == "route":
            if not state["category"]:
                state["category"] = classify_email(state["email"])

            dept = route_department(state["category"])
            state["department"] = dept
            action["department"] = dept

        elif action_type == "reply":
            if not state["category"]:
                state["category"] = classify_email(state["email"])

            response = generate_reply(state["email"], state["category"])
            action["response"] = response

        elif action_type == "resolve":
            pass

        r = requests.post(f"{BASE_URL}/step", json=action)
        data = r.json()

        obs = extract_obs(data)
        reward = data.get("reward", 0)
        done = data.get("done", False)

        step_count += 1
        total_reward += reward

        # ✅ REQUIRED STEP BLOCK
        print(f"[STEP] step={step_count} reward={reward}", flush=True)

    # ✅ REQUIRED END BLOCK
    print(f"[END] task=email_handling score={total_reward} steps={step_count}", flush=True)


if __name__ == "__main__":
    run()