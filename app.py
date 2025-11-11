from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import timedelta,datetime


app = Flask(__name__)
app.secret_key = "1q2w3e4r5t6y7u8i9o0p1a2s3d4f5g6h7j8k9l"
app.permanent_session_lifetime = timedelta(minutes=5)

## Falta validasr dsatos que funcione bien logica para encontrar buscar los datos de los usuarios, flata los objetivos para que pase de un lado a otro, tambien ver a donde
## redirigir los datos a un solo lado y almacenarlos

perfiles = []

correos = []
print(perfiles)

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

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        correo = request.form.get('correo')
        contraseña = request.form.get('contraseña')

        for perfil in perfiles:
            if correo == perfil['correo'] and contraseña == perfil['contraseña']:
                session['usuario'] = perfil
                return redirect('/perfil')

        flash("Correo o contraseña incorrectos")
        return render_template('login.html')

    return render_template('login.html')

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
        
        if contraseña != contrafirma:
            flash("Las contraseñas no coinciden", "danger")
            return render_template("registro.html")
            
        for u in perfiles:
            if u['correo'] != correo:
                usuario = {"nombre":nomyape, 
                    "correo":correo, 
                    "contraseña":contraseña,
                    "edad":edad, 
                    "peso":peso, 
                    "altura":altura, 
                    "sexo":sexo,
                    }
                session['usuario'] = correo
                perfiles.append(usuario)
                return render_template("objetivos.html")
            break
                    
    return render_template("registro.html")

@app.route('/objetivos', methods=["POST", "GET"])
def objetivos():
    if request.method == "POST":
        objetivo = request.form["objetivos"]

        for u in perfiles:
            if session['usuario'] == u['correo']:
                u["objetivo"] = objetivo 
                return redirect('/preferencias')
            break

        flash("No se encontró el usuario en sesión")
        return render_template("objetivos.html")

    return render_template("objetivos.html")

@app.route('/preferencias', methods=["POST","GET"])
def preferencias():
    if request.method == "POST":
        preferencias_usr = {
            "alergia": request.form["alergia"],
            "alergias": request.form["alergias"],
            "intolerancia": request.form["intolerancias"],
            "dietas": request.form["dietas"],
            "no_gusta": request.form["no_gustan"]
        }

        for u in perfiles:
            if session['usuario'] == u['correo']:
                u["preferencias"] = preferencias_usr
                return redirect('/nivel')

        flash("Error al guardar preferencias")
        return render_template("preferencias.html")

    return render_template("preferencias.html")

@app.route('/nivel', methods=["POST","GET"])
def experiencia():
    if request.method == "POST":
        experi = request.form["experiencia"]

        for u in perfiles:
            if session['usuario'] == u['correo']:
                u["experiencia"] = experi
                return redirect('/perfil')

        flash("No se pudo guardar la experiencia")
        return render_template("nivel.html")

    return render_template("nivel.html")

@app.route('/perfil')
def perfil():
    usua = None

    for u in perfiles:
        if session.get('usuario') == u['correo']:
            usua = u
            break

    if usua is None:
        flash("No se encontró el usuario en la sesión")
        return redirect('/registro')

    return render_template('perfil.html', usuario=usua)

@app.route('/registrar_alimentos')
def alimentos():
    return render_template("registrar_alimentos.html")

## De aqui para abajo despues no mover hasta la otra semana

@app.route('/acerca')
def acerca_de():
    return render_template("acerca_de.html")

@app.route('/contador')
def contador():
    return render_template("contador.html")

if __name__ == "__main__":
    app.run(debug=True)