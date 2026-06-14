function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');


function showNotification(message, type = 'success') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed top-0 end-0 m-3`;
    alertDiv.style.zIndex = '9999';
    alertDiv.style.minWidth = '300px';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.body.appendChild(alertDiv);
    
    
    setTimeout(() => {
        alertDiv.remove();
    }, 3000);
}


async function addToCart(productId, buttonElement) {
    const originalText = buttonElement.innerHTML;
    buttonElement.disabled = true;
    buttonElement.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Добавление...';
    
    try {
        const response = await fetch('/api/cart-elements/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ product: productId, quantity: 1 })
    })
        
        if (response.ok) {
            const data = await response.json();
            showNotification(data.message || 'Товар добавлен в корзину!', 'success');
            updateCartCount();
        } else {
            const error = await response.json();
            showNotification(error.error || 'Ошибка добавления', 'danger');
        }
    } catch (error) {
        console.error('Ошибка:', error);
        showNotification('Сервис временно недоступен', 'danger');
    } finally {
        buttonElement.disabled = false;
        buttonElement.innerHTML = originalText;
    }
}


async function updateCartCount() {
    try {
        const response = await fetch('/api/carts/');
        if (response.ok) {
            const data = await response.json();
            const cartCountElements = document.querySelectorAll('.cart-count');
            const totalItems = data.total_quantity || 0;
            
            cartCountElements.forEach(el => {
                el.textContent = totalItems;
                if (totalItems > 0) {
                    el.style.display = 'inline-block';
                } else {
                    el.style.display = 'none';
                }
            });
        }
    } catch (error) {
        console.error('Ошибка получения корзины:', error);
    }
}


async function loadProductsDynamic() {
    const container = document.getElementById('products-container');
    const spinner = document.getElementById('loading-spinner');
    
    if (!container) return;
    
    spinner.style.display = 'block';
    
    try {
        const response = await fetch('/api/products/');
        if (!response.ok) throw new Error('Ошибка загрузки');
        
        const products = await response.json();
        
        container.innerHTML = '';
        
        products.forEach(product => {
            const col = document.createElement('div');
            col.className = 'col-sm-6 col-md-6 col-lg-4 mb-4';
            col.innerHTML = `
                <div class="card h-100 shadow-sm">
                    <div class="card-body">
                        <h5 class="card-title">${product.name}</h5>
                        <p class="card-text text-muted">${product.category_name || 'Без категории'}</p>
                        <p class="card-text fw-bold fs-5">${product.price} BYN</p>
                        <button class="btn btn-primary w-100" onclick="addToCart(${product.id}, this)">
                            Добавить в корзину
                        </button>
                    </div>
                </div>
            `;
            container.appendChild(col);
        });
    } catch (error) {
        container.innerHTML = `<div class="col-12"><p class="text-center text-danger">Ошибка загрузки товаров: ${error.message}</p></div>`;
    } finally {
        spinner.style.display = 'none';
    }
}


document.addEventListener('DOMContentLoaded', function() {
    updateCartCount();
    
    
    if (document.getElementById('products-container')) {
        loadProductsDynamic();
    }
    
   
    document.querySelectorAll('.add-to-cart-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const productId = this.dataset.productId;
            addToCart(productId, this);
        });
    });
});
