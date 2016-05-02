$(function() {
    dispatcher = new Dispatcher();
    var urlMonitor = new URLMonitor(dispatcher);
    var ajax = new OfflineAjax(dispatcher);
    var visualizer = new Visualizer(dispatcher, 'svg');
    var svg = visualizer.svg;
    var visualizerUI = new VisualizerUI(dispatcher, svg);
    var annotatorUI = new AnnotatorUI(dispatcher, svg);
    var spinner = new Spinner(dispatcher, '#spinner');
    var logger = new AnnotationLog(dispatcher);
    dispatcher.post('init');

    function set_current_doc(curr_doc) {
        curr_doc.create_new_entity = function(type_, offset, comment, attr) {
            // TODO: support for attrs

            var max_id = 0,
                i, entity, curr_id, new_id;

            for (i = this["entities"].length - 1; i >= 0; i--) {
                entity = this["entities"][i];
                curr_id = parseInt(entity[0].slice(1));

                if (curr_id > max_id) {
                    max_id = curr_id;
                }
            }
            new_id = "T" + (max_id + 1)

            this["entities"].push([
                new_id,
                type_,
                offset
            ]);

            this.add_comment(new_id, comment)
        }

        curr_doc.update_entity = function(id, type_, offset, comment, attr) {
            this.delete_entity(id);

            this["entities"].push([
                id,
                type_,
                offset
            ]);

            this.add_comment(id, comment)
        }

        curr_doc.delete_entity = function(id) {
            var i, entity;

            for (i = this["entities"].length - 1; i >= 0; i--) {
                entity = this["entities"][i];
                if (entity[0] == id) {
                    this["entities"].splice(i, 1)
                    break;
                };
            }

            curr_doc.delete_comment(id);
        }

        curr_doc.add_comment = function(id, comment) {
            // First delete it (if any)
            this.delete_comment(id);

            if (comment) {
                this["comments"].push([
                    id, 
                    "AnnotatorNotes",
                    comment
                ]);
            }
        }

        curr_doc.delete_comment = function(id) {
            var i, curr_comment;

            for (i = this["comments"].length - 1; i >= 0; i--) {
                curr_comment = this["comments"][i];

                if (curr_comment[0] == id) {
                    this["comments"].splice(i, 1)
                    break;
                }
            }
        }

        window._current_doc = curr_doc;
        var words_count = $.grep(window._current_doc["token_offsets"], function(el, i){
            if ((el[1] - el[0]) > 1) {
                return true;
            }
            if (/[а-яА-ЯєіїЄЇІ]/.test(window._current_doc["text"].slice(el[0], el[1]))) {
                return true;
            } else {
                return false;
            }
        }).length;

        $(".stats-brat strong").html(words_count);
    }

    $(document.body).on("vulyk.next", function(e, data) {
        set_current_doc(data.result.task.data);
        dispatcher.post(0, "renderData", [data.result.task.data]);
    }).on("vulyk.save", function(e, callback) {
        callback(window._current_doc);
    }).on("vulyk.skip", function(e, callback) {
        callback();
    }).on("vulyk.task_error", function(e, data) {
        $.magnificPopup.open({
            items: {
                src: '<div class="zoom-anim-dialog small-dialog">' +
                '<div class="dialog-content">Нажаль, увесь пакет завдань був виконаний, але дуже скоро ми додамо нові.</div>' +
                '</div>',
                type: 'inline'
            }
        })
    });
});