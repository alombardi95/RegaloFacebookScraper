from datetime import datetime
import time

from app import app, db
from infrastructure.facebook.facebook_driver import FacebookDriver
from models.db_items import DettagliGruppoItem, GruppoItem
from utils.helpers import extract_dates, extract_number


def scrape_data(scraper: FacebookDriver, link: str):
    scraper.goto_group_about(link)
    time.sleep(3)
    scraper.wait_then_click('//div[@aria-label="Close"]')

    members_number = extract_number(scraper.wait_for("//span[contains(., 'total members')]").text)
    admin_list = scraper.wait_for("//div[@role='list']")
    admins = scraper.wait_for_many("div[@role='listitem']", from_element=admin_list)
    posts_last_month = extract_number(scraper.wait_for("//span[contains(., 'in the last month')]").text)
    dates = extract_dates(scraper.wait_for("//span[contains(., 'Group created on')]").text)

    str_format = '%d/%m/%Y'
    return {
        "numero_membri": members_number,
        "numero_admin": len(admins),
        "nuovi_posts": posts_last_month,
        "data_creazione": datetime.strptime(dates[0], str_format),
        "ultima_modifica": datetime.strptime(dates[1], str_format) if len(dates) > 1 else None
    }


def initialize_scraper(scraper: FacebookDriver):
    areCookiesAccepted = False
    scraper.goto("https://www.facebook.com")
    time.sleep(5)

    try:
        scraper.wait_then_click('//div[@role="button" and @aria-label="Allow all cookies" and @tabindex="0"]')
        areCookiesAccepted = True
    except:
        pass

    if not areCookiesAccepted:
        try:
            scraper.wait_then_click("//button[@data-testid='cookie-policy-manage-dialog-accept-button']")
        except:
            pass


def scrape_groups(links: list[str]):
    fs = FacebookDriver()
    initialize_scraper(fs)
    data = []

    with app.app_context():
        for link in links:
            gruppo_query = GruppoItem.query.filter_by(link=link)
            gruppo: GruppoItem = gruppo_query.first()

            try:
                result = scrape_data(fs, link)
            except:
                continue

            result['id_gruppo'] = link

            if gruppo and not gruppo.data_creazione:
                gruppo_query.update({'data_creazione': result['data_creazione']})

            del result['data_creazione']
            record = DettagliGruppoItem(**result)
            db.session.add(record)
            db.session.commit()

            data.append(result)
            time.sleep(5)

    fs.close()

    return data


if __name__ == '__main__':
    # Supponiamo di avere una stringa con una data
    data_stringa = "24/05/2024"

    # Definisci il formato della stringa
    formato_data = "%d/%m/%Y"

    # Usa strptime per convertire la stringa in un oggetto datetime
    data = datetime.strptime(data_stringa, formato_data)

    print(data)
