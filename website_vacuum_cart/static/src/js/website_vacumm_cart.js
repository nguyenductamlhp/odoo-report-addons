$(document).ready(function () {

$('.vacuum_cart').each(function () {
    var oe_website_sale = this;

    $(oe_website_sale).on("click", function () {
        openerp.jsonRpc("/shop/vacuum_cart", "call", {}).then(function(){
            location.reload();
        })
        return false;
    })

});

});
