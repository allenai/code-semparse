import json
import os

with open("source_domain_with_target_num0/split.json") as fp:
    split = json.load(fp)
    train = split["train"]
    test = split["test_s"]

os.makedirs("iid", exist_ok=True)
with open("iid/split.json", "w") as fp:
    fp.write(json.dumps({
        "train": train,
        "test": test,
    }) + "\n")