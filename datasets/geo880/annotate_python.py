# interactive annotation tool for geo880 dataset
# pick a random example from the dataset, ask the user to annotate it
# then update the dataset with the annotation

import json
import random

filepath = "all.jsonl"
examples = [json.loads(line) for line in open(filepath, "r")]

random = random.Random(0)
while True:
    ex = random.choice(examples)
    if "python" in ex:
        continue
    print(ex["query"])
    print(ex["funql"])

    # ask for multiple lines of input
    annotation = ""
    while True:
        line = input()
        annotation += line + "\n"
        if not line and annotation.strip():
            break

    if annotation == "exit":
        break

    ex["python"] = annotation.replace("#", "").replace("\t", "    ").strip()
    with open(filepath, "w") as f:
        for ex in examples:
            f.write(json.dumps(ex) + "\n")
