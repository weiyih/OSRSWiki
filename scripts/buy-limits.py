#Scripts updates page buy limits from csv file

import requests
import csv
import datetime
import time
import re

# TODO - MOVE LOGIN TO NAMESPACE
# ACCOUNT CREDENTIALS
BOT_USER = ''
BOT_PASS = ''
API_URL = 'https://oldschool.runescape.wiki/api.php'

# EDIT INFORMATION
EDIT_SUMMARY = 'Adding official buy limits'
EDIT_TOKEN = ''
PAGE= 'Module:Exchange/'

session = requests.Session()
def login_bot():
    # Login TOKEN
    request_token = session.get(API_URL, params={
        'format': 'json',
        'action': 'query',
        'meta': 'tokens',
        'type': 'login'
    })
    LOGIN_TOKEN = request_token.json()['query']['tokens']['logintoken']

    # Login
    login_request = session.post(API_URL, data={
        'action': 'login',
        'lgname': BOT_USER,
        'lgpassword': BOT_PASS,
        'lgtoken': LOGIN_TOKEN,
        'format': 'json'
    })

    # EDIT TOKEN - SAME ACCROSS LOGIN
    request_edit_token = session.get(API_URL, params={
        'action': 'query',
        'meta': 'tokens',
        'format': 'json'
    })
    global EDIT_TOKEN
    EDIT_TOKEN = request_edit_token.json()['query']['tokens']['csrftoken']
    print(EDIT_TOKEN)

def update_item_limits(item_name, item_limit):
    print("ITEM: {0}, ITEM LIMIT: {1}".format(item_name, item_limit))
    PAGENAME = PAGE + item_name

    load_page = session.get(API_URL, params={
        'action': 'parse',
        'page': PAGE+item_name,
        'prop' : 'wikitext',
        'format': 'json'
    })
    # REGEX REPLACE ITEM LIMIT
    REGEX_PATTERN = '(?P<limit> *limit *= )(nil)?(?P<num>[0-9]*)'
    REPLACE = '\g<limit>'+item_limit

    # Page does not exists
    try:
        load_page.json()['parse']
    except KeyError:
        error = load_page.json()['error']['info']
        with open('error.txt', 'a+') as errorfile:
            errorfile.write("{0} - {1} - {2}\n".format(datetime.datetime.utcnow(), item_name, error))
            errorfile.close()
        return

    # PARSE WIKITEXT CONTENT
    content = load_page.json()['parse']['wikitext']['*']
    new_content = re.sub(REGEX_PATTERN, REPLACE, content)
    # Riblet check
    match = re.search(REGEX_PATTERN, content)
    old_limit = 'nil'
    if match:
        old_limit = match.expand(r'\g<num>')
        if old_limit != item_limit and old_limit != 'nil':
            with open('matched.txt', 'a+') as matchfile:
                matchfile.write("{0} - OLD: {1}  NEW: {2}\n".format(item_name, old_limit, item_limit))
            matchfile.close()

    global EDIT_TOKEN
    edit_page = session.post(API_URL, data={
        'action': 'edit',
        'bot': 'true',
        'summary': EDIT_SUMMARY,
        'title': PAGENAME,
        'text': new_content,
        'bot': 'true',
        'nocreate': 'true',
        'token': EDIT_TOKEN,
        'format': 'json'
    })

    try:
        result = edit_page.json()['edit']

        if 'nochange' in result:
            with open('error.txt', 'a+') as sucessfile:
                sucessfile.write("ITEM NOT UPDATED - {0}\n".format(item_name))
            sucessfile.close()
        else:
            with open('error.txt', 'a+') as sucessfile:
                sucessfile.write("ITEM UPDATED - {0}   BUY: {1}  OLD: {2}\n".format(item_name, item_limit, old_limit))
            sucessfile.close()
    except KeyError:
        # PLEASE DON"T BREAK
        error = edit_page.json()['error']['info']
        with open('error.txt', 'a+') as errorfile:
            errorfile.write("{0} - {1} - {2}\n".format(datetime.datetime.utcnow(), item_name, error))
        errorfile.close()

    time.sleep(0.4)

login_bot()

update_item_limits('Amulet of chemistry', '200')
login_bot()

with open('ge_buylimits_filtered.csv', 'r') as csvfile:
    line_count = 0
    itemreader = csv.reader(csvfile, delimiter=',')
    for item in itemreader:
        if (line_count == 0):
            line_count += 1
        else:
            line_count += 1
            item_string = item[0].capitalize()
            item_limit = item[1]
            update_item_limits(item_string, item_limit)

