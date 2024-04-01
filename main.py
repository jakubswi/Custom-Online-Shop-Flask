import os

import stripe
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_bootstrap import Bootstrap5

stripe_keys = {
    "secret_key": os.environ["STRIPE_SECRET_KEY"],
    "publishable_key": os.environ["STRIPE_PUBLISHABLE_KEY"]
}
app = Flask(__name__)
Bootstrap5(app)


# stripe.api_key = stripe_keys["secret_key"]


@app.route('/')
def main_page():
    return render_template("index.html")


@app.route('/success')
def success():
    return render_template("success.html")


@app.route('/cancel')
def cancel():
    return render_template("cancel.html")


@app.route("/config")
def get_publishable_key():
    stripe_config = {"publicKey": stripe_keys["publishable_key"]}
    return jsonify(stripe_config)


@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    stripe.api_key = stripe_keys["secret_key"]
    try:
        line_items = []
        if 'cart' in session:
            for product_id, quantity in session['cart'].items():
                price_id = stripe.Product.retrieve(product_id)["default_price"]
                line_items.append({
                    "price": price_id,
                    "quantity": quantity,
                })
        checkout_session = stripe.checkout.Session.create(
            success_url=url_for('success'),
            cancel_url=url_for("cancel"),
            payment_method_types=["card"],
            mode="payment",
            line_items=line_items
        )
        return jsonify({"sessionId": checkout_session["id"]})
    except Exception as e:
        return jsonify(error=str(e)), 403


@app.route("/webhook", methods=["POST"])
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, stripe_keys["endpoint_secret"]
        )

    except ValueError as e:
        return "Invalid payload", 400
    except stripe.error.SignatureVerificationError as e:
        return "Invalid signature", 400

    if event['type'] == 'checkout.session.completed':
        session = stripe.checkout.Session.retrieve(
            event['data']['object']['id'],
            expand=['line_items'],
        )

        line_items = session.line_items
        # Fulfill the purchase...
        fulfill_order(line_items)

    return "Success", 200


@app.route('/login')
def login():
    # TODO: Implement logic for login in
    return render_template("login.html")


@app.route('/signup')
def signup():
    # TODO: Implement logic for registering
    return render_template("signup.html")


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/statute')
def statute():
    return render_template('statute.html')


@app.route('/products')
def products():
    response = stripe.Product.list()
    products = response['data']
    len_products = len(products)
    prices = [stripe.Price.retrieve(product['default_price']) for product in products]
    return render_template("products.html", products=products, prices=prices, len_products=len_products)


@app.route('/view_product/<id>')
def view_product(id):
    product = stripe.Product.retrieve(id)
    return render_template("product.html", product=product)


@app.route('/add_to_cart/<id>')
def add_to_cart(id):
    if 'cart' not in session:
        session['cart'] = {}
    if id not in session['cart']:
        session['cart'][id] = 1
    else:
        session['cart'][id] += 1
    return redirect(url_for('products'))


@app.route('/shopping_cart')
def shopping_cart():
    cart_items = []
    total_price = 0
    if 'cart' in session:
        for product_id, quantity in session['cart'].items():
            product = stripe.Product.retrieve(product_id)
            price = stripe.Price.retrieve(product['default_price'])['unit_amount'] * quantity
            total_price += price
            cart_items.append({'product': product['name'], 'quantity': quantity, 'price': price})
    return render_template('shopping_cart.html', cart_items=cart_items, total_price=total_price)


def fulfill_order(line_items):
    # TODO: Implement logic to fulfill order
    pass


if __name__ == "__main__":
    app.run(debug=True)
