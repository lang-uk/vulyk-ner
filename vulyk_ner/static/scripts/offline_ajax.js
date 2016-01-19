// -*- Mode: JavaScript; tab-width: 2; indent-tabs-mode: nil; -*-
// vim:set ft=javascript ts=2 sw=2 sts=2 cindent:

// Offline data files should go into URL_BASE directory (default:
// offline_data). Each directory should have collection.js which
// contains the result of getCollectionInformation action, and any
// number of *.data.js files, which contain the results of getDocument
// actions. The contents of both should be prefixed with "jsonp =".

var OfflineAjax = (function($, window, undefined) {
        var OfflineAjax = function(dispatcher) {
            var URL_BASE = 'offline_data';

            var that = this;
            var data;

            // merge data will get merged into the response data
            // before calling the callback
            var ajaxCall = function(data, callback, merge) {
                dispatcher.post('spin');

                var url;
                console.log(data.action);
                switch (data.action) {
                    case 'getDocument':
                        dispatcher.post('unspin');
                        return;

                    case 'getCollectionInformation':
                        data = {
                                "action": "getCollectionInformation",
                                "annotation_logging": false,
                                "description": null,
                                "disambiguator_config": [],
                                "entity_attribute_types": [],
                                "entity_types": [
                                        {
                                                "attributes": [],
                                                "bgColor": "#8fb2ff",
                                                "borderColor": "darken",
                                                "children": [],
                                                "fgColor": "black",
                                                "labels": null,
                                                "name": "ОРГ",
                                                "normalizations": [],
                                                "type": "ОРГ",
                                                "unused": false
                                        },
                                        {
                                                "attributes": [],
                                                "bgColor": "#ffccaa",
                                                "borderColor": "darken",
                                                "children": [],
                                                "fgColor": "black",
                                                "labels": null,
                                                "name": "ПЕРС",
                                                "normalizations": [],
                                                "type": "ПЕРС",
                                                "unused": false
                                        },
                                        {
                                                "attributes": [],
                                                "bgColor": "lightgreen",
                                                "borderColor": "darken",
                                                "children": [],
                                                "fgColor": "black",
                                                "labels": null,
                                                "name": "ЛОК",
                                                "normalizations": [],
                                                "type": "ЛОК",
                                                "unused": false
                                        },
                                        {
                                                "attributes": [],
                                                "bgColor": "#f1f447",
                                                "borderColor": "darken",
                                                "children": [],
                                                "fgColor": "black",
                                                "labels": null,
                                                "name": "РАЗН",
                                                "normalizations": [],
                                                "type": "РАЗН",
                                                "unused": false
                                        }
                                ],
                                "event_attribute_types": [],
                                "event_types": [],
                                "header": [
                                        [
                                                "Document",
                                                "string"
                                        ],
                                        [
                                                "Modified",
                                                "time"
                                        ],
                                        [
                                                "Entities",
                                                "int"
                                        ],
                                        [
                                                "Relations",
                                                "int"
                                        ],
                                        [
                                                "Events",
                                                "int"
                                        ]
                                ],
                                "items": [
                                        [
                                                "c",
                                                null,
                                                ".."
                                        ],
                                        [
                                                "d",
                                                null,
                                                "ned.train-doc-123",
                                                1396452023.0,
                                                32,
                                                0,
                                                0
                                        ],
                                        [
                                                "d",
                                                null,
                                                "ned.train-doc-46",
                                                1452371908.0,
                                                28,
                                                0,
                                                0
                                        ],
                                        [
                                                "d",
                                                null,
                                                "ned.train-doc-251",
                                                1354046512.0,
                                                21,
                                                0,
                                                0
                                        ],
                                        [
                                                "d",
                                                null,
                                                "ned.train-doc-118",
                                                1409691113.0,
                                                23,
                                                0,
                                                0
                                        ],
                                        [
                                                "d",
                                                null,
                                                "ned.train-doc-75",
                                                1452432571.0,
                                                10,
                                                0,
                                                0
                                        ],
                                        [
                                                "d",
                                                null,
                                                "ned.train-doc-181",
                                                1352355357.0,
                                                97,
                                                0,
                                                0
                                        ],
                                        [
                                                "d",
                                                null,
                                                "ned.train-doc-134",
                                                1399495899.0,
                                                16,
                                                0,
                                                0
                                        ],
                                        [
                                                "d",
                                                null,
                                                "ned.train-doc-236",
                                                1359766765.0,
                                                23,
                                                0,
                                                0
                                        ],
                                        [
                                                "d",
                                                null,
                                                "ned.train-doc-27",
                                                1452371778.0,
                                                23,
                                                0,
                                                0
                                        ],
                                        [
                                                "d",
                                                null,
                                                "ned.train-doc-184",
                                                1352355357.0,
                                                29,
                                                0,
                                                0
                                        ]
                                ],
                                "messages": [],
                                "ner_taggers": [],
                                "normalization_config": [],
                                "parent": "_2002",
                                "protocol": 1,
                                "relation_attribute_types": [],
                                "relation_types": [],
                                "search_config": [],
                                "ui_names": {
                                        "attributes": "attributes",
                                        "entities": "entities",
                                        "events": "events",
                                        "relations": "relations"
                                },
                                "unconfigured_types": [
                                        {
                                                "bgColor": "lightgreen",
                                                "borderColor": "darken",
                                                "fgColor": "black",
                                                "labels": null,
                                                "name": "SPAN_DEFAULT",
                                                "type": "SPAN_DEFAULT",
                                                "unused": true
                                        }
                                ]
                        }
                        dispatcher.post(0, callback, [data]);
                        dispatcher.post('unspin');
                        return;

                    case 'loadConf':
                        dispatcher.post(0, callback, [{"action": "loadConf", "messages": [], "protocol": 1}]);
                        dispatcher.post('unspin');
                        return;

                    case 'createSpan':
                        // url = '/ned.train-doc-118.data_edit.js'
                        // break
                        // window._current_doc
                        console.log(data);
                        window._current_doc.entities.push(
                            ["T12", data["type"], JSON.parse(data.offsets)]
                        );

                        dispatcher.post(0, callback, [
                                {
                                    "edited": [
                                            ["T16"]
                                    ],
                                    "protocol": 1,
                                    "messages": [],
                                    "undo": "{\"action\": \"add_tb\", \"attributes\": \"{}\", \"normalizations\": \"[]\", \"id\": \"T16\"}",
                                    "action": "createSpan",
                                    "annotations": window._current_doc
                                }
                        ]);
                        dispatcher.post('unspin');
                        return;

                    case 'whoami':
                        dispatcher.post(0, callback, [{"action": "whoami", "messages": [], "protocol": 1, "user": "crunchy"}]);
                        dispatcher.post('unspin');
                        return;

                    case 'storeSVG':
                        // ignore
                        // TODO: disable SVG links
                        dispatcher.post(0, callback, [{ user: null, messages: [], action: data.action }]);
                        dispatcher.post('unspin');
                        return;

                    default:
                        // an action that is not a visualisation action got through
                        alert("DEBUG TODO XXX UNSUPPORTED ALERT WHATNOW ETC: " + data.action); // XXX
                }

                // load the file
                // NOTE: beware, there is no error checking possible in this
                // loading method. No error handler. If the file is malformed,
                // there will be an error that is not under our control. If the
                // file is missing, there will be no error, and no callback -
                // the interface will get stuck. Be sure collection.js is up to
                // date, and no manual messing with URL :)
                var scr = document.createElement('script');
                scr.onload = function(evt) {
                    jsonp.messages = [];
                    if (merge) {
                        $.extend(jsonp, merge);
                    }
                    if (data.action == "getDocument") {
                        window._current_doc = jsonp;
                    }

                    dispatcher.post(0, callback, [jsonp]);
                    dispatcher.post('unspin');
                    document.head.removeChild(evt.target);
                };
                scr.type = 'text/javascript';
                scr.src = URL_BASE + url;
                document.head.appendChild(scr);

                /*
                * Chrome "feature" prevents this nice pure JSON solution
                * http://www.google.com/support/forum/p/Chrome/thread?tid=36708c2c62cb9b0c&hl=en
                * http://code.google.com/p/chromium/issues/detail?id=46167
                *
                *
                * chrome.exe --allow-file-access-from-files
                * open /Applications/Google\ Chrome.app --args --allow-file-access-from-files
                */
                /*
                var $iframe = $('<iframe/>');
                $iframe.bind('load', function(evt) {
                    console.log("foo3", evt.target);
                    var json = $iframe.contents().text();
                    console.log("ok1");
                    var response = $.parseJSON(json);
                    console.log("ok2", merge, json);
                    response.messages = [];
                    response.action = [];
                    $iframe.remove();

                    if (merge) {
                        $.extend(response, merge);
                    }
                    dispatcher.post(0, callback, [response]);
                    dispatcher.post('unspin');
                });

                $('body').append($iframe);
                $iframe.css('display', 'none');
                $iframe.attr('src', URL_BASE + url);
                console.log("foo2", $iframe);
                */
            };

            dispatcher.
                    on('ajax', ajaxCall);
        };

        return OfflineAjax;
})(jQuery, window);
