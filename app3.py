from flask import Flask, render_template, request

app = Flask(__name__)

def calcular_macros(calorias, proteina_pct, carbo_pct, grasa_pct):
    # Calorías por gramo
    CAL_PROTEINA = 4
    CAL_CARBO = 4
    CAL_GRASA = 9

    proteina_g = round(calorias * proteina_pct / 100 / CAL_PROTEINA, 1)
    carbo_g = round(calorias * carbo_pct / 100 / CAL_CARBO, 1)
    grasa_g = round(calorias * grasa_pct / 100 / CAL_GRASA, 1)

    return proteina_g, carbo_g, grasa_g

@app.route("/", methods=["GET", "POST"])
def macros():
    resultado = None
    if request.method == "POST":
        try:
            calorias = float(request.form["calorias"])
            proteina_pct = float(request.form["proteina_pct"])
            carbo_pct = float(request.form["carbo_pct"])
            grasa_pct = float(request.form["grasa_pct"])

            resultado = calcular_macros(calorias, proteina_pct, carbo_pct, grasa_pct)
        except:
            resultado = None

    return render_template("index.html", resultado=resultado)

if __name__ == "__main__":
    app.run(debug=True)
