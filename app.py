from flask import Flask, render_template, request

app = Flask(__name__)

def evaluar_imc(imc):
    if imc < 18.5:
        return "Tienes bajo peso. Es recomendable evaluar tu alimentación.", "alert-warning"
    elif 18.5 <= imc < 25:
        return "Tu peso es saludable. ¡Buen trabajo!", "alert-success"
    elif 25 <= imc < 30:
        return "Tienes sobrepeso. Considera mejorar hábitos de alimentación.", "alert-warning"
    else:
        return "Tienes obesidad. Es recomendable acudir con un profesional de la salud.", "alert-danger"

@app.route("/", methods=["GET", "POST"])
def index():
    imc_resultado = None
    mensaje = None
    color = None

    if request.method == "POST":
        try:
            peso = float(request.form["peso"])
            altura_cm = float(request.form["altura"])
            altura = altura_cm / 100  # convertir cm a metros

            imc = peso / (altura ** 2)
            imc = round(imc, 2)

            mensaje, color = evaluar_imc(imc)
            imc_resultado = imc

        except:
            imc_resultado = None

    return render_template("index.html", imc_resultado=imc_resultado, mensaje=mensaje, color=color)

if __name__ == "__main__":
    app.run(debug=True)
