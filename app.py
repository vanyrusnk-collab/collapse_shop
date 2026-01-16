from flask import Flask, render_template, session, redirect, url_for, request

app = Flask(__name__)
app.secret_key = 'collapse_secret_key'  # Потрібно для роботи кошика

# Наш каталок товарів (hardcoded, як ти просив)
PRODUCTS = [
    {
        "id": "1",
        "name": "Червоне плаття",
        "price": 2000,
        "image": "https://images.unsplash.com/photo-1595777457583-95e059d581b8?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60", # Приклад
        "desc": "Елегантне вечірнє плаття"
    },
    {
        "id": "2",
        "name": "Кросівки",
        "price": 3200,
        "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60", # Приклад
        "desc": "Зручні бігові кросівки"
    },
    {
        "id": "3",
        "name": "Біла сорочка",
        "price": 1200,
        "image": "https://images.unsplash.com/photo-1598033129183-c4f50c736f10?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60", # Приклад
        "desc": "Класична сорочка"
    }
]

@app.route('/')
def index():
    return render_template('index.html', products=PRODUCTS)

@app.route('/cart')
def cart():
    # Отримуємо ID товарів з сесії
    cart_ids = session.get('cart', [])
    cart_items = []
    total_price = 0
    
    # Знаходимо повну інформацію про товари за їх ID
    for item_id in cart_ids:
        for product in PRODUCTS:
            if product['id'] == item_id:
                cart_items.append(product)
                total_price += product['price']
                break
    
    return render_template('cart.html', cart_items=cart_items, total=total_price)

@app.route('/add_to_cart/<product_id>')
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = []
    
    session['cart'].append(product_id)
    session.modified = True
    return redirect(url_for('index'))

@app.route('/remove_from_cart/<product_id>')
def remove_from_cart(product_id):
    if 'cart' in session and product_id in session['cart']:
        session['cart'].remove(product_id)
        session.modified = True
    return redirect(url_for('cart'))

@app.route('/clear_cart')
def clear_cart():
    session.pop('cart', None)
    return redirect(url_for('cart'))

if __name__ == '__main__':
    app.run(debug=True)