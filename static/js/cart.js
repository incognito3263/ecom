$(document).ready(function(){
    $('.update-cart').each(function(){
       $(this).on('click', function(){
            var productID = $(this).attr('data-product');
            var action = $(this).attr('data-action');
            if (user === 'AnonymousUser') {
                addCookieItem(productID, action);
            } else {
                UpdateUserOrder(productID, action);
            }
       });
    });

    function addCookieItem(productId, action) {
        if (action === 'add') {
            if(cart[productId] === undefined) {
                cart[productId] = {'quantity': 1}
            } else {
                cart[productId]['quantity'] += 1
            }
        }

        if (action === 'remove') {
            cart[productId]['quantity'] -= 1
            if (cart[productId]['quantity'] <= 0) {
                alert('item removed...')
                delete cart[productId]
            }
        }
        console.log('Cookie_Cart: '+cart)
        document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
        location.reload()
    }

    function UpdateUserOrder(productId, action) {
        var url = '/update_user/'
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body:JSON.stringify({'productId': productId, 'action': action})
        })
        .then((response) =>{
            return response.json()
        }).then((data) =>{
            location.reload()
        })
    }
});