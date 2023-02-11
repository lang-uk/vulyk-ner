import sys
from typing import List
import argparse

from convert2vulyk import reconstruct_tokenized


def convert_sentence(sentence: List[str], prefix_text: str = "речення: ", no_tags_text: str = "Ніц нема") -> str:
    tokens: List[str] = []
    ner_tokens: List[str] = []

    ner_token_accum: List[str] = []
    ner_token_type: str = ""

    for line in sentence:
        w, tag = line.split(" ")
        tokens.append(w)

        if tag == "O" or tag.startswith("B-"):
            if ner_token_accum:
                ner_tokens.append(f"{ner_token_type}: {''.join(map(str, reconstruct_tokenized([ner_token_accum])))}")
                ner_token_accum = []

        if tag.startswith("B-"):
            ner_token_accum.append(w)
            ner_token_type = tag.replace("B-", "")

        if tag.startswith("I-"):
            ner_token_accum.append(w)

    final_sentence: str = "".join(map(str, reconstruct_tokenized([tokens])))
    if ner_tokens:
        return prefix_text + final_sentence + "\n" + '\n'.join(ner_tokens)
    else:
        return prefix_text + final_sentence + "\n" + no_tags_text


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Convert fixed-split dataset (IOB) prepared for the training of classifiers to"
        "the prompt format, suitable for the GPT2 eval. Output goes to stdout by default"
    )

    parser.add_argument("infile", nargs="?", type=argparse.FileType("r"), default=sys.stdin)
    parser.add_argument("outfile", nargs="?", type=argparse.FileType("w"), default=sys.stdout)

    args: argparse.Namespace = parser.parse_args()

    accum: List[str] = []

    for line in map(str.strip, args.infile):
        if not line.strip():
            if accum:
                args.outfile.write(convert_sentence(accum) + "\n\n")
                accum = []
        else:
            accum.append(line)

