fetch("/config")
  .then((result) => result.json())
  .then((data) => {
    const stripe = Stripe(data.publicKey);

    document.querySelector("#submitBtn").addEventListener("click", () => {
      fetch("/create-checkout-session", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({}),
      })
      .then((result) => result.json())
      .then((data) => {
        console.log(data);
        return stripe.redirectToCheckout({sessionId: data.sessionId});
      })
      .then((result) => {
        if (result.error) {
          console.error(result.error.message);
        }
      })
      .catch((error) => {
        console.error('Error:', error);
      });
    });
  })
  .catch((error) => {
    console.error('Error:', error);
  });
