from openerp import models,fields,api

class product_product(models.Model):
    _inherit='product.product'
    
    suggestive_product_ids=fields.Many2many('product.product','product_cross_rel','product_id','cross_sale_id',string="Suggest Product in Order Lines",help="Suggest Product in Sale Order Line")