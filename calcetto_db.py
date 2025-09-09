<<<<<<< HEAD
import sqlite3

def crea_database():
    # Connessione al database (se non esiste, verrà creato)
    conn = sqlite3.connect("calcetto_stats.db")
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
    conn = sqlite3.connect("calcetto_stats.db")
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

    aggiungi_partita(data, luogo, composizione_squadra_chiari, composizione_squadra_scuri, gol_squadra_chiari, gol_squadra_scuri, gol_individuali, voti_pagella)

def mostra_statistiche():
    conn = sqlite3.connect("calcetto_stats.db")
    c = conn.cursor()

    while True:
        print("\nOpzioni statistiche:")
        print("1. Mostra statistiche di un giocatore")
        print("2. Mostra tutte le partite registrate")
        print("3. Mostra statistiche di coppia")
        print("4. Mostra classifiche")
        print("5. Esci")
        scelta = input("Scegli un'opzione (1/2/3/4/5): ")

        if scelta == "1":
            nome_giocatore = input("Inserisci il nome del giocatore: ")

            # Ottenere il numero totale di partite
            c.execute('SELECT COUNT(*) FROM Partite')
            totale_partite = c.fetchone()[0]

            if totale_partite == 0:
                print("Non ci sono partite registrate.")
            else:
                # Recuperare le statistiche del giocatore selezionato
                c.execute('''
                SELECT nome, 
                       SUM(gol_individuali), 
                       SUM(partite_giocate), 
                       SUM(partite_vinte), 
                       SUM(partite_pareggiate), 
                       SUM(partite_perse), 
                       AVG(voto_pagella), 
                       AVG(gol_individuali), 
                       AVG(gol_fatti_squadra),
                       AVG(gol_subiti_squadra),
                       CAST(SUM(partite_vinte) AS REAL) / SUM(partite_giocate) * 100 AS percentuale_vittorie
                FROM Giocatori
                WHERE nome = ?
                GROUP BY nome
                ''', (nome_giocatore,))
                risultato = c.fetchone()

                if risultato:
                    # Filtrare i giocatori con almeno il 50% delle partite giocate
                    c.execute('''
                    SELECT nome, 
                           SUM(gol_individuali) AS gol_individuali, 
                           SUM(partite_giocate) AS partite_giocate, 
                           SUM(partite_vinte) AS partite_vinte, 
                           SUM(partite_pareggiate) AS partite_pareggiate, 
                           SUM(partite_perse) AS partite_perse, 
                           AVG(voto_pagella) AS voto_pagella, 
                           AVG(gol_individuali) AS media_gol, 
                           AVG(gol_fatti_squadra) AS media_gol_fatti_squadra,
                           AVG(gol_subiti_squadra) AS media_gol_subiti_squadra,
                           CAST(SUM(partite_vinte) AS REAL) / SUM(partite_giocate) * 100 AS percentuale_vittorie
                    FROM Giocatori
                    GROUP BY nome
                    HAVING SUM(partite_giocate) >= ?
                    ''', (totale_partite / 2,))
                    giocatori_valide = c.fetchall()
                    # Stampare solo i nomi dei giocatori
                    nomi_giocatori = [giocatore[0] for giocatore in giocatori_valide]
                    # Stampare la lunghezza della lista
                    print("Numero totale di giocatori con almeno 50 percento delle partite giocate:", len(giocatori_valide))
                    print("Nomi giocatori:", nomi_giocatori)

                    # Ordinare i giocatori per ciascuna statistica
                    ranking_gol = sorted(giocatori_valide, key=lambda x: x[1], reverse=True)
                    ranking_partite_giocate = sorted(giocatori_valide, key=lambda x: x[2], reverse=True)
                    ranking_vinte = sorted(giocatori_valide, key=lambda x: x[3], reverse=True)
                    ranking_voto = sorted(giocatori_valide, key=lambda x: x[6], reverse=True)
                    ranking_media_gol = sorted(giocatori_valide, key=lambda x: x[7], reverse=True)
                    ranking_percentuale = sorted(giocatori_valide, key=lambda x: x[10], reverse=True)
                    ranking_media_gol_fatti_squadra = sorted(giocatori_valide, key=lambda x: x[8], reverse=True)
                    ranking_media_gol_subiti_squadra = sorted(giocatori_valide, key=lambda x: x[9], reverse=True)

                    # Funzione per trovare la posizione di un giocatore
                    def trova_posizione(nome, ranking):
                        for posizione, giocatore in enumerate(ranking, start=1):
                            if giocatore[0] == nome:
                                return posizione
                        return "-"

                    # Calcolare le posizioni del giocatore selezionato
                    posizione_gol = trova_posizione(nome_giocatore, ranking_gol)
                    posizione_partite_giocate = trova_posizione(nome_giocatore, ranking_partite_giocate)
                    posizione_vinte = trova_posizione(nome_giocatore, ranking_vinte)
                    posizione_voto = trova_posizione(nome_giocatore, ranking_voto)
                    posizione_media_gol = trova_posizione(nome_giocatore, ranking_media_gol)
                    posizione_percentuale = trova_posizione(nome_giocatore, ranking_percentuale)
                    posizione_media_gol_fatti_squadra = trova_posizione(nome_giocatore, ranking_media_gol_fatti_squadra)
                    posizione_media_gol_subiti_squadra = trova_posizione(nome_giocatore, ranking_media_gol_subiti_squadra)
                    

                    # Stampare le statistiche con il ranking
                    print(f"\nStatistiche di {risultato[0]}, ranking tra i giocatori con almeno 50 percento delle partite giocate:")
                    print(f"Gol individuali: {risultato[1]} ({posizione_gol}°)")
                    print(f"Partite giocate: {risultato[2]} ({posizione_partite_giocate}°)")
                    print(f"Partite vinte: {risultato[3]} ({posizione_vinte}°)")
                    print(f"Partite pareggiate: {risultato[4]}")
                    print(f"Partite perse: {risultato[5]}")
                    print(f"Media voto in pagella: {risultato[6]:.2f} ({posizione_voto}°)")
                    print(f"Media gol segnati: {risultato[7]:.2f} ({posizione_media_gol}°)")
                    print(f"Percentuale partite vinte: {risultato[10]:.2f}% ({posizione_percentuale}°)")
                    print(f"Media gol segnati dalla sua squadra: {risultato[8]:.2f} ({posizione_media_gol_fatti_squadra}°)")
                    print(f"Media gol subiti dalla sua squadra: {risultato[9]:.2f} ({posizione_media_gol_subiti_squadra}°)")
                    
                else:
                    print("Giocatore non trovato.")

        elif scelta == "2":
            c.execute('SELECT * FROM Partite')
            partite = c.fetchall()
            if partite:
                print("\nPartite registrate:")
                for partita in partite:
                    print(f"ID: {partita[0]}, Data: {partita[1]}, Luogo: {partita[2]}, "
                          f"Gol squadra chiari: {partita[3]}, Gol squadra scuri: {partita[4]}")
            else:
                print("Non ci sono partite registrate.")

        elif scelta == "3":
           # Statistiche di coppia
           nome_giocatore1 = input("Inserisci il nome del primo giocatore: ")
           nome_giocatore2 = input("Inserisci il nome del secondo giocatore: ")
    
           # Trova partite giocate insieme nella stessa squadra
           c.execute('''
           SELECT COUNT(*) 
           FROM Giocatori AS g1
           JOIN Giocatori AS g2 
           ON g1.id_partita = g2.id_partita AND g1.squadra = g2.squadra
           WHERE g1.nome = ? AND g2.nome = ?
           ''', (nome_giocatore1, nome_giocatore2))
           partite_insieme = c.fetchone()[0]

           if partite_insieme == 0:
            print(f"{nome_giocatore1} e {nome_giocatore2} non hanno giocato insieme.")
           else:
             # Percentuale di vittorie insieme
             c.execute('''
             SELECT COUNT(*) 
             FROM Giocatori AS g1
             JOIN Giocatori AS g2 ON g1.id_partita = g2.id_partita
             WHERE g1.nome = ? AND g2.nome = ? AND g1.squadra = g2.squadra AND g1.partite_vinte = 1
             ''', (nome_giocatore1, nome_giocatore2))
             vittorie_insieme = c.fetchone()[0]
             percentuale_vittorie_insieme = (vittorie_insieme / partite_insieme) * 100

             # Gol segnati individualmente giocando insieme nella stessa squadra
             c.execute('''
             SELECT AVG(g1.gol_individuali), AVG(g2.gol_individuali)
             FROM Giocatori AS g1
             JOIN Giocatori AS g2 
             ON g1.id_partita = g2.id_partita AND g1.squadra = g2.squadra
             WHERE g1.nome = ? AND g2.nome = ?
             ''', (nome_giocatore1, nome_giocatore2))
             media_gol_insieme = c.fetchone()
             media_gol_insieme = (round(media_gol_insieme[0], 2), round(media_gol_insieme[1], 2))


             # Statistiche individuali nelle partite in cui NON hanno giocato insieme
             c.execute('''
             SELECT 
              CAST(SUM(partite_vinte) AS REAL) / SUM(partite_giocate) * 100 AS percentuale_vittorie,
              AVG(gol_individuali)
            FROM Giocatori
            WHERE nome = ? 
            AND id_partita NOT IN (
                SELECT DISTINCT g1.id_partita
                FROM Giocatori AS g1
                JOIN Giocatori AS g2 
                ON g1.id_partita = g2.id_partita AND g1.squadra = g2.squadra
                WHERE g1.nome = ? AND g2.nome = ?
             )
             ''', (nome_giocatore1, nome_giocatore1, nome_giocatore2))
             stats_no_insieme1 = c.fetchone()
             if stats_no_insieme1 is None or stats_no_insieme1[0] is None or stats_no_insieme1[1] is None:
              stats_no_insieme1 = (0.0, 0.0)
             else:
              stats_no_insieme1 = (round(stats_no_insieme1[0], 2), round(stats_no_insieme1[1], 2))

             c.execute('''
             SELECT 
              CAST(SUM(partite_vinte) AS REAL) / SUM(partite_giocate) * 100 AS percentuale_vittorie,
              AVG(gol_individuali)
            FROM Giocatori
            WHERE nome = ? 
            AND id_partita NOT IN (
              SELECT DISTINCT g1.id_partita
              FROM Giocatori AS g1
              JOIN Giocatori AS g2 
              ON g1.id_partita = g2.id_partita AND g1.squadra = g2.squadra
              WHERE g1.nome = ? AND g2.nome = ?
             )
             ''', (nome_giocatore2, nome_giocatore2, nome_giocatore1))
             stats_no_insieme2 = c.fetchone()
             if stats_no_insieme2 is None or stats_no_insieme2[0] is None or stats_no_insieme2[1] is None:
              stats_no_insieme2 = (0.0, 0.0)
             else:
              stats_no_insieme2 = (round(stats_no_insieme2[0], 2), round(stats_no_insieme2[1], 2))


             percentuale_vittorie_senza1 = f"{stats_no_insieme1[0]:.2f}%"
             percentuale_vittorie_senza2 = f"{stats_no_insieme2[0]:.2f}%"
             media_gol_senza1 = f"{stats_no_insieme1[1]:.2f}"
             media_gol_senza2 = f"{stats_no_insieme2[1]:.2f}"

             # Stampa i risultati con i valori 0.0 di default
             print(f"\nStatistiche di coppia tra {nome_giocatore1} e {nome_giocatore2}:")
             print(f"Partite giocate insieme: {partite_insieme}")
             print(f"Percentuale partite vinte insieme: {percentuale_vittorie_insieme:.2f}% "
                  f"({percentuale_vittorie_senza1} per {nome_giocatore1} senza {nome_giocatore2}, "
                  f"{percentuale_vittorie_senza2} per {nome_giocatore2} senza {nome_giocatore1})")
             print(f"Media Gol segnati da {nome_giocatore1} giocando con {nome_giocatore2}: {media_gol_insieme[0]:.2f} "
                  f"({media_gol_senza1} senza {nome_giocatore2})")
             print(f"Media Gol segnati da {nome_giocatore2} giocando con {nome_giocatore1}: {media_gol_insieme[1]:.2f} "
                  f"({media_gol_senza2} senza {nome_giocatore1})")

        elif scelta == "4":
            print("\nSeleziona la classifica che desideri visualizzare:")
            print("1. Gol individuali")
            print("2. Partite giocate")
            print("3. Partite vinte")
            print("4. Partite perse")
            print("5. Media voto")
            
            scelta_classifica = input("Scegli un'opzione (1/2/3/4/5): ")

            # Verifica il numero totale di partite per calcolare il 50%
            c.execute('SELECT COUNT(*) FROM Partite')
            totale_partite = c.fetchone()[0]

            if totale_partite == 0:
                print("Non ci sono partite registrate.")
            else:
                # Query base per ottenere tutti i giocatori
                query_tutti = '''
                SELECT nome, 
                       SUM(gol_individuali) AS gol_individuali, 
                       SUM(partite_giocate) AS partite_giocate, 
                       SUM(partite_vinte) AS partite_vinte, 
                       SUM(partite_perse) AS partite_perse, 
                       AVG(voto_pagella) AS media_voto
                FROM Giocatori
                GROUP BY nome
                '''

                c.execute(query_tutti)
                tutti_giocatori = c.fetchall()

                # Query per ottenere solo i giocatori con almeno il 50% delle partite giocate (per la media voto)
                query_50_percento = '''
                SELECT nome, 
                       SUM(gol_individuali) AS gol_individuali, 
                       SUM(partite_giocate) AS partite_giocate, 
                       SUM(partite_vinte) AS partite_vinte, 
                       SUM(partite_perse) AS partite_perse, 
                       AVG(voto_pagella) AS media_voto
                FROM Giocatori
                GROUP BY nome
                HAVING SUM(partite_giocate) >= ?
                '''

                c.execute(query_50_percento, (totale_partite / 2,))
                giocatori_50_percento = c.fetchall()

                # Dizionario per associare la scelta alla colonna corrispondente
                opzioni_classifica = {
                    "1": (1, "Gol individuali", tutti_giocatori),
                    "2": (2, "Partite giocate", tutti_giocatori),
                    "3": (3, "Partite vinte", tutti_giocatori),
                    "4": (4, "Partite perse", tutti_giocatori),
                    "5": (5, "Media voto", giocatori_50_percento)
                }

                if scelta_classifica in opzioni_classifica:
                    colonna_index, nome_statistica, dataset = opzioni_classifica[scelta_classifica]

                    # Se la classifica riguarda la media voto, mostra il messaggio di avviso
                    if scelta_classifica == "5":
                        print("\n Classifica basata solo sui giocatori con almeno il 50 percento delle partite giocate.")

                    if not dataset:
                        print(f"Nessun giocatore disponibile per la classifica {nome_statistica}.")
                    else:
                        classifica = sorted(dataset, key=lambda x: x[colonna_index], reverse=True)

                        print(f"\nClassifica per {nome_statistica}:")
                        for posizione, giocatore in enumerate(classifica, start=1):
                            # Se è la classifica della media voto, mostra con 2 decimali, altrimenti senza decimali
                            valore = f"{giocatore[colonna_index]:.2f}" if scelta_classifica == "5" else f"{str(int(giocatore[colonna_index]))}"
                            print(f"{posizione}. {giocatore[0]} - {valore}")

                else:
                    print("Opzione non valida. Riprova.")


        elif scelta == "5":
          print("Uscita dal menu delle statistiche.")
          break
        else:
         print("Opzione non valida. Riprova.")
    conn.close()

if __name__ == "__main__":
    conn = sqlite3.connect("calcetto_stats.db")
    c = conn.cursor()
    
    while True:
        print("\nMenu principale:")
        print("1. Inserisci una nuova partita")
        print("2. Mostra statistiche")
        print("3. Mostra tutti i giocatori")
        print("4. Esci")
        scelta = input("Scegli un'opzione (1/2/3/4): ")

        if scelta == "1":
            inserisci_dati_da_terminale()
        elif scelta == "2":
            mostra_statistiche()
        elif scelta == "3":
            c.execute("SELECT DISTINCT nome FROM Giocatori")
            giocatori = c.fetchall()
            print("\nLista giocatori registrati:")
            for giocatore in giocatori:
                print(giocatore[0])
        elif scelta == "4":
            print("Uscita dal programma. Alla prossima!")
            break
        else:
            print("Opzione non valida. Riprova.")
    
    conn.close()

=======
import sqlite3

def crea_database():
    # Connessione al database (se non esiste, verrà creato)
    conn = sqlite3.connect("calcetto_stats.db")
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
    conn = sqlite3.connect("calcetto_stats.db")
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

    aggiungi_partita(data, luogo, composizione_squadra_chiari, composizione_squadra_scuri, gol_squadra_chiari, gol_squadra_scuri, gol_individuali, voti_pagella)

def mostra_statistiche():
    conn = sqlite3.connect("calcetto_stats.db")
    c = conn.cursor()

    while True:
        print("\nOpzioni statistiche:")
        print("1. Mostra statistiche di un giocatore")
        print("2. Mostra tutte le partite registrate")
        print("3. Mostra statistiche di coppia")
        print("4. Mostra classifiche")
        print("5. Esci")
        scelta = input("Scegli un'opzione (1/2/3/4/5): ")

        if scelta == "1":
            nome_giocatore = input("Inserisci il nome del giocatore: ")

            # Ottenere il numero totale di partite
            c.execute('SELECT COUNT(*) FROM Partite')
            totale_partite = c.fetchone()[0]

            if totale_partite == 0:
                print("Non ci sono partite registrate.")
            else:
                # Recuperare le statistiche del giocatore selezionato
                c.execute('''
                SELECT nome, 
                       SUM(gol_individuali), 
                       SUM(partite_giocate), 
                       SUM(partite_vinte), 
                       SUM(partite_pareggiate), 
                       SUM(partite_perse), 
                       AVG(voto_pagella), 
                       AVG(gol_individuali), 
                       AVG(gol_fatti_squadra),
                       AVG(gol_subiti_squadra),
                       CAST(SUM(partite_vinte) AS REAL) / SUM(partite_giocate) * 100 AS percentuale_vittorie
                FROM Giocatori
                WHERE nome = ?
                GROUP BY nome
                ''', (nome_giocatore,))
                risultato = c.fetchone()

                if risultato:
                    # Filtrare i giocatori con almeno il 50% delle partite giocate
                    c.execute('''
                    SELECT nome, 
                           SUM(gol_individuali) AS gol_individuali, 
                           SUM(partite_giocate) AS partite_giocate, 
                           SUM(partite_vinte) AS partite_vinte, 
                           SUM(partite_pareggiate) AS partite_pareggiate, 
                           SUM(partite_perse) AS partite_perse, 
                           AVG(voto_pagella) AS voto_pagella, 
                           AVG(gol_individuali) AS media_gol, 
                           AVG(gol_fatti_squadra) AS media_gol_fatti_squadra,
                           AVG(gol_subiti_squadra) AS media_gol_subiti_squadra,
                           CAST(SUM(partite_vinte) AS REAL) / SUM(partite_giocate) * 100 AS percentuale_vittorie
                    FROM Giocatori
                    GROUP BY nome
                    HAVING SUM(partite_giocate) >= ?
                    ''', (totale_partite / 2,))
                    giocatori_valide = c.fetchall()
                    # Stampare solo i nomi dei giocatori
                    nomi_giocatori = [giocatore[0] for giocatore in giocatori_valide]
                    # Stampare la lunghezza della lista
                    print("Numero totale di giocatori con almeno 50 percento delle partite giocate:", len(giocatori_valide))
                    print("Nomi giocatori:", nomi_giocatori)

                    # Ordinare i giocatori per ciascuna statistica
                    ranking_gol = sorted(giocatori_valide, key=lambda x: x[1], reverse=True)
                    ranking_partite_giocate = sorted(giocatori_valide, key=lambda x: x[2], reverse=True)
                    ranking_vinte = sorted(giocatori_valide, key=lambda x: x[3], reverse=True)
                    ranking_voto = sorted(giocatori_valide, key=lambda x: x[6], reverse=True)
                    ranking_media_gol = sorted(giocatori_valide, key=lambda x: x[7], reverse=True)
                    ranking_percentuale = sorted(giocatori_valide, key=lambda x: x[10], reverse=True)
                    ranking_media_gol_fatti_squadra = sorted(giocatori_valide, key=lambda x: x[8], reverse=True)
                    ranking_media_gol_subiti_squadra = sorted(giocatori_valide, key=lambda x: x[9], reverse=True)

                    # Funzione per trovare la posizione di un giocatore
                    def trova_posizione(nome, ranking):
                        for posizione, giocatore in enumerate(ranking, start=1):
                            if giocatore[0] == nome:
                                return posizione
                        return "-"

                    # Calcolare le posizioni del giocatore selezionato
                    posizione_gol = trova_posizione(nome_giocatore, ranking_gol)
                    posizione_partite_giocate = trova_posizione(nome_giocatore, ranking_partite_giocate)
                    posizione_vinte = trova_posizione(nome_giocatore, ranking_vinte)
                    posizione_voto = trova_posizione(nome_giocatore, ranking_voto)
                    posizione_media_gol = trova_posizione(nome_giocatore, ranking_media_gol)
                    posizione_percentuale = trova_posizione(nome_giocatore, ranking_percentuale)
                    posizione_media_gol_fatti_squadra = trova_posizione(nome_giocatore, ranking_media_gol_fatti_squadra)
                    posizione_media_gol_subiti_squadra = trova_posizione(nome_giocatore, ranking_media_gol_subiti_squadra)
                    

                    # Stampare le statistiche con il ranking
                    print(f"\nStatistiche di {risultato[0]}, ranking tra i giocatori con almeno 50 percento delle partite giocate:")
                    print(f"Gol individuali: {risultato[1]} ({posizione_gol}°)")
                    print(f"Partite giocate: {risultato[2]} ({posizione_partite_giocate}°)")
                    print(f"Partite vinte: {risultato[3]} ({posizione_vinte}°)")
                    print(f"Partite pareggiate: {risultato[4]}")
                    print(f"Partite perse: {risultato[5]}")
                    print(f"Media voto in pagella: {risultato[6]:.2f} ({posizione_voto}°)")
                    print(f"Media gol segnati: {risultato[7]:.2f} ({posizione_media_gol}°)")
                    print(f"Percentuale partite vinte: {risultato[10]:.2f}% ({posizione_percentuale}°)")
                    print(f"Media gol segnati dalla sua squadra: {risultato[8]:.2f} ({posizione_media_gol_fatti_squadra}°)")
                    print(f"Media gol subiti dalla sua squadra: {risultato[9]:.2f} ({posizione_media_gol_subiti_squadra}°)")
                    
                else:
                    print("Giocatore non trovato.")

        elif scelta == "2":
            c.execute('SELECT * FROM Partite')
            partite = c.fetchall()
            if partite:
                print("\nPartite registrate:")
                for partita in partite:
                    print(f"ID: {partita[0]}, Data: {partita[1]}, Luogo: {partita[2]}, "
                          f"Gol squadra chiari: {partita[3]}, Gol squadra scuri: {partita[4]}")
            else:
                print("Non ci sono partite registrate.")

        elif scelta == "3":
           # Statistiche di coppia
           nome_giocatore1 = input("Inserisci il nome del primo giocatore: ")
           nome_giocatore2 = input("Inserisci il nome del secondo giocatore: ")
    
           # Trova partite giocate insieme nella stessa squadra
           c.execute('''
           SELECT COUNT(*) 
           FROM Giocatori AS g1
           JOIN Giocatori AS g2 
           ON g1.id_partita = g2.id_partita AND g1.squadra = g2.squadra
           WHERE g1.nome = ? AND g2.nome = ?
           ''', (nome_giocatore1, nome_giocatore2))
           partite_insieme = c.fetchone()[0]

           if partite_insieme == 0:
            print(f"{nome_giocatore1} e {nome_giocatore2} non hanno giocato insieme.")
           else:
             # Percentuale di vittorie insieme
             c.execute('''
             SELECT COUNT(*) 
             FROM Giocatori AS g1
             JOIN Giocatori AS g2 ON g1.id_partita = g2.id_partita
             WHERE g1.nome = ? AND g2.nome = ? AND g1.squadra = g2.squadra AND g1.partite_vinte = 1
             ''', (nome_giocatore1, nome_giocatore2))
             vittorie_insieme = c.fetchone()[0]
             percentuale_vittorie_insieme = (vittorie_insieme / partite_insieme) * 100

             # Gol segnati individualmente giocando insieme nella stessa squadra
             c.execute('''
             SELECT AVG(g1.gol_individuali), AVG(g2.gol_individuali)
             FROM Giocatori AS g1
             JOIN Giocatori AS g2 
             ON g1.id_partita = g2.id_partita AND g1.squadra = g2.squadra
             WHERE g1.nome = ? AND g2.nome = ?
             ''', (nome_giocatore1, nome_giocatore2))
             media_gol_insieme = c.fetchone()
             media_gol_insieme = (round(media_gol_insieme[0], 2), round(media_gol_insieme[1], 2))


             # Statistiche individuali nelle partite in cui NON hanno giocato insieme
             c.execute('''
             SELECT 
              CAST(SUM(partite_vinte) AS REAL) / SUM(partite_giocate) * 100 AS percentuale_vittorie,
              AVG(gol_individuali)
            FROM Giocatori
            WHERE nome = ? 
            AND id_partita NOT IN (
                SELECT DISTINCT g1.id_partita
                FROM Giocatori AS g1
                JOIN Giocatori AS g2 
                ON g1.id_partita = g2.id_partita AND g1.squadra = g2.squadra
                WHERE g1.nome = ? AND g2.nome = ?
             )
             ''', (nome_giocatore1, nome_giocatore1, nome_giocatore2))
             stats_no_insieme1 = c.fetchone()
             if stats_no_insieme1 is None or stats_no_insieme1[0] is None or stats_no_insieme1[1] is None:
              stats_no_insieme1 = (0.0, 0.0)
             else:
              stats_no_insieme1 = (round(stats_no_insieme1[0], 2), round(stats_no_insieme1[1], 2))

             c.execute('''
             SELECT 
              CAST(SUM(partite_vinte) AS REAL) / SUM(partite_giocate) * 100 AS percentuale_vittorie,
              AVG(gol_individuali)
            FROM Giocatori
            WHERE nome = ? 
            AND id_partita NOT IN (
              SELECT DISTINCT g1.id_partita
              FROM Giocatori AS g1
              JOIN Giocatori AS g2 
              ON g1.id_partita = g2.id_partita AND g1.squadra = g2.squadra
              WHERE g1.nome = ? AND g2.nome = ?
             )
             ''', (nome_giocatore2, nome_giocatore2, nome_giocatore1))
             stats_no_insieme2 = c.fetchone()
             if stats_no_insieme2 is None or stats_no_insieme2[0] is None or stats_no_insieme2[1] is None:
              stats_no_insieme2 = (0.0, 0.0)
             else:
              stats_no_insieme2 = (round(stats_no_insieme2[0], 2), round(stats_no_insieme2[1], 2))


             percentuale_vittorie_senza1 = f"{stats_no_insieme1[0]:.2f}%"
             percentuale_vittorie_senza2 = f"{stats_no_insieme2[0]:.2f}%"
             media_gol_senza1 = f"{stats_no_insieme1[1]:.2f}"
             media_gol_senza2 = f"{stats_no_insieme2[1]:.2f}"

             # Stampa i risultati con i valori 0.0 di default
             print(f"\nStatistiche di coppia tra {nome_giocatore1} e {nome_giocatore2}:")
             print(f"Partite giocate insieme: {partite_insieme}")
             print(f"Percentuale partite vinte insieme: {percentuale_vittorie_insieme:.2f}% "
                  f"({percentuale_vittorie_senza1} per {nome_giocatore1} senza {nome_giocatore2}, "
                  f"{percentuale_vittorie_senza2} per {nome_giocatore2} senza {nome_giocatore1})")
             print(f"Media Gol segnati da {nome_giocatore1} giocando con {nome_giocatore2}: {media_gol_insieme[0]:.2f} "
                  f"({media_gol_senza1} senza {nome_giocatore2})")
             print(f"Media Gol segnati da {nome_giocatore2} giocando con {nome_giocatore1}: {media_gol_insieme[1]:.2f} "
                  f"({media_gol_senza2} senza {nome_giocatore1})")

        elif scelta == "4":
            print("\nSeleziona la classifica che desideri visualizzare:")
            print("1. Gol individuali")
            print("2. Partite giocate")
            print("3. Partite vinte")
            print("4. Partite perse")
            print("5. Media voto")
            
            scelta_classifica = input("Scegli un'opzione (1/2/3/4/5): ")

            # Verifica il numero totale di partite per calcolare il 50%
            c.execute('SELECT COUNT(*) FROM Partite')
            totale_partite = c.fetchone()[0]

            if totale_partite == 0:
                print("Non ci sono partite registrate.")
            else:
                # Query base per ottenere tutti i giocatori
                query_tutti = '''
                SELECT nome, 
                       SUM(gol_individuali) AS gol_individuali, 
                       SUM(partite_giocate) AS partite_giocate, 
                       SUM(partite_vinte) AS partite_vinte, 
                       SUM(partite_perse) AS partite_perse, 
                       AVG(voto_pagella) AS media_voto
                FROM Giocatori
                GROUP BY nome
                '''

                c.execute(query_tutti)
                tutti_giocatori = c.fetchall()

                # Query per ottenere solo i giocatori con almeno il 50% delle partite giocate (per la media voto)
                query_50_percento = '''
                SELECT nome, 
                       SUM(gol_individuali) AS gol_individuali, 
                       SUM(partite_giocate) AS partite_giocate, 
                       SUM(partite_vinte) AS partite_vinte, 
                       SUM(partite_perse) AS partite_perse, 
                       AVG(voto_pagella) AS media_voto
                FROM Giocatori
                GROUP BY nome
                HAVING SUM(partite_giocate) >= ?
                '''

                c.execute(query_50_percento, (totale_partite / 2,))
                giocatori_50_percento = c.fetchall()

                # Dizionario per associare la scelta alla colonna corrispondente
                opzioni_classifica = {
                    "1": (1, "Gol individuali", tutti_giocatori),
                    "2": (2, "Partite giocate", tutti_giocatori),
                    "3": (3, "Partite vinte", tutti_giocatori),
                    "4": (4, "Partite perse", tutti_giocatori),
                    "5": (5, "Media voto", giocatori_50_percento)
                }

                if scelta_classifica in opzioni_classifica:
                    colonna_index, nome_statistica, dataset = opzioni_classifica[scelta_classifica]

                    # Se la classifica riguarda la media voto, mostra il messaggio di avviso
                    if scelta_classifica == "5":
                        print("\n Classifica basata solo sui giocatori con almeno il 50 percento delle partite giocate.")

                    if not dataset:
                        print(f"Nessun giocatore disponibile per la classifica {nome_statistica}.")
                    else:
                        classifica = sorted(dataset, key=lambda x: x[colonna_index], reverse=True)

                        print(f"\nClassifica per {nome_statistica}:")
                        for posizione, giocatore in enumerate(classifica, start=1):
                            # Se è la classifica della media voto, mostra con 2 decimali, altrimenti senza decimali
                            valore = f"{giocatore[colonna_index]:.2f}" if scelta_classifica == "5" else f"{str(int(giocatore[colonna_index]))}"
                            print(f"{posizione}. {giocatore[0]} - {valore}")

                else:
                    print("Opzione non valida. Riprova.")


        elif scelta == "5":
          print("Uscita dal menu delle statistiche.")
          break
        else:
         print("Opzione non valida. Riprova.")
    conn.close()

if __name__ == "__main__":
    conn = sqlite3.connect("calcetto_stats.db")
    c = conn.cursor()
    
    while True:
        print("\nMenu principale:")
        print("1. Inserisci una nuova partita")
        print("2. Mostra statistiche")
        print("3. Mostra tutti i giocatori")
        print("4. Esci")
        scelta = input("Scegli un'opzione (1/2/3/4): ")

        if scelta == "1":
            inserisci_dati_da_terminale()
        elif scelta == "2":
            mostra_statistiche()
        elif scelta == "3":
            c.execute("SELECT DISTINCT nome FROM Giocatori")
            giocatori = c.fetchall()
            print("\nLista giocatori registrati:")
            for giocatore in giocatori:
                print(giocatore[0])
        elif scelta == "4":
            print("Uscita dal programma. Alla prossima!")
            break
        else:
            print("Opzione non valida. Riprova.")
    
    conn.close()

>>>>>>> c1353a8311871b386ba7ca30ef8f226a832261cf
