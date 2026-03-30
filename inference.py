import os
import requests

BASE_URL = "http://localhost:7860"

HF_TOKEN = os.getenv("HF_TOKEN")
MODEL = os.getenv("MODEL_NAME")
API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

def generate_response(email):
    prompt = f"Reply professionally to this email:\n{email}"

    res = requests.post(API_URL, headers=headers, json={"inputs": prompt})

    try:
        return res.json()[0]["generated_text"]
    except:
        return "Sorry, we will help you."

def run():
    total_reward = 0

    r = requests.post(f"{BASE_URL}/reset")
    data = r.json()

    done = False

    while not done:
        email = data["observation"]["email"]

        response = generate_response(email)

        r = requests.post(
            f"{BASE_URL}/step",
            json={"response": response}
        )

        data = r.json()
        total_reward += data["reward"]
        done = data["done"]

    print("Final Score:", total_reward)


if __name__ == "__main__":
    run()