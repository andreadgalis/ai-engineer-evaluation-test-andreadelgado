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
    text = "You shall not pass!"
    emb = client.embeddings.create(model="openai/text-embedding-3-small", input=text).data[0].embedding
    print(len(emb))
    print(emb)

if __name__ == "__main__":
    main()