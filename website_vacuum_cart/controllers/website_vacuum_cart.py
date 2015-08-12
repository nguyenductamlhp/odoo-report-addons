from openerp.addons.web import http
from openerp.addons.web.http import request

class website_sale_vacuum_cart( http.Controller ):
    @http.route( ['/shop/vacuum_cart'], type='json', auth="public", website=True )
    def clear_cart( self ):
        order = request.website.sale_get_order()
        if order:
            for line in order.website_order_line:
                line.unlink()
