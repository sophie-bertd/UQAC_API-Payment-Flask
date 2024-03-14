$(document).ready(() => {
  let isFirstProductAdded = false;
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
    if (!isFirstProductAdded) {
      $(".addToCart").not(this).prop("disabled", true);
      isFirstProductAdded = true;
    }

    currentProductQuantity += 1;
    const $cardBody = $(this).closest(".card-body");
    const productName = $cardBody.find(".card-title").text();
    const productPrice = parseFloat(
      $cardBody.find(".card-text").eq(0).text().replace("$", "")
    );
    const productQuantityText = $cardBody
      .find(".card-text")
      .eq(1)
      .text()
      .trim();
    const productWeight =
      parseFloat(productQuantityText.split("g")[0].trim()) / 1000;

    const existingItem = $("#cartSidebar .list-group").find(
      `li[data-product="${productName}"]`
    );

    if (existingItem.length > 0) {
      const currentQuantity = parseFloat(existingItem.attr("data-quantity"));
      existingItem.attr("data-quantity", currentQuantity + productWeight);
      existingItem.html(
        `${productName} - $${productPrice.toFixed(2)} /kg - ${(
          currentQuantity + productWeight
        ).toFixed(3)} kg (Quantité: ${currentProductQuantity})`
      );
    } else {
      $("#cartSidebar .list-group").append(
        `<li class="list-group-item" data-product="${productName}" data-quantity="${productWeight}">
                ${productName} - $${productPrice.toFixed(
          2
        )} /kg - ${productWeight.toFixed(
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
      // const quantity = parseFloat($(this).attr("data-quantity"));
      // total += price * quantity;
      total += price * currentProductQuantity;
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
          expiration_year: parseInt($("#creditCardYear").val()),
          expiration_month: parseInt($("#creditCardMonth").val()),
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
