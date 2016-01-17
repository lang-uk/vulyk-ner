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
                        data = {
                            "modifications": [],
                            "normalizations": [],
                            "ctime": 1452432571.0,
                            "triggers": [],
                            "text": "Algemeen Minder sperma achter het stuur De Morgen Dat heeft alles te maken met de hoge temperatuur van de balzak, die bij mannen die in de auto zitten na twee uur rijden met meer dan twee graden stijgt, van 34,2 graden naar 36,2 graden. Dr. Mieusset mat de temperatuur bij de proefpersonen elke twee minuten op door thermometers die bevestigd waren aan het scrotum in een auto zonder airconditioning. Maar niet alleen lange ritten hebben een negatieve invloed op de productie van sperma, ook korte ritten van amper twintig minuten doen de temperatuur in de balzak al stijgen. Mannen die veel achter het stuur zitten, of ze nu trucker zijn of vertegenwoordiger, doen er langer over om hun vrouw zwanger te maken. Dat veel autorijden de kwaliteit van het sperma aantast, bleek al uit vorig onderzoek. Een auto met airconditioning is dus geen overbodig luxe voor wie vaak op de baan is. Dat heeft alles te maken met de kwaliteit van hun sperma, dat aangetast wordt door de lange autoritten. Aula pagina Nu is bewezen dat de stijgende temperatuur in de balzak verantwoordelijk is voor de slechtere kwaliteit. Dr. Roger Mieusset, die de Human Fertility Research Group in Toulouse leidt, ontdekte dat professionele automobilisten niet alleen minder sperma produceren, maar dat hun sperma ook meer afwijkingen vertoont. auteur Als de normale temperatuur in de balzak 34,2 graden is, dan wordt het na twintig minuten al één graad warmer dan goed is voor het sperma. publicatie Al kunnen andere factoren in de levensstijl van mensen die voor hun werk veel achter het stuur zitten, ook een invloed hebben. sectie editie Katrijn Serneels (KS) publicatiedatum vrijdag, 2 juni 2000 ",
                            "source_files": ["ann", "txt"],
                            "mtime": 1452432571.0,
                            "messages": [],
                            "sentence_offsets": [
                                [0, 236],
                                [237, 400],
                                [401, 575],
                                [576, 711],
                                [712, 798],
                                [799, 883],
                                [884, 987],
                                [988, 1104],
                                [1105, 1668]
                            ],
                            "relations": [],
                            "entities": [
                                ["T1", "ORG", [
                                    [40, 49]
                                ]],
                                ["T2", "PER", [
                                    [241, 249]
                                ]],
                                ["T3", "MISC", [
                                    [988, 992]
                                ]],
                                ["T4", "PER", [
                                    [1109, 1123]
                                ]],
                                ["T5", "ORG", [
                                    [1132, 1162]
                                ]],
                                ["T6", "LOC", [
                                    [1166, 1174]
                                ]],
                                ["T7", "PER", [
                                    [1610, 1626]
                                ]],
                                ["T8", "PER", [
                                    [1628, 1630]
                                ]],
                                ["T9", "LOC", [
                                    [1182, 1208]
                                ]],
                                ["T10", "ORG", [
                                    [1209, 1223]
                                ]]
                            ],
                            "comments": [
                                ["T10", "AnnotatorNotes", "sdfg"]
                            ],
                            "token_offsets": [
                                [0, 8],
                                [9, 15],
                                [16, 22],
                                [23, 29],
                                [30, 33],
                                [34, 39],
                                [40, 42],
                                [43, 49],
                                [50, 53],
                                [54, 59],
                                [60, 65],
                                [66, 68],
                                [69, 74],
                                [75, 78],
                                [79, 81],
                                [82, 86],
                                [87, 98],
                                [99, 102],
                                [103, 105],
                                [106, 113],
                                [114, 117],
                                [118, 121],
                                [122, 128],
                                [129, 132],
                                [133, 135],
                                [136, 138],
                                [139, 143],
                                [144, 150],
                                [151, 153],
                                [154, 158],
                                [159, 162],
                                [163, 169],
                                [170, 173],
                                [174, 178],
                                [179, 182],
                                [183, 187],
                                [188, 194],
                                [195, 202],
                                [203, 206],
                                [207, 211],
                                [212, 218],
                                [219, 223],
                                [224, 228],
                                [229, 236],
                                [237, 240],
                                [241, 249],
                                [250, 253],
                                [254, 256],
                                [257, 268],
                                [269, 272],
                                [273, 275],
                                [276, 289],
                                [290, 294],
                                [295, 299],
                                [300, 307],
                                [308, 310],
                                [311, 315],
                                [316, 328],
                                [329, 332],
                                [333, 342],
                                [343, 348],
                                [349, 352],
                                [353, 356],
                                [357, 364],
                                [365, 367],
                                [368, 371],
                                [372, 376],
                                [377, 383],
                                [384, 400],
                                [401, 405],
                                [406, 410],
                                [411, 417],
                                [418, 423],
                                [424, 430],
                                [431, 437],
                                [438, 441],
                                [442, 451],
                                [452, 459],
                                [460, 462],
                                [463, 465],
                                [466, 475],
                                [476, 479],
                                [480, 487],
                                [488, 491],
                                [492, 497],
                                [498, 504],
                                [505, 508],
                                [509, 514],
                                [515, 522],
                                [523, 530],
                                [531, 535],
                                [536, 538],
                                [539, 550],
                                [551, 553],
                                [554, 556],
                                [557, 563],
                                [564, 566],
                                [567, 575],
                                [576, 582],
                                [583, 586],
                                [587, 591],
                                [592, 598],
                                [599, 602],
                                [603, 608],
                                [609, 616],
                                [617, 619],
                                [620, 622],
                                [623, 625],
                                [626, 633],
                                [634, 638],
                                [639, 641],
                                [642, 660],
                                [661, 665],
                                [666, 668],
                                [669, 675],
                                [676, 680],
                                [681, 683],
                                [684, 687],
                                [688, 693],
                                [694, 701],
                                [702, 704],
                                [705, 711],
                                [712, 715],
                                [716, 720],
                                [721, 731],
                                [732, 734],
                                [735, 744],
                                [745, 748],
                                [749, 752],
                                [753, 759],
                                [760, 768],
                                [769, 774],
                                [775, 777],
                                [778, 781],
                                [782, 787],
                                [788, 798],
                                [799, 802],
                                [803, 807],
                                [808, 811],
                                [812, 827],
                                [828, 830],
                                [831, 834],
                                [835, 839],
                                [840, 849],
                                [850, 854],
                                [855, 859],
                                [860, 863],
                                [864, 868],
                                [869, 871],
                                [872, 874],
                                [875, 879],
                                [880, 883],
                                [884, 887],
                                [888, 893],
                                [894, 899],
                                [900, 902],
                                [903, 908],
                                [909, 912],
                                [913, 915],
                                [916, 925],
                                [926, 929],
                                [930, 933],
                                [934, 941],
                                [942, 945],
                                [946, 955],
                                [956, 961],
                                [962, 966],
                                [967, 969],
                                [970, 975],
                                [976, 987],
                                [988, 992],
                                [993, 999],
                                [1000, 1002],
                                [1003, 1005],
                                [1006, 1013],
                                [1014, 1017],
                                [1018, 1020],
                                [1021, 1030],
                                [1031, 1042],
                                [1043, 1045],
                                [1046, 1048],
                                [1049, 1055],
                                [1056, 1072],
                                [1073, 1075],
                                [1076, 1080],
                                [1081, 1083],
                                [1084, 1093],
                                [1094, 1104],
                                [1105, 1108],
                                [1109, 1114],
                                [1115, 1124],
                                [1125, 1128],
                                [1129, 1131],
                                [1132, 1137],
                                [1138, 1147],
                                [1148, 1156],
                                [1157, 1162],
                                [1163, 1165],
                                [1166, 1174],
                                [1175, 1181],
                                [1182, 1190],
                                [1191, 1194],
                                [1195, 1208],
                                [1209, 1223],
                                [1224, 1228],
                                [1229, 1235],
                                [1236, 1242],
                                [1243, 1249],
                                [1250, 1261],
                                [1262, 1266],
                                [1267, 1270],
                                [1271, 1274],
                                [1275, 1281],
                                [1282, 1285],
                                [1286, 1290],
                                [1291, 1302],
                                [1303, 1312],
                                [1313, 1319],
                                [1320, 1323],
                                [1324, 1326],
                                [1327, 1334],
                                [1335, 1346],
                                [1347, 1349],
                                [1350, 1352],
                                [1353, 1359],
                                [1360, 1364],
                                [1365, 1371],
                                [1372, 1375],
                                [1376, 1379],
                                [1380, 1385],
                                [1386, 1389],
                                [1390, 1392],
                                [1393, 1400],
                                [1401, 1408],
                                [1409, 1411],
                                [1412, 1415],
                                [1416, 1421],
                                [1422, 1428],
                                [1429, 1432],
                                [1433, 1437],
                                [1438, 1440],
                                [1441, 1445],
                                [1446, 1449],
                                [1450, 1457],
                                [1458, 1468],
                                [1469, 1471],
                                [1472, 1478],
                                [1479, 1485],
                                [1486, 1494],
                                [1495, 1497],
                                [1498, 1500],
                                [1501, 1512],
                                [1513, 1516],
                                [1517, 1523],
                                [1524, 1527],
                                [1528, 1532],
                                [1533, 1536],
                                [1537, 1541],
                                [1542, 1546],
                                [1547, 1553],
                                [1554, 1557],
                                [1558, 1563],
                                [1564, 1571],
                                [1572, 1575],
                                [1576, 1579],
                                [1580, 1587],
                                [1588, 1595],
                                [1596, 1602],
                                [1603, 1609],
                                [1610, 1617],
                                [1618, 1626],
                                [1627, 1631],
                                [1632, 1647],
                                [1648, 1656],
                                [1657, 1658],
                                [1659, 1663],
                                [1664, 1668]
                            ],
                            "action": "getDocument",
                            "attributes": [],
                            "equivs": [],
                            "events": [],
                            "protocol": 1
                        };
                        dispatcher.post(0, callback, [data]);
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
                                                "name": "ORG",
                                                "normalizations": [],
                                                "type": "ORG",
                                                "unused": false
                                        },
                                        {
                                                "attributes": [],
                                                "bgColor": "#ffccaa",
                                                "borderColor": "darken",
                                                "children": [],
                                                "fgColor": "black",
                                                "labels": null,
                                                "name": "PER",
                                                "normalizations": [],
                                                "type": "PER",
                                                "unused": false
                                        },
                                        {
                                                "attributes": [],
                                                "bgColor": "lightgreen",
                                                "borderColor": "darken",
                                                "children": [],
                                                "fgColor": "black",
                                                "labels": null,
                                                "name": "LOC",
                                                "normalizations": [],
                                                "type": "LOC",
                                                "unused": false
                                        },
                                        {
                                                "attributes": [],
                                                "bgColor": "#f1f447",
                                                "borderColor": "darken",
                                                "children": [],
                                                "fgColor": "black",
                                                "labels": null,
                                                "name": "MISC",
                                                "normalizations": [],
                                                "type": "MISC",
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
