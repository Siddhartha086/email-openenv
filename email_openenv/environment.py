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

        if action_type == "classify":
            self.state["current_stage"] = "classified"
            self.state["history"].append("classified")
            self.state["available_actions"] = ["route"]
            reward = 0.3

        elif action_type == "route":
            self.state["current_stage"] = "routed"
            self.state["history"].append("routed")
            self.state["available_actions"] = ["reply"]
            reward = 0.5

        elif action_type == "reply":
            self.state["current_stage"] = "replied"
            self.state["history"].append("replied")
            self.state["available_actions"] = ["resolve"]
            reward = 0.7

        elif action_type == "resolve":
            self.state["current_stage"] = "resolved"
            self.state["history"].append("resolved")
            self.state["available_actions"] = []
            reward = 1.0

        else:
            self.state["last_action_error"] = "Invalid action"
            reward = -1.0

        done = self.state["current_stage"] == "resolved"

        return {
            "observation": self.state,
            "reward": reward,
            "done": done,
            "info": {}
        }