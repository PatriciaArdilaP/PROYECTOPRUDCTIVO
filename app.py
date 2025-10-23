from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

# ---------- RUTAS PRINCIPALES ----------
@app.route('/')
def home():
    return render_template('Home.html')

# Rutas directas
@app.route('/juana')
def juana():
    return render_template('juana.html')

@app.route('/dani')
def dani():
    return render_template('dani.html')

@app.route('/kevin')
def kevin():
    return render_template('kevin.html')

@app.route('/joel')
def joel():
    return render_template('joel.html')


# Alias para coincidir con el HTML existente
@app.route('/portafolio_dani')
def portafolio_dani():
    return render_template('portafolios/dani.html')
@app.route('/portafolio_juana')
def portafolio_juana():
    return render_template('portafolios/juana.html')

@app.route('/portafolio_kevin')
def portafolio_kevin():
    return render_template('portafolios/kevin.html')

@app.route('/portafolio_joel')
def portafolio_joel():
    return render_template('portafolios/joel.html')


# ---------- RUTA TIENDA ----------
@app.route("/tienda")
def tienda():
    products = [
        {"id": "p-01", "name": "Flawless Foundation", "price": 39900, "old": 55900, "badge": "NEW", "img": "img/productos_tienda.jpg"},
        {"id": "p-02", "name": "Premium Gloss", "price": 25000, "old": 31000, "badge": "SALE", "img": "img/producto_brillo1.jpg"},
        {"id": "p-03", "name": "Active Shadow", "price": 29900, "img": "img/producto_sombra.jpg"},
        {"id": "p-04", "name": "Liquid Lip Gloss", "price": 22500, "old": 27900, "badge": "SALE", "img": "img/Producto_labial1.jpg"},
        {"id": "p-05", "name": "Natural Cream", "price": 35000, "img": "img/productos_tienda.jpg"},
        {"id": "p-06", "name": "Lipstick Duo", "price": 28900, "img": "img/Producto_labial1.jpg"},
        {"id": "p-07", "name": "Gold Shadow", "price": 31500, "img": "img/producto_sombra.jpg"},
        {"id": "p-08", "name": "Brillo Gloss", "price": 24900, "img": "img/producto_brillo1.jpg"}
    ]
    return render_template("tienda.html", products=products)


# ---------- RUTAS DE CARRITO ----------
@app.route('/cart')
def cart_view():
    return render_template('cart.html')

@app.route('/cart/add', methods=['POST'])
def cart_add():
    product_id = request.form.get('id')
    print(f"Producto agregado al carrito: {product_id}")
    return redirect(url_for('cart_view'))


# ---------- OTRAS PÁGINAS ----------
@app.route('/articulos')
def articulos():
    return render_template("articulos.html")

@app.route('/equipo')
def equipo():
    return render_template("equipo.html")

@app.route('/faq')
def faq():
    return render_template("faq.html")


# ---------- MANEJO DE ERRORES ----------
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# ---------- EJECUCIÓN LOCAL ----------
if __name__ == '__main__':
    app.run(debug=True)



