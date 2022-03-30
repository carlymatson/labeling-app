from pathlib import Path
import csv
import re
from pprint import pprint
import json


def underscore_to_title_case(s: str):
    without_underscores = " ".join(s.split("_"))
    return without_underscores.title()


def get_D1_dictionary(text):
    all_matches = re.findall("D1: ([a-zA-Z ]+)\nDefinition\n(.+)\n", text)
    d1_labels = {name: defn for name, defn in all_matches}
    return d1_labels


def parse_confluence_docs():
    root = Path(__file__).parent
    confluence_path = root / "confluence_docs"
    sublabels = {}
    for pth in confluence_path.iterdir():
        d0_name = underscore_to_title_case(pth.stem)
        text = pth.read_text()
        d1_labels = get_D1_dictionary(text)
        sublabels[d0_name] = d1_labels
    return sublabels


def parse_docs():
    root = Path(__file__).parent
    confluence_path = root / "confluence_docs"
    for pth in confluence_path.iterdir():
        d0_name = underscore_to_title_case(pth.stem)


def nested_dict_to_rows(d):
    rows = []
    for key1, subdict_1 in d.items():
        for key2, value in subdict_1.items():
            rows.append((key1, key2, value))
    return rows


def write_to_csv(rows, filename):
    path = Path(filename)
    with path.open("w") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(["D0", "D1", "Definition"])
        csvwriter.writerows(rows)


if __name__ == "__main__":
    labels_combos = parse_confluence_docs()
    combo_rows = nested_dict_to_rows(labels_combos)
    write = True
    if write:
        write_to_csv(combo_rows, "vocabulary_D0D1.csv")
    pprint(combo_rows)
