from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)

@app.route('/')
def home():
    
    informacion = [
                    {"imagen":"static/imagenes/La-diferencia-entre-nutricion-y-alimentacion1.jpg",
                    "descripcion":"Some quick example text to build on the card title and make up the bulk of the card’s content.",
                    },
                    {"imagen":"",
                    "descripcion":"",
                    },
                    {"imagen":"",
                    "descripcion":"",
                    },
                ]
    
    return render_template("home.html",informacion=informacion)

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/registro')
def registro():
    return render_template("registro.html")

@app.route('/perfil')
def perfil():
    return render_template("perfil.html")

if __name__ == "__main__":
    app.run(debug=True)