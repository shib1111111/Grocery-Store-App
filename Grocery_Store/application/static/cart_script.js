document.addEventListener('DOMContentLoaded', function() {
    const quantityInputs = document.querySelectorAll('input[data-item-id]');
    quantityInputs.forEach(input => {
      input.addEventListener('change', function() {
        const item_id = input.dataset.itemId;
        const quantity = parseInt(input.value, 10);
        if (quantity >= 1) {
          updateQuantity(item_id, quantity);
        } else {
          input.value = 1; 
        }
      });
    });
  
    const updateButtons = document.querySelectorAll('button[data-item-id]');
    updateButtons.forEach(button => {
      button.addEventListener('click', function() {
        const item_id = button.dataset.itemId;
        updateQuantity(item_id, parseInt(document.querySelector(`input[data-item-id="${item_id}"]`).value, 10));
      });
    });
  
    function getProductList() {
      fetch('/get_products')
        .then(response => response.json())
        .then(data => {
          console.log(data);
        })
        .catch(error => {
          console.error('Error fetching product list:', error);
        });
    }
      getProductList();
  });
  
  function updateQuantity(item_id) {
    const quantityInput = document.querySelector(`input[data-item-id="${item_id}"]`);
    const newQuantity = parseInt(quantityInput.value, 10);
    if (newQuantity >= 1) {
        fetch(`/update_quantity/${item_id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ quantity: newQuantity }),
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            location.reload();
        })
        .catch(error => {
            console.error('Error updating quantity:', error);
        });
    }
}

function removeItem(item_id) {
    fetch(`/remove_item/${item_id}`, {
        method: 'DELETE',
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        location.reload();
    })
    .catch(error => {
        console.error('Error removing item:', error);
    });
}
function checkout() {
    fetch('/checkout', {
        method: 'POST',
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        location.reload();
    })
    .catch(error => {
        console.error('Error during checkout:', error);
    });
}
