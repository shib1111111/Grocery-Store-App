from flask import Blueprint, render_template, request, flash, redirect, url_for,flash,jsonify
from flask_login import login_required, current_user
from .models import  User, Category, Product, Cart,CartItem,Order,OrderItem
from . import db
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime  
import os
from flask import Flask, render_template, request, redirect, url_for

user_views = Blueprint("user_views", __name__)
#defining admin
admin_username = "admin"
# User Section

# User Home Page
@user_views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    categories = Category.query.all()
    products = Product.query.all()
    return render_template('home.html',curr_user= current_user,admin_username=admin_username,categories=categories,products=products)

# route for add to cart
@user_views.route('/add_to_cart', methods=['POST'])
@login_required
def add_to_cart():
    quantity = int(request.form['quantity'])
    # Check if the product exists and the quantity is valid
    product_id = int(request.form['product_id'])
    product = Product.query.get(product_id)
    if not product or quantity <= 0 or quantity > product.stock_quantity:
        flash('Invalid product or quantity.', 'error')
        return redirect(url_for('user_views.home'))
    # Check if the user already has a cart
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if not cart:
        # Create a new cart for the user if they don't have one
        cart = Cart(user_id=current_user.id, created_at=datetime.now())
        db.session.add(cart)
        db.session.commit()
    # Add the product to the cart
    cart_item = CartItem(cart_id=cart.cart_id, product_id=product_id, quantity=quantity,user_id=current_user.id)
    db.session.add(cart_item)
    db.session.commit()
    flash('Product added to cart successfully!', 'success')
    return redirect(url_for('user_views.home'))

# API endpoint to update item in cart
@user_views.route('/update_quantity/<int:item_id>', methods=['PUT'])
def update_quantity(item_id):
    data = request.get_json()
    new_quantity = data.get('quantity', 1)  
    cart_item = CartItem.query.get(item_id)
    if cart_item:
        cart_item.quantity = new_quantity
        db.session.commit()
        return jsonify({'message': 'Quantity updated successfully.'}), 200
    else:
        return jsonify({'error': 'Cart item not found.'}), 404

# API endpoint to remove item from cart
@user_views.route('/remove_item/<int:item_id>', methods=['DELETE'])
def remove_item(item_id):
    cart_item = CartItem.query.get(item_id)
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        return jsonify({'message': 'Item removed successfully.'}), 200
    else:
        return jsonify({'error': 'Cart item not found.'}), 404

# Cart Page
@user_views.route('/cart', methods=['GET', 'POST'])
@login_required
def cart():
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if not cart:
        cart = Cart(user_id=current_user.id, created_at=datetime.utcnow())
        db.session.add(cart)
        db.session.commit()

    categories = Category.query.all()

    if request.method == 'POST':
        data = request.get_json()
        for item_id, quantity in data.items():
            # Update the quantity for each item in the cart
            cart_item = CartItem.query.get(item_id)
            if cart_item:
                cart_item.quantity = quantity
        db.session.commit()

    cart_items = CartItem.query.filter_by(cart_id=cart.cart_id).all()
    total_checkout_price = cart.total_price if cart_items else 0.0

    return render_template('cart.html', cart_items=cart_items, categories=categories, total_checkout_price=total_checkout_price)

# API endpoint to get product
@user_views.route('/get_products')
def get_products():
    # Retrieve the product list from the database and convert it to a JSON response
    products = Product.query.all()
    product_list = [{'product_name': product.product_name, 'price': product.price} for product in products]
    return jsonify(product_list)

# route for checkout
@user_views.route('/checkout', methods=['POST'])
def checkout():
    try:
        user = User.query.get(current_user.id) 
        cart = Cart.query.filter_by(user_id=user.id).first()
        if cart:
            order = Order(user_id=user.id, order_date=datetime.now(), total_price=cart.total_price)
            db.session.add(order)
            db.session.commit()

            for cart_item in cart.cart_items:
                order_item = OrderItem(
                    order_id=order.order_id,
                    product_id=cart_item.product_id,
                    quantity=cart_item.quantity)
                
                db.session.add(order_item)
                db.session.commit()
                product = Product.query.get(cart_item.product_id)
                product.stock_quantity -= cart_item.quantity
                db.session.commit()
            CartItem.query.filter_by(user_id=user.id).delete()
            db.session.commit()
            return jsonify({'message': 'Checkout successful'})
        else:
            return jsonify({'message': 'Cart is empty'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# User Profile Page
@user_views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    curr_user = current_user  
    orders = Order.query.filter_by(user_id=curr_user.id).all()
    product_name_map = {product.product_id: product.product_name for product in Product.query.all()}
    order_details = []
    for order in orders:
        order_items = []
        for order_item in order.order_items:
            product_name = product_name_map.get(order_item.product_id, "Unknown Product")
            order_items.append({
                "product_name": product_name,
                "quantity": order_item.quantity
            })
        formatted_order_date = order.order_date.strftime("%Y-%m-%d %I:%M %p")
        order_details.append({
            "order_date": formatted_order_date,
            "total_price": order.total_price,
            "order_items": order_items
        })
    return render_template('profile.html', curr_user=curr_user, order_details=order_details,admin_username=admin_username)



