<<<<<<< HEAD
from db import aggiungi_partita
from stats import mostra_statistiche


def inserisci_dati_da_terminale():
    print("Inserimento dati partita:")
    data = input("Data della partita (YYYY-MM-DD): ")
    luogo = input("Luogo della partita: ")
    gol_squadra_chiari = int(input("Gol squadra chiari: "))
    gol_squadra_scuri = int(input("Gol squadra scuri: "))
    
    # Chiedere il numero di giocatori per squadra
    num_giocatori = int(input("Quanti giocatori per squadra? "))
    
    print("Inserisci i giocatori della squadra chiari:")
    composizione_squadra_chiari = []
    gol_chiari = []
    voti_chiari = []
    for i in range(num_giocatori):
        nome = input(f"Nome giocatore {i+1}: ")
        composizione_squadra_chiari.append(nome)
        gol = int(input(f"Gol segnati da {nome}: "))
        gol_chiari.append(gol)
        voto = float(input(f"Voto in pagella di {nome} (0-10): "))
        voti_chiari.append(voto)

    print("Inserisci i giocatori della squadra scuri:")
    composizione_squadra_scuri = []
    gol_scuri = []
    voti_scuri = []
    for i in range(num_giocatori):
        nome = input(f"Nome giocatore {i+1}: ")
        composizione_squadra_scuri.append(nome)
        gol = int(input(f"Gol segnati da {nome}: "))
        gol_scuri.append(gol)
        voto = float(input(f"Voto in pagella di {nome} (0-10): "))
        voti_scuri.append(voto)

    gol_individuali = {
        "squadra_chiari": gol_chiari,
        "squadra_scuri": gol_scuri
    }

    voti_pagella = {
        "squadra_chiari": voti_chiari,
        "squadra_scuri": voti_scuri
    }

=======
from db import aggiungi_partita
from stats import mostra_statistiche


def inserisci_dati_da_terminale():
    print("Inserimento dati partita:")
    data = input("Data della partita (YYYY-MM-DD): ")
    luogo = input("Luogo della partita: ")
    gol_squadra_chiari = int(input("Gol squadra chiari: "))
    gol_squadra_scuri = int(input("Gol squadra scuri: "))
    
    # Chiedere il numero di giocatori per squadra
    num_giocatori = int(input("Quanti giocatori per squadra? "))
    
    print("Inserisci i giocatori della squadra chiari:")
    composizione_squadra_chiari = []
    gol_chiari = []
    voti_chiari = []
    for i in range(num_giocatori):
        nome = input(f"Nome giocatore {i+1}: ")
        composizione_squadra_chiari.append(nome)
        gol = int(input(f"Gol segnati da {nome}: "))
        gol_chiari.append(gol)
        voto = float(input(f"Voto in pagella di {nome} (0-10): "))
        voti_chiari.append(voto)

    print("Inserisci i giocatori della squadra scuri:")
    composizione_squadra_scuri = []
    gol_scuri = []
    voti_scuri = []
    for i in range(num_giocatori):
        nome = input(f"Nome giocatore {i+1}: ")
        composizione_squadra_scuri.append(nome)
        gol = int(input(f"Gol segnati da {nome}: "))
        gol_scuri.append(gol)
        voto = float(input(f"Voto in pagella di {nome} (0-10): "))
        voti_scuri.append(voto)

    gol_individuali = {
        "squadra_chiari": gol_chiari,
        "squadra_scuri": gol_scuri
    }

    voti_pagella = {
        "squadra_chiari": voti_chiari,
        "squadra_scuri": voti_scuri
    }

>>>>>>> c1353a8311871b386ba7ca30ef8f226a832261cf
    aggiungi_partita(data, luogo, composizione_squadra_chiari, composizione_squadra_scuri, gol_squadra_chiari, gol_squadra_scuri, gol_individuali, voti_pagella)