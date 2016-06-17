# -*- coding: utf-8 -*-

from openerp import models, fields, api

class irModelFieldEpt(models.Model):
    _name = 'ir.model.field.ept'

    field_id = fields.Many2one('ir.model.fields', 'Field')
    model_id = fields.Many2one(related='field_id.model_id', store=True)
    field_name = fields.Char(related='field_id.name')
    exportable = fields.Boolean('Exportable', default=True)
    export_help = fields.Char('Export Note', size=500)

    @api.model
    def sync_fields(self):
        old_flds = self.search([]).mapped('field_id')
        new_flds = self.env['ir.model.fields'].search([('id', 'not in', old_flds.ids)])
        for fld in new_flds:
            exportable = True
            if fld.name in ["create_uid", "create_date", "write_uid", "write_date", "parent_right", "parent_left"]:
                exportable = False
            for f in ['can_', 'edit_']:
                if fld.name.startswith(f):
                    exportable = False
            if fld.ttype in ['binary', 'serialized']:
                exportable = False
            self.create({'field_id': fld.id,
                         'exportable': exportable})
