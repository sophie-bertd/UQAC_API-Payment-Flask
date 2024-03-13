from flask import escape

def index(products):
    view = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>5 Fruits et Légumes</title>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
    <style>
        .cart-sidebar {
            position: fixed;
            top: 0;
            right: -250px;
            width: 250px;
            height: 100%;
            background-color: #f8f9fa;
            transition: all 0.3s;
        }
        .cart-sidebar.open {
            right: 0;
        }
        .close-icon {
            position: absolute;
            top: 10px;
            left: 10px;
            cursor: pointer;
        }
        .in-stock-icon {
            color: green;
        }
        .out-of-stock-icon {
            color: red;
        }
    </style>
</head>
<body>
<div class="container mt-5">
    <div class="row mb-3">
        <div class="col">
            <h1 class="text-center">5 Fruits et Légumes</h1>
        </div>
    </div>

    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <a class="navbar-brand" href="#">5 Fruits et Légumes</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ml-auto">
                <li class="nav-item">
                    <a class="nav-link" href="#">Top</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="#"><button class="btn btn-info" id="cartToggle"><i class="fas fa-list fa-lg"></i></button></a>
                </li>
            </ul>
        </div>
    </nav>

    <div class="row">
        <div class="col">
            <h2>Produits</h2>
        </div>
    </div>
    <div class="row" id="products">
    """

    if products:
        for product in products:
            view += """
                <div class="col-md-4">
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title">{name}</h5>
                            <p class="card-text">${price} /kg</p>
                            <p class="card-text">{weight}g</p>
                            <p class="card-text">{description}</p>
                            <button class="btn btn-primary addToCart">Ajouter au panier</button>
                            <span class="stock-icon">{in_stock}</span>
                        </div>
                    </div>
                </div>
            """.format(name=product.name, price=product.price, weight=product.weight, description=product.description, in_stock=product.in_stock)
    else:
        view += """
        <p>Aucun produit</p>
        """

    return view + """
    </div>
</div>

<div class="cart-sidebar" id="cartSidebar">
    <span class="close-icon"><i class="fas fa-times-circle fa-2x"></i></span>
    <h2 class="text-center pt-3">Panier</h2>
    <div class="cart-total text-center mt-3">Total: $0.00</div>
    <ul class="list-group mt-3">
    </ul>
    <div class="text-center mt-3">
        <button class="btn btn-primary" id="checkoutButton" data-toggle="modal" data-target="#paymentModal">Paiement</button>
    </div>
</div>

<div class="modal fade" id="paymentModal" tabindex="-1" role="dialog" aria-labelledby="paymentModalLabel" aria-hidden="true">
    <div class="modal-dialog" role="document">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="paymentModalLabel">Paiement</h5>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>
            <div class="modal-body">
                <p>Informations bancaires</p>
                <input type="text" placeholder="Credit card number" class="form-control mb-2">
                <input type="text" placeholder="Expiry date" class="form-control mb-2">
                <input type="text" placeholder="CVV" class="form-control mb-2">
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-dismiss="modal">Fermer</button>
                <button type="button" class="btn btn-primary">Continuer</button>
            </div>
        </div>
    </div>
</div>

<script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.3/dist/umd/popper.min.js"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
<script>
    $(document).ready(function(){
        $('.card').each(function() {
            let isInStock = Math.random() < 0.5;
            let iconClass = isInStock ? 'fas fa-check-circle in-stock-icon' : 'fas fa-times-circle out-of-stock-icon';
            $(this).find('.stock-icon').html('<i class="' + iconClass + '"></i>');
        });

        $('#cartToggle').click(function(){
            $('#cartSidebar').toggleClass('open');
        });

        $('.close-icon').click(function(){
            $('#cartSidebar').removeClass('open');
        });

        $('.addToCart').click(function(){
            let productName = $(this).siblings('.card-title').text();
            let productPrice = parseFloat($(this).siblings('.card-text').first().text().replace("$", ""));
            let productQuantityText = $(this).siblings('.card-text').eq(1).text().trim();
            let quantityRegex = /([\d.]+)\s*(kg|g)/i;
            let matches = productQuantityText.match(quantityRegex);
            if (matches && matches.length === 3) {
                let productQuantity = parseFloat(matches[1]);
                let quantityUnit = matches[2].toLowerCase();
                if (quantityUnit === 'g') {
                    productQuantity /= 1000;
                }
            } else {
                console.error('Quantity format not recognized for product:', productName);
                return;
            }

            let existingItem = $('#cartSidebar .list-group').find('li[data-product="' + productName + '"]');

            if(existingItem.length > 0) {
                let currentQuantity = parseFloat(existingItem.attr('data-quantity'));
                existingItem.attr('data-quantity', currentQuantity + productQuantity);
                existingItem.html(productName + ' - ' + productPrice.toFixed(2) + ' /kg (Quantité: ' + (currentQuantity + productQuantity).toFixed(3) + ' kg)');
            } else {
                $('#cartSidebar .list-group').append('<li class="list-group-item" data-product="' + productName + '" data-quantity="' + productQuantity + '">' + productName + ' - ' + productPrice.toFixed(2) + ' /kg (Quantité: ' + productQuantity.toFixed(3) + ' kg)</li>');
            }

            updateCartTotal();
        });

        function updateCartTotal() {
            let total = 0;
            $('#cartSidebar .list-group li').each(function() {
                let price = parseFloat($(this).text().split(' - ')[1].replace("$", "").split(' ')[0]);
                let quantity = parseFloat($(this).attr('data-quantity'));
                total += price * quantity;
            });
            $('.cart-total').text('Total: $' + total.toFixed(2));
        }
    });
</script>
</body>
</html>
    """