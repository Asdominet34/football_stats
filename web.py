<<<<<<< HEAD
from flask import Flask, request, render_template
from stats import get_statistiche_giocatore, get_lista_giocatori, get_partite, get_classifica, get_statistiche_coppia

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.get("/giocatori")
def lista_giocatori():
    giocatori = get_lista_giocatori()
    return render_template("giocatori.html", giocatori=giocatori)

@app.get("/partite")
def lista_partite():
    partite = get_partite()
    return render_template("partite.html", partite=partite)

@app.get("/giocatore")
def giocatore():
    nome = request.args.get("nome")
    stats = get_statistiche_giocatore(nome) if nome else None
    return render_template("giocatore.html", stats=stats)

@app.route("/classifiche")
def menu_classifiche():
    return render_template("menu_classifiche.html")

@app.route("/classifiche/<tipo>")
def classifiche(tipo):
    titolo, classifica = get_classifica(tipo)
    return render_template("classifica_singola.html", titolo=titolo, classifica=classifica, tipo=tipo)

@app.route("/coppia", methods=["GET"])
def coppia():
    g1 = request.args.get("g1")
    g2 = request.args.get("g2")

    giocatori = get_lista_giocatori()  # lista per i menu a tendina

    stats = None
    if g1 and g2:
        stats = get_statistiche_coppia(g1, g2)

    return render_template("coppia.html", giocatori=giocatori, stats=stats, g1=g1, g2=g2)

if __name__ == "__main__":
    app.run(debug=True)

=======
from flask import Flask, request, render_template
from stats import get_statistiche_giocatore, get_lista_giocatori, get_partite, get_classifica, get_statistiche_coppia

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.get("/giocatori")
def lista_giocatori():
    giocatori = get_lista_giocatori()
    return render_template("giocatori.html", giocatori=giocatori)

@app.get("/partite")
def lista_partite():
    partite = get_partite()
    return render_template("partite.html", partite=partite)

@app.get("/giocatore")
def giocatore():
    nome = request.args.get("nome")
    stats = get_statistiche_giocatore(nome) if nome else None
    return render_template("giocatore.html", stats=stats)

@app.route("/classifiche")
def menu_classifiche():
    return render_template("menu_classifiche.html")

@app.route("/classifiche/<tipo>")
def classifiche(tipo):
    titolo, classifica = get_classifica(tipo)
    return render_template("classifica_singola.html", titolo=titolo, classifica=classifica, tipo=tipo)

@app.route("/coppia", methods=["GET"])
def coppia():
    g1 = request.args.get("g1")
    g2 = request.args.get("g2")

    giocatori = get_lista_giocatori()  # lista per i menu a tendina

    stats = None
    if g1 and g2:
        stats = get_statistiche_coppia(g1, g2)

    return render_template("coppia.html", giocatori=giocatori, stats=stats, g1=g1, g2=g2)

if __name__ == "__main__":
    app.run(debug=True)

>>>>>>> c1353a8311871b386ba7ca30ef8f226a832261cf
