$(document).ready(function(){
    var shipping = '{{order.shipping}}';
    alert(shipping);

    if (shipping === 'False') {
        $('#shipping-info').html(' ');
    }
});


