---
title: Email OpenEnv Agent
emoji: 📧
colorFrom: blue
colorTo: green
sdk: docker
app_file: main.py
pinned: false
---

# Email OpenEnv Agent

## Overview

This project implements a real-world email handling environment using OpenEnv.

The agent workflow:
- classify email
- route to department
- generate reply
- resolve issue

---

## Actions

classify:
{ "type": "classify", "label": "billing | technical | general" }

route:
{ "type": "route", "department": "billing | tech | support" }

reply:
{ "type": "reply", "response": "text reply" }

resolve:
{ "type": "resolve" }

---

## Tasks

1. Classification
2. Routing
3. Reply generation
4. Resolution

---

## Reward

- correct: +0.3  
- wrong: -0.2  
- invalid order: -0.3  
- completion: +1.0  

---

## Endpoints

POST /reset  
POST /step  
GET /state  

---

## Env Variables

HF_TOKEN  
MODEL_NAME  
API_BASE_URL  

---


## Reward Design
The environment uses incremental reward shaping (0.3 → 0.5 → 0.7 → 1.0) to reflect partial task completion and discourage invalid transitions.

## Real-world Relevance
Simulates email triage workflows used in customer support systems (billing, technical, sales).

## Status

Submission ready