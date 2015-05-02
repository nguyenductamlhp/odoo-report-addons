from openerp import models,fields,api

class suggest_product_wizard(models.TransientModel):
    _name="suggest.product.wizard"
    
    sale_line_ids=fields.One2many('suggest.product.line.wizard','suggest_product_wizard_id',"Sale Lines")
    suggest_product_line_wizard_ids=fields.One2many('suggest.product.line.wizard2','suggest_product_wizard_id',"Suggest Product")
    
    @api.model
    def get_tax_id_ept(self,tax_ids,company_id):
        return_tax_ids = []
        for tax in  self.env['account.tax'].browse(tax_ids):
            if tax.company_id.id==company_id:
                return_tax_ids.append(tax.id)
        return return_tax_ids
    
    @api.multi
    def add_products(self):        
        for wizard_record in self:                        
            self.create_lines(wizard_record,wizard_record.sale_line_ids)
            self.create_lines(wizard_record,wizard_record.suggest_product_line_wizard_ids)
        return True
    
    @api.model
    def create_lines(self,wizard_record,line_ids):
        sale_order_line_obj=self.env['sale.order.line']
        sale_order_obj=self.env['sale.order']
        sale_id=self.env.context.get("sale_id")
        sale_order=sale_id and sale_order_obj.browse(sale_id)
        company_id=sale_order and sale_order.partner_id and sale_order.partner_id.company_id and sale_order.partner_id.company_id.id or False
                                                   
        for line in line_ids:
            if float(line.qty)<=0.0:
                line.sale_line_id and line.sale_line_id.unlink()
                continue
            pricelist=sale_order and sale_order.pricelist_id.id or False
            product_id=line.product_id.id or False
            uom_id=line.product_id.uom_id and line.product_id.uom_id.id
            name=line.product_id.name or False
            fiscal_position= sale_order and sale_order.fiscal_position and sale_order.fiscal_position.id or False 
            product_data=sale_order_line_obj.product_id_change_with_wh(pricelist,product_id,line.qty,uom_id
                                                                            ,line.qty,False,name,sale_order.partner_id.id
                                                                            ,False,True,sale_order.date_order,False,
                                                                            fiscal_position,False,warehouse_id=sale_order.warehouse_id and sale_order.warehouse_id.id or False)
            product_data=product_data.get('value')                  
            tax_id=product_data.get("tax_id",[])
            tax_id=self.get_tax_id_ept(tax_id,company_id)
            product_data.update(
                                {
                                'product_id':line.product_id.id,
                                'order_id':sale_id,
                                'product_uom_qty':line.qty,
                                'product_uos_qty':line.qty,                                    
                                'tax_id':[(6,0,tax_id)]}                                    
                                )                
            if line.sale_line_id:
                line.sale_line_id.write(product_data)
            else:
                sale_order_line_obj.create(product_data)
        return True
    
    @api.model
    def default_get(self,fields=None):
        sale_result=[]
        suggested_result=[]
        res={}
        
        sale_order_id=self.env.context.get('sale_id',False)
        sale_order=self.env['sale.order'].browse(sale_order_id)
        
        sale_line_product_ids=[]
        for line in sale_order.order_line:
            line.product_id and sale_line_product_ids.append(line.product_id.id)
        
        for line in sale_order.order_line:
            if not line.product_id:
                continue                                                  
            
            sale_info={'product_id':line.product_id.id,
                  'qty_available':line.product_id.qty_available,
                  'qty':line.product_uom_qty,
                  'sale_line_id':line.id,                     
                }
            sale_result.append(sale_info)
            
            
            for product in line.product_id.suggestive_product_ids:
                if product.id in sale_line_product_ids:
                    continue                    
                suggested_info={'product_id':product.id,
                                'suggested_of':line.product_id.default_code,
                                'qty_available':product.qty_available or 0.0,
                                'qty':0.0,
                                'sale_line_id':False,                     
                                }
                suggested_result.append(suggested_info)

        res.update({'sale_line_ids':sale_result})
        res.update({'suggest_product_line_wizard_ids':suggested_result})        
        return res