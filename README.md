---
title: email-env
emoji: "🚀"
colorFrom: blue
colorTo: green
sdk: docker
---

# Project Title

Email Environment - OpenEnv Hackathon Project

---

## Overview

This project is built for the India AI Hackathon 2026 using OpenEnv.

It processes environment inputs, runs inference, and returns reward-based evaluation scores.

---

## Features

- OpenEnv compatible inference pipeline
- Automated evaluation system
- Reward based scoring
- Docker deployment support

---

## How It Works

Input -> inference.py -> processing -> rewards -> final score

Score formula:

score = sum(rewards) / len(rewards)

---

## Setup Instructions

Install dependencies:
pip install -r requirements.txt

Run locally:
python inference.py

---

## Docker

Build image:
docker build -t openenv-project .

Run container:
docker run openenv-project

---

## Notes

- Keep structure unchanged
- Ensure inference.py runs without errors
- Do not modify OpenEnv config files
