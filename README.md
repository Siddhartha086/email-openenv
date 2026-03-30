 Email OpenEnv Agent
 Overview

This project implements a real-world email triage environment using the OpenEnv specification.
The environment simulates how support teams process incoming emails step-by-step.

 Problem Definition

Given an incoming email, the agent must:

Classify the email intent
Route it to the correct department
Generate a reply
Resolve the issue
 Environment Design
Observation Space
goal: Task objective
email_content: Input email
current_stage: Workflow stage
history: Action history
available_actions: Allowed actions
last_action_error: Error signal
Action Space
Action	Description
classify	Identify intent
route	Assign department
reply	Generate response
resolve	Close issue
 Workflow
start → classify → route → reply → resolve → done
 Reward Function
Step	Reward
classify	+0.3
route	+0.3
reply	+0.3
resolve	+1.0
wrong step	-0.2

 Dense reward encourages correct sequencing
 Penalizes invalid transitions

 Example

Input:

Payment failed but money deducted

Agent flow:

classify → route → reply → resolve
 Inference

Run:

python inference.py
 API Endpoints
Endpoint	Method	Description
/reset	POST	Reset environment
/step	POST	Execute action
/state	GET	Get current state
 Deployment
Dockerized application
Hosted on Hugging Face Spaces
FastAPI backend
 Environment Variables
Name	Description
HF_TOKEN	Hugging Face API key
MODEL_NAME	LLM model
API_BASE_URL	Inference endpoint
 OpenEnv Compliance
Typed Observation/Action models ✔
step/reset/state endpoints ✔
Deterministic transitions ✔
Reward shaping ✔
 Baseline Performance

Total reward (optimal path):

1.9
 Future Improvements
Multi-email batching
Priority classification
LLM-based response generation
Escalation handling