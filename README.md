# La Tienda

La Tienda is a Django-based e-commerce web application for a clothing store. It offers a responsive user interface for browsing and purchasing clothing items, managing shopping carts, and handling orders.

Check out the live demo at [La Tienda](http://latienda.pythonanywhere.com).

## Table of Contents

1. [Features](#features)
2. [Technologies Used](#technologies-used)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Contributing](#contributing)
6. [License](#license)

## Features

- Browse a wide range of clothing items
- Shopping cart using web sessions
- Add items to a shopping cart
- Update item quantities and remove items from the cart
- Checkout process with stock availability checks
- Order management for admins
- Responsive design using Bootstrap 5

## Technologies Used

- Django
- Bootstrap 5
- SQLite (default, replaceable with other databases)
- HTML/CSS
- JavaScript

## Installation

To run this project locally, follow these steps:

1. **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/la-tienda.git
    cd la-tienda
    ```

2. **Create and activate a virtual environment:**
    ```bash
    python -m venv env
    env\Scripts\activate  # On Linux use `source env/bin/activate`
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Apply migrations:**
    ```bash
    python manage.py migrate
    ```
    
5. **Collect static files:**
    ```bash
    python manage.py collectstatic
    ```

6. **Create a superuser:**
    ```bash
    python manage.py createsuperuser
    ```

7. **Run the development server:**
    ```bash
    python manage.py runserver
    ```

## Usage

- Access the website at `http://127.0.0.1:8000/`
- Admin panel is available at `http://127.0.0.1:8000/admin/`
- Browse and add items to your shopping cart
- Proceed to checkout and place orders
- Manage orders through the admin panel

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature-name`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature-name`)
5. Open a pull request

## License

This project is licensed under the GPL-3.0 License. See the [LICENSE](LICENSE.txt) file for details.
