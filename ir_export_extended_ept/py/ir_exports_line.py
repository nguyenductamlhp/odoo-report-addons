from openerp import models, fields, api

_FIELD_LIST = [( '', '' )]
class ir_exports_line( models.Model ):
    _name = "ir.exports.line"
    _inherit = "ir.exports.line"
    _order = "sequence,id"

    def get_fields( self ):
        return []

    heading = fields.Char( string="Label", size=512 )
    sequence = fields.Integer( 'Sequence', default=100 )

    @api.multi
    @api.onchange('field1_id', 'field2_id', 'field3_id', 'field4_id',)
    def _onchange_field_x(self):
        parts = list()
        for num in range(1, 5):
            field = self.field_n(num)
            if not field:
                break
            # Translate label if possible
            try:
                parts.append(
                    self.env[self.model_n(num).model]._fields[field.name]
                    .get_description(self.env)["string"])
            except KeyError:
                # No human-readable string available, so empty this
                return
        self.heading = '/'.join(parts)