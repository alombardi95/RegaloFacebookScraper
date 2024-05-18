import time

from infrastructure.facebook.facebook_driver import FacebookDriver
from utils.helpers import extract_dates, extract_number


def scrape_data(scraper: FacebookDriver, link: str):
    scraper.goto_group_about(link)
    scraper.wait_then_click('//div[@aria-label="Close"]')

    members_number = extract_number(scraper.wait_for("//span[contains(., 'total members')]").text)
    admin_list = scraper.wait_for("//div[@role='list']")
    admins = scraper.wait_for_many("div[@role='listitem']", from_element=admin_list)
    posts_last_month = extract_number(scraper.wait_for("//span[contains(., 'in the last month')]").text)
    dates = extract_dates(scraper.wait_for("//span[contains(., 'Group created on')]").text)

    return {
        "members_number": members_number,
        "admins": len(admins),
        "posts_last_month": posts_last_month,
        "creation_date": dates[0],
        "last_modified_date": dates[1] if len(dates) > 1 else None
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
            exit()


if __name__ == '__main__':
    links = [
        "https://www.facebook.com/groups/teloregaloagiulianova/about",
        "https://www.facebook.com/groups/1550734864947613",
        "https://www.facebook.com/groups/chicercalavoroonlinechioffrlavoroonline"
    ]
    fs = FacebookDriver()

    initialize_scraper(fs)
    data = []
    for link in links:
        data.append(scrape_data(fs, link))
        time.sleep(5)

    print(data)
