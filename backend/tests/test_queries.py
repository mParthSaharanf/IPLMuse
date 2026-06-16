import requests
import json

results = []

with open("queries.txt") as f:
    questions = [line.strip() for line in f if line.strip()]

for q in questions:
    r = requests.get(
        "http://localhost:8000/ask",
        params={"q": q}
    )

    results.append({
        "question": q,
        "response": r.json()
    })

with open("results5.json", "w") as f:
    json.dump(results, f, indent=4)

print("Saved results to results.json")