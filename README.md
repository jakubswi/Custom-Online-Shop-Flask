# Project Name

This project is a Flask-based web application integrated with Stripe for handling payments and managing an online store.

## Features

- **User Authentication**: Allows users to sign up and log in to the system.
- **Product Management**: Users can view available products, view product details, and add products to their shopping cart.
- **Shopping Cart**: Users can add products to their shopping cart and view the items in their cart.
- **Checkout**: Users can proceed to checkout where they can finalize their purchases using Stripe's payment processing.
- **Webhooks**: Includes a webhook endpoint to handle events like successful checkout sessions and fulfill orders accordingly.
- **Static Pages**: Provides static pages like About, Statute, etc.

## Prerequisites

Before running the application, make sure you have the following:

- Python installed on your system.
- Stripe account to obtain API keys.
- Flask and Flask Bootstrap libraries installed.

## Setup

1. Clone the repository:

    ```bash
    git clone <repository_url>
    cd <project_directory>
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up environment variables:

    - `STRIPE_SECRET_KEY`: Your Stripe Secret Key.
    - `STRIPE_PUBLISHABLE_KEY`: Your Stripe Publishable Key.

4. Run the application:

    ```bash
    python app.py
    ```

5. Access the application through your web browser at `http://localhost:5000`.

## Usage

- Navigate through the website to explore available products, add them to the shopping cart, and proceed to checkout.
- Sign up or log in to manage your account and view order history.

## Structure

- `app.py`: Contains the main Flask application code.
- `templates/`: Directory containing HTML templates for different pages.
- `static/`: Directory containing static assets like CSS and JavaScript files.

## Contributing

Contributions are welcome! Feel free to open issues or pull requests.

