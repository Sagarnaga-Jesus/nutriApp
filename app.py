from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import timedelta,datetime
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash,check_password_hash
import re 
import json
import requests


app = Flask(__name__)
app.secret_key = "1q2w3e4r5t6y7u8i9o0p1a2s3d4f5g6h7j8k9l"
app.permanent_session_lifetime = timedelta(minutes=60)

API_URL = "https://api.edamam.com/api/recipes/v2"
API_ID = "693b2b1a"
API_KEY = "38a99c86ea2c3d1562b6106cec16abdb"

NUTRIENTES_API_URL = "https://api.edamam.com/api/food-database/v2/parser"
NUTRIENTES_API_ID = "8497257e"
NUTRIENTES_API_KEY = "937ef3deb00ae9d109f4bd50ec9fc6fe"

##Configuracion MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'alum1#19' ##poner alum1#19 si eres Sagarnaga, sacarlo si eres Luis DATE CUENTAA
app.config['MYSQL_DB'] = 'bdnutriapp'
##app.config['MYSQL_CURSORCLASS']='DictCursor'## hace que se vuelva diccionario por la informacion esta en  tuplas

mysql = MySQL(app)


## falta revision final
## no se que mas podemos agregar ideas o mejorar
## vere si hacer la bd de alimentos, no la hice
## ando viendo si poner el home en lo de iniciar sesion o dejarlo nomas con el nombre de la app
##  vere si mañana puedo hacer la paginacion de las recetas, no pude
## falta revisar los porcentajes de la api de luis esta raro, lo checa luis


def crear_tabla():##Funcion para crear la tabla de usuarios
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuario(
                id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(50) NULL DEFAULT NULL,
                apellido VARCHAR(50) NULL DEFAULT NULL,
                correo VARCHAR(150) NULL DEFAULT NULL,
                contraseña VARCHAR(255) NULL DEFAULT NULL,
                edad INT(11) NULL DEFAULT NULL,
                peso FLOAT NULL DEFAULT NULL,
                altura FLOAT NULL DEFAULT NULL,
                actividad VARCHAR(40) NULL DEFAULT NULL,
                sexo VARCHAR(25) NULL DEFAULT NULL,
                objetivo VARCHAR(150) NULL DEFAULT NULL,
                preferencias VARCHAR(250) NULL DEFAULT NULL,
                experiencia VARCHAR(150) NULL DEFAULT NULL
            );
        ''')
        mysql.connection.commit()
    except Exception as e:
        print("Error al crear la tabla:", e)

def email_existe(correo):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM usuario WHERE correo = %s", (correo,))
        return cursor.fetchone() is not None
    except Exception as e:
        print(f"Error verificando el email: {e}")
        return False

def obtener(correo):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM usuario WHERE correo = %s", (correo, ))
        usuario = cursor.fetchone()
        return usuario
    except Exception as e:
        print(f"No se encontro al usuario {e}")

def registra_usuario(nombre, apellido, correo, contraseña, edad, peso, altura, actividad, sexo):##Funcion de registro de usuario
    try:
        cursor = mysql.connection.cursor()

        hashed_password = generate_password_hash(contraseña)
        
        cursor.execute('''
            INSERT INTO usuario
            (nombre, apellido, correo, contraseña, edad, peso, altura, sexo, actividad)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (nombre, apellido, correo, hashed_password, edad, peso, altura, sexo, actividad))
        
        mysql.connection.commit()
        return True
    except Exception as e:
        print("Error al registrar el usuario:", e)
        return False, "Error al registrar el usuario."
    
def registrar_objetivos(objetivo):
    try:
        cursor = mysql.connection.cursor()
        correo = session.get('correo_registro')
        
        if not correo:
            return False, "No hay correo en sesión"

        cursor.execute("""
            UPDATE usuario
            SET objetivo = %s
            WHERE correo = %s
        """, (objetivo, correo))
        mysql.connection.commit()
        cursor.close()
        return True
    except Exception as e:
        print("Error al registrar los objetivos:", e)
        return False, "Error al registrar los objetivos."

    
def registrar_preferencias(preferencias):
    try:
        cursor = mysql.connection.cursor()
        correo=session.get('correo_registro')
        
        cursor.execute('''
            UPDATE usuario
            SET preferencias = %s
                WHERE correo = %s
        ''', (preferencias,correo))
        mysql.connection.commit()
        cursor.close()
        return True
    except Exception as e:
        print("Error al registrar los objetivos:", e)
        return False, "Error al registrar los objetivos."
    
def registrar_experiencia(experi):
    try:
        cursor = mysql.connection.cursor()
        correo=session.get('correo_registro')
        
        if not correo:
            return False, "No hay correo en sesión"
        
        cursor.execute('''
            UPDATE usuario
            SET experiencia = %s
                WHERE correo = %s
        ''', (experi,correo))
        mysql.connection.commit()
        cursor.close()
        return True
    except Exception as e:
        print("Error al registrar los objetivos:", e)
        return False, "Error al registrar los objetivos."

def obtener_usuario(correo):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM usuario WHERE correo = %s", (correo,))
        usuario = cursor.fetchone()
        cursor.close()
        
        return usuario
    except Exception as e:
        print(f"Error al obtener el usuario: {e}")
        return None

perfiles = []

alimentos_cons = []

print(perfiles)

@app.route('/') ## No mover
def home():
    
    informacion = [
                    {"imagen":"static/imagenes/La-diferencia-entre-nutricion-y-alimentacion1.jpg",
                    "descripcion":"Esta página nutricional ha sido creada para que las personas puedan llevar un control adecuado de su consumo diario de calorías. Actualmente, solo un pequeño porcentaje de la población se preocupa por monitorear su ingesta calórica, lo cual puede afectar su salud y bienestar. Por esta razón, esta página tiene como objetivo ayudar a las personas a mantener un registro claro y accesible de su consumo, promoviendo hábitos alimenticios más saludables.",
                    },
                    {"imagen":"static/imagenes/nutri.jpg",
                    "descripcion":"El fin de esta página es mostrar nuestra actividad calórica y fomentar una vida saludable, guiando a las personas por un buen camino. De esta manera, se busca que, a futuro, no presenten problemas de salud como obesidad u otras complicaciones relacionadas con una mala alimentación.",
                    },
                    {"imagen":"static/imagenes/Estado_Nutri-Post-de-Twitter.jpg",
                    "descripcion":"Esta página cuenta con una sección de alimentos y sus calorías, además de un calendario que permite llevar un control diario del consumo de calorías y de agua. También incluye un apartado de perfil que facilita revisar el progreso según el plan que cada persona siga. El propósito de esta plataforma es apoyar y facilitar una vida más saludable, contribuyendo al bienestar de las personas y a un mejor futuro.",
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
        
        usuario = obtener_usuario(correo)
        
        
        if check_password_hash(usuario[4],contraseña):
            session['usuario'] = usuario[3]
            session['correo_registro'] = usuario[3]
            session['nombre'] = usuario[1]
            return redirect('/')
        else:
            flash("Correo o contraseña incorrectos", "danger")
            return render_template('login.html')
        
    return render_template('login.html')        

@app.route('/logout')## cierra sesion
def logout():
    session.pop('usuario', None)
    session.pop('nombre', None)
    flash("Has cerrado sesión correctamente.", "success")
    return redirect('/')

@app.route('/registro', methods=["POST", "GET"])##Registro
def registro():
    if request.method == "POST":
        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
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
        
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]', correo):
            flash("Correo electrónico inválido", "danger")
            return render_template("registro.html")

        if  email_existe(correo) == True:
            flash("El correo ya está registrado.", "danger")
            return render_template("registro.html")
            
        if not registra_usuario(nombre, apellido, correo, contraseña, edad, peso, altura, actividad, sexo):
            return render_template("registro.html")
        else:
            session['correo_registro'] = correo
            session['nombre_registro'] = nombre
            return redirect("/objetivos")

    return render_template("registro.html")

##Registro de datos de usuario
@app.route('/objetivos', methods=["POST", "GET"])
def objetivos():
    if request.method == "POST":
        objetivo = request.form["objetivos"]
        
        if not objetivo:
            flash("Debes ingresar un objetivo", "danger")
            return redirect("/objetivos")

        exito = registrar_objetivos(objetivo)
        if exito:
            return redirect("/preferencias")
        else:
            flash("Error al registrar los objetivos", "danger")
            return redirect("/objetivos")

    return render_template("objetivos.html")

@app.route('/preferencias', methods=["POST","GET"])
def preferencias():
    if request.method == "POST":
        alergia = request.form["alergia"]
        alergias = request.form.getlist("alergias")
        intolerancia = request.form["intolerancias"]
        dietas = request.form["dietas"]
        no_gusta = request.form["no_gustan"]
        
        if not alergias:
            alergias = ["ninguno"]
            
        if alergia == "si":
            flash("Debes selecionar alnua alergia", "danger")
            return redirect("/campreferencias")
        
        preferencias={
            "alergia":alergia,
            "alergias":alergias,
            "intolerancia":intolerancia,
            "dietas":dietas,
            "no_gusta":no_gusta
        }

        exito = registrar_preferencias(preferencias)
        if exito:
            return redirect("/nivel")
        else:
            flash("Error al registrar las preferencias", "danger")
            return redirect("/preferencias")
    return render_template("preferencias.html")

@app.route('/nivel', methods=["POST","GET"])
def nivel():
    if request.method == "POST":
        experi = request.form["experiencia"]

        exito = registrar_experiencia(experi)
        if exito:
            session['usuario'] = session.get('correo_registro')
            session['nombre'] = session.get('nombre_registro')
            return redirect("/")
        else:
            flash("Error al registrar la experiencia", "danger")
            return redirect("/nivel")
    
    
    return render_template("nivel.html")
##Acaba el registro de usuario

@app.route('/perfil')
def perfil():
    correo = session.get('usuario')
    if not correo:
        flash("Debes iniciar sesión", "danger")
        return redirect('/login')
    
    usuarioe = obtener_usuario(correo)
    diccionario = usuarioe[11]
    diccionario = diccionario.replace("'", '"')
    
    preferencias = json.loads(diccionario)
    if not usuarioe:
        flash("Usuario no encontrado", "danger")
        return redirect('/registro')
    
    return render_template('perfil.html', usuario=usuarioe, preferencias=preferencias)

## Rutas para realizar cambios en la aplicacion
@app.route('/bancorecetas')##Ruta del banco de recetas☺
def bancorecetas():
    return render_template('bancorecetas.html')

@app.route('/camobjetivo', methods=["POST","GET"])##cambio de objetivos
def camobjetivo():
    if request.method == "POST":
        objetivo = request.form["objetivos"]
        
        if not objetivo:
            flash("Debes ingresar un objetivo", "danger")
            return redirect("/camobjetivos")

        exito = registrar_objetivos(objetivo)
        if exito:
            return redirect("/")
        else:
            flash("Error al registrar los objetivos", "danger")
            return redirect("/camobjetivos")
        
    return render_template('cambio-objetivo.html')

@app.route('/campreferencias', methods=["POST","GET"])
def campreferencias():
    if request.method == "POST":
        alergia = request.form["alergia"]
        alergias = request.form.getlist("alergias")
        intolerancia = request.form["intolerancias"]
        dietas = request.form["dietas"]
        no_gusta = request.form["no_gustan"]
        
        if not alergias:
            alergias = ["ninguno"]
            
        if alergia == "si":
            flash("Debes selecionar alnua alergia", "danger")
            return redirect("/campreferencias")
        
        preferencias={
            "alergia":alergia,
            "alergias":alergias,
            "intolerancia":intolerancia,
            "dietas":dietas,
            "no_gusta":no_gusta
        }

        exito = registrar_preferencias(preferencias)
        if exito:
            return redirect("/")
        else:
            flash("Error al registrar las preferencias", "danger")
            return redirect("/campreferencias")
    return render_template("cambio-preferencias.html")

@app.route('/camnivel', methods=["POST","GET"])
def camnivel():
    if request.method == "POST":
        experi = request.form["experiencia"]

        exito = registrar_experiencia(experi)
        if exito:
            return redirect("/")
        else:
            flash("Error al registrar la experiencia", "danger")
            return redirect("/camnivel")
    
    
    return render_template("cambio-nivel.html")
## acaba aqui

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

@app.route('/planificador')## no tiene nada 
def planificador():
    correo = session.get('usuario')
    if not correo:
        flash("Debes iniciar sesión", "danger")
        return redirect('/login')
    
    
    return render_template("planificador.html")


##Calculadoras 

@app.route('/registrar_alimentos')## guarda e calcula una lista de nutrientes de alimentos, para nada fue echo solo por chatpt tambien por mi😊
def alimentos():
    
    return render_template("registrar_alimentos.html")

@app.route("/contador", methods=["GET", "POST"])
def contador():

    if request.method == "GET":
        return render_template(
            "contador.html",
            alimento=session.get("alimentos", [])
        )

    alimento = request.form.get('alimento', '').strip().lower()
    agua = request.form.get("agua", 0)

    if not alimento:
        flash("Ingresa un alimento", "danger")
        return redirect(url_for('registrar_alimentos'))

    try:
        agua = float(agua) if agua else 0
    except ValueError:
        agua = 0

    if "alimentos" not in session:
        session["alimentos"] = []

    try:
        response = requests.get(
            "https://api.edamam.com/api/food-database/v2/parser",
            params={
                "ingr": alimento,
                "app_id": NUTRIENTES_API_ID,
                "app_key": NUTRIENTES_API_KEY
            }
        )

        data = response.json()

        if data.get("parsed"):
            food = data["parsed"][0]["food"]
        elif data.get("hints"):
            food = data["hints"][0]["food"]
        else:
            flash("No se encontró el alimento.", "danger")
            return redirect(url_for('registrar_alimentos'))

        nutrients = food.get("nutrients", {})

        grasa = float(nutrients.get("FAT", 0) or 0)
        proteina = float(nutrients.get("PROCNT", 0) or 0)
        carbohidratos = float(nutrients.get("CHOCDF", 0) or 0)

        resultado = {
            "nombre": food.get("label", alimento),
            "calorias": float(nutrients.get("ENERC_KCAL", 0) or 0),
            "grasa": grasa,
            "proteina": proteina,
            "carbohidratos": carbohidratos,
            "grasa_calorias": grasa * 9,
            "proteina_calorias": proteina * 4,
            "carbohidratos_calorias": carbohidratos * 4,
            "agua": agua
        }

        session["alimentos"].append(resultado)
        session.modified = True

        return redirect(url_for("contador"))

    except Exception as e:
        print("ERROR:", e)
        flash("Error al analizar el alimento.", "danger")
        return redirect(url_for('registrar_alimentos'))

    

@app.route("/eliminar")## elimina el ultimo alimento ingresado
def eliminar ():
    session["alimentos"].pop(-1)
    session.modified = True
    return render_template("contador.html")

@app.route("/calculoene") ## ingreso de datos para energetico por ahora no se usa por que se saca automaticamente informacion
def calculoene ():
    
    return render_template("calculotbmygct.html")

@app.route("/calculotbmygct") ## calculadora de tmb y gct
def calculotbmygct():
    return render_template("calculotbmygct.html")

@app.route('/energiresu', methods = ["Get", "POST"]) ## Calculadora de gct y tmb, registro automatico
def energiresu(): 
    correo = session.get('usuario')
    usuarioe = obtener_usuario(correo)

    
    edad = float(usuarioe[5])
    peso = float(usuarioe[6])
    altu = float(usuarioe[7])
    genero = usuarioe[9]
    actividad = usuarioe[8]

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
    return render_template("energiresu.html",usuario=usuarioe, get=get, tbm=tbm)

@app.route('/energiresumis', methods = ["Get", "POST"]) ## Calculadora de gct y tmb, sin registro y por si mismo
def energiresumis():
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
    return render_template('Calculoene.html',get=get,tbm=tbm,)

@app.route('/registroimc')## Registro de datos imc
def registroimc():
    return render_template('registroimc.html')  

@app.route('/calcuimc', methods=["POST", "GET"]) ## calculadora de imc, registro automaticamente
def imc():
    correo = session.get('usuario')
    usuarioe = obtener_usuario(correo)

    peso = float(usuarioe[6])
    altu = float(usuarioe[7])
    
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
    
    return render_template('calculadoraimc.html', usuario=usuarioe, imc=imc, informacion=info, recomendaciones=reco )

@app.route('/calcuimcmis', methods=["POST", "GET"]) ## calculadora de imc, registro y sin registro
def imcmis():
    
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
    
    return render_template('calculadora-imc-mis.html',peso=peso, altura=altura, imc=imc, informacion=info, recomendaciones=reco )

@app.route("/registropsi")## Registro del psi
def registropsi():
    return render_template("registro-psi-sin.html")

@app.route('/calcupeso', methods=["POST", "GET"])##calculadora peso corporal ideal registro automaticamente
def peso():
    correo = session.get('usuario')
    usuarioe = obtener_usuario(correo)

    altu = float(usuarioe[7])
    genero = usuarioe[9]
    
    altu_cm = altu*100
    psi = None
    
    if genero == "Masculino":
        psi = (altu_cm - 100) * 0.90
        psi = round(psi, 2)
    else:
        if genero == "Femenino":
            psi = (altu_cm - 100) * 0.85
            psi = round(psi, 2)
    return render_template('calculadorapeso.html', usuario=usuarioe, psi=psi)

@app.route('/calcupesomis', methods=["POST", "GET"])##calculadora peso corporal ideal sin registro y ayuda a calcular otra vez
def pesomis():
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
        return render_template('calculadora-psi-mis.html',altura=altura, peso=peso, psi=psi)

@app.route('/informacion')##Ruta de informacion funcional
def info():
    return render_template('informacion.html')


if __name__ == "__main__":
    app.run(debug=True)
