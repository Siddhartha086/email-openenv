import gradio as gr
import os
os.environ["GRADIO_SERVER_NAME"] = "0.0.0.0"
os.environ["GRADIO_SERVER_PORT"] = "7860"

# import your env safely
env = None

def init_env():
    global env
    if env is None:
        from env.environment import EmailEnv
        env = EmailEnv()
    return env


def reset_env():
    try:
        e = init_env()
        obs = e.reset()
        return {
            "observation": obs.dict(),
            "reward": 0.0,
            "done": False,
            "info": {}
        }
    except Exception as ex:
        return {"error": str(ex)}


def step_env(action):
    try:
        e = init_env()
        obs, reward, done, info = e.step({"action": action})
        return {
            "observation": obs.dict(),
            "reward": reward,
            "done": done,
            "info": info
        }
    except Exception as ex:
        return {"error": str(ex)}


def get_state():
    try:
        e = init_env()
        return e.state()
    except Exception as ex:
        return {"error": str(ex)}


# 🎨 UI
with gr.Blocks() as demo:
    gr.Markdown("# 📧 Email Automation Agent")
    gr.Markdown("Simulate email handling using AI agent environment")

    with gr.Row():
        reset_btn = gr.Button("🔄 Reset")
        state_btn = gr.Button("📊 Get State")

    action_input = gr.Textbox(
        label="Action",
        placeholder="classify / route / reply / resolve"
    )

    step_btn = gr.Button("⚡ Run Step")

    output = gr.JSON(label="Output")

    reset_btn.click(reset_env, outputs=output)
    state_btn.click(get_state, outputs=output)
    step_btn.click(step_env, inputs=action_input, outputs=output)


# 🚀 launch
demo.launch(server_name="0.0.0.0", server_port=7860, share=False)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)