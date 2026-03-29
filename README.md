---
title: Email OpenEnv Agent
emoji: 📧
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
---

# Email OpenEnv Agent

This is an automated email handling agent built using OpenEnv.

## Features
- Classify emails
- Route emails
- Generate replies
- Resolve issues

## API Endpoint

POST /reset

Example:
```bash
curl -X POST https://your-space-url/reset -H "Content-Type: application/json" -d '{}'