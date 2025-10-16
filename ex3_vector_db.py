import os
from pathlib import Path
from typing import List
from dotenv import load_dotenv
from openai import OpenAI

def split_markdown_h2(md: str) -> List[str]:
    parts, current = [], []
    for line in md.splitlines():
        if line.startswith("## "):
            if current:
                parts.append("\n".join(current).strip())
                current = []
        current.append(line)
    if current:
        parts.append("\n".join(current).strip())
    return parts or [md]

class MiniVectorDB:
    def __init__(self, client: OpenAI):
        self.client = client
        self.chunks: List[str] = []
        self.embeddings: List[List[float]] = []

    def embed(self, text: str) -> List[float]:
        return self.client.embeddings.create(model="openai/text-embedding-3-small", input=text).data[0].embedding

    def load_document(self, md_text: str) -> None:
        self.chunks = split_markdown_h2(md_text)
        self.embeddings = [self.embed(c) for c in self.chunks]

    def load_document_from_path(self, path: Path) -> None:
        text = Path(path).read_text(encoding="utf-8")
        self.load_document(text)

    def nearest_chunks(self, query: str, top_n: int = 3) -> List[str]:
        q = self.embed(query)
        sims = []
        for i, e in enumerate(self.embeddings):
            dot = sum(a*b for a,b in zip(q, e))
            sims.append((dot, i))
        sims.sort(reverse=True, key=lambda x: x[0])
        return [self.chunks[i] for _, i in sims[:top_n]]

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
    print(len(vdb.embeddings))
    top = vdb.nearest_chunks("Darle funcionalidad a la base de datos")[0]
    print(top)

if __name__ == "__main__":
    main()