import os
import urllib.request

URLS = {
    "rag_eval_v0.3.3.html": "https://docs.ragas.io/en/v0.3.3/getstarted/rag_eval/",
    "rag_eval_v0.3.0.html": "https://docs.ragas.io/en/v0.3.0/getstarted/rag_eval/",
    "cli_rag_eval_stable.html": "https://docs.ragas.io/en/stable/howtos/cli/rag_eval/",
    "experimentation_stable.html": "https://docs.ragas.io/en/stable/concepts/experimentation/",
}

out_dir = "evals/datasets/ragas_docs"
os.makedirs(out_dir, exist_ok=True)

for name, url in URLS.items():
    path = os.path.join(out_dir, name)
    print("Downloading:", url)

    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp, open(path, "wb") as f:
        f.write(resp.read())
    print("Saved:", path)