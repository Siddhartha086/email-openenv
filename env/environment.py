from pydantic import BaseModel
from typing import List, Optional
import random


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
        emails = [
            "Need pricing details",
            "Payment failed but money deducted",
            "App crashing on login"
        ]

        self.state = {
            "goal": "Handle the email end-to-end correctly",
            "email_content": random.choice(emails),
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

    def _build_obs(self):
        return Observation(
            goal=self.state["goal"],
            email_content=self.state["email_content"],
            current_stage=self.state["current_stage"],
            history=self.state["history"],
            available_actions=["classify", "route", "reply", "resolve"],
            last_action_error=self.state["last_action_error"]
        )

    def step(self, action_dict):
        # 🔥 HARD SAFETY (fixes all malformed inputs)
        if not isinstance(action_dict, dict):
            return self._build_obs().dict(), -0.5, False, {}

        action_type = action_dict.get("type")

        reward = 0.0
        done = False
        info = {}

        valid_actions = ["classify", "route", "reply", "resolve"]

        if action_type not in valid_actions:
            self.state["last_action_error"] = "Invalid action"
            return self._build_obs().dict(), -0.5, False, {}

        # -------------------------
        # CLASSIFY
        # -------------------------
        if action_type == "classify":
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
        elif action_type == "route":
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
        elif action_type == "reply":
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
        elif action_type == "resolve":
            if self.state["current_stage"] != "replied":
                self.state["last_action_error"] = "Expected reply"
                reward -= 0.2
            else:
                self.state["current_stage"] = "done"
                self.state["history"].append("resolved")
                self.state["last_action_error"] = None
                reward += 1.0
                done = True

        # -------------------------
        # BONUS + PENALTY
        # -------------------------
        if done and self.state["history"] == ["classified", "routed", "replied", "resolved"]:
            reward += 0.5

        if len(self.state["history"]) > 6:
            reward -= 0.3

        return self._build_obs().dict(), reward, done, info

    def state(self):
        return self.state