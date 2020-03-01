import requests
import keyring
import configparser


class AccountSession:

    def __init__(self):
        try:
            # Load username from config file
            config = configparser.ConfigParser()
            config.read('config.ini')
            self.BOT_USER = config['DEFAULT']['USER']
            #Load password from system keyring
            self.BOT_PASS = keyring.get_password('osrs_wiki_bot', self.BOT_USER)
            print(self.BOT_PASS, self.BOT_USER)
            if self.BOT_PASS == None:
                raise Exception('Error retrieving password')
        except Exception as error:
            print(error)
            quit()

        self.API_URL = config['DEFAULT']['API_URL']

        self.session = requests.Session()
        self.EDIT_TOKEN = None
        self.LOGIN_TOKEN = None
        return

    def get_session(self):
        return self.session

    # Login process
    # TODO - Add retry 
    def login_bot(self):
        try:
            # login_attempt = 0
            # while self.LOGIN_TOKEN == None and login_attempt < 4:
            #     self.get_login_token()

            # Get login token before logging in
            self.get_login_token()
            print('LOGIN TOKEN: ', self.LOGIN_TOKEN)
        except Exception as error:
            print(error)

        # Logging in
        try:
            login_request = self.session.post(self.API_URL, data={
                'action': 'login',
                'lgname': self.BOT_USER,
                'lgpassword': self.BOT_PASS,
                'lgtoken': self.LOGIN_TOKEN,
                'format': 'json'
            })
            print(login_request.json())
        except Exception as error:
            print(error)

    # Login token
    def get_login_token(self):
        try:
            request_token = self.session.get(self.API_URL, params={
                'format': 'json',
                'action': 'query',
                'meta': 'tokens',
                'type': 'login'
            })
            token = request_token.json()['query']['tokens']['logintoken']
            self.set_login_token(token)
        except Exception as error:
            raise Exception(error)
        return

    def set_login_token(self, token):
        self.LOGIN_TOKEN = token
        return


    # CSRF edit token
    # TODO - Update CSRF token in case of expiry
    def get_edit_token(self):
        request_edit_token = self.session.get(self.API_URL, params={
            'action': 'query',
            'meta': 'tokens',
            'format': 'json'
        })

        self.EDIT_TOKEN = request_edit_token.json()['query']['tokens']['csrftoken']
        print(self.EDIT_TOKEN)
        return