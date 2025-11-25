from flask import Flask, render_template, request

app = Flask(__name__)

# Factores de actividad
ACTIVITY_LEVELS = {
    "sedentario": 1.2,
    "ligero": 1.375,
    "moderado": 1.55,
    "intenso": 1.725,
    "muy_intenso": 1.9
}

# Ajustes por objetivo
OBJETIVOS = {
    "perder": 0.85,
    "mantener": 1.0,
    "ganar": 1.10
}

# Macros recomendados (%) según objetivo
MACROS_RECOMENDADOS = {
    "perder": {"proteina": 30, "carbo": 40, "grasa": 30},
    "mantener": {"proteina": 25, "carbo": 50, "grasa": 25},
    "ganar": {"proteina": 20, "carbo": 55, "grasa": 25}
}

# Consumo diario recomendado (g/día)
CONSUMO_RECOMENDADO = {
    "carbohidratos": (280, 405),
    "proteinas": (62, 218),
    "grasas": (55, 97)
}

def calcular_tmb_mifflin(peso, altura, edad, sexo):
    return 10*peso + 6.25*altura - 5*edad + (5 if sexo=="hombre" else -161)

def calcular_tdee(tmb, actividad):
    return tmb * ACTIVITY_LEVELS.get(actividad, 1.2)

def ajustar_calorias(tdee, objetivo):
    return tdee * OBJETIVOS.get(objetivo, 1.0)

def calcular_macros(calorias, proteina_pct, carbo_pct, grasa_pct):
    return (round(calorias*proteina_pct/100/4,1),
            round(calorias*carbo_pct/100/4,1),
            round(calorias*grasa_pct/100/9,1))

def evaluar_estado(proteina_pct, carbo_pct, grasa_pct):
    mensajes = []
    color = "alert-success"
    if proteina_pct < 15:
        mensajes.append("Proteína baja: posible fatiga o pérdida muscular.")
        color = "alert-warning"
    if carbo_pct < 30:
        mensajes.append("Carbohidratos bajos: poca energía para actividad intensa.")
        color = "alert-warning"
    if grasa_pct < 20:
        mensajes.append("Grasas bajas: puede afectar hormonas y energía.")
        color = "alert-warning"
    if not mensajes:
        mensajes.append("¡Macros equilibrados! Excelente trabajo.")
    return color, " ".join(mensajes)

@app.route("/", methods=["GET","POST"])
def index():
    resultado = None
    mensaje = None
    color = None
    valores = {
        "sexo": None, "edad": None, "peso": None, "altura": None,
        "actividad": None, "objetivo": None
    }

    if request.method=="POST":
        try:
            sexo = request.form["sexo"]
            edad = int(request.form["edad"])
            peso = float(request.form["peso"])
            altura = float(request.form["altura"])
            actividad = request.form["actividad"]
            objetivo = request.form["objetivo"]

            valores.update({
                "sexo": sexo, "edad": edad, "peso": peso, "altura": altura,
                "actividad": actividad, "objetivo": objetivo
            })

            tmb = calcular_tmb_mifflin(peso, altura, edad, sexo)
            tdee = calcular_tdee(tmb, actividad)
            calorias = ajustar_calorias(tdee, objetivo)

            macros_pct = MACROS_RECOMENDADOS[objetivo]
            proteina_pct = macros_pct["proteina"]
            carbo_pct = macros_pct["carbo"]
            grasa_pct = macros_pct["grasa"]

            color, mensaje = evaluar_estado(proteina_pct, carbo_pct, grasa_pct)

            proteina_g, carbo_g, grasa_g = calcular_macros(calorias, proteina_pct, carbo_pct, grasa_pct)
            resultado = {
                "tmb_mifflin": round(tmb,1),
                "tdee": round(tdee,1),
                "calorias_ajustadas": round(calorias,1),
                "proteina_g": proteina_g,
                "carbo_g": carbo_g,
                "grasa_g": grasa_g,
                "proteina_pct": proteina_pct,
                "carbo_pct": carbo_pct,
                "grasa_pct": grasa_pct
            }

        except:
            color = "alert-danger"
            mensaje = "Error en los datos ingresados, verifica e intenta de nuevo."

    return render_template("index.html",
                        resultado=resultado,
                        mensaje=mensaje,
                        color=color,
                        valores=valores,
                        consumo_recomendado=CONSUMO_RECOMENDADO)

if __name__=="__main__":
    app.run(debug=True)
