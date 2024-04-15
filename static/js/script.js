$(document).ready(() => {
  // let isFirstProductAdded = false;
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

        $("#shippingCountryInfo").text(response.shipping_information.country);
        $("#shippingAddressInfo").text(response.shipping_information.address);
        $("#shippingCityInfo").text(response.shipping_information.city);
        $("#shippingProvinceInfo").text(response.shipping_information.province);
        $("#shippingPostalCodeInfo").text(
          response.shipping_information.postal_code
        );
        $("#emailInfo").text(response.email);
        $("#totalPriceInfo").text("$" + (response.total_price / 1).toFixed(2));
        $("#paidInfo").text(response.paid ? "Yes" : "No");

        let productsHtml = "";
        response.products.forEach((product) => {
          productsHtml += `<li>Product ID: ${product.id}, Quantity: ${product.quantity}</li>`;
        });
        $("#productsInfo").html(productsHtml);

        $("#ccNameInfo").text(response.credit_card.name);
        $("#ccFirstDigitsInfo").text(response.credit_card.number.slice(0, 4));
        $("#ccLastDigitsInfo").text(response.credit_card.number.slice(-4));
        $("#ccExpirationInfo").text(
          `${response.credit_card.expiration_month}/${response.credit_card.expiration_year}`
        );

        $("#transactionSuccessInfo").text(
          response.transaction.success ? "Yes" : "No"
        );
        $("#amountChargedInfo").text(
          "$" + (response.transaction.amount_charged / 1).toFixed(2)
        );

        $("#shippingPriceInfo").text(
          "$" + (response.shipping_price / 1).toFixed(2)
        );
        $("#orderIdInfo").text(response.id);
      },
      error: (xhr, status, error) => {
        console.error(error);

        $("#orderModal").modal("hide");
        $("#orderInfoModal").modal("hide");
        // $("#orderInfoModalFalse").modal("show");

        $("#resultModal").modal("show");
        $("#resultModalTitle").text("Order not found");
        $("#resultModalBody").text(`The order ID you entered does not exist`);
      },
      complete: () => {
        $("#orderInput").val("");
      },
    });
  });

  $("#orderInfoBtn").click(function () {
    $("#orderInfoModal").modal("hide");
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
      complete: () => {
        $("#emailInput").val("");
        $("#countryInput").val("");
        $("#addressInput").val("");
        $("#postalCodeInput").val("");
        $("#cityInput").val("");
        $("#provinceInput").val("");
      },
    });
  });

  $("#placeOrderBtn").click(function () {
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

        $("#resultModal").modal("show");
        $("#resultModalTitle").text("Order sucess");
        $("#resultModalBody").text(`Your order was placed successfully`);

        console.log("Order placed with id:", order_id);
      },
      error: (xhr, status, error) => {
        $("#paymentModal").modal("hide");

        $("#resultModal").modal("show");
        $("#resultModalTitle").text("Order failed");
        $("#resultModalBody").text(`Your order could not be placed`);

        console.error(error);
        console.log(error.responseJSON.error);
      },
      complete: () => {
        order_id = null;
        products_id = [];
        currentProductQuantity = null;
        updateCartTotal();

        $("#cartSidebar .list-group").empty();

        $("#creditCardName").val("");
        $("#creditCardNumber").val("");
        $("#creditCardYear").val("");
        $("#creditCardMonth").val("");
        $("#cvv").val("");
      },
    });
  });
});
