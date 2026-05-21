"""
Deep Researcher — ChromaDB + local sentence-transformers embedding helper.

Indexes: research corpus (agents/deep-researcher/memory/) + shared shelf (.claude/reference/).
Uses sentence-transformers/all-MiniLM-L6-v2 — runs on CPU, free, works offline.
NO OpenAI. NO API keys.

First run: downloads ~200MB model to HuggingFace cache (~/.cache/huggingface/).
Subsequent runs: uses cached model — works offline.

Usage:
    python embed.py index                    # index research corpus → chroma DB
    python embed.py query "ICT order block"  # semantic search
    python embed.py query "market scan" 5    # top-5 results
"""

import sys
import os
from pathlib import Path

VAULT_ROOT = Path(__file__).parents[4]
AGENT_DIR = Path(__file__).parents[2]       # agents/deep-researcher/
SHARED_SHELF = VAULT_ROOT / ".claude" / "reference"
RESEARCH_CORPUS = AGENT_DIR / "memory"
CHROMA_PATH = Path(__file__).parent / "chroma"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
COLLECTION_NAME = "deep-researcher-corpus"

INCLUDE_EXTS = {".md", ".txt"}
SKIP_DIRS = {".venv", "site-packages", "vendor", ".git", "chroma", "graphify-out", "__pycache__"}


def _get_chroma():
    import chromadb
    from chromadb.utils import embedding_functions
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=MODEL_NAME)
    client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    collection = client.get_or_create_collection(name=COLLECTION_NAME, embedding_function=ef)
    return collection


def _collect_files(roots: list[Path]) -> list[Path]:
    files = []
    for root in roots:
        if not root.exists():
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for f in filenames:
                p = Path(dirpath) / f
                if p.suffix in INCLUDE_EXTS:
                    files.append(p)
    return files


def index_corpus() -> int:
    """Index research corpus + shared shelf into ChromaDB."""
    collection = _get_chroma()
    files = _collect_files([RESEARCH_CORPUS, SHARED_SHELF])
    ids, docs, metas = [], [], []
    for f in files:
        try:
            content = f.read_text(encoding="utf-8", errors="ignore").strip()
            if not content:
                continue
            rel = str(f.relative_to(VAULT_ROOT))
            ids.append(rel)
            docs.append(content[:8000])
            metas.append({"path": rel, "source": "research" if AGENT_DIR in f.parents else "shared-shelf"})
        except Exception as e:
            print(f"SKIP {f}: {e}")

    batch = 100
    for i in range(0, len(ids), batch):
        collection.upsert(ids=ids[i:i+batch], documents=docs[i:i+batch], metadatas=metas[i:i+batch])
    print(f"Indexed {len(ids)} files into {CHROMA_PATH}")
    return len(ids)


def query_corpus(text: str, n_results: int = 5, source_filter: str = None) -> list[dict]:
    """Semantic search. Optional source_filter: 'research' or 'shared-shelf'."""
    collection = _get_chroma()
    where = {"source": source_filter} if source_filter else None
    results = collection.query(query_texts=[text], n_results=n_results, where=where)
    output = []
    for i, (doc_id, distance, document, meta) in enumerate(zip(
        results["ids"][0], results["distances"][0], results["documents"][0], results["metadatas"][0]
    )):
        output.append({
            "rank": i + 1,
            "path": doc_id,
            "source": meta.get("source", "unknown"),
            "score": round(1 - distance, 4),
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
        count = index_corpus()
        print(f"Done. {count} documents indexed.")
    elif cmd == "query":
        if len(args) < 2:
            print("Usage: python embed.py query <text> [n_results]")
            sys.exit(1)
        text = args[1]
        n = int(args[2]) if len(args) > 2 else 5
        results = query_corpus(text, n)
        for r in results:
            print(f"[{r['rank']}] [{r['source']}] {r['path']} (score: {r['score']})")
            print(f"    {r['snippet'][:150]}...")
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
