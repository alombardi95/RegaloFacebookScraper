import re
from datetime import datetime


def extract_number(text):
    # Trova una corrispondenza con il pattern che identifica numeri potenzialmente seguiti da K o M
    match = re.search(r'\b(\d+(\.\d+)?)([KM]?)\b', text.replace(',', ''))
    if match:
        # Estraendo il numero base
        number = float(match.group(1))
        # Estraendo l'eventuale indicatore di K o M
        multiplier = match.group(3)
        if multiplier == 'K':
            return int(number * 1000)
        elif multiplier == 'M':
            return int(number * 1000000)
        else:
            return int(number)
    else:
        # Se non viene trovato alcun match, restituisci None o un errore appropriato
        return None


def extract_dates(text):
    # Regex per identificare le date nel formato "Month day, year"
    date_pattern = re.compile(
        r'(January|February|March|April|May|June|July|August|September|October|November|December)\s(\d{1,2}),\s(\d{4})')

    # Trova tutte le occorrenze nel testo
    matches = date_pattern.findall(text)

    # Lista per mantenere le date formattate
    formatted_dates = []

    # Converte le date trovate nel formato desiderato
    for match in matches:
        # Creazione di una data da stringhe
        date_str = ' '.join(match)  # Esempio: "August 21 2015"
        date_obj = datetime.strptime(date_str, '%B %d %Y')  # Converte in oggetto datetime
        formatted_date = date_obj.strftime('%d/%m/%Y')  # Formatta la data come "dd/mm/yyyy"
        formatted_dates.append(formatted_date)

    return formatted_dates


def ensure_about_suffix(url):
    # Controlla se l'URL termina con '/about', '/about/', o non ha una parte finale dopo il nome del gruppo
    if url.endswith('/about'):
        return url
    elif url.endswith('/about/'):
        return url[:-1]  # Rimuove lo slash finale
    elif url.endswith('/'):
        return url + 'about'
    else:
        return url + '/about'
