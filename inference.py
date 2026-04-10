import asyncio
import os
from typing import List

from openai import OpenAI

from models import EmailAction
from server.email_env_environment import EmailEnvironment


API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY")

MAX_STEPS = 10

client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)


def log_start(task: str, env: str, model: str):
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step: int, action: str, reward: float, done: bool, error: str | None):
    err = error if error else "null"
    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error={err}", flush=True)


def log_end(success: bool, steps: int, rewards: List[float]):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} rewards={rewards_str}", flush=True)


def get_llm_decision(email: str):
    prompt = f"""
You are an AI customer support agent.

Analyze the email and decide:
1. route (billing, tech, general, spam)
2. priority (high, medium, low)

Respond ONLY in this format:
route=<route>,priority=<priority>

Email:
{email}
"""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=50,
        )

        output = response.choices[0].message.content.strip()

        # Parse output
        parts = output.split(",")
        route = parts[0].split("=")[1].strip()
        priority = parts[1].split("=")[1].strip()

        return route, priority

    except Exception as e:
        print(f"[DEBUG] LLM error: {e}")
        return "general", "low"


async def main():
    env = EmailEnvironment()

    rewards = []
    steps = 0
    success = False

    log_start(task="email_task", env="email_env", model=MODEL_NAME)

    try:
        obs = env.reset()
        email = obs.email

        for step in range(1, MAX_STEPS + 1):
            if obs.done:
                break

            route, priority = get_llm_decision(email)

            action = EmailAction(route=route, priority=priority)

            obs = env.step(action)

            reward = obs.reward or 0.0
            done = obs.done

            rewards.append(reward)
            steps = step

            action_str = f"route={route},priority={priority}"

            log_step(step, action_str, reward, done, None)

            email = obs.email

            if done:
                break

        success = sum(rewards) > 2.0 if rewards else False

    finally:
        log_end(success, steps, rewards)


if __name__ == "__main__":
    asyncio.run(main())