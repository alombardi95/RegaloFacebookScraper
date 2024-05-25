from utils.helpers import ensure_about_suffix
from infrastructure.common.proxy_driver import ProxyDriver


class FacebookDriver(ProxyDriver):

    def __init__(self, timeout=10, browser='chrome', headless: bool = False, detached: bool = False):
        super().__init__(timeout, browser, headless, detached)

        self.base_url = "https://www.facebook.com/"

        self.accounts_center_url = "https://accountscenter.instagram.com/"
        self.profile_edit_url = "https://www.instagram.com/accounts/edit/"
        self.direct_inbox_url = "https://www.instagram.com/direct/inbox/"

    def goto_group_about(self, group_link):
        ensure_group_about = ensure_about_suffix(group_link)
        self.goto(ensure_group_about)

    def close(self):
        self.driver.close()
