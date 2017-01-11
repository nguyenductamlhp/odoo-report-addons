# -*- encoding: utf-8 -*-
from openerp.http import request
from openerp.addons.web.controllers.main import Export

import logging
_logger = logging.getLogger(__name__)

class ExportEpt(Export):

    def fields_get(self, model):
        Model = request.session.model(model)
        fields = Model.fields_get(False, request.context)
        _logger.info('FIELDS 1: %s', fields.keys())
        ir_model = request.env['ir.model'].search([('model', '=', model)])
        blocked_fields = request.env['ir.model.field.ept'].search([('model_id', '=', ir_model.id),('exportable', '=', False)])
        _logger.info('Blocked fields: %s %s', model, blocked_fields)
        for fld in blocked_fields:
            if fld.field_id.name in fields:
                _logger.info('Popping %s', fld.field_id.name)
                fields.pop(fld.field_id.name, None)
        _logger.info('FIELDS: %s', fields.keys())
        return fields
