from pydantic import BaseModel
from typing import List, Optional


# -------------------------
# Models
# -------------------------
class Observation(BaseModel):
    goal: str
    email_content: str
    current_stage: str
    history: List[str]
    available_actions: List[str]
    last_action_error: Optional[str] = None


class Action(BaseModel):
    type: str
    label: Optional[str] = None
    department: Optional[str] = None
    response: Optional[str] = None


# -------------------------
# Environment
# -------------------------
class EmailEnv:
    def __init__(self):
        self.reset()

    def reset(self):
        self.state = {
            "goal": "Handle the email end-to-end correctly",
            "email_content": "Payment failed but money deducted",
            "current_stage": "start",
            "history": [],
            "last_action_error": None,
        }

        return Observation(
            goal=self.state["goal"],
            email_content=self.state["email_content"],
            current_stage=self.state["current_stage"],
            history=self.state["history"],
            available_actions=["classify", "route", "reply", "resolve"],
            last_action_error=None
        )

    def step(self, action_dict):
        action = Action(**action_dict)

        reward = 0.0
        done = False
        info = {}

        # -------------------------
        # CLASSIFY
        # -------------------------
        if action.type == "classify":
            if self.state["current_stage"] != "start":
                self.state["last_action_error"] = "Already classified"
                reward -= 0.1
            else:
                self.state["current_stage"] = "classified"
                self.state["history"].append("classified")
                self.state["last_action_error"] = None
                reward += 0.3

        # -------------------------
        # ROUTE
        # -------------------------
        elif action.type == "route":
            if self.state["current_stage"] != "classified":
                self.state["last_action_error"] = "Expected classify"
                reward -= 0.2
            else:
                self.state["current_stage"] = "routed"
                self.state["history"].append("routed")
                self.state["last_action_error"] = None
                reward += 0.3

        # -------------------------
        # REPLY
        # -------------------------
        elif action.type == "reply":
            if self.state["current_stage"] != "routed":
                self.state["last_action_error"] = "Expected route"
                reward -= 0.2
            else:
                self.state["current_stage"] = "replied"
                self.state["history"].append("replied")
                self.state["last_action_error"] = None
                reward += 0.3

        # -------------------------
        # RESOLVE
        # -------------------------
        elif action.type == "resolve":
            if self.state["current_stage"] != "replied":
                self.state["last_action_error"] = "Expected reply"
                reward -= 0.2
            else:
                self.state["current_stage"] = "done"
                self.state["history"].append("resolved")
                self.state["last_action_error"] = None
                reward += 1.0
                done = True

        else:
            self.state["last_action_error"] = "Invalid action"
            reward -= 0.5

        # ✅ CRITICAL FIX (no **state)
        obs = Observation(
            goal=self.state["goal"],
            email_content=self.state["email_content"],
            current_stage=self.state["current_stage"],
            history=self.state["history"],
            available_actions=["classify", "route", "reply", "resolve"],
            last_action_error=self.state["last_action_error"]
        )

        return obs.dict(), reward, done, info

    def state(self):
        return self.state