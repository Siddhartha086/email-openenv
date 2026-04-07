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
                {
                    "role": "system",
                    "content": (
                        "Classify the email intent. "
                        "Return ONLY one word: reset, refund, or investigate."
                    ),
                },
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
        # 🔥 fallback (important for stability)
        if "refund" in email:
            return "refund"
        elif "login" in email or "password" in email:
            return "reset"
        else:
            return "investigate"


# ---------- POLICY ---------- #

def decide_action(step):
    if step == 1:
        return {"type": "classify"}
    elif step == 2:
        return {"type": "route"}
    elif step == 3:
        return {"type": "reply"}
    else:
        return {"type": "resolve"}


# ---------- MAIN ---------- #

def run():
    for task in TASKS:
        env = EmailOpenEnv()

        rewards = []
        steps_taken = 0
        success = False

        log_start(task["id"], "email_openenv", MODEL)

        try:
            result = env.reset()

            # 🔥 LLM used here
            intent = get_intent(task["email"])

            for step in range(1, 11):
                if result.get("done"):
                    break

                action = decide_action(step)

                result = env.step(action)

                reward = max(0.0, min(1.0, result.get("reward", 0)))
                done = result.get("done", False)
                error = result.get("observation", {}).get("last_action_error")

                rewards.append(reward)
                steps_taken = step

                log_step(step, action["type"], reward, done, error)

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