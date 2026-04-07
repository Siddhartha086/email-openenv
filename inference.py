import os
from typing import List

from openai import OpenAI
from email_openenv.environment import EmailOpenEnv
from email_openenv.tasks import TASKS


# --- ENV ---
API_BASE_URL = os.getenv("API_BASE_URL")
HF_TOKEN = os.getenv("HF_TOKEN")
MODEL = os.getenv("MODEL_NAME", "gpt-4o-mini")

client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)


# ---------- LOGGING ---------- #

def log_start(task, env, model):
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step, action, reward, done, error):
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} "
        f"done={str(done).lower()} error={error or 'null'}",
        flush=True,
    )


def log_end(success, steps, score, rewards: List[float]):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(
        f"[END] success={str(success).lower()} steps={steps} "
        f"score={score:.2f} rewards={rewards_str}",
        flush=True,
    )


# ---------- LLM INTENT ---------- #

def get_intent(email: str):
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "Classify intent: reset, refund, or investigate. One word."},
                {"role": "user", "content": email},
            ],
            temperature=0,
        )

        intent = response.choices[0].message.content.strip().lower()

        if "refund" in intent:
            return "refund"
        elif "reset" in intent or "password" in intent:
            return "reset"
        else:
            return "investigate"

    except Exception:
        if "refund" in email:
            return "refund"
        elif "login" in email or "password" in email:
            return "reset"
        else:
            return "investigate"


# ---------- STRICT LLM POLICY ---------- #

def decide_action_llm(email, intent, step, history, last_action):
    # STRICT FSM — no shortcuts
    flow = {
        None: ["classify"],
        "classify": ["route"],
        "route": ["reply"],
        "reply": ["resolve"],
        "resolve": []
    }

    valid_actions = flow.get(last_action, ["classify"])

    # Few-shot examples (safe + aligned)
    examples = """
Example:
Email: "Refund my money"
Intent: refund
Steps: classify → route → reply → resolve

Email: "Forgot password"
Intent: reset
Steps: classify → route → reply → resolve
"""

    try:
        prompt = f"""
You are an email handling agent.

{examples}

Current Task:
Email: {email}
Intent: {intent}

Step: {step}
History: {history}
Previous action: {last_action}

Allowed actions: {valid_actions}

Rules:
- Follow exact sequence
- Do not skip steps
- Do not repeat invalid actions
- Move forward toward resolve

Return ONLY one action.
"""

        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )

        action = response.choices[0].message.content.strip().lower()

        if action not in valid_actions:
            return valid_actions[0]

        return action

    except Exception:
        return valid_actions[0]


# ---------- MAIN ---------- #

def run():
    for task in TASKS:
        env = EmailOpenEnv()

        rewards = []
        steps_taken = 0
        success = False
        history = []
        last_action = None

        log_start(task["id"], "email_openenv", MODEL)

        try:
            result = env.reset()
            email = task["email"]

            intent = get_intent(email)

            for step in range(1, 11):
                if result.get("done"):
                    break

                action_type = decide_action_llm(
                    email, intent, step, history, last_action
                )

                action = {"type": action_type}

                result = env.step(action)

                reward = max(0.0, min(1.0, result.get("reward", 0)))
                done = result.get("done", False)
                error = result.get("observation", {}).get("last_action_error")

                rewards.append(reward)
                steps_taken = step

                log_step(step, action_type, reward, done, error)

                # update only if valid
                if not error:
                    last_action = action_type

                history.append(f"{action_type}:{reward:.2f}")

                if done:
                    success = True
                    break

        except Exception as e:
            print(f"[DEBUG] {str(e)}", flush=True)

        finally:
            score = sum(rewards) / len(rewards) if rewards else 0.0
            score = max(0.0, min(1.0, score))

            log_end(success, steps_taken, score, rewards)


if __name__ == "__main__":
    run()