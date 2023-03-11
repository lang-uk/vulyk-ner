# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from vulyk.models.task_types import AbstractTaskType
from vulyk_ner.models.tasks import NERTaggingAnswer, NERTaggingTask


class NERTaggingTaskType(AbstractTaskType):
    """
    NER Tagging Task to work with Vulyk.
    """

    answer_model = NERTaggingAnswer
    task_model = NERTaggingTask

    name = "Тегування іменованих сутностей в тексті"
    description = "Допоможіть нам знайти людей, організації, локації та інші іменовані сутності в тексті"

    template = "base.html"
    helptext_template = "help.html"
    type_name = "ner_tagging_task"

    redundancy = 2

    JS_ASSETS = [
        "static/scripts/vendor/jquery-ui.min.js",
        "static/scripts/vendor/jquery-ui.combobox.js",
        "static/scripts/vendor/jquery.svg.min.js",
        "static/scripts/vendor/jquery.svgdom.min.js",
        "static/scripts/vendor/jquery.ba-bbq.min.js",
        "static/scripts/vendor/jquery.json.min.js",
        "static/scripts/vendor/sprintf.js",
        "static/scripts/vendor/webfont.js",
        # # brat helpers
        "static/scripts/src/configuration.js",
        "static/scripts/src/util.js",
        "static/scripts/src/annotation_log.js",
        # # brat modules
        "static/scripts/src/dispatcher.js",
        "static/scripts/src/url_monitor.js",
        "static/scripts/offline_ajax.js",
        "static/scripts/src/visualizer.js",
        "static/scripts/src/visualizer_ui.js",
        "static/scripts/src/annotator_ui.js",
        "static/scripts/src/spinner.js",
        "static/scripts/init.js",
    ]

    CSS_ASSETS = [
        "static/styles/jquery-theme/jquery-ui.css",
        "static/styles/jquery-theme/jquery-ui-redmond.css",
        "static/styles/style-vis.css",
        "static/styles/style-ui.css",
        "static/styles/fixes.css",
    ]
