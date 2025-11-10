from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import timedelta,datetime


app = Flask(__name__)
app.secret_key = "1q2w3e4r5t6y7u8i9o0p1a2s3d4f5g6h7j8k9l"
app.permanent_session_lifetime = timedelta(minutes=5)

## Falta validasr dsatos que funcione bien logica para encontrar buscar los datos de los usuarios, flata los objetivos para que pase de un lado a otro, tambien ver a donde
## redirigir los datos a un solo lado y almacenarlos

perfiles = [
        {"nombre":"Admin", 
        "correo":"Admin/08-@gmail.com",
        "contraseña":"Admin1920",
        "edad":"17", 
        "peso":"95.7", 
        "altura":"1.79", 
        "sexo":"Masculino",
        }
]

@app.route('/') ## No mover
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

@app.route('/login', methods=["POST", "GET"])##Iniciar sesion 
def login():
    usuario = []
    if request.method == "POST":
        correo = request.form["correo"]
        contraseña =request.form("contraseña")
        
        for perfil in perfiles:
            if correo == perfil["correo"]:##falta hay error aqui
                usuario = perfil
                flash(f"Perfil encontrado", "success")
                return render_template("perfil.html")
            else:
                flash(f"No se encontro perfil", "danger")
                return render_template("login.html")
            
    return render_template("login.html")

@app.route('/registro' , methods=["POST", "GET"])##Registro
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
            flash("Las contraseñas no coinciden", "danger")
            return render_template("registro.html")
        else:
            session['usuario']= {"nombre":nomyape, 
                "correo":correo, 
                "contraseña":contraseña,
                "edad":edad, 
                "peso":peso, 
                "altura":altura, 
                "sexo":sexo
                }
            return render_template("objetivos.html")
        
    return render_template("registro.html")

@app.route('/objetivos', methods=["POST", "GET"])##Objetivos
def objetivos():
    if request.method == "POST":
        objetivos = request.form["objetivos"]
        session['usuario']['objetivo'] = objetivos
        return redirect('/preferencias')
    
    return render_template("objetivos.html")

@app.route('/preferencias',methods=["POST","GET"])
def preferencias():
    if request.method == "POST":
        alergia = request.form["alergia"]
        alergias = request.form["alergias"]
        intolerancia = request.form["intolerancias"]
        dietas = request.form["dietas"]
        no_gusta = request.form["no_gustan"]
        
        preferencias = { "alergia":alergia,
                        "alergias":alergias,
                        "intolerancia":intolerancia,
                        "dietas":dietas,
                        "no_gusta":no_gusta
                        }
        
        session['usuario']['preferencias'] = preferencias
        return redirect('/nivel')
    return render_template("preferencias.html")

@app.route('/nivel',methods={"POST","GET"})
def experiencia():
    if request.method == "POST":
        experi = request.form["experiencia"]
        
        session['usuario']['experiencia'] = experi
        
        perfiles.append(session['usuario'])
        return redirect('/login')## no manda a logiiin
    return render_template("experiencia.html")



## De aqui para abajo despues no mover hasta la otra semana
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