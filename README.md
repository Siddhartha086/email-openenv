---

title: Email OpenEnv Agent
emoji: 📧
colorFrom: blue
colorTo: green
sdk: docker
app_file: main.py
pinned: false
-------------

# 📧 Email OpenEnv Agent

## 🚀 Overview

This project implements a **real-world email handling environment** using the OpenEnv specification.

The environment simulates how support teams process emails:

* Understand the issue
* Classify the request
* Route to the correct department
* Generate a reply
* Resolve the issue

This models a **real production workflow**, not a toy problem.

---

## 🧠 Environment Design

### Observation

Each state includes:

* `goal`: Complete the email workflow
* `email_content`: Input email text
* `current_stage`: Current step
* `history`: Actions taken
* `available_actions`: Allowed actions
* `last_action_error`: Error feedback

---

### Actions

1. **classify**

```json
{ "type": "classify", "label": "billing | technical | general" }
```

2. **route**

```json
{ "type": "route", "department": "billing | tech | support" }
```

3. **reply**

```json
{ "type": "reply", "response": "text reply" }
```

4. **resolve**

```json
{ "type": "resolve" }
```

---

## 📋 Tasks (Graded)

### Task 1 — Classification (Easy)

* Identify email type

### Task 2 — Routing (Medium)

* Route to correct department

### Task 3 — Reply (Medium)

* Generate valid response

### Task 4 — Resolution (Hard)

* Complete full pipeline

---

## 🎯 Reward Function

| Condition      | Reward |
| -------------- | ------ |
| Correct action | +0.3   |
| Wrong action   | -0.2   |
| Invalid order  | -0.3   |
| Completion     | +1.0   |
| Perfect flow   | +0.5   |

---

## 🔄 API Endpoints

### Reset

```
POST /reset
```

### Step

```
POST /step
```

Input:

```json
{
  "action": {...},
  "email_content": "optional"
}
```

Output:

```json
{
  "observation": {...},
  "reward": float,
  "done": bool,
  "info": {}
}
```

### State

```
GET /state
```

---

## 🧪 Example

```bash
BASE="https://your-space-url"

curl -X POST $BASE/reset

curl -X POST $BASE/step \
-d '{"action":{"type":"classify","label":"billing"}}'

curl -X POST $BASE/step \
-d '{"action":{"type":"route","department":"billing"}}'

curl -X POST $BASE/step \
-d '{"action":{"type":"reply","response":"We are checking your issue"}}'

curl -X POST $BASE/step \
-d '{"action":{"type":"resolve"}}'
```

---

## 🤖 Baseline Inference

Uses:

* `HF_TOKEN`
* `MODEL_NAME`
* `API_BASE_URL`

Runs full pipeline and produces reproducible scores.

---

## 🔑 Environment Variables

Set in HF Space settings:

* HF_TOKEN
* MODEL_NAME = google/flan-t5-large
* API_BASE_URL = https://api-inference.huggingface.co

---

## 🐳 Deployment

* Docker-based Hugging Face Space
* Includes:

  * main.py
  * inference.py
  * openenv.yaml

---

## ✅ OpenEnv Compliance

* step() implemented
* reset() implemented
* state() implemented
* Typed models
* openenv.yaml present

---

## 📊 Evaluation Coverage

* Real-world task ✅
* 3+ tasks ✅
* Reward shaping ✅
* Docker deploy ✅
* HF Space working ✅

---

## 🎯 Status

✅ Submission-ready
