Eseguire da "main.py"

################################
FILE CONFIGURAZIONE (app_config.json)
################################

WORKERS -> numero di scraper da eseguire in contemporanea.
    - svuotare la cartella %TEMP%
    - POTREBBE aumentare rischio detection

DATABASE_CONNECTION_STRING -> stringa connessione al db
    # MIGRAZIONE #
    1. Posizionati con il terminale sulla stessa cartella di "app.py"
    2. esegui
        "flask --app db init"
        "flask db migrate -m <nome migration>"
        "flask db upgrade"

CSV_HEADERS -> per facilitare il mapping del csv da importare
