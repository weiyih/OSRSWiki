from AccountSession import *
import logging
import sys


def main():
    # logger = logging.getLogger('wiki_bot')
    # logger.setLevel(logging.ERROR)
    # logger.
    # (filename='error.log', level=logging.ERROR, format='%(asctime) %(levelname)s:-%(message)s')
    account = AccountSession()
    print('Logging in bot')
    account.login_bot()
    print('finished logging in')


if __name__ == '__main__':
    main()
