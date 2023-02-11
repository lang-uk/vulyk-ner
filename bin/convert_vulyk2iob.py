import argparse
import json
import logging
import re
import glob
import pathlib
from typing import Union, List

log = logging.getLogger(__name__)


def convert_answer(task_record: dict) -> Union[str, None]:
    warning: bool = False

    for f in ["text", "token_offsets", "entities", "sentence_offsets"]:
        if f not in task_record:
            log.warning(f"Cannot find field {f} in answer")
            warning = True

    if warning:
        return None

    text: str = task_record["text"]

    # Sorting just to make sure that we are fine
    sentences_off: List[List[int]] = sorted(task_record["sentence_offsets"], key=lambda x: x[0])
    tokens_off: List[List[int]] = sorted(task_record["token_offsets"], key=lambda x: x[0])
    entities: List[tuple[str, int, int]] = []

    # Rearranging entities a bit
    # Treating fragmented entities as separate for now
    for ent in task_record["entities"]:
        for subent in ent[2]:
            entities.append((ent[1], subent[0], subent[1]))

    entities = sorted(entities, key=lambda x: x[1])

    current_sent: int = 0
    prev_position: int = 0
    current_entity: int = 0
    result: List[str] = []

    for token in tokens_off:
        # First add things in between tokens
        if token[0] > prev_position + 1:
            result.append(text[prev_position : token[0]] + " O")

        # Validate boundaries of sentences
        if token[0] > sentences_off[current_sent][1]:
            current_sent += 1
            result.append("")

        tag: str = " O"
        if current_entity < len(entities):
            if entities[current_entity][2] > token[0] >= entities[current_entity][1]:
                if token[0] == entities[current_entity][1]:
                    tag = f" B-{entities[current_entity][0]}"
                else:
                    tag = f" I-{entities[current_entity][0]}"

            if token[1] >= entities[current_entity][2]:
                current_entity += 1

        # Adding the token itself
        result.append(text[token[0] : token[1]] + tag)

        prev_position = token[1]

    # Leftovers
    if text[prev_position:]:
        result.append(text[prev_position:] + " O")

    return "\n".join(result)


def parse_jsonlines(jsonl_file: pathlib.Path, output_dir: pathlib.Path) -> None:
    input_file_base: str = jsonl_file.with_suffix("").name

    batch_dir: pathlib.Path = output_dir / input_file_base
    batch_dir.mkdir(exist_ok=True)

    with jsonl_file.open("r") as fp:
        for line_no, l in enumerate(fp):
            for answer in json.loads(l):
                for f in ["answer", "task", "user"]:
                    if f not in answer:
                        log.warning(f"Cannot find field {f} in answer, skipping")
                        continue

                iob = convert_answer(answer["answer"])
                if iob is None:
                    log.warning(f"Cannot find parse answer in the line #{line_no} of file {fp}, skipping")
                    continue
                else:
                    user: str = answer["user"]["username"].replace("@", "_").replace(".", "_")
                    user_dir: pathlib.Path = batch_dir / user
                    user_dir.mkdir(exist_ok=True)

                    with open(user_dir / (answer["task"]["id"] + ".iob"), "w") as fp_out:
                        fp_out.write(iob)


if __name__ == "__main__":
    logging.basicConfig()

    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Convert jsonlines output files exported from vulyk into IOB format (currently). "
        "Each answer will be stored in the separate file, located in the `batch_dir/username/task_id.iob`"
    )

    parser.add_argument("jsonl_files", help="File mask to collect jsonlines files to process.")
    parser.add_argument("output_dir", help="Directory to store converted files", type=pathlib.Path)

    parser.add_argument(
        "-d",
        "--debug",
        help="Print even more logs (debug)",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
        default=logging.WARNING,
    )

    parser.add_argument(
        "-v",
        "--verbose",
        help="Print more logs (info)",
        action="store_const",
        dest="loglevel",
        const=logging.INFO,
    )

    args: argparse.Namespace = parser.parse_args()
    assert args.output_dir.is_dir(), f"{args.output_dir} is not a directory"

    log.setLevel(args.loglevel)

    for jsonl in map(pathlib.Path, glob.glob(args.jsonl_files)):
        parse_jsonlines(jsonl, args.output_dir)
