# Grocery Store

This is a simple web application for a grocery store built using Flask, a lightweight web framework in Python. The application allows users to view a list of available products, add items to their shopping cart, and place orders. The admin panel allows authorized users to manage products, categories, and view summary reports of product and category-wise sales.

## Technologies Used:
- Flask (web framework in Python)
- SQLAlchemy (database toolkit and ORM)
- Flask-Login (user authentication)
- Flask-WTF (web forms)
- Flask-RESTful (extension for building RESTful APIs)
- SQLite (database)
- HTML, CSS, JavaScript (front-end)
- Matplotlib (graphical visualizations)

## Database Schema Design

- **User Table**: This table stores information about users, including a unique identifier (ID), their username, and password. Each user can have multiple cart items and orders associated with them.

- **Category Table**: The category table holds different product categories, each identified by a unique category ID. Each category can have multiple products associated with it.

- **Product Table**: This table contains details about individual products. Each product is identified by a unique product ID and has a name, price, stock quantity, and belongs to a specific category.

- **Cart Table**: The cart table manages user shopping carts. Each cart is assigned a unique cart ID and is associated with a specific user. It also keeps track of the cart’s creation date.

- **CartItem Table**: This table stores the items added to a user’s shopping cart. Each cart item has a unique identifier (item ID) and is associated with a specific cart and product. It also includes the quantity of the product added to the cart.

- **Order Table**: The order table tracks user orders. Each order is identified by a unique order ID and is associated with a specific user. It also records the order date and the total price of the order.

- **OrderItem Table**: This table stores the items within each order. Each order item has a unique identifier (item ID) and is associated with a specific order and product. It also includes the quantity of the product ordered.

## API Design

The API has been meticulously designed to retrieve essential data pertaining to a user's interactions on the platform. This data encompasses a variety of actions, such as for admin deleting category names, managing product names, adding new products, for user updating the shopping cart, and removing products from the cart. To access this valuable information, the API offers a single, well-defined endpoint that requires the user to provide their unique ID as input. Upon successful execution, the API responds by delivering a structured JSON object containing the relevant engagement data.

## Application Usage & Features:

- **User Authentication**
  - Users and administrators can sign in using their username and password on the login page.
  - New users can register by entering a unique username and password and clicking the “Register” button.
  - After successful login or registration, users & admin will be redirected to the home page and admin dashboard, respectively.

- **User Home Page**
  - The user home page displays various product categories and the available products under each category.
  - Users can click on a product to view its details and add it to their cart.
  - The cart icon at the top-right corner shows the number of items in the user’s cart.
  - Users can click on the cart icon to view and manage the items in their cart.
  - The cart page allows users to update the quantities of items or remove them from the cart.
  - Users can proceed to checkout by clicking the “Checkout” button on the cart page.

- **Admin Dashboard**
  - Administrators can sign in using the predefined admin username and password on the login page.
  - After successful login, administrators will be redirected to the admin dashboard.
  - The admin dashboard provides options to add new categories, add new products, and delete products.
  - The admin dashboard provides options to preview the user home page, allowing administrators to experience all the app’s features from a user’s perspective.
  - The admin can also view a summary page with graphical analysis of product-wise and category-wise sales and revenue.

- **User Profile Page**
  - Logged-in users can access their profile page to view their order history.
  - The profile page displays the date of each order, the total price, and the products purchased in each order.

- **Summary Page**
  - The summary page displays graphical analysis of various product-wise and category-wise sales and revenue data.
  - The graphs provide insights into the performance of different products and categories over time.

- To log out, click the “Logout” link.

## Video:
[Demo Video](https://drive.google.com/file/d/1D1AdoiWmMt6uuFHKex8Z_PLZGrzyTPBH/view?usp=sharing)

## Submitted by:
Shib Kumar Saraf
- Email ID: shibkumarsaraf2001@gmail.com
