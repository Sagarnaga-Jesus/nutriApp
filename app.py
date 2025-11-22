from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import timedelta,datetime
import requests


app = Flask(__name__)
app.secret_key = "1q2w3e4r5t6y7u8i9o0p1a2s3d4f5g6h7j8k9l"
app.permanent_session_lifetime = timedelta(minutes=5)

API_URL = "https://api.edamam.com/api/recipes/v2"
API_ID = "54f74682"
API_KEY = "40219f3173e572e7d42a1ef58874bab2"

NUTRIENTES_API_URL = "https://api.edamam.com/api/food-database/v2/parser"
NUTRIENTES_API_ID = "8497257e"
NUTRIENTES_API_KEY = "937ef3deb00ae9d109f4bd50ec9fc6fe"

## Falta modificar el navbar al momento de iniciar sesion 
## Meter dos apis mas 1 nutrientes, y analizador de recetas
## Parece no funcionar ahorita la api de recetas ni idea
## Analizador de recetas meter 2 plantillas una de "Registro de alimentos para analizarlos" y "Receta analizada"

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

@app.route('/acerca')## acerca de
def acerca_de():
    return render_template("acerca_de.html")

@app.route('/login', methods=['POST', 'GET'])##iniciar sesion
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

@app.route('/logout')## cierra sesion
def logout():
    session.pop('usuario', None)
    session.permanent = False
    flash("Has cerrado sesión correctamente.", "success")
    return redirect('/login')

@app.route('/registro', methods=["POST", "GET"])##Registro
def registro():
    if request.method == "POST":
        nomyape = request.form["nombre"]
        correo = request.form["email"]
        contraseña = request.form["contraseña"]
        edad = request.form["edad"]
        peso = request.form["peso"]
        altura = request.form["altura"]
        actividad = request.form["actividad"]
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
            "actividad": actividad,
            "sexo": sexo,
            "objetivo": "",
            "preferencias": {},
            "experiencia": ""
        }

        perfiles.append(usuario)
        session['usuario'] = correo
        return redirect("/objetivos")

    return render_template("registro.html")

##Registro de datos de usuario
@app.route('/objetivos',methods=["POST", "GET"])
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
##Acaba el registro de usuario

@app.route('/perfil')## perfil de usuario envia datos del registro de usuario
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



##Buscadores de rcetas
@app.route('/buscador')
def buscador():
    return render_template("buscador.html")

@app.route('/buscar', methods=['POST'])
def buscar():
    recetas = []
    
    alimento = request.form.get('name', '').strip().lower()
    
    if not alimento:
        flash("Ingresa un ingrediente", "danger")
        return redirect(url_for('buscador'))

    params = {
        "type": "public",
        "q": alimento,
        "app_id": API_ID,
        "app_key": API_KEY
    }

    try:
        
        if not alimento:
            flash('Por favor ingresa un nombre de Alimento válido.', 'danger')
            return redirect(url_for('buscador'))
        
        response = requests.get(API_URL, params=params)
        data = response.json()
        

        if "hits" not in data or not data["hits"]:
            flash("No se encontraron recetas.", "danger")
            return redirect(url_for('buscador'))

        
        for item in data["hits"]:
            receta = item["recipe"]
            recetas.append({
                "name": receta["label"],
                "imagen": receta["images"]["REGULAR"]["url"],
                "calorias": int(receta["calories"]),
                "ingredientes": receta["ingredientLines"]
            })

        return render_template("targeta.html", recetas=recetas)

    except Exception as e:
        print("ERROR:", e)
        flash("Error al conectar con Edamam.", "danger")
        return redirect(url_for('buscador'))

##Calculadoras 

@app.route('/registrar_alimentos')## guarda e calcula una lista de nutrientes de alimentos
def alimentos():
    return render_template("registrar_alimentos.html")

@app.route("/contador",methods=["POST","GET"])## contador de nutrientes
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

@app.route("/eliminar")## elimina el ukltimo alimento ingresado
def eliminar ():
    if alimentos_cons:
        alimentos_cons.pop(-1)
    return render_template("contador.html", alimento=alimentos_cons )

@app.route("/calculoene") ## ingreso de datos para energetico por ahora no se usa por que se saca automaticamente informacion
def calculoene ():
    return render_template("calculotbmygct.html")

@app.route("/energia", methods = ["Get", "POST"]) ## calcula el tmb y gasto energetico total
def energia():
    if request.method == "POST":
        peso = request.form["peso"]
        edad= request.form["edad"]
        altura=  request.form["altura"]
        genero= request.form["genero"]
        actividad= request.form["actividad"]
    
    tbm = 0
    get = 0
    nivel = 0
    peso = float(peso)
    altura = float(altura)*100

        
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

@app.route('/energiresu') ## creo que hizimos 2 gasto energetico
def energiresu():
    usua = None

    for u in perfiles:
        if session.get('usuario') == u['correo']:
            usua = u
            break

    if usua is None:
        flash("No se encontró el usuario en la sesión", "danger")
        return redirect('/registro')

    edad = float(usua["edad"])
    peso = float(usua["peso"])
    altu = float(usua["altura"])
    genero = usua["sexo"]
    actividad = usua["actividad"]

    altura = altu * 100

    if actividad == "sedentario":
        nivel = 1.2
    elif actividad == "ligera":
        nivel = 1.375
    elif actividad == "moderada":
        nivel = 1.55
    elif actividad == "alta":
        nivel = 1.725
    else:
        nivel = 1.2

    if genero == "hombre":
        tbm = 10 * peso + 6.25 * altura - 5 * edad + 5
    else:
        tbm = 10 * peso + 6.25 * altura - 5 * edad - 161

    get = tbm * nivel
    
    get = round(get, 2)
    tbm = round(tbm, 2)

    return render_template("energiresu.html", get=get, tbm=tbm)

@app.route('/calcuimc') ## calculadora de imc
def imc():
    usua = None
    for u in perfiles:
        if session.get('usuario') == u['correo']:
            usua = u
            break

    if usua is None:
        flash("No se encontró el usuario en la sesión", "danger")
        return redirect('/registro')
    
    edad = float(usua["edad"])
    peso = float(usua["peso"])
    altu = float(usua["altura"])
    
    altura2 = altu * altu
    
    imc = peso/altura2
    
    imc=round(imc,2)
    
    info = None
    reco = None
    if imc <= 18.5:
        info = "Bajo de peso"
        reco = "Pídale a su médico que lo ayude a calcular la cantidad de calorías que necesita diariamente para mantener su encuadre ligero actual, teniendo en cuenta su edad, nivel de actividad y género"
    else:
        if imc >= 18.5 and imc <= 24.9:
            info = "Peso normal"
            reco = "Para mantener un peso saludable evite los alimentos densos en calorías. Y evite las bebidas azucaradas."
        else:
            if imc >= 25 and imc <= 29.9:
                info = "Sobrepeso"
                reco = "se recomienda una combinación de una dieta saludable y actividad física regular. Esto incluye consumir abundantes frutas y verduras, limitar grasas y azúcares, preferir métodos de cocción como la plancha o el vapor, tomar suficiente agua y realizar ejercicio físico adaptado a las capacidades individuales, además de mantener un seguimiento médico regular"
            else:
                if imc >= 30 and imc <= 34.9:
                    info = "Obesidad ligera"
                    reco =  "La mejor estrategia implica una combinación de cambios en la dieta y aumento de la actividad física, siempre bajo la supervisión de un profesional médico"      
                else:
                    if imc >= 35 and imc <= 39.9:
                        info = "Obesidad"
                        reco = "Algunas medidas que se pueden adoptar y que servirán para mantener el peso adecuado son: 1- Mantenerte activo. 2- Comer sano. 3- Ingerir agua.4- Llevar a cabo chequeo médico por lo menos una vez al año. 5- Evitar alimentos ricos en grasas y carbohidratos."
                    else: 
                        if imc >= 40:
                            info = "Obesidad morbida o grave"
                            reco = "Para evitar el aumento de peso es necesario llevar un estilo de vida saludable, la práctica de deporte y el control de las ingestas diarias. Realizar ejercicio de forma regular, se recomienda caminar, correr o nadar." 
    
    
    return render_template('calculadoraimc.html', usuario=usua, imc=imc, informacion=info, recomendaciones=reco )

@app.route('/calcupeso')##calculadora peso corporal ideal
def peso():
    usua = None
    for u in perfiles:
        if session.get('usuario') == u['correo']:
            usua = u
            break

    if usua is None:
        flash("No se encontró el usuario en la sesión", "danger")
        return redirect('/registro')
    
    altu = float(usua["altura"])
    genero = usua["sexo"]
    
    altu_cm = altu*100
    psi = None
    
    if genero == "Masculino":
        psi = (altu_cm - 100) * 0.90
        psi = round(psi, 2)
    else:
        if genero == "Femenino":
            psi = (altu_cm - 100) * 0.85
            psi = round(psi, 2)
    return render_template('calculadorapeso.html', usuario=usua, psi=psi)
    
@app.route('/registroimc')
def registroimc():
    return render_template('registroimc.html')  

@app.route("/registropsi")
def registropsi():
    return render_template("registro-psi-sin.html")

@app.route('/cal-sin-imc', methods=["POST", "GET"])
def registroimc2():
    if request.method == "POST":
        peso = request.form["peso"]
        altura = request.form["altura"]
        
    peso = float(peso)
    altu = float(altura)

    altura2 = altu * altu
    
    imc = peso/altura2
    
    imc=round(imc,2)
    
    info = None
    reco = None
    if imc <= 18.5:
        info = "Bajo de peso"
        reco = "Pídale a su médico que lo ayude a calcular la cantidad de calorías que necesita diariamente para mantener su encuadre ligero actual, teniendo en cuenta su edad, nivel de actividad y género"
    else:
        if imc >= 18.5 and imc <= 24.9:
            info = "Peso normal"
            reco = "Para mantener un peso saludable evite los alimentos densos en calorías. Y evite las bebidas azucaradas."
        else:
            if imc >= 25 and imc <= 29.9:
                info = "Sobrepeso"
                reco = "se recomienda una combinación de una dieta saludable y actividad física regular. Esto incluye consumir abundantes frutas y verduras, limitar grasas y azúcares, preferir métodos de cocción como la plancha o el vapor, tomar suficiente agua y realizar ejercicio físico adaptado a las capacidades individuales, además de mantener un seguimiento médico regular"
            else:
                if imc >= 30 and imc <= 34.9:
                    info = "Obesidad ligera"
                    reco =  "La mejor estrategia implica una combinación de cambios en la dieta y aumento de la actividad física, siempre bajo la supervisión de un profesional médico"      
                else:
                    if imc >= 35 and imc <= 39.9:
                        info = "Obesidad"
                        reco = "Algunas medidas que se pueden adoptar y que servirán para mantener el peso adecuado son: 1- Mantenerte activo. 2- Comer sano. 3- Ingerir agua.4- Llevar a cabo chequeo médico por lo menos una vez al año. 5- Evitar alimentos ricos en grasas y carbohidratos."
                    else: 
                        if imc >= 40:
                            info = "Obesidad morbida o grave"
                            reco = "Para evitar el aumento de peso es necesario llevar un estilo de vida saludable, la práctica de deporte y el control de las ingestas diarias. Realizar ejercicio de forma regular, se recomienda caminar, correr o nadar." 
    
    
    return render_template('cal-imc-sin.html',peso=peso, altura=altura, imc=imc, informacion=info, recomendaciones=reco )

@app.route('/calcupeso', methods=["POST", "GET"])##calculadora peso corporal ideal sin registro
def peso2():
    if request.method == "POST":
        genero = request.form["sexo"]
        peso = request.form["peso"]
        altura = request.form["altura"]
        
    altura = float(altura)
    altu_cm = altura*100
    psi = None
    
    if genero == "Masculino":
        psi = (altu_cm - 100) * 0.90
        psi = round(psi, 2)
    else:
        if genero == "Femenino":
            psi = (altu_cm - 100) * 0.85
            psi = round(psi, 2)
    return render_template('cal-psi-sin.html', psi=psi, peso=peso, altura=altura,)
    
if __name__ == "__main__":
    app.run(debug=True)