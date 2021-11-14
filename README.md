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
python3 -m unittest discover -s test
```

## Conversion utils included

### Preprocess plain text and format it into Vulyk JSON
This will tokenize text, perform NER search and output results into Vulyk compatible json format.

```shell
cat file.txt | python3 convert2vulyk.py > save_to_file.json
```

Import to Vulyk 
```shell
./manage.py db load ner_tagging_task --batch batch_name ./path/save_to_file.json
```

You can also convert to vulyk json an already annotated text (Brat format only):
```shell
python3 convert2vulyk.py --brat_annotation annotation.ann > save_to_file.json
```

For more details and possible parameters refer to `python3 convert2vulyk.py -h`

