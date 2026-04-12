import asyncio
import os
from typing import List
from openai import OpenAI

from models import EmailAction
from server.email_env_environment import EmailEnvironment



client = OpenAI(
    base_url=os.environ.get("API_BASE_URL"),
    api_key=os.environ.get("API_KEY", "test"),  # fallback for local
)

MODEL_NAME = os.environ.get("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")


def log_start(task: str, env: str, model: str):
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step: int, action: str, reward: float, done: bool, error):
    error_val = error if error else "null"
    done_val = str(done).lower()
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={done_val} error={error_val}",
        flush=True,
    )


def get_action(email: str) -> str:
    prompt = f"""
You are an email triage agent.

Email:
{email}

Decide:
- route: billing / tech / general / spam
- priority: high / medium / low

Output strictly in format:
route=<route>,priority=<priority>
"""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=50,
        )
        return response.choices[0].message.content.strip()
    except:
        return "route=general,priority=low"


async def run_task(task_name: str):
    env = EmailEnvironment()

   
    env.current_task = task_name
    env.emails = env.tasks[task_name]
    env.index = 0

    rewards: List[float] = []
    steps = 0

    log_start(task_name, "email_env", MODEL_NAME)

    obs = env.reset()

    for step in range(1, 10):
        if obs.done:
            break

        action_str = get_action(obs.email)

        try:
            parts = action_str.split(",")
            route = parts[0].split("=")[1]
            priority = parts[1].split("=")[1]
        except:
            route = "general"
            priority = "low"

        action = EmailAction(route=route, priority=priority)

        obs = env.step(action)

        reward = obs.reward

        
        reward = max(0.1, min(0.9, reward))

        rewards.append(reward)
        steps = step

        log_step(step, action_str, reward, obs.done, None)

        if obs.done:
            break

   
    score = sum(rewards) / (len(rewards) * 1.0)
    score = max(0.1, min(0.9, score))

    success = score > 0.2

    rewards_str = ",".join(f"{r:.2f}" for r in rewards)

    print(
        f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}",
        flush=True,
    )


async def main():
   
    await run_task("easy")
    await run_task("medium")
    await run_task("hard")


if __name__ == "__main__":
    asyncio.run(main())