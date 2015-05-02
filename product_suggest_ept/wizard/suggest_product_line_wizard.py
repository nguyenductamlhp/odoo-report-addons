from openerp import models,fields,api
import openerp.addons.decimal_precision as dp

class suggest_product_line_wizard(models.TransientModel):
    _name="suggest.product.line.wizard"
    
    product_id=fields.Many2one('product.product',string="Product",readonly=True)
    suggested_of=fields.Char('Suggested Of')
    qty_available=fields.Float("Qty On Hand",digits= dp.get_precision('Product Price'),readonly=True)
    qty=fields.Float("Quantity",digits= dp.get_precision('Product Price'))
    sale_line_id=fields.Many2one('sale.order.line',"Sale Order Line")
    suggest_product_wizard_id=fields.Many2one('suggest.product.wizard',"Suggest Product")
    
class suggest_product_line_wizard2(models.TransientModel):
    _name="suggest.product.line.wizard2"
    _order="suggested_of asc"
    
    product_id=fields.Many2one('product.product',string="Product",readonly=True)
    suggested_of=fields.Char('Suggested Of')
    qty_available=fields.Float("Qty On Hand",digits= dp.get_precision('Product Price'),readonly=True)
    qty=fields.Float("Quantity",digits= dp.get_precision('Product Price'))
    sale_line_id=fields.Many2one('sale.order.line',"Sale Order Line")
    suggest_product_wizard_id=fields.Many2one('suggest.product.wizard',"Suggest Product")
    