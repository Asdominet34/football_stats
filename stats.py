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

            # Numero totale di partite registrate
            c.execute('SELECT COUNT(*) FROM Partite')
            totale_partite = c.fetchone()[0]

            if totale_partite == 0:
                print("Non ci sono partite registrate.")
            else:
                # --- Recupero statistiche del giocatore scelto ---
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
                    # --- Recupero giocatori per ranking ---
                    # Tutti i giocatori (per ranking "normali")
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
                    GROUP BY nome
                    ''')
                    giocatori_tutti = c.fetchall()

                    # Solo giocatori con almeno 5 partite (per media voto e media gol)
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
                    GROUP BY nome
                    HAVING SUM(partite_giocate) >= 5
                    ''')
                    giocatori_5 = c.fetchall()

                    # --- Calcolo ranking ---
                    ranking_gol = sorted(giocatori_tutti, key=lambda x: x[1], reverse=True)
                    ranking_partite_giocate = sorted(giocatori_tutti, key=lambda x: x[2], reverse=True)
                    ranking_vinte = sorted(giocatori_tutti, key=lambda x: x[3], reverse=True)
                    ranking_percentuale = sorted(giocatori_tutti, key=lambda x: x[10], reverse=True)
                    ranking_media_gol_fatti_squadra = sorted(giocatori_tutti, key=lambda x: x[8], reverse=True)
                    ranking_media_gol_subiti_squadra = sorted(giocatori_tutti, key=lambda x: x[9], reverse=True)

                    # ✅ Ranking solo per chi ha almeno 5 partite
                    ranking_voto = sorted(giocatori_5, key=lambda x: x[6], reverse=True)
                    ranking_media_gol = sorted(giocatori_5, key=lambda x: x[7], reverse=True)

                    # Funzione per trovare posizione in classifica
                    def trova_posizione(nome, ranking):
                        for posizione, giocatore in enumerate(ranking, start=1):
                            if giocatore[0] == nome:
                                return posizione
                        return "-"

                    # --- Calcolo posizioni ---
                    posizione_gol = trova_posizione(nome_giocatore, ranking_gol)
                    posizione_partite_giocate = trova_posizione(nome_giocatore, ranking_partite_giocate)
                    posizione_vinte = trova_posizione(nome_giocatore, ranking_vinte)
                    posizione_voto = trova_posizione(nome_giocatore, ranking_voto)
                    posizione_media_gol = trova_posizione(nome_giocatore, ranking_media_gol)
                    posizione_percentuale = trova_posizione(nome_giocatore, ranking_percentuale)
                    posizione_media_gol_fatti_squadra = trova_posizione(nome_giocatore, ranking_media_gol_fatti_squadra)
                    posizione_media_gol_subiti_squadra = trova_posizione(nome_giocatore, ranking_media_gol_subiti_squadra)

                    # --- Output su console ---
                    print(f"\nStatistiche di {risultato[0]} (ranking calcolato su tutti i giocatori tranne media voto/gol -> min 5 partite):")
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

                # Verifica il numero totale di partite (solo per messaggi informativi)
                c.execute('SELECT COUNT(*) FROM Partite')
                totale_partite = c.fetchone()[0]

                if totale_partite == 0:
                        print("Non ci sono partite registrate.")
                else:
                        # soglia minima per le classifiche basate su medie
                        min_partite = 5

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

                        # Query per ottenere solo i giocatori con almeno min_partite (per la media voto)
                        query_min_partite = '''
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

                        c.execute(query_min_partite, (min_partite,))
                        giocatori_min_partite = c.fetchall()

                        # Dizionario per associare la scelta alla colonna corrispondente
                        opzioni_classifica = {
                                "1": (1, "Gol individuali", tutti_giocatori),
                                "2": (2, "Partite giocate", tutti_giocatori),
                                "3": (3, "Partite vinte", tutti_giocatori),
                                "4": (4, "Partite perse", tutti_giocatori),
                                "5": (5, f"Media voto (>= {min_partite} partite)", giocatori_min_partite)
                        }

                        if scelta_classifica in opzioni_classifica:
                                colonna_index, nome_statistica, dataset = opzioni_classifica[scelta_classifica]

                                # Se la classifica riguarda la media voto, mostra il messaggio di avviso
                                if scelta_classifica == "5":
                                        print(f"\nClassifica basata solo sui giocatori con almeno {min_partite} partite giocate.")

                                if not dataset:
                                        print(f"Nessun giocatore disponibile per la classifica {nome_statistica}.")
                                else:
                                        classifica = sorted(dataset, key=lambda x: x[colonna_index], reverse=True)

                                        print(f"\nClassifica per {nome_statistica}:")
                                        for posizione, giocatore in enumerate(classifica, start=1):
                                                # Se è la classifica della media voto, mostra con 2 decimali, altrimenti senza decimali
                                                if scelta_classifica == "5":
                                                        valore = f"{giocatore[colonna_index]:.2f}"
                                                else:
                                                        # per sicurezza se il valore è None -> 0
                                                        try:
                                                                valore = f"{int(giocatore[colonna_index])}"
                                                        except Exception:
                                                                valore = str(giocatore[colonna_index])
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

    # 🔎 Recupera le statistiche del giocatore
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

    if not risultato:
        conn.close()
        return None

    # Salva statistiche del giocatore in variabili
    nome, gol_totali, partite_giocate, vinte, pareggiate, perse, media_voto, media_gol, media_gol_fatti, media_gol_subiti, perc_vittorie = risultato

    # 1️⃣ Recupera tutti i giocatori per ranking
    c.execute('''
        SELECT nome, 
               SUM(gol_individuali) AS gol_totali,
               SUM(partite_giocate) AS partite_giocate,
               SUM(partite_vinte) AS partite_vinte,
               AVG(voto_pagella) AS media_voto,
               AVG(gol_individuali) AS media_gol,
               AVG(gol_fatti_squadra) AS media_gol_fatti_squadra,
               AVG(gol_subiti_squadra) AS media_gol_subiti_squadra
        FROM Giocatori
        GROUP BY nome
    ''')
    tutti_giocatori = c.fetchall()

    conn.close()

    # 📊 Calcola ranking
    def trova_posizione(nome, ranking):
        for pos, g in enumerate(ranking, start=1):
            if g[0] == nome:
                return pos
        return None

    # 🔢 Classifica per gol totali (su tutti)
    ranking_gol = sorted(tutti_giocatori, key=lambda x: x[1] or 0, reverse=True)
    pos_gol = trova_posizione(nome, ranking_gol)

    # 🎯 Filtra solo giocatori con almeno 5 partite
    giocatori_min5 = [g for g in tutti_giocatori if g[2] and g[2] >= 5]

    # Ranking per statistiche medie (solo >= 5 partite)
    ranking_media_voto = sorted(giocatori_min5, key=lambda x: x[4] or 0, reverse=True)
    ranking_media_gol = sorted(giocatori_min5, key=lambda x: x[5] or 0, reverse=True)
    ranking_media_gol_fatti = sorted(giocatori_min5, key=lambda x: x[6] or 0, reverse=True)
    ranking_media_gol_subiti = sorted(giocatori_min5, key=lambda x: x[7] or 0)  # crescente (meno subiti = meglio)

    pos_media_voto = trova_posizione(nome, ranking_media_voto)
    pos_media_gol = trova_posizione(nome, ranking_media_gol)
    pos_media_gol_fatti = trova_posizione(nome, ranking_media_gol_fatti)
    pos_media_gol_subiti = trova_posizione(nome, ranking_media_gol_subiti)

    # 🏆 Classifica per percentuale vittorie (solo >= 5 partite)
    ranking_vittorie = sorted(
        [(g[0], (g[3] / g[2] * 100) if g[2] > 0 else 0) for g in giocatori_min5],
        key=lambda x: x[1],
        reverse=True
    )
    pos_percentuale_vittorie = trova_posizione(nome, ranking_vittorie)

    # 🔎 Cerca la foto del giocatore
    nome_file_base = nome.lower().strip().replace(" ", "_")
    cartella_foto = os.path.join("static", "img", "giocatori")
    foto_trovata = None
    for estensione in [".jpg", ".jpeg", ".png"]:
        possibile_foto = os.path.join(cartella_foto, nome_file_base + estensione)
        if os.path.exists(possibile_foto):
            foto_trovata = f"img/giocatori/{nome_file_base}{estensione}"
            break
    if not foto_trovata:
        foto_trovata = "img/placeholder.jpg"

    # 📊 Restituisce tutte le statistiche + ranking
    return {
        "nome": nome,
        "gol_totali": gol_totali,
        "ranking_gol": pos_gol,
        "partite_giocate": partite_giocate,
        "partite_vinte": vinte,
        "partite_pareggiate": pareggiate,
        "partite_perse": perse,
        "media_voto": round(media_voto, 2) if media_voto else 0,
        "ranking_media_voto": pos_media_voto,
        "media_gol": round(media_gol, 2) if media_gol else 0,
        "ranking_media_gol": pos_media_gol,
        "media_gol_fatti_squadra": round(media_gol_fatti, 2) if media_gol_fatti else 0,
        "ranking_media_gol_fatti": pos_media_gol_fatti,
        "media_gol_subiti_squadra": round(media_gol_subiti, 2) if media_gol_subiti else 0,
        "ranking_media_gol_subiti": pos_media_gol_subiti,
        "percentuale_vittorie": round(perc_vittorie, 2) if perc_vittorie else 0,
        "ranking_percentuale_vittorie": pos_percentuale_vittorie,
        "foto": foto_trovata
    }

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

    # ✅ Filtro aggiornato: almeno 5 partite per media voto
    query_5 = query_base + " HAVING SUM(partite_giocate) >= 5"

    if tipo == "gol":
        c.execute(query_base)
        classifica = sorted(c.fetchall(), key=lambda x: x[1], reverse=True)
        titolo = "Classifica Gol"

    elif tipo == "giocate":
        c.execute(query_base)
        classifica = sorted(c.fetchall(), key=lambda x: x[2], reverse=True)
        titolo = "Classifica Partite Giocate"

    elif tipo == "vinte":
        c.execute(query_base)
        classifica = sorted(c.fetchall(), key=lambda x: x[3], reverse=True)
        titolo = "Classifica Partite Vinte"

    elif tipo == "perse":
        c.execute(query_base)
        classifica = sorted(c.fetchall(), key=lambda x: x[4], reverse=True)
        titolo = "Classifica Partite Perse"

    elif tipo == "voto":
        c.execute(query_5)
        classifica = sorted(c.fetchall(), key=lambda x: x[5], reverse=True)
        titolo = "Classifica Media Voto (>=5 partite)"

    else:
        conn.close()
        return None, []

    conn.close()
    return titolo, classifica
