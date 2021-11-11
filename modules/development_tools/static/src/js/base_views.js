odoo.define('development_tools.DebugManager', function (require) {

    "use strict";

    var core = require("web.core");
    var DebugManager = require('web.DebugManager');


    DebugManager.include({

        start: function () {
            return this._super.apply(this, arguments);
        },

        reload_view: function (params, ev) {
            var self = this;
            self._rpc({
                model: 'ir.ui.view',
                method: 'reload',
                args: [[params.id]]
            });

            self.exit();
        },

        exit: function () {
            this.do_action({
                type: 'ir.actions.client',
                tag: 'reload'
            });
        },

    }); // DebugManager.include

});
/*

var self = this;
            self._rpc({
                model: 'ir.actions.act_window',
                method: 'search_read',
                domain: [['id', '=', params.id]],
                fields: ['name', 'model', 'type'],
                limit: 1,
            })
            .then(function (views) {
                console.log(views);
            });

name
type
view_id
domain
context
res_id
res_model
src_model
target
view_mode
view_type
usage
view_ids
views
limit
groups_id
search_view_id
filter
auto_search
search_view
multi
xml_id
help
binding_model_id
binding_type
id
display_name
create_uid
create_date
write_uid
write_date
__last_update*/

// openerp.development_tools = function (openerp) {
//     openerp.web.ViewManagerAction = openerp.web.ViewManagerAction.extend({
//         init: function () {
//             this._super.apply(this, arguments);
//             console.log('Search view initialized');
//         },
//         on_debug_changed: function (evt) {
//             this._super.apply(this, arguments);
//             console.log('Pasé por aquí')
//         }
//     });
// }


// function oe_debug_view_log() {
//     try {
//         _from = jQuery('h3.modal-title').text().search(/\(/i) + 1
//         _to = jQuery('h3.modal-title').text().search(/\)/i)

//         _model = jQuery('h3.modal-title').text().substring(_from, _to)

//         _id = jQuery('.oe_debug_view_log table tr:first-child() td').text();
//         _xid = jQuery('.oe_debug_view_log table tr:nth-child(2) td').text();

//         args = [_model, eval(_id), _xid]
//         setTimeout("location.reload(true);", 1000);
//         return new openerp.Model('ir.model').call('reload', args);
//     } catch(err) {
//         console.log(err)
//     }
// }

