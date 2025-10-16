import os
from pathlib import Path
from typing import List
from dotenv import load_dotenv
from openai import OpenAI
from ex3_vector_db import MiniVectorDB

SYSTEM_PROMPT = (
    "Eres un asistente que responde SÓLO con información presente en los fragmentos de contexto. "
    "Si la respuesta no está en el contexto, responde 'No aparece en la guía'. "
    "Responde en español de forma breve y precisa."
)

def main():
    load_dotenv()
    api_key = os.getenv("LITELLM_KEY")
    base_url = os.getenv("BASE_URL", "https://llmproxy.ai.orange")
    if not api_key:
        raise RuntimeError("Missing LITELLM_KEY in .env")
    client = OpenAI(api_key=api_key, base_url=base_url)

    guide_path = Path("ai-engineer-evaluation-test.md")
    if not guide_path.exists():
        raise FileNotFoundError("ai-engineer-evaluation-test.md not found.")
    vdb = MiniVectorDB(client)
    vdb.load_document_from_path(guide_path)

    question = "¿Qué modelos hay disponibles para el uso en el ejercicio?"
    context_chunks: List[str] = vdb.nearest_chunks(question, top_n=3)
    context = "\n\n---\n\n".join(context_chunks)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Pregunta: {question}\n\nContexto:\n{context}"}
    ]
    resp = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=messages,
        temperature=0.0
    )
    print(resp.choices[0].message.content.strip())

if __name__ == "__main__":
    main()