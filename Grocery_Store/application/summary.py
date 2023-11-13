import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
from .models import  User, Category, Product, Cart,CartItem,Order,OrderItem



# Generic function to make graph
def generate_bar_graph(data, labels, xlabel, ylabel, title, image_path):
    plt.bar(labels, data)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks()
    plt.tight_layout()
    plt.savefig(image_path)
    plt.close()

# logic of graphs
def generate_graphs():
    all_products = Product.query.all()
    all_categories = Category.query.all()
# Bar Plots for Products 
    # Product Price Distribution 
    total_prices = [product.price for product in all_products]
    generate_bar_graph(total_prices, [product.product_name for product in all_products],
                       'Product', 'Price per Product', 'Product Price Distribution', 'Grocery_Store/application/static/summary/product_price_distribution.png')

    # Stock Availability per Product
    stock_availability = [product.stock_quantity for product in all_products]
    generate_bar_graph(stock_availability, [product.product_name for product in all_products],
                       'Product', 'Stock Availability','Stock Availability per Product',  'Grocery_Store/application/static/summary/stock_availability_per_product.png')

    # Sales Volume for each Product
    product_sold = [sum([item.quantity for item in OrderItem.query.filter_by(product_id=product.product_id)]) for product in all_products]
    generate_bar_graph(product_sold, [product.product_name for product in all_products],
                       'Product', 'Sales Volume', 'Sales Volume for each Product', 'Grocery_Store/application/static/summary/sales_volume_for_each_product.png')
    
# Bar Plots for Products 

    # Category-wise Product Distribution
    category_names = [category.category_name for category in all_categories]
    category_counts = [len(category.products) for category in all_categories]
    generate_bar_graph(category_counts, category_names,
                       'Category', 'Number of Products', 'Category-wise Product  Distribution', 'Grocery_Store/application/static/summary/category_wise_product_distribution.png')

    # Stock Availability per Category
    category_stock = [sum([product.stock_quantity for product in category.products]) for category in all_categories]
    generate_bar_graph(category_stock, category_names,
                       'Category', 'Stock Availability', 'Stock Availability per Category', 'Grocery_Store/application/static/summary/stock_availability_per_category.png')

    # Sales Volume for each Category
    category_sold = [sum([item.quantity for item in OrderItem.query.join(Product).filter(Product.category_id == category.category_id)]) for category in all_categories]
    generate_bar_graph(category_sold, category_names,
                       'Category', 'Sales Volume', 'Sales Volume for each Category', 'Grocery_Store/application/static/summary/sales_volume_for_each_category.png')


