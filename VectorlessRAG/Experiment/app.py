
import json
from pathlib import Path

from pageindex import PageIndexClient


ROOT = Path("/workspace")
DOCUMENTS = ROOT / "documents"
OUTPUT = ROOT / "data" / "trees"
STORAGE = ROOT / "data" / "pageindex"

OUTPUT.mkdir(parents=True, exist_ok=True)
STORAGE.mkdir(parents=True, exist_ok=True)

MODEL = "openai/qwen3:4b-instruct-2507-q4_K_M"

client = PageIndexClient(
    index={
        "model": MODEL,
        "backend": {
            "api_key": "ollama",
            "api_base": "http://ollama:11434/v1"
        },
        "storage_path": str(STORAGE),
        "optimize": "merge",
        "summary_concurrency": 1
    }
)

pdf = DOCUMENTS / "2005.11401v4.pdf"

if not pdf.exists():
    raise FileNotFoundError(f"PDF not found: {pdf}")

print(f"\nIndexing: {pdf.name}")

result = client.submit_document(str(pdf))
doc_id = result["doc_id"]

print(f"Document ID: {doc_id}")

tree = client.get_tree(
    doc_id,
    node_summary=True,
    include_text=False
)

tree_file = OUTPUT / f"{pdf.stem}.json"

with tree_file.open("w", encoding="utf-8") as file:
    json.dump(tree, file, indent=2, ensure_ascii=False)

print("\nTREE GENERATED SUCCESSFULLY")
print(f"Saved at: {tree_file}")

print("\nTREE PREVIEW:")
print(json.dumps(tree, indent=2, ensure_ascii=False)[:5000])
