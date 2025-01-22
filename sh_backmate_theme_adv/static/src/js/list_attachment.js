/** @odoo-module **/
import ListController from "web.ListController";
import ListRenderer from "web.ListRenderer";
import rpc from 'web.rpc';
import DocumentViewer from '@mail/js/document_viewer';
import core from "web.core";
const _t = core._t;

// var ListRenderer = require('web.ListRenderer');

ListRenderer.include({

    events: _.extend({}, ListRenderer.prototype.events, {
        "click .sh_attachment_item": "shShowAttachmemt",
    }),

    shShowAttachmemt: function (ev) {
        let attachment_id = parseInt($(ev.currentTarget).data("id"));
        let record_id = parseInt($(ev.currentTarget).data("record_id"));
        let attachment_mimetype = $(ev.currentTarget).data("mimetype");
        let mimetype_match = attachment_mimetype.match("(image|application/pdf|text|video)");
        var attachment_data = this.sh_attachments[0];
        if (mimetype_match) {
            var sh_attachment_id = attachment_id;
            var sh_attachment_list = [];
            attachment_data[record_id].forEach((attachment) => {
                if (attachment.attachment_mimetype.match("(image|application/pdf|text|video)")) {
                    sh_attachment_list.push({
                        id: attachment.attachment_id,
                        filename: attachment.attachment_name,
                        name: attachment.attachment_name,
                        url: "/web/content/" + attachment.attachment_id + "?download=true",
                        type: attachment.attachment_mimetype,
                        mimetype: attachment.attachment_mimetype,
                        is_main: false,
                    });
                }
            });
            var sh_attachmentViewer = new DocumentViewer(self, sh_attachment_list, sh_attachment_id);
            sh_attachmentViewer.appendTo($("body"));
        } else this.call("notification", "notify", {
            title: _t("File Format Not Supported"),
            message: _t("You can not preview this file!"),
            sticky: false,
        });
    },




    async _renderView() {

        var self = this

        const _super = this._super.bind(this);
        if (self.activeActions != undefined) {
            await rpc.query({
                model: 'res.users',
                method: 'get_attachment_data',
                args: [this.state.model, this.state.res_ids],
            }).then(function (data) {
                self.sh_attachments = data[0]
                self.sh_show_attachment_in_list_view = data[1]
            });
        }


        return _super(...arguments);
    },




    _renderRow: function (record) {

        var res = this._super.apply(this, arguments);

        if (this.sh_show_attachment_in_list_view && this.sh_attachments && this.activeActions != undefined) {

            let attachment_data = this.sh_attachments[0]

            if (attachment_data[record.data.id]) {

                var $main_attachment_div = $("<div>", {
                    class: "sh_main_attachment_div",
                });

                var $sh_inner_attachment_div = $("<div>", {
                    class: "sh_inner_attachment_div d-flex align-items-center justify-content-center w-100 position-absolute flex-wrap",
                    id: record.id,
                });

                attachment_data[record.data.id].every((attachment, index, arr) => {

                    if (index < 5) {

                        var $sh_attachment_item = $("<div>", {
                            class: "sh_attachment_item border d-flex align-items-center mx-2",
                            "data-id": attachment.attachment_id,
                            "data-name": attachment.attachment_name,
                            "data-mimetype": attachment.attachment_mimetype,
                            "data-record_id": record.data.id,
                        });

                        var $attachment_image = $("<span>", {
                            "data-mimetype": attachment.attachment_mimetype,
                            class: "sh_attachment_icon o_image mr-2",
                        })
                        $sh_attachment_item = $sh_attachment_item.append($attachment_image);

                        var $attachment_name = $("<span>", {
                            class: "sh_attachment_name text-nowrap",
                        }).append($("<span>").html(attachment.attachment_name));
                        $sh_attachment_item = $sh_attachment_item.append($attachment_name);

                        $sh_inner_attachment_div = $sh_inner_attachment_div.append($sh_attachment_item);
                        $main_attachment_div = $main_attachment_div.append($sh_inner_attachment_div);

                        return true;

                    } else {
                        if (attachment.attachment_mimetype.match("(image|application/pdf|text|video)")) {
                        var $sh_attachment_item = $("<div>", {
                            class: "sh_attachment_item border attachment_box_counter d-flex align-items-center px-2 ",
                            "data-id": attachment.attachment_id,
                            "data-name": attachment.attachment_name,
                            "data-mimetype": attachment.attachment_mimetype,
                            "data-record_id": record.data.id,
                        });

                        var $attachment_name = $("<span>", {
                            class: "sh_attachment_name text-nowrap",
                        }).append(
                            $("<span>").html("+" + (arr.length - 5))
                        );

                        $sh_attachment_item = $sh_attachment_item.append($attachment_name);
                        $sh_inner_attachment_div = $sh_inner_attachment_div.append($sh_attachment_item);
                        $main_attachment_div = $main_attachment_div.append($sh_inner_attachment_div);

                        return false;
                        }

                        else{

                            return true;
                        }

                    }
                });

                res = res.add($main_attachment_div);

            }
        }

        return res


    }
})