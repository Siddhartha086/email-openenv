import random
from env.models import Observation


EMAILS = [
    {
        "text": "Payment failed but money deducted",
        "classification": "urgent",
        "route": "billing"
    },
    {
        "text": "App is crashing on login",
        "classification": "urgent",
        "route": "tech"
    },
    {
        "text": "Need info about pricing plans",
        "classification": "normal",
        "route": "sales"
    }
]


class EmailEnv:
    def __init__(self):
        self.reset()

    def reset(self):
        self.sample = random.choice(EMAILS)

        self.state_data = {
            "stage": "start",
            "email": self.sample["text"],
            "classification": None,
            "route": None,
            "reply": None,
            "history": []
        }

        return self._get_obs()

    def step(self, action):
        action_type = action.get("action_type")
        payload = action.get("payload")

        reward = 0.0
        done = False
        error = None

        try:
            if self.state_data["stage"] == "start":
                if action_type == "classify":
                    self.state_data["classification"] = payload
                    self.state_data["stage"] = "classified"

                    if payload == self.sample["classification"]:
                        reward += 0.3
                else:
                    error = "Expected classify"
                    reward -= 0.2

            elif self.state_data["stage"] == "classified":
                if action_type == "route":
                    self.state_data["route"] = payload
                    self.state_data["stage"] = "routed"

                    if payload == self.sample["route"]:
                        reward += 0.3
                else:
                    error = "Expected route"
                    reward -= 0.2

            elif self.state_data["stage"] == "routed":
                if action_type == "reply":
                    self.state_data["reply"] = payload
                    self.state_data["stage"] = "replied"
                    reward += 0.2
                else:
                    error = "Expected reply"
                    reward -= 0.2

            elif self.state_data["stage"] == "replied":
                if action_type == "resolve":
                    reward += 0.2
                    done = True
                else:
                    error = "Expected resolve"
                    reward -= 0.2

        except Exception as e:
            error = str(e)
            reward -= 0.2

        self.state_data["history"].append(f"{action_type}:{payload}")

        return self._get_obs(error), reward, done, {}

    def state(self):
        return self.state_data

    def _get_obs(self, error=None):
        return Observation(
            goal="Handle the email end-to-end correctly",
            email_content=self.state_data["email"],
            current_stage=self.state_data["stage"],
            history=self.state_data["history"],
            available_actions=["classify", "route", "reply", "resolve"],
            last_action_error=error
        )