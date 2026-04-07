import os
from openai import OpenAI
from email_openenv.environment import EmailOpenEnv
from email_openenv.tasks import TASKS

client = OpenAI(
    base_url=os.getenv("API_BASE_URL"),
    api_key=os.getenv("HF_TOKEN"),
)

MODEL = os.getenv("MODEL_NAME")


def run():
    for task in TASKS:
        print(f"[START] task={task['id']} env=email_openenv model={MODEL}")

        try:
            env = EmailOpenEnv(task=task)
        except:
            env = EmailOpenEnv()

        state = env.reset()

        done = False
        step_count = 0
        rewards = []

        while not done and step_count < 10:
            step_count += 1

            try:
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=[
                        {"role": "system", "content": "You are an email assistant."},
                        {"role": "user", "content": f"Email: {task['email']}. What action?"}
                    ]
                )
                action_text = response.choices[0].message.content.lower()
            except:
                action_text = "auto"

            # LLM-based mapping
            if "refund" in action_text:
                action = {"action": "refund"}
            elif "reset" in action_text or "password" in action_text:
                action = {"action": "reset"}
            elif "fix" in action_text or "issue" in action_text:
                action = {"action": "investigate"}
            else:
                action = {"action": "auto"}

            result = env.step(action)

            reward = result.get("reward", 0)
            done = result.get("done", False)

            rewards.append(reward)

            print(f"[STEP] task={task['id']} step={step_count} action={action['action']} reward={reward:.2f} done={done} error=null")

        score = sum(rewards) / len(rewards) if rewards else 0

        print(f"[END] task={task['id']} success={done} steps={step_count} score={score:.2f}")


if __name__ == "__main__":
    run()