# -*- encoding: utf-8 -*-
from openerp.http import request
from openerp.addons.web.controllers.main import Export


class ExportEpt(Export):

    def fields_get(self, model):
        Model = request.session.model(model)
        fields = Model.fields_get(False, request.context)

        ir_model = request.env['ir.model'].search([('model', '=', model)])
        blocked_fields = request.env['ir.model.field.ept'].search([('model_id', '=', ir_model.id),('exportable', '=', False)])
        for fld in blocked_fields:
            if fld.field_id.name in fields:
                fields.pop(fld.field_id.name, None)
        return fields
