import os
import sqlite3
from db import DB_NAME


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

def get_statistiche_giocatore(nome_giocatore):
    conn = sqlite3.connect("calcetto_stats.db")
    c = conn.cursor()

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
    conn.close()

    if risultato:
        # 🔎 Cerca la foto del giocatore
        nome_file_base = risultato[0].lower().strip().replace(" ", "_")
        cartella_foto = os.path.join("static", "img", "giocatori")

        foto_trovata = None
        for estensione in [".jpg", ".jpeg", ".png"]:
            possibile_foto = os.path.join(cartella_foto, nome_file_base + estensione)
            if os.path.exists(possibile_foto):
                foto_trovata = f"img/giocatori/{nome_file_base}{estensione}"
                break

        if not foto_trovata:
            foto_trovata = "img/placeholder.jpg"

        # 📊 Restituisce tutte le statistiche
        return {
            "nome": risultato[0],
            "gol_totali": risultato[1],
            "partite_giocate": risultato[2],
            "partite_vinte": risultato[3],
            "partite_pareggiate": risultato[4],
            "partite_perse": risultato[5],
            "media_voto": round(risultato[6], 2) if risultato[6] else 0,
            "media_gol": round(risultato[7], 2) if risultato[7] else 0,
            "media_gol_fatti_squadra": round(risultato[8], 2) if risultato[8] else 0,
            "media_gol_subiti_squadra": round(risultato[9], 2) if risultato[9] else 0,
            "percentuale_vittorie": round(risultato[10], 2) if risultato[10] else 0,
            "foto": foto_trovata
        }
    else:
        return None

def get_statistiche_coppia(nome1, nome2):
    conn = sqlite3.connect("calcetto_stats.db")
    c = conn.cursor()

    # Partite giocate insieme
    c.execute('''
        SELECT COUNT(*) 
        FROM Giocatori AS g1
        JOIN Giocatori AS g2 
        ON g1.id_partita = g2.id_partita AND g1.squadra = g2.squadra
        WHERE g1.nome = ? AND g2.nome = ?
    ''', (nome1, nome2))
    partite_insieme = c.fetchone()[0]

    if partite_insieme == 0:
        conn.close()
        return None  # nessuna partita insieme

    # Vittorie insieme
    c.execute('''
        SELECT COUNT(*) 
        FROM Giocatori AS g1
        JOIN Giocatori AS g2 ON g1.id_partita = g2.id_partita
        WHERE g1.nome = ? AND g2.nome = ? AND g1.squadra = g2.squadra AND g1.partite_vinte = 1
    ''', (nome1, nome2))
    vittorie_insieme = c.fetchone()[0]
    percentuale_vittorie_insieme = round((vittorie_insieme / partite_insieme) * 100, 2)

    # Gol segnati giocando insieme
    c.execute('''
        SELECT AVG(g1.gol_individuali), AVG(g2.gol_individuali)
        FROM Giocatori AS g1
        JOIN Giocatori AS g2 
        ON g1.id_partita = g2.id_partita AND g1.squadra = g2.squadra
        WHERE g1.nome = ? AND g2.nome = ?
    ''', (nome1, nome2))
    media_gol_insieme = c.fetchone()
    media_gol_insieme = (
        round(media_gol_insieme[0] or 0, 2),
        round(media_gol_insieme[1] or 0, 2)
    )

    # Statistiche senza l’altro (giocatore 1)
    c.execute('''
        SELECT 
            CAST(SUM(partite_vinte) AS REAL) / SUM(partite_giocate) * 100,
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
    ''', (nome1, nome1, nome2))
    stats_no_insieme1 = c.fetchone()
    stats_no_insieme1 = (
        round(stats_no_insieme1[0] or 0, 2),
        round(stats_no_insieme1[1] or 0, 2)
    )

    # Statistiche senza l’altro (giocatore 2)
    c.execute('''
        SELECT 
            CAST(SUM(partite_vinte) AS REAL) / SUM(partite_giocate) * 100,
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
    ''', (nome2, nome2, nome1))
    stats_no_insieme2 = c.fetchone()
    stats_no_insieme2 = (
        round(stats_no_insieme2[0] or 0, 2),
        round(stats_no_insieme2[1] or 0, 2)
    )

    conn.close()

    return {
        "giocatore1": nome1,
        "giocatore2": nome2,
        "partite_insieme": partite_insieme,
        "vittorie": vittorie_insieme,
        "percentuale_vittorie": percentuale_vittorie_insieme,
        "media_gol_insieme": media_gol_insieme,
        "stats_no_insieme1": stats_no_insieme1,
        "stats_no_insieme2": stats_no_insieme2
    }

def get_lista_giocatori():
    conn = sqlite3.connect("calcetto_stats.db")
    c = conn.cursor()

    c.execute("SELECT DISTINCT nome FROM Giocatori ORDER BY nome")
    risultati = c.fetchall()
    conn.close()

    return [r[0] for r in risultati]

def get_partite():
    conn = sqlite3.connect("calcetto_stats.db")
    c = conn.cursor()

    c.execute("SELECT * FROM Partite ORDER BY data DESC")
    partite = c.fetchall()
    conn.close()

    # Ritorniamo una lista di dizionari per leggibilità
    risultati = []
    for p in partite:
        risultati.append({
            "id": p[0],
            "data": p[1],
            "luogo": p[2],
            "gol_chiari": p[3],
            "gol_scuri": p[4]
        })
    return risultati

def get_dettaglio_partita(id_partita):
    conn = sqlite3.connect("calcetto_stats.db")
    c = conn.cursor()

    # Info della partita
    c.execute("""
        SELECT id_partita, data, luogo, gol_squadra_chiari, gol_squadra_scuri
        FROM Partite
        WHERE id_partita = ?
    """, (id_partita,))
    partita = c.fetchone()

    # Giocatori squadra chiari
    c.execute("""
        SELECT nome, gol_individuali, voto_pagella
        FROM Giocatori
        WHERE id_partita = ? AND squadra = 'Chiari'
    """, (id_partita,))
    giocatori_chiari = c.fetchall()

    # Giocatori squadra scuri
    c.execute("""
        SELECT nome, gol_individuali, voto_pagella
        FROM Giocatori
        WHERE id_partita = ? AND squadra = 'Scuri'
    """, (id_partita,))
    giocatori_scuri = c.fetchall()

    conn.close()
    return partita, giocatori_chiari, giocatori_scuri

def get_classifica(tipo):
    conn = sqlite3.connect("calcetto_stats.db")
    c = conn.cursor()

    # Conta partite per regola del 50%
    c.execute("SELECT COUNT(*) FROM Partite")
    totale_partite = c.fetchone()[0]

    # Query base
    query_base = '''
        SELECT nome, 
               SUM(gol_individuali) AS gol_individuali, 
               SUM(partite_giocate) AS partite_giocate, 
               SUM(partite_vinte) AS partite_vinte, 
               SUM(partite_perse) AS partite_perse, 
               AVG(voto_pagella) AS media_voto
        FROM Giocatori
        GROUP BY nome
    '''

    # Query con filtro 50% partite (solo per media voto)
    query_50 = query_base + " HAVING SUM(partite_giocate) >= ?"

    if tipo == "gol":
        c.execute(query_base)
        giocatori = c.fetchall()
        classifica = sorted(giocatori, key=lambda x: x[1], reverse=True)
        titolo = "Classifica Gol"

    elif tipo == "giocate":
        c.execute(query_base)
        giocatori = c.fetchall()
        classifica = sorted(giocatori, key=lambda x: x[2], reverse=True)
        titolo = "Classifica Partite Giocate"

    elif tipo == "vinte":
        c.execute(query_base)
        giocatori = c.fetchall()
        classifica = sorted(giocatori, key=lambda x: x[3], reverse=True)
        titolo = "Classifica Partite Vinte"

    elif tipo == "perse":
        c.execute(query_base)
        giocatori = c.fetchall()
        classifica = sorted(giocatori, key=lambda x: x[4], reverse=True)
        titolo = "Classifica Partite Perse"

    elif tipo == "voto":
        c.execute(query_50, (totale_partite / 2,))
        giocatori = c.fetchall()
        classifica = sorted(giocatori, key=lambda x: x[5], reverse=True)
        titolo = "Classifica Media Voto (>=50% partite)"

    else:
        conn.close()
        return None, []

    conn.close()
    return titolo, classifica