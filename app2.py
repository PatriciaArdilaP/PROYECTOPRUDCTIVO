from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.config["SECRET_KEY"] = "cambia-esta-clave"  # ⚠️ cambia por una clave segura

# ===== Catálogo (8 productos; reutiliza tus 4 imágenes) =====
PRODUCTS = [
    {"id": "p-01", "name": "Flawless Foundation", "price": 39900, "img": "img/productos_tienda.jpg", "stars": 4.5, "old": 55900, "badge": "NEW"},
    {"id": "p-02", "name": "Premium Gloss",        "price": 25000, "img": "img/producto_brillo1.jpg",  "stars": 5,   "old": 31000, "badge": "SALE"},
    {"id": "p-03", "name": "Active Shadow",         "price": 29900, "img": "img/producto_sombra.jpg",   "stars": 4},
    {"id": "p-04", "name": "Liquid Lip Gloss",      "price": 22500, "img": "img/Producto_labial1.jpg",  "stars": 5,   "old": 27900, "badge": "SALE"},
    {"id": "p-05", "name": "Natural Cream",         "price": 35000, "img": "img/productos_tienda.jpg",  "stars": 4},
    {"id": "p-06", "name": "Lipstick Duo",          "price": 28900, "img": "img/Producto_labial1.jpg",  "stars": 4.5},
    {"id": "p-07", "name": "Gold Shadow",           "price": 31500, "img": "img/producto_sombra.jpg",   "stars": 5},
    {"id": "p-08", "name": "Brillo Gloss",          "price": 24900, "img": "img/producto_brillo1.jpg",  "stars": 4},
]

# ===== Utilidades de carrito =====
def _get_cart():
    return session.setdefault("cart", [])

def _save_cart(cart):
    session["cart"] = cart
    session.modified = True

def _find_product(pid):
    return next((p for p in PRODUCTS if p["id"] == pid), None)

@app.context_processor
def inject_cart_count():
    count = sum(i["qty"] for i in session.get("cart", []))
    return {"cart_count": count}

# ===== Rutas existentes =====
@app.route("/")
def home():
    return render_template("Home.html")

@app.route("/tienda")
def tienda():
    # pasa el catálogo para renderizar los productos y el botón "Agregar al carrito"
    return render_template("tienda.html", products=PRODUCTS)

@app.route("/articulos")
def articulos():
    return render_template("articulos.html")

@app.route("/equipo")
def equipo():
    return render_template("equipo.html")

@app.route("/faq")
def faq():
    return render_template("faq.html")

# ===== Rutas de carrito =====
@app.post("/cart/add")
def cart_add():
    pid = request.form.get("id")
    p = _find_product(pid)
    if not p:
        return redirect(url_for("tienda"))

    cart = _get_cart()
    for item in cart:
        if item["id"] == pid:
            item["qty"] += 1
            break
    else:
        # Guarda la URL absoluta de la imagen para usarla en el carrito
        cart.append({
            "id": p["id"],
            "name": p["name"],
            "price": p["price"],
            "img": url_for("static", filename=p["img"]),
            "qty": 1
        })
    _save_cart(cart)
    return redirect(request.referrer or url_for("cart_view"))

@app.post("/cart/update")
def cart_update():
    pid = request.form.get("id")
    qty = max(1, int(request.form.get("qty", 1)))
    cart = _get_cart()
    for item in cart:
        if item["id"] == pid:
            item["qty"] = qty
            break
    _save_cart(cart)
    return redirect(url_for("cart_view"))

@app.post("/cart/remove")
def cart_remove():
    pid = request.form.get("id")
    cart = [i for i in _get_cart() if i["id"] != pid]
    _save_cart(cart)
    return redirect(url_for("cart_view"))

@app.get("/cart")
def cart_view():
    cart = _get_cart()
    total = sum(i["price"] * i["qty"] for i in cart)
    return render_template("cart.html", cart=cart, total=total)

# ===== Entrypoint =====
if __name__ == "__main__":
    app.run(debug=True)
