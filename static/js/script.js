$(document).ready(() => {
  let order_id = null;
  let product_id = null;
  let currentProductQuantity = 0;

  $("#cartToggle").click(function () {
    $("#cartSidebar").toggleClass("open");
  });

  $(".close-icon").click(function () {
    $("#cartSidebar").removeClass("open");
  });

  $(".addToCart").click(function () {
    currentProductQuantity += 1;
    product_id = $(this).closest(".col-md-4").find(".card").data("product-id");

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
        `${productName} - ${productPrice.toFixed(2)} /kg - ${(
          currentQuantity + productQuantity
        ).toFixed(3)} kg (Quantité: ${currentProductQuantity})`
      );
    } else {
      $("#cartSidebar .list-group").append(
        `<li class="list-group-item" data-product="${productName}" data-quantity="${productQuantity}">
            ${productName} - ${productPrice.toFixed(
          2
        )} /kg - ${productQuantity.toFixed(
          3
        )} kg (Quantité: ${currentProductQuantity})
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

    $.ajax({
      url: "/order",
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify({
        product: {
          id: product_id,
          quantity: currentProductQuantity,
        },
      }),
      success: (response) => {
        order_id = response.id;
        console.log("Order created with id:", order_id);
      },
      error: (xhr, status, error) => {
        console.error(error);
      },
    });
  });

  $("#continueToPaymentBtn").click(function () {
    $("#userInfoModal").modal("hide");
    $("#paymentModal").modal("show");

    let email = $("#emailInput").val();
    let country = $("#countryInput").val();
    let address = $("#addressInput").val();
    let postalCode = $("#postalCodeInput").val();
    let city = $("#cityInput").val();
    let province = $("#provinceInput").val();

    $("#shippingEmail").text(email);
    $("#shippingCountry").text(country);
    $("#shippingAddress").text(address);
    $("#shippingPostalCode").text(postalCode);
    $("#shippingCity").text(city);
    $("#shippingProvince").text(province);

    $.ajax({
      url: `/order/${order_id}`,
      type: "PUT",
      contentType: "application/json",
      data: JSON.stringify({
        order: {
          email: email,
          shipping_information: {
            country: country,
            address: address,
            postal_code: postalCode,
            city: city,
            province: province,
          },
        },
      }),
      success: (response) => {
        console.log("Order updated with shipping information");
      },
      error: (xhr, status, error) => {
        console.error(error);
      },
    });
  });

  $("#placeOrderBtn").click(function () {
    $("#paymentModal").modal("hide");
    $("#orderPlacedModal").modal("show");

    $.ajax({
      url: `/order/${order_id}`,
      type: "PUT",
      contentType: "application/json",
      data: JSON.stringify({
        credit_card: {
          name: $("#creditCardName").val(),
          number: $("#creditCardNumber").val(),
          expiration_year: parseInt($("#expirationYear").val()),
          expiration_month: parseInt($("#expirationMonth").val()),
          cvv: $("#cvv").val(),
        },
      }),
      success: (response) => {
        $("#paymentModal").modal("hide");
        $("#orderPlacedModalTrue").modal("show");

        console.log("Order placed with id:", order_id);
      },
      error: (xhr, status, error) => {
        $("#paymentModal").modal("hide");
        $("#orderPlacedModalFalse").modal("show");

        console.error(error);
        console.log(error.responseJSON.error);
      },
    });
  });
});
