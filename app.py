from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import timedelta,datetime
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash,check_password_hash
import re 
import requests


app = Flask(__name__)
app.secret_key = "1q2w3e4r5t6y7u8i9o0p1a2s3d4f5g6h7j8k9l"
app.permanent_session_lifetime = timedelta(minutes=5)

API_URL = "https://api.edamam.com/api/recipes/v2"
API_ID = "6d8321c7"
API_KEY = "3299bb508e6a3b92fd7b3d8597f1e80d"

NUTRIENTES_API_URL = "https://api.edamam.com/api/food-database/v2/parser"
NUTRIENTES_API_ID = "8497257e"
NUTRIENTES_API_KEY = "937ef3deb00ae9d109f4bd50ec9fc6fe"

##Configuracion MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'bdnutriapp'
app.config['MYSQL_CURSORCLASS']='DictCursor'## hace que se vuelva diccionario por la informacion esta en  tuplas

mysql = MySQL(app)


## Meter dos apis mas 1 nutrientes, y analizador de recetas
## Parece no funcionar ahorita la api de recetas ni idea
## Analizador de recetas meter 2 plantillas una de "Registro de alimentos para analizarlos" y "Receta analizada"
## bd agregar a contraseña 255 en caracteres

def crear_tabla():##Funcion para crear la tabla de usuarios
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios(
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                telefono VARCHAR(20),
                fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        mysql.connection.commit()
    except Exception as e:
        print("Error al crear la tabla:", e)

def email_existe(email):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        return cursor.fetchone() is not None
    except Exception as e:
        print(f"Error verificando el email: {e}")
        return False
    
def registra_usuario(nombre, email, password, telefono):##Funcion de registro de usuario
    try:
        cursor = mysql.connection.cursor()

        hashed_password = generate_password_hash(password)
        
        cursor.execute('''
                INSERT INTO usuarios (nombre, email, password, telefono)
                VALUES (%s, %s, %s, %s)
                ''', (nombre, email, hashed_password, telefono))
        
        mysql.connection.commit()
        return True, "Usuario registrado exitosamente."
    except Exception as e:
        print("Error al registrar el usuario:", e)
        return False, "Error al registrar el usuario."

perfiles = [
    {
        "nombre": "Admin",
        "correo": "admin@example.com",
        "contraseña": "Admin#12345",
        "edad": "25",
        "peso": "70",
        "altura": "1.75",
        "actividad": "Moderada",
        "sexo": "Masculino",
        "objetivo": "Bajar de peso",
        "preferencias": {
            "alergia": "Ninguna",
            "alergias": "Ninguna",
            "intolerancia": "Ninguna",
            "dietas": "Balanceada",
            "no_gusta": "Brócoli"
        },
        "experiencia": "Intermedio"
    }
]

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

@app.route('/nutri', methods=['POST', 'GET'])
def nutri():
    if request.method == 'POST':
        busqueda_nutri = request.form.get('busqueda_nutri', '').strip()
        if not busqueda_nutri:
            flash('Por favor, ingrese un término de búsqueda válido.', 'warning')
            return redirect(url_for('home'))
        
        params = {
            'app_id': NUTRIENTES_API_ID,
            'app_key': NUTRIENTES_API_KEY,
            'ingr': busqueda_nutri
        }
        try:
            response = requests.get(NUTRIENTES_API_URL, params=params)
            if response.status_code != 200:
                flash (f"Error en la solicitud a la API: {response.status_code}", 'error')
                return redirect(url_for('home'))
            
            data = response.json()
            alimentos_encontrados = data.get('hints', [])
            if not alimentos_encontrados:
                flash(f"No se encontraron alimentos para la búsqueda proporcionada.", 'warning')
                return redirect(url_for('home'))
    
            return render_template('Nutrientes.html', alimentos=alimentos_encontrados, busqueda=busqueda_nutri)
        
        except requests.exceptions.RequestException as e:
            flash(f"Error en la solicitud a la API: {e}", 'error')
            return redirect(url_for('home'))
        
    return render_template('buscanutri.html')

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
        
        response = requests.get(API_URL, params)
        data = response.json()
        

        if "hits" not in data or not data["hits"]:
            flash("No se encontraron recetas.", "danger")
            return redirect(url_for('buscador'))

        recetas = []
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

@app.route("/eliminar")## elimina el ultimo alimento ingresado
def eliminar ():
    if alimentos_cons:
        alimentos_cons.pop(-1)
    return render_template("contador.html", alimento=alimentos_cons )



@app.route("/calculoene") ## ingreso de datos para energetico por ahora no se usa por que se saca automaticamente informacion
def calculoene ():
    return render_template("calculotbmygct.html")

@app.route('/energiresu', methods = ["Get", "POST"]) ## Calculadora de gct y tmb, registro y sin registro
def energiresu(): 
    usua = None
    for u in perfiles:
        if session.get('usuario') == u['correo']:
            usua = u
            break

    if usua is None:
        if request.method == "POST":
            pesoregistro = request.form["peso"]
            edadregistro = request.form["edad"]
            alturaregistro =  request.form["altura"]
            generoregistro = request.form["genero"]
            actividadregistro = request.form["actividad"]
    
            tbm = 0
            get = 0
            nivel = 0
            peso = float(pesoregistro)
            altura = float(alturaregistro)*100

        
        if actividadregistro == "sedentario":
            nivel = 1.2
        else:
            if actividadregistro == "ligera":
                nivel = 1.375
            else:
                if actividadregistro == "moderada":
                    nivel=1.55
                else:
                    if actividadregistro == "alta":
                        nivel = 1.725
            
            if generoregistro == "hombre":
                tbm = 10*float(pesoregistro)+6.25*float(alturaregistro)-5*float(edadregistro)+5
            else:
                if generoregistro == "mujer":
                    tbm = 10*float(pesoregistro)+6.25*float(alturaregistro)-5*float(edadregistro)-161
            
            get = tbm * nivel
            get = round(get, 2)
            tbm = round(tbm, 2)
        return render_template('energiresu.html',get=get,tbm=tbm,)
    
    else:
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
    return render_template("energiresu.html",usuario=usua, get=get, tbm=tbm)

@app.route('/registroimc')## Registro de datos imc
def registroimc():
    return render_template('registroimc.html')  

@app.route('/calcuimc', methods=["POST", "GET"]) ## calculadora de imc, registro y sin registro
def imc():
    usua = None
    for u in perfiles:
        if session.get('usuario') == u['correo']:
            usua = u
            break

    if usua is None:
        
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
        
        return render_template('calculadoraimc.html',peso=peso, altura=altura, imc=imc, informacion=info, recomendaciones=reco )

    else:
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

@app.route("/registropsi")## Registro del psi
def registropsi():
    return render_template("registro-psi-sin.html")

@app.route('/calcupeso', methods=["POST", "GET"])##calculadora peso corporal ideal, registro y sin registro
def peso():
    usua = None
    for u in perfiles:
        if session.get('usuario') == u['correo']:
            usua = u
            break

    if usua is None:
        if request.method == "POST":
            altura = request.form["altura"]
            peso = request.form["peso"]
            genero = request.form["sexo"]
            
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
        return render_template('calculadorapeso.html',altura=altura, peso=peso, psi=psi)
    else:
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

@app.route('/informacion')##no funciona corrigo ahorita 
def info():
    return render_template('informacion.html')


if __name__ == "__main__":
    app.run(debug=True)