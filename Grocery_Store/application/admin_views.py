from flask import Blueprint, render_template, request, flash, redirect, url_for,flash,jsonify
from flask_login import login_required, current_user
from .models import  User, Category, Product, Cart,CartItem,Order,OrderItem
from . import db
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime  
import os
from flask import Flask, render_template, request, redirect, url_for
from application.summary import generate_graphs
admin_views = Blueprint("admin_views", __name__)


# admin Section 

# Admin Home Page
@admin_views.route('/admin_home', methods=['GET', 'POST'])
@login_required
def admin_home():
    if request.method == 'POST':
        category_name = request.form['category_name']
        category = Category(category_name=category_name)
        db.session.add(category)
        db.session.commit()

    categories = Category.query.all()
    return render_template('admin_dashboard.html', categories=categories)

# API endpoint to add a new product
@admin_views.route('/api/products', methods=['POST'])
def add_product():
    if request.method == 'POST':
        data = request.get_json()

        product_name = data.get('product_name')
        stock_quantity = data.get('stock_quantity')
        price = data.get('price')
        category_id = data.get('category_id')

        if not all([product_name, stock_quantity, price, category_id]):
            return jsonify({'message': 'Missing required fields'}), 400

        try:
            product = Product(product_name=product_name, stock_quantity=stock_quantity,
                              price=price, category_id=category_id)
            db.session.add(product)
            db.session.commit()
        except Exception as e:
            return jsonify({'message': 'Failed to add the product', 'error': str(e)}), 500

        return jsonify({'message': 'Product added successfully', 'category_id': category_id}), 201


# API endpoint to update a product
@admin_views.route('/api/products/<int:product_id>', methods=['PUT'])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)

    if request.method == 'PUT':
        data = request.get_json()

        product_name = data.get('product_name')
        stock_quantity = data.get('stock_quantity')
        price = data.get('price')

        if not all([product_name, stock_quantity, price]):
            return jsonify({'message': 'Missing required fields'}), 400

        try:
            product.product_name = product_name
            product.stock_quantity = stock_quantity
            product.price = price
            db.session.commit()
        except Exception as e:
            return jsonify({'message': 'Failed to edit the product', 'error': str(e)}), 500

        return jsonify({'message': 'Product edited successfully', 'category_id': product.category_id}), 200

# API endpoint to delete a product
@admin_views.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    category_id = product.category_id
    try:
        db.session.delete(product)
        db.session.commit()
    except Exception as e:
        return jsonify({'message': 'Failed to delete the product', 'error': str(e)}), 500

    return jsonify({'message': 'Product deleted successfully', 'category_id': category_id}), 200

# API endpoint to get product by its category
@admin_views.route('/api/categories/<int:category_id>/products', methods=['GET'])
def get_products_by_category(category_id):
    category = Category.query.get_or_404(category_id)
    products = category.products
    product_list = [{'product_id': product.product_id,
                     'product_name': product.product_name,
                     'stock_quantity': product.stock_quantity,
                     'price': product.price} for product in products]
    return jsonify({'category_id': category_id, 'products': product_list}), 200

# Summary Page
@admin_views.route('/summary', methods=['GET', 'POST'])
@login_required
def summary():
    # Generate the graphs with current data
   generate_graphs()
  
   return render_template('summary.html')

