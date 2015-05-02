{
    'name': 'Suggest Product',
    'version': '1.0',
    'category': 'Sale',
    'description': """
            - Allows to configure multiple suggested products on product.
            - This module allows users to add alternate product in case of one of the product stock is not available.
            - You can configure products which needs to be added along with other product.
    """,
    'author': 'Emipro Technologies',
    'website': 'www.emiprotechnologies.com',
    'depends': ['sale'],
    'installable': True,
    'data': ['view/sale_order_view.xml',
             'view/product_view.xml',
             'wizard/suggest_product_wizard.xml'                            
    ],
}
