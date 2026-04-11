import gradio as gr
import requests

BASE_URL = "https://thrupthi13-email-env.hf.space"


def reset_env():
    res = requests.post(f"{BASE_URL}/reset")
    data = res.json()
    return data["email"], "0.0"


def step_env(email, route, priority):
    payload = {
        "route": route,
        "priority": priority
    }

    res = requests.post(f"{BASE_URL}/step", json=payload)
    data = res.json()

    return data["email"], str(data["reward"])


with gr.Blocks() as demo:
    gr.Markdown("# 📧 Email Triage AI System")

    email_box = gr.Textbox(label="Email", interactive=False)
    reward_box = gr.Textbox(label="Reward", interactive=False)

    route = gr.Dropdown(["billing", "tech", "general", "spam"], label="Route")
    priority = gr.Dropdown(["high", "medium", "low"], label="Priority")

    reset_btn = gr.Button("Reset")
    step_btn = gr.Button("Take Action")

    reset_btn.click(fn=reset_env, outputs=[email_box, reward_box])
    step_btn.click(fn=step_env, inputs=[email_box, route, priority], outputs=[email_box, reward_box])


demo.launch()