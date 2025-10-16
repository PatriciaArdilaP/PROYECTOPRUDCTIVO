from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.config["SECRET_KEY"] = "cambia-esta-clave-super-secreta"  # ⚠️ cambia por una clave segura en prod

# =========================
# Catálogo (8 productos)
# =========================
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

# =========================
# Utilidades de carrito
# =========================
def _get_cart():
    return session.setdefault("cart", [])

def _save_cart(cart):
    session["cart"] = cart
    session.modified = True

def _find_product(pid):
    return next((p for p in PRODUCTS if p["id"] == pid), None)

def cart_total():
    return sum(i["price"] * i["qty"] for i in session.get("cart", []))

@app.context_processor
def inject_cart_count():
    return {"cart_count": sum(i["qty"] for i in session.get("cart", []))}

# =========================
# Rutas principales
# =========================
@app.get("/")
def home():
    return render_template("Home.html")

@app.get("/tienda")
def tienda():
    return render_template("tienda.html", products=PRODUCTS)


@app.get("/articulos")
def articulos():
    # Redirige al bloque de productos dentro de Tienda
    return redirect(url_for("home") + "#aprender")

@app.get("/equipo")
def equipo():
    # Envía a la sección "Conoce el equipo" dentro de Home
    return redirect(url_for("home") + "#equipo")


@app.get("/faq")
def faq():
    return redirect(url_for("home") + "#faq")

# =========================
# Carrito
# =========================
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
        # guarda URL absoluta de la imagen para mostrarla en /cart
        cart.append({
            "id": p["id"],
            "name": p["name"],
            "price": p["price"],
            "img": url_for("static", filename=p["img"]),
            "qty": 1
        })
    _save_cart(cart)
    # vuelve a la página anterior o al carrito
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
    total = cart_total()
    return render_template("cart.html", cart=cart, total=total)

# =========================
# Checkout → Pago → Confirmación
# =========================
@app.get("/checkout")
def checkout_get():
    if not session.get("cart"):
        return redirect(url_for("tienda") + "#productos")
    data = session.get("checkout", {})
    return render_template("checkout.html", data=data, cart=session["cart"], total=cart_total())

@app.post("/checkout")
def checkout_post():
    if not session.get("cart"):
        return redirect(url_for("tienda") + "#productos")
    session["checkout"] = {
        "email": request.form["email"],
        "name": request.form.get("name", ""),
        "address": request.form.get("address", ""),
        "city": request.form.get("city", ""),
        "zip": request.form.get("zip", "")
    }
    session.modified = True
    return redirect(url_for("payment_get"))

@app.get("/payment")
def payment_get():
    if not session.get("cart"):
        return redirect(url_for("tienda") + "#productos")
    if not session.get("checkout"):
        return redirect(url_for("checkout_get"))
    return render_template("payment.html", cart=session["cart"], total=cart_total())

@app.post("/payment/confirm")
def payment_confirm():
    # Simula pago OK (en producción integra pasarela y valida webhook)
    order_id = "ORD-" + str(abs(hash(str(session.get("checkout")))) % 10_000_000)
    # Vacía carrito; deja checkout para mostrar datos en confirmación
    session.pop("cart", None)
    session.modified = True
    return redirect(url_for("order_confirm", order_id=order_id))

@app.get("/order/confirm/<order_id>")
def order_confirm(order_id):
    return render_template("order_confirm.html", order_id=order_id, checkout=session.get("checkout"))

# =========================
# Entrypoint
# =========================


if __name__ == "__main__":
    app.run(debug=True)
