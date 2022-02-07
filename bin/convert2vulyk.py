#!env python

import argparse
import json
import logging
import re
import time
import glob
import pathlib
from typing import Any, Generator
from collections import namedtuple
from enum import Enum
from itertools import chain

from tokenize_uk import tokenize_text  # type: ignore

log = logging.getLogger(__name__)

BsfInfo = namedtuple("BsfInfo", "id, tag, start_idx, end_idx, token")


class AlignedToken(namedtuple("AlignedToken", ("token", "orig_pos", "new_pos"))):
    """
    As we do changing the whitespaces in tokenized text according to the punctuation rules,
    we need a class to maintain the positions of whitespace tokenized vs. normalized one
    """

    __slots__: tuple = ()

    def __str__(self) -> str:
        return str(self.token)


class TokenizationType(Enum):
    NOOP = 1
    WHITESPACE = 2
    TOKENIZE_UK = 3


class AbstractNER:
    def __init__(self, model: str) -> None:
        raise NotImplementedError()

    def tag_text(self, txt: str) -> str:
        raise NotImplementedError()


class StanzaNER(AbstractNER):
    def __init__(self, model: str) -> None:
        import stanza  # type: ignore

        logging.getLogger("stanza").setLevel(log.level)
        stanza.download(model)

        self.ner = stanza.Pipeline(lang=model, processors="tokenize,mwt,ner", tokenize_pretokenized="true")

    def tag_text(self, txt: str) -> str:
        doc = self.ner(txt)

        brat_str: str = ""

        for tok_i, ent in enumerate(doc.ents):
            brat_str += f"T{tok_i + 1}\t{ent.type} {ent.start_char} {ent.end_char}\t{ent.text}\n"

        return brat_str


class SpacyNER(AbstractNER):
    def __init__(self, model: str) -> None:
        import spacy

        self.ner = spacy.load(model)

    def tag_text(self, txt: str) -> str:
        doc = self.ner(txt)

        brat_str: str = ""

        if doc.ents:
            for tok_i, ent in enumerate(doc.ents):
                brat_str += f"T{tok_i + 1}\t{ent.label_} {ent.start_char} {ent.end_char}\t{ent.text}\n"

        return brat_str


def parse_bsf(bsf_data: str) -> list[BsfInfo]:
    """
    Convert multiline textual bsf representation to a list of named entities.

    :param bsf_data: data in the format 'T9 PERS 778 783    токен'. Can be multiple lines.
    :return: list of named tuples for each line of the data representing a single named entity token
    """

    data = bsf_data.strip()
    if not data:
        return []
    #                     Token_id Entity start  end    text within range
    #                        \/      \/     \/    \/      \/
    ln_ptrn = re.compile(r"(T\d+)\s(\w+)\s(\d+)\s(\d+)\s(.+?)(?=T\d+\s\w+\s\d+\s\d+|$)", flags=re.DOTALL)
    result: list = []
    for m in ln_ptrn.finditer(data):
        bsf = BsfInfo(m.group(1), m.group(2), int(m.group(3)), int(m.group(4)), m.group(5).strip())
        result.append(bsf)
    return result


def simple_tokenizer(text: str) -> list[list[str]]:
    """
    Given whitespace/newline tokenized text, return the
    list of sentences (where each sentence is made of tokens)
    using whitespaces and newlines
    """

    doc: list[list[str]] = []
    if text:
        for s in text.split("\n"):
            doc.append(s.split(" "))

    return doc


def read_and_tokenize(text: str, fmt: str, tokenizer: TokenizationType) -> list[list[str]]:
    if fmt == "json":
        assert tokenizer == TokenizationType.NOOP, "Json is meant to be already tokenized"
        return json.loads(text)
    else:
        assert tokenizer != TokenizationType.NOOP, "You cannot keep texts not-tokenized"
        if tokenizer == TokenizationType.WHITESPACE:
            return simple_tokenizer(text)
        elif tokenizer == TokenizationType.TOKENIZE_UK:
            return list(chain(*tokenize_text(text)))

    return []  # Calm down, mypy


def reconstruct_tokenized(tokenized_text: list[list[str]]) -> Generator[AlignedToken, None, None]:
    """
    Accepts tokenized text [["sent1_word1", "sent1_word2"], ["sent2_word2"]]
    and normalizing the spaces in the text according to the punctuation.
    Returns an iterator over AlignedToken, where each token has the information
    on the original position and updated position
    """
    SPACES_BEFORE: str = "([“«"
    NO_SPACE_BEFORE: str = ".,:!?)]”»"

    orig_pos: int = 0
    adj_pos: int = 0

    for s_idx, s in enumerate(tokenized_text):
        if s_idx > 0:
            yield AlignedToken("\n", (orig_pos, orig_pos + 1), (adj_pos, adj_pos + 1))
            orig_pos += 1
            adj_pos += 1

        prev_token: str = ""
        for w_idx, w in enumerate(s):
            w_stripped = w.strip()

            if not w_stripped:
                # If original text contained a space(-es), let's adjust original position for it
                # + one space after
                orig_pos += len(w)
                if w_idx > 0:
                    orig_pos += 1

                continue

            if w_idx > 0:
                if w_stripped not in NO_SPACE_BEFORE and not prev_token in SPACES_BEFORE:
                    yield AlignedToken(" ", (orig_pos, orig_pos + 1), (adj_pos, adj_pos + 1))
                    orig_pos += 1
                    adj_pos += 1
                else:
                    # If we are omitting the space (for example, before comma), we
                    # adjusting original position as if it's there
                    orig_pos += 1

            yield AlignedToken(w_stripped, (orig_pos, orig_pos + len(w)), (adj_pos, adj_pos + len(w_stripped)))

            orig_pos += len(w)
            adj_pos += len(w_stripped)

            prev_token = w_stripped


def convert_bsf_2_vulyk(tokenized_text: list[list[str]], bsf_markup: str, compensate_for_offsets: bool = False) -> dict:
    """
    Given tokenized text and named entities in Brat standoff format, generate object
    in the format compatible with Vulyk markup tool.
    :param text: tokenized text
    :param bsf_markup: named entities in Brat standoff format
    :param compensate_for_offsets: when converting already tokenized text from txt/ann pair, this will
    displace NER tokens according to the changes made to the punctuation/whitespaces
    :return: dict that can be directly converted to Vulyk json file
    """

    tags_mapping = {"PERS": "ПЕРС", "ORG": "ОРГ", "LOC": "ЛОК", "MISC": "РІЗН"}

    bsf: list[BsfInfo] = parse_bsf(bsf_markup)
    ents: list[list[Any]] = [[e.id, tags_mapping.get(e.tag, e.tag), [(e.start_idx, e.end_idx)]] for e in bsf]

    idx: int = 0
    t_idx: int = 0
    s_offsets: list[tuple[int, int]] = []
    t_offsets: list[tuple[int, int]] = []
    text: str = ""
    s: str = ""
    prev_displacement: int = 0

    displacements: list[tuple[int, int]] = []

    for w in reconstruct_tokenized(tokenized_text):
        # Here we constructing a displacement map, i.e how we should adjust all the entities
        # after origina tokens were displaced according to space normalization.
        if w.orig_pos[0] > w.new_pos[0]:
            if w.orig_pos[0] - w.new_pos[0] > prev_displacement:
                displacements.append((w.orig_pos[0], w.orig_pos[0] - w.new_pos[0] - prev_displacement))
                prev_displacement = w.orig_pos[0] - w.new_pos[0]

        if w.token == "\n":
            if s:
                s_offsets.append((idx, idx + len(s)))

            idx += len(s) + 1
            s = ""
        else:
            s += w.token

        text += w.token

        if w.token not in [" ", "\n"]:
            t_offsets.append((t_idx, t_idx + len(w.token)))

        t_idx += len(w.token)

    if s:
        s_offsets.append((idx, idx + len(s)))

    if compensate_for_offsets:
        for ent in ents:
            offset: int = 0
            for disp in displacements:
                if ent[2][0][0] >= disp[0]:
                    offset += disp[1]

            ent[2][0] = (ent[2][0][0] - offset, ent[2][0][1] - offset)

    ts: int = int(time.time())
    vulyk: dict = {
        "modifications": [],
        "equivs": [],
        "protocol": 1,
        "ctime": ts,
        "triggers": [],
        "text": text,
        "source_files": ["ann", "txt"],
        "messages": [],
        "sentence_offsets": s_offsets,
        "comments": [],
        "entities": ents,
        "mtime": ts,
        "relations": [],
        "token_offsets": t_offsets,
        "action": "getDocument",
        "normalizations": [],
        "attributes": [],
        "events": [],
        "document": "",
        "collection": "/",
    }

    return vulyk


def convert(input_files: str, fmt: str, ignore_annotations: bool, ann_autodiscovery: str) -> None:
    for text in map(pathlib.Path, glob.glob(input_files)):
        log.info(f"Found text file {text}, parsing it")

        markup = ""

        if not ignore_annotations:
            if ann_autodiscovery == "append":
                ann = text.with_name(text.name + ".ann")
            else:
                ann = text.with_suffix(".ann")

            if not ann.exists():
                log.warning(f"Cannot find annotation file {ann} alongside to text file {text}, skipping")
            else:
                markup = ann.read_text()

        tokenized: list[list[str]] = read_and_tokenize(
            text.read_text(), fmt, TokenizationType.NOOP if fmt == "json" else TokenizationType.WHITESPACE
        )

        vulyk_obj: dict = convert_bsf_2_vulyk(tokenized, markup, compensate_for_offsets=True)
        print(json.dumps(vulyk_obj, ensure_ascii=False, sort_keys=True))


def convert_command(args: argparse.Namespace) -> None:
    return convert(
        input_files=args.input_files,
        fmt=args.format,
        ignore_annotations=args.ignore_annotations,
        ann_autodiscovery=args.ann_autodiscovery,
    )


def tag(input_files: str, fmt: str, ner_framework: str, ner_model: str) -> None:
    if ner_framework == "stanza":
        model: AbstractNER = StanzaNER(ner_model)
    elif ner_framework == "spacy":
        model = SpacyNER(ner_model)

    for text in map(pathlib.Path, glob.glob(input_files)):
        log.info(f"Found text file {text}, tagging it")

        tokenized: list[list[str]] = read_and_tokenize(
            text.read_text(), fmt, TokenizationType.NOOP if fmt == "json" else TokenizationType.TOKENIZE_UK
        )

        markup: str = model.tag_text("".join(map(str, reconstruct_tokenized(tokenized))))

        vulyk_obj = convert_bsf_2_vulyk(tokenized, markup, compensate_for_offsets=False)

        print(json.dumps(vulyk_obj, ensure_ascii=False, sort_keys=True))


def tag_command(args: argparse.Namespace) -> None:
    return tag(args.input_files, args.format, args.ner_framework, args.ner_model)


if __name__ == "__main__":
    logging.basicConfig()

    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Convert tokenized pre-annotated texts or tag generic texts to jsonlines file supported by Vulyk. \n"
        "Data files supplied via glob-like cmd line arguments. Output goes directly to stdout. \n"
        "Script has two modes: convert, to convert texts (with optional annotations) "
        "and tag, to tag provided tokenized texts using one of supported frameworks. "
        "Please check help texts for the respecting commands for details on parameters."
    )

    subparsers: argparse._SubParsersAction = parser.add_subparsers(dest="cmd", help="Available commands")

    convert_parser: argparse.ArgumentParser = subparsers.add_parser(
        "convert",
        help="Convert tokenized texts (with optional annotations in a separate files) to a Vulyk format "
        "To make it parse all text files together with annotations you should use something like this "
        "`python bin/convert2vulyk.py convert -v 'corpus/*.txt'`. Annotation auto-discovery is ruled "
        "by the setting --ann_autodiscovery, which might append or replace .ann extension in the name of the text file "
        "To disable annotation auto-discovery use --ignore_annotations flag",
    )

    convert_parser.set_defaults(func=convert_command)
    convert_parser.add_argument(
        "--ann_autodiscovery",
        default="replace",
        choices=("append", "replace"),
        help="How to find *.ann files: by appending or replacing the extension",
    )
    convert_parser.add_argument(
        "--ignore_annotations", default=False, action="store_true", help="Do not try to load *.ann files"
    )

    tag_parser: argparse.ArgumentParser = subparsers.add_parser(
        "tag",
        help="Tag given files using one of frameworks/models specified in params. "
        "Currently the script supports Stanza and Spacy frameworks. To use the script in this mode you should install "
        "additional packages from extra_requirements.txt. "
        "Make sure that you have enough RAM and some patience",
    )

    tag_parser.add_argument(
        "--ner_framework",
        choices=("stanza", "spacy"),
        default="stanza",
        help="Which framework to use for the tagging",
    )

    tag_parser.add_argument(
        "--ner_model",
        default="uk",
        help="Which model to use. Stanza has pre-built model `uk` for ukrainian language. "
        "For Spacy you might specify pre-built model (you should run `python -m spacy download model_name` first) "
        "or provide a path to the directory with the model",
    )

    tag_parser.set_defaults(func=tag_command)

    parser.add_argument(
        "input_files",
        help="File mask to collect files to process. "
        "Might be raw texts or json files in format "
        "`[['sent1_word1', 'sent1_word2'], ['sent2_word1', 'sent2_word2']]`. "
        "Use `--format` flag to specify the format [`txt` (default) or `json`]. "
        "For text files tokenize_uk tokenizer will be applied. "
        "For json files, provided tokenization will remain intact, however, "
        "spaces will be normalized/restored according to the `reconstruct_tokenized` logic",
    )

    parser.add_argument(
        "-f",
        "--format",
        help="How to treat input files? As textual or pre-tokenized json's",
        dest="format",
        choices=("txt", "json"),
        default="txt",
    )

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

    log.setLevel(args.loglevel)

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_usage()
