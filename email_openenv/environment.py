class EmailOpenEnv:
    def __init__(self):
        self.state = {}

    def reset(self):
        self.state = {
            "goal": "Handle the email end-to-end correctly",
            "email_content": "Payment failed but money deducted",
            "current_stage": "start",
            "history": [],
            "available_actions": ["classify"],
            "last_action_error": None
        }

        return {
            "observation": self.state,
            "reward": 0.0,
            "done": False,
            "info": {}
        }

    def step(self, action: dict):
        action_type = action.get("type")

        reward = 0.0

        # --- VALID ACTION FLOW ---
        if action_type == "classify" and self.state["current_stage"] == "start":
            self.state["current_stage"] = "classified"
            self.state["history"].append("classified")
            self.state["available_actions"] = ["route"]
            reward = 0.3

        elif action_type == "route" and self.state["current_stage"] == "classified":
            self.state["current_stage"] = "routed"
            self.state["history"].append("routed")
            self.state["available_actions"] = ["reply"]
            reward = 0.5

        elif action_type == "reply" and self.state["current_stage"] == "routed":
            self.state["current_stage"] = "replied"
            self.state["history"].append("replied")
            self.state["available_actions"] = ["resolve"]
            reward = 0.7

        elif action_type == "resolve" and self.state["current_stage"] == "replied":
            self.state["current_stage"] = "resolved"
            self.state["history"].append("resolved")
            self.state["available_actions"] = []
            reward = 1.0

        else:
            # ❌ invalid or out-of-order action
            self.state["last_action_error"] = f"Invalid or out-of-order action: {action_type}"
            reward = -1.0

        done = self.state["current_stage"] == "resolved"

        return {
            "observation": self.state,
            "reward": reward,
            "done": done,
            "info": {}
        }