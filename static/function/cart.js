var removeCartItemButtons = document.getElementsByClassName('btn-danger')
console.log(removeCartItemButtons)
var total = 0
for (var i=0; i<removeCartItemButtons.length; i++) {
    var button = removeCartItemButtons[i]
    button.addEventListener('click', function(event) {
        var buttonClicked = event.target
        var proInfoElement = buttonClicked.closest('.pro-info');
        if (proInfoElement) {
            proInfoElement.remove();
        }
        updateCartTotal()
    })
}

function removeCartItem(event){
    var buttonClicked = event.target
    var buttonClicked = event.target
        var proInfoElement = buttonClicked.closest('.pro-info');
        if (proInfoElement) {
            proInfoElement.remove();
        }
    updateCartTotal()
} 

function quantityChanged(event){
    var input = event.target
    if (isNaN(input.value) || input.value <= 0){
        input.value = 1
    }
    updateCartTotal()
}

var quantityInputs = document.getElementsByClassName('cart-quantity-input')
for (var i = 0; i < quantityInputs.length; i++) {
    quantityInputs[i].addEventListener('change', quantityChanged)
}

function updateCartTotal() {
    // get array of all the items in the cart
    var cartItemContainer = document.getElementsByClassName('cart-items')[0]
    var cartRows = cartItemContainer.getElementsByClassName('pro-info')
    var total = 0
    for (var i=0; i<cartRows.length; i++) {
        var cartRow = cartRows[i]
        var priceElement = cartRow.getElementsByClassName('cart-price')[0]
        var quantityElement = cartRow.getElementsByClassName('cart-quantity-input')[0]
        var price = parseFloat(priceElement.innerText.replace('$', ''))
        var quantity = parseFloat(quantityElement.value)
        total = total + (price * quantity)
    }
    document.getElementsByClassName('cart-total-price')[0].innerText = '$' + total
}

// Add event listeners to quantity input elements
var quantityInputs = document.getElementsByClassName('cart-quantity-input')
for (var i = 0; i < quantityInputs.length; i++) {
    quantityInputs[i].addEventListener('change', updateCartTotal)
}
