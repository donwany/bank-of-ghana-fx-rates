
# python scraperv2.py https://www.bog.gov.gh/treasury-and-the-markets/treasury-bill-rates/
# python scraperv2.py https://www.bog.gov.gh/treasury-and-the-markets/historical-interbank-fx-rates/

import requests
from bs4 import BeautifulSoup as bs
import urllib3
from _datetime import datetime
import csv
import sys
from time import sleep
import argparse
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = 'https://www.bog.gov.gh/wp-admin/admin-ajax.php?action=get_wdtable&table_id'

def mkdir(path):
    """
    Create directory
    """
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        print(f' * Directory %s already exists = {path}')



# def argparser():
#     '''
#     argparser defnition
#     '''
#     parser = argparse.ArgumentParser(description='Bank of Ghana FX Rates')
#     parser.add_argument('--url',
#                         default='https://www.bog.gov.gh/treasury-and-the-markets/historical-interbank-fx-rates/',
#                         type=str,
#                         help='URL to page to scrap')
#
#     #parser.add_argument('--dataFolder', default='', type=str, help='Where to output historical data')
#
#     args = parser.parse_args()
#     return args
#
# args = argparser()

def scrape_table(url=''):
    '''scrape table definition'''
    if url == '':
        url = 'https://www.bog.gov.gh/treasury-and-the-markets/historical-interbank-fx-rates/'
    table = get_table_info(url)
    if table is None:
        return
    draw = 1
    start = 0
    length = 10000
    lines = []
    while True:
        try:
            response = send_request(table['wdtNonce'], table['id'], draw, start, length)
            if len(response['data']) > 0:
                for line in response['data']:
                    lines.append(line)
                start += length
            else:
                break
        except:
            print('Unsuccessful request. Trying again in few seconds.')
            sleep(5)
    try:
        lines.sort(key=lambda x: datetime.strptime(x[0], '%d %b %Y'), reverse=True)
    except:
        pass
    return {'name': table['name'], 'data': lines, 'headers': table['headers']}


def get_table_info(url):
    '''Get table information'''
    print('Loading table id...')
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                      " Chrome/85.0.4183.121 Safari/537.36"
    }
    html = requests.get(url, headers=headers, verify=False).text
    soup = bs(html, 'lxml')
    table = soup.find('table', id='table_1')
    input_wdt = soup.find('input', id='wdtNonceFrontendEdit')
    if table is None or input_wdt is None:
        print('Non-generic table url. Please contact developer.')
        return None
    if url[-1] in '/':
        name = url.split('/')[-2]
    else:
        name = url.split('/')[-1]
    table_id = table['data-wpdatatable_id']
    headers = []
    for header in table.find('thead').find('tr').find_all('th'):
        headers.append(header.get_text().strip())
    wdt_nonce = input_wdt['value']
    table_info = {'name': name, 'id': table_id, 'wdtNonce': wdt_nonce, 'headers': headers}
    print(f'Table id is {table_id}')
    return table_info


def send_request(wdt, table_id, draw, start, length):
    '''send request to scrape page'''
    print('Scraping data from API...')
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                      " Chrome/85.0.4183.121 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept": "application/json, text/javascript, */*; q=0.01",
    }
    data = {
        "draw": draw,
        "wdtNonce": wdt,
        "start": start,
        "length": length
    }
    response = requests.post(f'{BASE_URL}={table_id}',headers=headers, data=data, verify=False)
    return response.json()


def save_csv(name, headers, lines):
    '''save scraped data to csv'''
    print('Saving results in csv...')
    with open(f"{name}.csv", "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(headers)
        for line in lines:
            writer.writerow(line)
    print(f'{name}.csv saved! Total records: {len(lines)}')

class RatesURL(object):
    def __init__(self, url=''):
        self.url = url

    def getUrl(self):
        return self.url

    def setUrl(self, url):
        self.url = url

def run(url):
    #if len(sys.argv) > 1 and 'https://' in sys.argv[1]:
    #url = sys.argv[1].strip()
    #url = args.url
    #url = RatesURL(url)

    if 'https://' in url.getUrl():
        table = scrape_table(str(url.getUrl()))
    else:
        table = scrape_table()
    if table is not None:
        save_csv(table['name'], table['headers'], table['data'])


if __name__ == '__main__':
    url = RatesURL()
    url.setUrl('https://www.bog.gov.gh/treasury-and-the-markets/treasury-bill-rates/')
    run(url)








