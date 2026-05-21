"""
Librarian — ChromaDB + local sentence-transformers embedding helper.

Indexes the full vault on weekly sweep.
Uses sentence-transformers/all-MiniLM-L6-v2 — runs on CPU, free, works offline.
NO OpenAI. NO API keys.

First run: downloads ~200MB model to HuggingFace cache (~/.cache/huggingface/).
Subsequent runs: uses cached model — works offline.

Usage:
    python embed.py index                    # index vault → chroma DB
    python embed.py query "stale memory"     # semantic search
    python embed.py query "stale memory" 5   # top-5 results
"""

import sys
import os
from pathlib import Path

VAULT_ROOT = Path(__file__).parents[4]  # PrimoLabs_PoweredByClaude/
CHROMA_PATH = Path(__file__).parent / "chroma"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
COLLECTION_NAME = "librarian-vault"

# Extensions to index
INCLUDE_EXTS = {".md", ".txt"}
# Paths to skip
SKIP_DIRS = {".venv", "site-packages", "vendor", ".git", "chroma", "graphify-out", "__pycache__"}


def _get_chroma():
    """Lazy import — only loads when needed to avoid startup cost."""
    import chromadb
    from chromadb.utils import embedding_functions
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=MODEL_NAME)
    client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    collection = client.get_or_create_collection(name=COLLECTION_NAME, embedding_function=ef)
    return collection


def _collect_files(root: Path) -> list[Path]:
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for f in filenames:
            p = Path(dirpath) / f
            if p.suffix in INCLUDE_EXTS:
                files.append(p)
    return files


def index_vault() -> int:
    """Walk vault, embed all markdown files, upsert into ChromaDB collection."""
    collection = _get_chroma()
    files = _collect_files(VAULT_ROOT)
    ids, docs, metas = [], [], []
    for f in files:
        try:
            content = f.read_text(encoding="utf-8", errors="ignore").strip()
            if not content:
                continue
            rel = str(f.relative_to(VAULT_ROOT))
            ids.append(rel)
            docs.append(content[:8000])  # ChromaDB doc limit safeguard
            metas.append({"path": rel, "size": len(content)})
        except Exception as e:
            print(f"SKIP {f}: {e}")

    # Upsert in batches of 100
    batch = 100
    for i in range(0, len(ids), batch):
        collection.upsert(ids=ids[i:i+batch], documents=docs[i:i+batch], metadatas=metas[i:i+batch])
    print(f"Indexed {len(ids)} files into {CHROMA_PATH}")
    return len(ids)


def query_vault(text: str, n_results: int = 5) -> list[dict]:
    """Semantic search over indexed vault. Returns list of {path, score, snippet}."""
    collection = _get_chroma()
    results = collection.query(query_texts=[text], n_results=n_results)
    output = []
    for i, (doc_id, distance, document) in enumerate(zip(
        results["ids"][0], results["distances"][0], results["documents"][0]
    )):
        output.append({
            "rank": i + 1,
            "path": doc_id,
            "score": round(1 - distance, 4),  # convert distance to similarity
            "snippet": document[:300]
        })
    return output


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(0)

    cmd = args[0]
    if cmd == "index":
        count = index_vault()
        print(f"Done. {count} documents indexed.")
    elif cmd == "query":
        if len(args) < 2:
            print("Usage: python embed.py query <text> [n_results]")
            sys.exit(1)
        text = args[1]
        n = int(args[2]) if len(args) > 2 else 5
        results = query_vault(text, n)
        for r in results:
            print(f"[{r['rank']}] {r['path']} (score: {r['score']})")
            print(f"    {r['snippet'][:150]}...")
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
