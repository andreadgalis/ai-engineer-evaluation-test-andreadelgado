import os
from dotenv import load_dotenv
from openai import OpenAI

def main():
    load_dotenv()
    api_key = os.getenv("LITELLM_KEY")
    base_url = os.getenv("BASE_URL", "https://llmproxy.ai.orange")
    if not api_key:
        raise RuntimeError("Missing LITELLM_KEY in .env")
    client = OpenAI(api_key=api_key, base_url=base_url)
    prompt = "¿Cuántas 'a' tiene la palabra MasOrange? Responde solo con un número."
    resp = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    print(resp.choices[0].message.content.strip())

if __name__ == "__main__":
    main()