from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import timedelta,datetime
import requests


app = Flask(__name__)
app.secret_key = "1q2w3e4r5t6y7u8i9o0p1a2s3d4f5g6h7j8k9l"
app.permanent_session_lifetime = timedelta(minutes=5)

## Falta revisar el iniciar secion, tambien modificar el navbar para que cambie segun si hay sesion iniciada o no mostrar ciertas cosas como contador perfil etc
## Solo debe de mostar alinicio home , login, registro, acerca de

perfiles = []

correos = []

alimentos_cons = []

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
                session['usuario'] = perfil['correo']
                session.permanent = True
                return redirect('/perfil')

        flash("Correo o contraseña incorrectos", "danger")
        return render_template('login.html')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    session.permanent = False
    flash("Has cerrado sesión correctamente.", "success")
    return redirect('/login')

@app.route('/registro', methods=["POST", "GET"])
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
            if u['correo'] == correo:
                flash("El correo ya está registrado.", "danger")
                return render_template("registro.html")
        usuario = {
            "nombre": nomyape,
            "correo": correo,
            "contraseña": contraseña,
            "edad": edad,
            "peso": peso,
            "altura": altura,
            "sexo": sexo,
            "objetivo": "",
            "preferencias": {},
            "experiencia": ""
        }

        perfiles.append(usuario)
        session['usuario'] = correo
        return redirect("/objetivos")

    return render_template("registro.html")

@app.route('/objetivos', methods=["POST", "GET"])
def objetivos():
    if request.method == "POST":
        objetivo = request.form["objetivos"]

        for u in perfiles:
            if session.get('usuario') == u['correo']:
                u["objetivo"] = objetivo 
                return redirect('/preferencias')
        else:
            flash("No se encontró el usuario en sesión", "danger")
            return render_template("objetivos.html")

    return render_template("objetivos.html")

@app.route('/preferencias', methods=["POST","GET"])
def preferencias():
    if request.method == "POST":
        alergia = request.form["alergia"]
        alergias = request.form["alergias"]
        intolerancia = request.form["intolerancias"]
        dietas = request.form["dietas"]
        no_gusta = request.form["no_gustan"]
        
        preferencias={
            "alergia":alergia,
            "alergias":alergias,
            "intolerancia":intolerancia,
            "dietas":dietas,
            "no_gusta":no_gusta
        }

        for u in perfiles:
            if session.get('usuario') == u['correo']:
                u["preferencias"] = preferencias
                return redirect('/nivel')
        else:
            flash("Error al guardar preferencias", "danger")
            return render_template("preferencias.html")
    return render_template("preferencias.html")

@app.route('/nivel', methods=["POST","GET"])
def nivel():
    if request.method == "POST":
        experi = request.form["experiencia"]

        for u in perfiles:
            if session.get('usuario') == u['correo']:
                u["experiencia"] = experi
                return redirect('/perfil')
        else:
            flash("No se pudo guardar la experiencia", "danger")
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
        flash("No se encontró el usuario en la sesión" , "danger")
        return redirect('/registro')

    return render_template('perfil.html', usuario=usua)

@app.route('/acerca')
def acerca_de():
    return render_template("acerca_de.html")

## De aqui para abajo despues no mover hasta la otra semana



@app.route('/registrar_alimentos')
def alimentos():
    return render_template("registrar_alimentos.html")

@app.route("/contador",methods=["POST","GET"])
def contador():
    
    if  request.method == "POST":
        nombre = request.form["alimento"]
        grasas = request.form["grasas"]
        prote = request.form["proteinas"]
        carbo = request.form["carbohidratos"]
        agua = request.form["agua"]
        
        grasa=0
        proteinas=0
        carbohidratos=0
        
        grasa = 9*float(grasas)
        proteinas = 4*float(prote)
        carbohidratos = 4*float(carbo)
        
        
        grasat = str(grasa)
        proteinast = str(proteinas)
        carbohidratost = str(carbohidratos)
        
        alimento = {
            "nombre": nombre ,
            "grasas": grasas ,
            "proteinas": prote ,
            "carbohidratos":carbo ,
            "grasasc":grasat,
            "proteinasc":proteinast,
            "carbohidratosc":carbohidratost,
            "agua":agua
        }
        alimentos_cons.append(alimento)
        
    return render_template("contador.html", alimento=alimentos_cons,)

@app.route("/eliminar")
def eliminar ():
    if alimentos_cons:
        alimentos_cons.pop(-1)
    return render_template("contador.html", alimento=alimentos_cons )

@app.route("/calculoene")
def calculoene ():
    return render_template("Calculoene.html")

@app.route("/energia", methods = ["Get", "POST"])
def energia():
    usua = None

    for u in perfiles:
        if session.get('usuario') == u['correo']:
            usua = u
            break

    if usua is None:
        flash("No se encontró el usuario en la sesión" , "danger")
        return redirect('/registro')
    
    if request .method == "POST":
        edad = request.form["edad"]
        altu = request.form["altu"]
        peso = request.form["peso"]
        genero = request.form["genero"]
        actividad = request.form["activi"]
        
        tbm = 0
        get = 0
        nivel = 0
        altura = float(altu)*100
        
        if actividad == "sedentario":
            nivel = 1.2
        else:
            if actividad == "ligera":
                nivel = 1.375
            else:
                if actividad == "moderada":
                    nivel=1.55
                else:
                    if actividad == "alta":
                        nivel = 1,725
        
        if genero == "hombre":
            tbm = 10*float(peso)+6.25*float(altura)-5*float(edad)+5
        else:
            if genero == "mujer":
                tbm = 10*float(peso)+6.25*float(altura)-5*float(edad)-161
        
        get = tbm * nivel
        
    return render_template("energiresu.html",get=get,tbm=tbm,)

if __name__ == "__main__":
    app.run(debug=True)