from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)

@app.route('/')
def home():
    
    informacion = [
                    {"imagen":"static/imagenes/La-diferencia-entre-nutricion-y-alimentacion1.jpg",
                    "descripcion":"Esta pagina nutricional es una creada para que la gente pueda llevar un control de consumo de calorías, actualmente es muy bajo el porcentaje de personas que se preocupan por su consumo diario de calorías, por eso esta pagina esta hecha con el fin de que las personas como ya mencionado con anterioridad tenga un control.",
                    },
                    {"imagen":"static/imagenes/nutri.jpg",
                    "descripcion":"El fin de esta pagina es mostrar nuestra actividad calórica y dar una vida saludable a las personas llevandolas por un buen camino y a si esa persona a futuro no tenga problemas dde salud como obesidad o cosas asi.",
                    },
                    {"imagen":"static/imagenes/Estado_Nutri-Post-de-Twitter.jpg",
                    "descripcion":"Esta pagina cuenta con alimentos y sus calorías, un calendario que de un control diario de consumo de calorias al igual que el agua, tiene un apartado de perfil que nos permitira ir llevando una reivisión sobre el plan que tenga, el proposito es facilitar y ayudar a las personas para ser un mundo mejor en el futuro",
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

@app.route('/acerca')
def acerca_de():
    return render_template("acerca_de.html")

if __name__ == "__main__":
    app.run(debug=True)