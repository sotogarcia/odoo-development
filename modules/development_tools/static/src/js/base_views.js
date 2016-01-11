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
