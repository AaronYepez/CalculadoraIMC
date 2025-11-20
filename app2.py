from flask import Flask, render_template, request

app = Flask(__name__)

def calcular_pci(altura_cm, sexo):
    altura_in = altura_cm / 2.54  # Convertir cm a pulgadas
    if sexo == "hombre":
        peso_ideal = 50 + 2.3 * (altura_in - 60)
    else:  # mujer
        peso_ideal = 45.5 + 2.3 * (altura_in - 60)
    return round(peso_ideal, 2)

@app.route("/", methods=["GET", "POST"])
def pci():
    peso_ideal = None
    if request.method == "POST":
        try:
            altura_cm = float(request.form["altura"])
            sexo = request.form["sexo"]
            peso_ideal = calcular_pci(altura_cm, sexo)
        except:
            peso_ideal = None
    return render_template("index.html", peso_ideal=peso_ideal)
    
if __name__ == "__main__":
    app.run(debug=True)
