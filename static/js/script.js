$(document).ready(function () {
  $("#cartToggle").click(function () {
    $("#cartSidebar").toggleClass("open");
  });

  $(".close-icon").click(function () {
    $("#cartSidebar").removeClass("open");
  });

  $(".addToCart").click(function () {
    const productName = $(this).siblings(".card-title").text();
    const productPrice = parseFloat(
      $(this).siblings(".card-text").first().text().replace("$", "")
    );
    const productQuantityText = $(this)
      .siblings(".card-text")
      .eq(1)
      .text()
      .trim();
    const quantityRegex = /([\d.]+)\s*(kg|g)/i;
    const matches = productQuantityText.match(quantityRegex);

    let productQuantity = 0;
    if (matches && matches.length === 3) {
      productQuantity = parseFloat(matches[1]);
      const quantityUnit = matches[2].toLowerCase();
      if (quantityUnit === "g") {
        productQuantity /= 1000;
      }
    } else {
      console.error("Quantity format not recognized for product:", productName);
      return;
    }

    const existingItem = $("#cartSidebar .list-group").find(
      `li[data-product="${productName}"]`
    );

    if (existingItem.length > 0) {
      const currentQuantity = parseFloat(existingItem.attr("data-quantity"));
      existingItem.attr("data-quantity", currentQuantity + productQuantity);
      existingItem.html(
        `${productName} - ${productPrice.toFixed(2)} /kg (Quantité: ${(
          currentQuantity + productQuantity
        ).toFixed(3)} kg)`
      );
    } else {
      $("#cartSidebar .list-group").append(
        `<li class="list-group-item" data-product="${productName}" data-quantity="${productQuantity}">
            ${productName} - ${productPrice.toFixed(
          2
        )} /kg (Quantité: ${productQuantity.toFixed(3)} kg)
          </li>`
      );
    }

    updateCartTotal();
  });

  function updateCartTotal() {
    let total = 0;
    $("#cartSidebar .list-group li").each(function () {
      const price = parseFloat(
        $(this).text().split(" - ")[1].replace("$", "").split(" ")[0]
      );
      const quantity = parseFloat($(this).attr("data-quantity"));
      total += price * quantity;
    });
    $(".cart-total").text(`Total: $${total.toFixed(2)}`);
  }

  $("#checkoutButton").click(function () {
    $("#userInfoModal").modal("show");
  });

  $("#continueToPaymentBtn").click(function () {
    $("#userInfoModal").modal("hide");
    $("#paymentModal").modal("show");

    var email = $("#emailInput").val();
    var country = $("#countryInput").val();
    var address = $("#addressInput").val();
    var postalCode = $("#postalCodeInput").val();
    var city = $("#cityInput").val();
    var province = $("#provinceInput").val();

    $("#shippingEmail").text(email);
    $("#shippingCountry").text(country);
    $("#shippingAddress").text(address);
    $("#shippingPostalCode").text(postalCode);
    $("#shippingCity").text(city);
    $("#shippingProvince").text(province);
  });

  $("#placeOrderBtn").click(function () {
    $("#paymentModal").modal("hide");
    $("#orderPlacedModal").modal("show");
  });
});
