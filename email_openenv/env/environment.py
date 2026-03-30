# environment.py

from typing import Dict, Any


class EmailOpenEnv:
    def __init__(self):
        self.reset()

    def reset(self) -> Dict[str, Any]:
        self.current_stage = "start"
        self.history = []
        self.last_action_error = None

        # sample email (can randomize later)
        self.email_content = "Payment failed but money deducted"

        return self._get_observation()

    def state(self) -> Dict[str, Any]:
        return self._get_observation()

    def step(self, action: Dict[str, Any]):

        # Define correct flow
        expected_action = {
            "start": "classify",
            "classified": "route",
            "routed": "reply",
            "replied": "resolve"
        }

        done = False
        reward = 0.0

        correct_action = expected_action.get(self.current_stage)

        # ❌ Wrong action
        if action.get("type") != correct_action:
            self.last_action_error = f"Expected {correct_action}"
            reward = -0.2
            return self._get_observation(), reward, False, {}

        # ✅ Correct action → move forward
        self.last_action_error = None

        if self.current_stage == "start":
            self.current_stage = "classified"
            reward = 0.3
            self.history.append("classified")

        elif self.current_stage == "classified":
            self.current_stage = "routed"
            reward = 0.5
            self.history.append("routed")

        elif self.current_stage == "routed":
            self.current_stage = "replied"
            reward = 0.7
            self.history.append("replied")

        elif self.current_stage == "replied":
            self.current_stage = "resolved"
            reward = 1.0
            done = True
            self.history.append("resolved")

        return self._get_observation(), reward, done, {}

    def _get_observation(self) -> Dict[str, Any]:

        expected_action = {
            "start": "classify",
            "classified": "route",
            "routed": "reply",
            "replied": "resolve",
            "resolved": None
        }

        next_action = expected_action.get(self.current_stage)

        return {
            "goal": "Handle the email end-to-end correctly",
            "email_content": self.email_content,
            "current_stage": self.current_stage,
            "history": self.history,
            "available_actions": [next_action] if next_action else [],
            "last_action_error": self.last_action_error
        }