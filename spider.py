import concurrent.futures
import threading
from datetime import datetime
import time

from app import app, db, config
from infrastructure.facebook.facebook_driver import FacebookDriver
from models.db_items import DettagliGruppoItem, GruppoItem
from utils.helpers import extract_dates, extract_number

from joblib import Parallel, delayed


# scraped_data = []
scrape_list_lock = threading.Lock()


def scrape_data(link: str):
    scraper = FacebookDriver(headless=False)

    try:
        scraper.goto_group_about(link)
        scraper.wait_for("//span[contains(., 'Group')]")
        #time.sleep(2)
        #scraper.wait_then_click('//div[@aria-label="Close"]')

        new_posts_today_element = scraper.wait_for("//span[contains(., 'new posts today')]")
        if not new_posts_today_element:
            new_posts_today_element = scraper.wait_for("//span[contains(., 'new post today')]")

        members_number = extract_number(scraper.wait_for("//span[contains(., 'total members')]").text)
        admin_list = scraper.wait_for("//div[@role='list']")
        admins = scraper.wait_for_many("div[@role='listitem']", from_element=admin_list)
        posts_last_month = extract_number(scraper.wait_for("//span[contains(., 'in the last month')]").text)
        posts_today = extract_number(new_posts_today_element.text)
        dates = extract_dates(scraper.wait_for("//span[contains(., 'Group created on')]").text)
    except Exception as e:
        print(f"Errore selenium in scrape data {link} : {e}")
        return
    finally:
        scraper.close()

    str_format = '%d/%m/%Y'

    return {
        "id_gruppo": link,
        "numero_membri": members_number,
        "numero_admin": len(admins),
        "posts_mensili": posts_last_month,
        "posts_giornalieri": posts_today,
        "data_creazione": datetime.strptime(dates[0], str_format),
        "ultima_modifica": datetime.strptime(dates[1], str_format) if len(dates) > 1 else None
    }


def scrape_groups(links: list[str]):
    def shift_list_next(lst, element):
        if element not in lst:
            raise ValueError("Element not found in the list")

        index = lst.index(element)
        next_index = (index + 1) % len(lst)
        return lst[next_index:] + lst[:next_index]

    def divide_list(input_list, n):
        return [input_list[i:i + n] for i in range(0, len(input_list), n)]

    with app.app_context():
        ultimo_dettaglio: DettagliGruppoItem = \
            DettagliGruppoItem.query\
            .order_by(DettagliGruppoItem.timestamp.desc())\
            .first()

        if ultimo_dettaglio:
            links = shift_list_next(links, ultimo_dettaglio.id_gruppo)

    for chunk in divide_list(links, config.WORKERS*2):
        scraped_data = Parallel(n_jobs=config.WORKERS)(delayed(scrape_data)(url) for url in chunk)

        [save_scrape_result_to_db(result) for result in scraped_data if result]

        print(f"Processed links {len(scraped_data)}/{config.WORKERS*2}")
        time.sleep(1)


def save_scrape_result_to_db(result):
    new_result = {k: v for k, v in result.items() if k != "data_creazione"}
    record = DettagliGruppoItem(**new_result)
    with app.app_context():
        gruppo_query = GruppoItem.query.filter_by(link=result['id_gruppo'])
        gruppo: GruppoItem = gruppo_query.first()
        if gruppo and not gruppo.data_creazione:
            gruppo_query.update({'data_creazione': result['data_creazione']})

        db.session.add(record)
        db.session.commit()


if __name__ == '__main__':
    # Supponiamo di avere una stringa con una data
    data_stringa = "24/05/2024"

    # Definisci il formato della stringa
    formato_data = "%d/%m/%Y"

    # Usa strptime per convertire la stringa in un oggetto datetime
    data = datetime.strptime(data_stringa, formato_data)

    print(data)
