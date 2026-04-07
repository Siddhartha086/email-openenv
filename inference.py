import os
from typing import List

from email_openenv.environment import EmailOpenEnv
from email_openenv.tasks import TASKS


API_BASE_URL = os.getenv("API_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME", "rule-based")
HF_TOKEN = os.getenv("HF_TOKEN")


# ---------- LOGGING (STRICT FORMAT) ---------- #

def log_start(task: str, env: str, model: str):
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step: int, action: str, reward: float, done: bool, error: str):
    done_val = str(done).lower()
    error_val = error if error else "null"
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={done_val} error={error_val}",
        flush=True,
    )


def log_end(success: bool, steps: int, score: float, rewards: List[float]):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(
        f"[END] success={str(success).lower()} steps={steps} score={score:.2f} rewards={rewards_str}",
        flush=True,
    )


# ---------- RULE-BASED POLICY (STABLE) ---------- #

def decide_action(email: str, step: int):
    # Follow your env flow: classify → route → reply → resolve
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

        log_start(task=task["id"], env="email_openenv", model=MODEL_NAME)

        try:
            result = env.reset()

            for step in range(1, 11):
                if result.get("done"):
                    break

                action = decide_action(task["email"], step)

                result = env.step(action)

                reward = result.get("reward", 0.0)
                reward = max(0.0, min(1.0, reward))  # normalize
                done = result.get("done", False)
                error = result.get("observation", {}).get("last_action_error")

                rewards.append(reward)
                steps_taken = step

                log_step(
                    step=step,
                    action=action["type"],
                    reward=reward,
                    done=done,
                    error=error,
                )

                if done:
                    success = True
                    break

        except Exception as e:
            print(f"[DEBUG] {str(e)}", flush=True)

        finally:
            score = sum(rewards) / len(rewards) if rewards else 0.0
            score = max(0.0, min(1.0, score))

            log_end(
                success=success,
                steps=steps_taken,
                score=score,
                rewards=rewards,
            )


if __name__ == "__main__":
    run()