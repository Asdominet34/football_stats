import sqlite3

from db import crea_database
from stats import get_classifica
from cli import inserisci_dati_da_terminale, mostra_statistiche

if __name__ == "__main__":
    conn = sqlite3.connect("calcetto_stats.db")
    c = conn.cursor()
    
    while True:
        print("\nMenu principale:")
        print("1. Inserisci una nuova partita")
        print("2. Mostra statistiche")
        print("3. Mostra tutti i giocatori")
        print("4. Mostra classifiche")
        print("5. Esci")
        scelta = input("Scegli un'opzione (1/2/3/4/5): ")

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
            print("\nScegli classifica:")
            print("1. Gol")
            print("2. Partite giocate")
            print("3. Partite vinte")
            print("4. Partite perse")
            print("5. Media voto")
            tipo = input("Inserisci numero: ")

            mapping = {
                "1": "gol",
                "2": "giocate",
                "3": "vinte",
                "4": "perse",
                "5": "voto"
            }

            if tipo in mapping:
                titolo, classifica = get_classifica(mapping[tipo])
                print("\n", titolo)
                for pos, g in enumerate(classifica, start=1):
                    if mapping[tipo] == "voto":
                        print(f"{pos}. {g[0]} - {g[5]:.2f}")
                    elif mapping[tipo] == "gol":
                        print(f"{pos}. {g[0]} - {g[1]} gol")
                    elif mapping[tipo] == "giocate":
                        print(f"{pos}. {g[0]} - {g[2]} partite")
                    elif mapping[tipo] == "vinte":
                        print(f"{pos}. {g[0]} - {g[3]} vinte")
                    elif mapping[tipo] == "perse":
                        print(f"{pos}. {g[0]} - {g[4]} perse")
            else:
                print("Scelta non valida.")
        elif scelta == "5":
            print("Uscita dal programma. Alla prossima!")
            break
        else:
            print("Opzione non valida. Riprova.")
    
    conn.close()
