function getProductList(categoryId) {
    fetch(`/api/categories/${categoryId}/products`)
        .then(response => response.json())
        .then(data => {
            const productList = document.getElementById(`productList${categoryId}`);
            productList.innerHTML = "";
            data.products.forEach(product => {
                productList.innerHTML += `
                    <li class="product-tab">${product.product_name} - Stock: ${product.stock_quantity} - Price: ${product.price}</li>
                    <button onclick="editProduct(${ product.product_id })">Edit</button>
                    <button onclick="deleteProduct(${product.product_id})">Delete</button>
                `;
            });
        })
        .catch(error => {
            console.error(error);
        });
}

function addProduct(event, categoryId) {
    event.preventDefault();

    const productForm = event.target;
    const productData = {
        product_name: productForm.product_name.value,
        stock_quantity: productForm.stock_quantity.value,
        price: productForm.price.value,
        category_id: categoryId
    };
    fetch('/api/products', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(productData)
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Failed to add the product.');
        }
    })
    .then(data => {
        getProductList(categoryId);
    })
    .catch(error => {
        alert(error.message);
    });
}


function editProduct(productId) {
    const productForm = {
        product_name: prompt("Enter the new product name"),
        stock_quantity: prompt("Enter the new stock quantity"),
        price: prompt("Enter the new price"),
    };
    fetch(`/api/products/${productId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(productForm)
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Failed to edit the product.');
        }
    })
    .then(data => {
        getProductList(data.category_id);
    })
    .catch(error => {
        alert(error.message);
    });
}

function deleteProduct(productId) {
    fetch(`/api/products/${productId}`, {
        method: 'DELETE'
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Failed to delete the product.');
        }
    })
    .then(data => {
        getProductList(data.category_id);
    })
    .catch(error => {
        alert(error.message);
    });
}

document.addEventListener("DOMContentLoaded", () => {
    const categories = document.getElementsByClassName("category-tab");
    for (const category of categories) {
        const categoryId = category.getAttribute("data-category-id");
        getProductList(categoryId);
    }
});

