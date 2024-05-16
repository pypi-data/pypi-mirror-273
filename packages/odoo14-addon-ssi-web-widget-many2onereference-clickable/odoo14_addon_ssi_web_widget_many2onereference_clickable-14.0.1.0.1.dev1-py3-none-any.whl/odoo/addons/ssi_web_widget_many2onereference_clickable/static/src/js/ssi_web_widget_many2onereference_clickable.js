odoo.define(
    "ssi_web_widget_many2onereference_clickable.many2one_reference_clickable",
    function (require) {
        "use strict";

        var ListRenderer = require("web.ListRenderer");
        var FieldReference = require("web.relational_fields").FieldReference;

        ListRenderer.include({
            _renderBodyCell: function (record, node, colIndex, options) {
                if (
                    !node.attrs.widget &&
                    node.attrs.name &&
                    this.state.fields[node.attrs.name] &&
                    this.state.fields[node.attrs.name].type === "reference"
                ) {
                    // No explicit widget provided on a many2one_reference field,
                    // force `many2one_reference` widget
                    node.attrs.widget = "many2one_reference";
                }
                return this._super(record, node, colIndex, options);
            },
        });

        FieldReference.include({
            _renderReadonly: function () {
                this._super.apply(this, arguments);
                var self = this;

                if (!this.noOpen && this.value) {
                    // Replace '<a>' element
                    this.$el.removeClass("o_form_uri");
                    this.$el = $("<span/>", {
                        html: this.$el.html(),
                        class: this.$el.attr("class") + " o_field_text",
                        name: this.$el.attr("name"),
                    });

                    // Append button
                    var $a = $("<a/>", {
                        href: "#",
                        class:
                            "o_form_uri btn btn-sm btn-secondary" +
                            " fa fa-angle-double-right",
                    }).on("click", function (ev) {
                        ev.preventDefault();
                        ev.stopPropagation();

                        self.do_action({
                            type: "ir.actions.act_window",
                            res_model: self.field.relation,
                            res_id: self.value.res_id,
                            views: [[false, "form"]],
                            target: "target",
                            context: self.record.getContext({
                                additionalContext: self.attrs.context || {},
                            }),
                        });
                    });
                    this.$el.append($a);
                }
            },
        });
    }
);
