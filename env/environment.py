from typing import Tuple, Dict, Any


class EmailEnv:
    def __init__(self):
        self.reset()

    def reset(self):
        self.current_stage = "start"
        self.email_content = "Need info about pricing plans"
        self.history = []
        return self._get_obs()

    def state(self):
        return {
            "current_stage": self.current_stage,
            "history": self.history,
            "email": self.email_content
        }

    def step(self, action: Dict[str, Any]) -> Tuple[Dict, float, bool, Dict]:
        action_type = action.get("type")

        # ❗ validate action exists
        if not action_type:
            return self._error("Missing action type", -0.2)

        # ======================
        # STAGE LOGIC
        # ======================

        if self.current_stage == "start":
            if action_type != "classify":
                return self._error("Expected classify", -0.2)

            self.current_stage = "classified"
            self.history.append("classify")
            return self._success("Email classified", 0.3)

        elif self.current_stage == "classified":
            if action_type != "route":
                return self._error("Expected route", -0.2)

            self.current_stage = "routed"
            self.history.append("route")
            return self._success("Email routed", 0.3)

        elif self.current_stage == "routed":
            if action_type != "reply":
                return self._error("Expected reply", -0.2)

            self.current_stage = "replied"
            self.history.append("reply")
            return self._success("Replied to email", 0.3)

        elif self.current_stage == "replied":
            if action_type != "resolve":
                return self._error("Expected resolve", -0.2)

            self.current_stage = "done"
            self.history.append("resolve")
            return self._success("Task completed", 1.0, done=True)

        return self._error("Invalid state", -0.5)

    # ======================
    # HELPERS
    # ======================

    def _get_obs(self):
        return {
            "goal": "Handle the email end-to-end correctly",
            "email_content": self.email_content,
            "current_stage": self.current_stage,
            "history": self.history,
            "available_actions": ["classify", "route", "reply", "resolve"],
        }

    def _success(self, msg, reward, done=False):
        return self._get_obs(), reward, done, {"message": msg}

    def _error(self, msg, reward):
        return self._get_obs(), reward, False, {"error": msg}