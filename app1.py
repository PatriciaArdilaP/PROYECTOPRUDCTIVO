from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("Home.html")

@app.route('/tienda')
def tienda():
    return render_template("tienda.html")

@app.route('/articulos')
def articulos():
    return render_template("articulos.html")

@app.route('/equipo')
def equipo():
    return render_template("equipo.html")

@app.route('/faq')
def faq():
    return render_template("faq.html")

if __name__ == '__main__':
    app.run(debug=True)

