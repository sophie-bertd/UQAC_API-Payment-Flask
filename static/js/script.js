$(document).ready(() => {
  let isFirstProductAdded = false;
  let order_id = null;
  let products_id = [];
  let currentProductQuantity = null;

  $("#cartToggle").click(function () {
    $("#cartSidebar").toggleClass("open");
  });

  $(".close-icon").click(function () {
    $("#cartSidebar").removeClass("open");
  });

  $("#orderToggle").click(function () {
    $("#orderModal").modal("show");
  });

  $("#orderBtn").click(function () {
    let orderId = $("#orderInput").val();

    $.ajax({
      url: `/order/${orderId}`,
      type: "GET",
      success: (response) => {
        $("#orderModal").modal("hide");
        $("#orderInfoModal").modal("show");

        $("#shippingCountry").text(response.shipping_information.country);
        $("#shippingAddress").text(response.shipping_information.address);
        $("#shippingCity").text(response.shipping_information.city);
        $("#shippingProvince").text(response.shipping_information.province);
        $("#shippingPostalCode").text(
          response.shipping_information.postal_code
        );
        $("#email").text(response.email);
        $("#totalPrice").text("$" + (response.total_price / 1).toFixed(2));
        $("#paid").text(response.paid ? "Yes" : "No");

        let productsHtml = "";
        response.products.forEach((product) => {
          productsHtml += `<li>Product ID: ${product.id}, Quantity: ${product.quantity}</li>`;
        });
        $("#productsOrder").html(productsHtml);

        $("#ccName").text(response.credit_card.name);
        $("#ccFirstDigits").text(response.credit_card.number.slice(0, 4));
        $("#ccLastDigits").text(response.credit_card.number.slice(-4));
        $("#ccExpiration").text(
          `${response.credit_card.expiration_month}/${response.credit_card.expiration_year}`
        );

        $("#transactionSuccess").text(
          response.transaction.success ? "Yes" : "No"
        );
        $("#amountCharged").text(
          "$" + (response.transaction.amount_charged / 1).toFixed(2)
        );

        $("#shippingPrice").text(
          "$" + (response.shipping_price / 1).toFixed(2)
        );
        $("#orderId").text(response.id);
      },
      error: (xhr, status, error) => {
        console.error(error);
      },
    });
  });

  $("#orderInfoBtn").click(function () {
    $("#orderInfoModal").modal("hide");
  });

  $("#orderBtn").click(function () {
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
  });

  $(".addToCart").click(function () {
    // if (!isFirstProductAdded) {
    //   $(".addToCart").not(this).prop("disabled", true);
    //   isFirstProductAdded = true;
    // }

    product = $(this).closest(".col-md-4").find(".card").data("product-id");

    if (products_id.find((element) => element.id === product)) {
      products_id.find((element) => element.id === product).quantity += 1;
    } else {
      products_id.push({ id: product, quantity: 1 });
    }

    currentProductQuantity = products_id.find(
      (element) => element.id === product
    ).quantity;

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
        products: products_id,
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
