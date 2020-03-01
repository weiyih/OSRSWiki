# Standard library
import logging
import sys

# Local packages
from AccountSession import AccountSession
from NullEdit import NullEdit

def main():
    # logger = logging.getLogger('wiki_bot')
    # logger.setLevel(logging.ERROR)
    # logger.
    # (filename='error.log', level=logging.ERROR, format='%(asctime) %(levelname)s:-%(message)s')

    with open('test.txt') as read_file:
        list_pages = read_file.read().splitlines()

    account = AccountSession()
    account.login_bot()
    account.get_edit_token()

    editor = NullEdit(account)
    editor.load_pages(list_pages)
    editor.edit_pages()


if __name__ == '__main__':
    main()
