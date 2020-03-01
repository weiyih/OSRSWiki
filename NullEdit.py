import configparser
import requests
from AccountSession import AccountSession


class NullEdit:

    def __init__(self, act: AccountSession):
        self.account = act
        self.pages_to_edit = []

        self.session = self.account.get_session()

        config = configparser.ConfigParser()
        config.read('config.ini')
        self.API_URL = config['DEFAULT']['API_URL']

        
    def load_pages(self, pages: list):
        self.pages_to_edit = pages

    # TODO - Reobtain CSRF token if error
    def edit(self, page_name):
        EDIT_PARAM = {
            'action': 'edit',
            'title': page_name,
            'token': self.account.EDIT_TOKEN,
            'format': 'json',
            'appendtext': ''
        }
        try:
            res = self.session.post(self.API_URL, EDIT_PARAM)
            print(res.json())
        except Exception as error:
            print(error)


    def edit_pages(self):
        for page in self.pages_to_edit:
            self.edit(page)


