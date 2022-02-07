# NER tagging plugin for Vulyk, crowdsourcing framework

To connect plugin to Vulyk:
1. Install this plugin as pip package `pip install git+https://github.com/lang-uk/vulyk-ner.git`
2. Make sure to include configuration for it in `local_settings.py`
```python
ENABLED_TASKS = {
    # other plugins will be somewhere here
    'vulyk_ner': 'NERTaggingTaskType'
}
```

Full installation instructions can be found here https://github.com/mrgambal/vulyk

Running tests after you made changes
```shell
python -m unittest discover -s test
```

## Conversion utils included
There are two utitilies included in this package:
 * `convert2vulyk.py` which is Swiss Army Knife to convert/tag texts into the format, suitable for vulyk tasks
 * `convert_vulyk2iob.py` which allows you to convert the individual answers, exported from vulyk with `./manage.py db export` command into standard IOB

### Convert texts with `convert2vulyk.py`
`convert2vulyk.py` subcommand `convert` allows you to convert bunch of files (either txt or json, see `--format`) into a jsonlines file that you can feed directly into vulyk. It also can autodiscover annotation layer in brat standoff format (see `--ann_autodiscovery`). You can supply a glob-style string as `input_files` param for batch processing. Beware, when applied to raw txt file, the tool will fix the whitespaces around punctuation according to the rules of typography

#### Converting pre-tokenized json files ([["sent1_word1", "sent1_word2"], ["sent2_word1"]] format) 

```shell
python bin/convert2vulyk.py -f json convert  tokenized/jsons/*.json > vulyk_tasks.jsonlines
```
#### Converting text files with no annotations

This will tokenize input text files using whitespace tokenizer, adjust whitespaces and ignore annotation layer (if any)

```shell
python bin/convert2vulyk.py -f txt convert --ignore_annotations tokenized/txt/*.txt > vulyk_tasks.jsonlines
```

#### Converting text files with annotation layer stored in *.ann format

This will tokenize input text files using whitespace tokenizer, adjust whitespaces, autodiscover *.ann file next to *.txt (if any) and adjust positions of found NER tokens.

```shell
python bin/convert2vulyk.py -f txt convert  tokenized/txt/*.txt > vulyk_tasks.jsonlines
```

### Tag texts with `convert2vulyk.py`

Subcommand `tag` allows you to pre-annotate given texts (tokenized or raw) using either `stanza` or `spacy`. You might as well specify your own models with `--ner-model`

To do so, you have to install extra dependencies
```shell
pip install -r extra_requirements.txt
```

#### Tag pretokenized json files with SpaCy model

```shell
python bin/convert2vulyk.py -f json tag --ner_framework spacy --ner_model /my/best/spacy/model tokenized/json/*.json > vulyk_tasks.jsonlines
```

#### Tokenize and tag raw text files with stanza model
Beware: to tokenize raw texts, script will use lang-uk's `tokenize-uk` tokenizer, which is sometime naïve

```shell
python bin/convert2vulyk.py -f txt tag --ner_framework stanza --ner_model "uk" tokenized/txt/*.txt > vulyk_tasks.jsonlines
```

#### Import to Vulyk 
```shell
./manage.py db load ner_tagging_task --batch batch_name ./path/save_to_file.json
```

For more details and possible parameters refer to `python bin/convert2vulyk.py -h`

### Convert vulyk results to IOB with `convert2vulyk.py`
The tool allows you to convert one or more batches with answers, exported from vulyk into the iob files:

```shell
python bin/convert_vulyk2iob.py "test_results/*.jsonlines" test_results/iobs/
```

Each individual answer from the annotator will be stored according to scheme `{batch_dir}/{username}/{task_id}.iob`, where `batch_dir` is the basename of the input files, `username` is the name of the annotator, `task_id` is the unique identifier of the task from vulyk.

As usual, `python bin/convert_vulyk2iob.py -h` is your friend.
