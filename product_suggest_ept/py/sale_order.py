from openerp import models,api

class sale_order(models.Model):
    _inherit='sale.order'
    
    @api.multi
    def suggest_alternative_product(self):
        context=dict(self.env.context or {})
        context.update({'sale_id':self.ids[0] or None})            
        res = self.env.ref('product_suggest_ept.suggest_product_wizard')
        
        action = {
            'name':'Suggest Product',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': res.ids,
            'res_model': 'suggest.product.wizard',
            'context': context,
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target':'new',
                   }
        return action     
    
    
    
    
    