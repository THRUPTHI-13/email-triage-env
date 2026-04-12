# India AI Hackathon 2026 - OpenEnv Project

## Project Overview

This project is built for the **India AI Hackathon 2026** using the OpenEnv framework.  
It demonstrates a reinforcement-learning style environment where an agent interacts with a simulated system and receives rewards based on performance.

The goal of the project is to efficiently process inputs, generate predictions/actions, and compute a final reward score for evaluation.

---

## Key Features

- OpenEnv-compatible inference pipeline
- Reward-based evaluation system
- Modular and easy-to-extend architecture
- Docker-ready setup for reproducibility
- Supports automated evaluation by hackathon system

---

## Project Structure

├── inference.py # Main inference logic
├── Dockerfile # Container setup
├── requirements.txt # Dependencies
├── README.md # Project documentation

---

## How It Works

1. The environment sends input data to `inference.py`
2. The model processes the input and generates outputs
3. Each output is assigned a reward value
4. Final score is computed as:
   score = sum(rewards) / len(rewards)
5. The score is returned for evaluation

---

## ⚙️ Setup & Installation

### 1. Clone the repository

```bash
git clone <your-repo-link>
cd <repo-folder>
```

### 2. Install dependencies

pip install -r requirements.txt

### 3. Run locally

python inference.py

---

## Docker Setup

### 1. Build Docker image

docker build -t openenv-project .

### 2. Run container

docker run openenv-project

---

## Evaluation Logic

-Rewards are collected for each inference step
-Final score is calculated using average reward
-Higher score indicates better model performance

---

## Tech Stack

-Python
-OpenEnv Framework
-Docker
-Reinforcement Learning concepts

---
