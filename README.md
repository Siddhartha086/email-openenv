# Email Automation OpenEnv

## Overview
Simulates real-world email triage and resolution workflow using AI agent actions.

## Actions
- classify('urgent' | 'normal' | 'low')
- route('billing' | 'tech' | 'sales')
- reply('text')
- resolve()

## Tasks
- Easy: classify email
- Medium: classify + route
- Hard: full resolution

## Run
docker build -t email-env .
docker run -p 7860:7860 email-env

## Test
python inference.py