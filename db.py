import sqlite3

DB_NAME = "calcetto_stats.db"

def crea_database():
    # Connessione al database (se non esiste, verrà creato)
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Creazione delle tabelle
    c.execute('''
    CREATE TABLE IF NOT EXISTS Partite (
        id_partita INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT NOT NULL,
        luogo TEXT NOT NULL,
        gol_squadra_chiari INTEGER,
        gol_squadra_scuri INTEGER
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS Giocatori (
        id_giocatore INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        gol_individuali INTEGER DEFAULT 0,
        gol_fatti_squadra INTEGER DEFAULT 0,
        gol_subiti_squadra INTEGER DEFAULT 0,
        partite_giocate INTEGER DEFAULT 0,
        partite_vinte INTEGER DEFAULT 0,
        partite_pareggiate INTEGER DEFAULT 0,
        partite_perse INTEGER DEFAULT 0,
        voto_pagella REAL DEFAULT 0,
        id_partita INTEGER,
        squadra TEXT NOT NULL,
        FOREIGN KEY (id_partita) REFERENCES Partite (id_partita)
    )
    ''')

    # Salva i cambiamenti e chiudi la connessione
    conn.commit()
    conn.close()
    print("Database creato con successo!")

def aggiungi_partita(data, luogo, composizione_squadra_chiari, composizione_squadra_scuri, gol_squadra_chiari, gol_squadra_scuri, gol_individuali, voti_pagella):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Inserire la partita
    c.execute('''
    INSERT INTO Partite (data, luogo, gol_squadra_chiari, gol_squadra_scuri)
    VALUES (?, ?, ?, ?)
    ''', (data, luogo, gol_squadra_chiari, gol_squadra_scuri))

    id_partita = c.lastrowid

    # Determinare risultato
    if gol_squadra_chiari > gol_squadra_scuri:
        risultato_squadra_chiari = "vinta"
        risultato_squadra_scuri = "persa"
    elif gol_squadra_chiari < gol_squadra_scuri:
        risultato_squadra_chiari = "persa"
        risultato_squadra_scuri = "vinta"
    else:
        risultato_squadra_chiari = risultato_squadra_scuri = "pareggiata"

    # Inserire i giocatori della squadra chiari
    for giocatore, gol, voto in zip(composizione_squadra_chiari, gol_individuali["squadra_chiari"], voti_pagella["squadra_chiari"]):
        c.execute('''
        INSERT INTO Giocatori (nome, gol_individuali, gol_fatti_squadra, gol_subiti_squadra, partite_giocate, partite_vinte, partite_pareggiate, partite_perse, voto_pagella, id_partita, squadra)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            giocatore, gol, gol_squadra_chiari, gol_squadra_scuri, 1, 1 if risultato_squadra_chiari == "vinta" else 0,
            1 if risultato_squadra_chiari == "pareggiata" else 0, 1 if risultato_squadra_chiari == "persa" else 0,
            voto, id_partita, "Chiari"
        ))

    # Inserire i giocatori della squadra scuri
    for giocatore, gol, voto in zip(composizione_squadra_scuri, gol_individuali["squadra_scuri"], voti_pagella["squadra_scuri"]):
        c.execute('''
        INSERT INTO Giocatori (nome, gol_individuali, gol_fatti_squadra, gol_subiti_squadra, partite_giocate, partite_vinte, partite_pareggiate, partite_perse, voto_pagella, id_partita, squadra)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            giocatore, gol, gol_squadra_scuri, gol_squadra_chiari, 1, 1 if risultato_squadra_scuri == "vinta" else 0,
            1 if risultato_squadra_scuri == "pareggiata" else 0, 1 if risultato_squadra_scuri == "persa" else 0,
            voto, id_partita, "Scuri"
        ))

    conn.commit()
    conn.close()
    print(f"Partita del {data} aggiunta con successo!")