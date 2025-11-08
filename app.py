from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import timedelta,datetime


app = Flask(__name__)

perfiles = []

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
                    "descripcion":"Esta pagina cuenta con alimentos y sus calorías, un calendario que de un control diario de consumo de calorias al igual que el agua, tiene un apartado de perfil que nos permitira ir llevando una reivisión sobre el plan que tenga, el proposito es facilitar y ayudar a las personas para ser un mundo mejor en el futuro.",
                    },
                ]
    
    return render_template("home.html",informacion=informacion)

@app.route('/login', methods=["POST", "GET"])
def login():
    error = None
    contraseña =request.form("contraseña")
    
    return render_template("login.html")

@app.route('/registro' , methods=["POST", "GET"])
def registro():
    if request.method == "POST":
        nomyape = request.form["nombre"]
        correo = request.form["email"]
        contraseña = request.form["contraseña"]
        edad = request.form["edad"]
        peso = request.form["peso"]
        altura = request.form["altura"]
        sexo = request.form["sexo"]
        contrafirma = request.form["confirmar_contraseña"]
        
        error = None
        
        if contraseña != contrafirma:
            flash(f"Las contraseñas no coinciden" , "danger")
            return render_template(("registro.html"))
        else:
            perfiles.append(
                {"nombre":nomyape, 
                "correo":correo, 
                "contraseña":contraseña,
                "edad":edad, 
                "peso":peso, 
                "altura":altura, 
                "sexo":sexo
                })
            return render_template("perfil.html")
        
    return render_template("registro.html")

@app.route('/perfil')
def perfil():
    return render_template("perfil.html")

@app.route('/acerca')
def acerca_de():
    return render_template("acerca_de.html")

@app.route('/contador')
def contador():
    return render_template("contador.html")

if __name__ == "__main__":
    app.run(debug=True)