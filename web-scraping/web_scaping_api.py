import os
from decimal import Decimal
import random
import requests
import re
import pandas as pd
from bs4 import BeautifulSoup



def parse_url(url):
    UAS = ("Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1",
           "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
           "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0",
           "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
           "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
           "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
           )

    ua = UAS[random.randrange(len(UAS))]

    headers = {'user-agent': ua}
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "lxml")

    return soup

def clean_property_info(house_data_raw):

    result = dict()
    #price
    price_raw = house_data_raw.get('price')

    try:
        price = float("".join(d for d in price_raw if d.isdigit() or d == '.'))
    except:
        price = None

    result['price'] = price


    #address
    # the address
    address_raw = house_data_raw.get('address')
    address_raw = address_raw.split(", ")
    print(address_raw)
    #result['street'] = address_raw[0]
    #result['city'] = address_raw[1]
    result['county'] = address_raw[-1]

    #rooms
    rooms_raw = house_data_raw.get('rooms')
    rooms_raw = rooms_raw.split()
    result['rooms'] = rooms_raw[0]

    #bath
    bath_raw = house_data_raw.get('baths')
    bath_raw = bath_raw.split()
    result['baths'] = bath_raw[0]

    #size
    size_raw = house_data_raw.get('size')
    try:
        size_raw = size_raw.split()
        result['size'] = size_raw[0]
    except:
        result['size'] = None

    #type
    result['type'] = house_data_raw.get('type')

    #energy class
    energy_raw = house_data_raw.get('energy_class')
    head, tail = os.path.split(energy_raw)
    energy = tail.split()
    result['energy'] = energy[0]

    #agent
    result['agent'] = house_data_raw.get('agent')

    return result


def get_text_from_tag(tag, attibute):

    try:
        result = tag.find('p', attrs={'data-testid': attibute}).getText()
    except:
        result = ""

    return result

# TODO should be called just once
def total_houses(soup):
    total_houses = soup.find('h1', attrs={'data-testid': 'search-h1'}).text
    return total_houses


def extract_data(soup):
    properties_group = soup.find('ul', attrs={'data-testid': 'results'})
    result_houses_page = pd.DataFrame()

    regex = re.compile('result-.*')
    for prop in properties_group.find_all('li', attrs={'data-testid': regex}):
        price = prop.find('div', attrs={'data-testid': 'price'}).text
        address = prop.find('p', attrs={'data-testid': 'address'}).text

        house_info = prop.find('div', attrs={'data-testid': 'card-info'})
        rooms = get_text_from_tag(house_info, 'beds')
        baths = get_text_from_tag(house_info, 'baths')
        size = get_text_from_tag(house_info, 'floor-area')
        type = get_text_from_tag(house_info, 'property-type')

        energy_class = house_info.find('img', attrs={'data-testid': 'ber-image'}).attrs.get('src')

        agent = prop.find('div', attrs={'data-testid': 'callout-container'}).find('span', attrs={
            'data-testid': 'agent-name'}).text

        house_data_raw = dict()
        house_data_raw['price'] = price
        house_data_raw['address'] = address
        house_data_raw['rooms'] = rooms
        house_data_raw['baths'] = baths
        house_data_raw['size'] = size
        house_data_raw['type'] = type
        house_data_raw['energy_class'] = energy_class
        house_data_raw['agent'] = agent

        house_cleaned = clean_property_info(house_data_raw)

        result_houses_page = result_houses_page.append(house_cleaned, ignore_index=True)

    return result_houses_page


def get_content_from_url():
    pass

def create_page_interval(items_per_page: int, total_items: int):

    list_url = list()

    for i in range(0, total_items, items_per_page):
        url = f"https://www.daft.ie/property-for-sale/ireland?pageSize={items_per_page}from={i}"
        list_url.append(url)

    return list_url

def run_extraction(list_url):

    result_dataset = pd.DataFrame()
    for url in list_url:

        soap = parse_url(url)
        house_page = extract_data(soap)
        result_dataset = result_dataset.append(house_page, ignore_index=True)

    return result_dataset

def export_dataset(dataset):
    dataset.to_csv('dataset.csv', index=False)

if __name__ == "__main__":
    items_per_page = 20
    total = 45

    list_url = create_page_interval(items_per_page, total)
    print(list_url)
    dataset = run_extraction(list_url)
    export_dataset(dataset)


    # url = f"https://www.daft.ie/property-for-sale/ireland?pageSize={items_per_page}from={0}"
    # soap = parse_url(url)
    # extract_data(soap)


#
# for element in soup.find_all('ul', attrs={'data-testid': 'results'
#                                                     }):
#     price = element.find('div', attrs={'data-test': 'sl.price-label'}).text  # => price.text return the price value
#     agency_link = element.find_all('div', {'class': 'Contact__ContentContainer-sc-3d01ca-2 cKwmCO'})
#     for agency in agency_link:
#         agency_name = agency.a.text
#         agency_name_value = agency_name
#     type = element.find('div', attrs={'data-test': 'sl.title'}).text
#
#     address = element.find('div', attrs={'data-test': 'sl.address'}).text
#
#     ul_tagsLine_0 = element.find('ul', attrs={'data-test': 'sl.tagsLine_0'})
#     list_ul_tagsLine_0 = []
#
#     for li in ul_tagsLine_0.find_all("li"):
#         list_ul_tagsLine_0.append(li.text)
#
#     numbers_of_pieces, rooms, size = getLiValue(list_ul_tagsLine_0)
#     # print('\n')
#     list_all_ads.append({"price": price,
#                          "agency_name": agency_name_value,
#                          "type":type, "address":address,
#                          "numbers_of_pieces":numbers_of_pieces,
#                          "rooms":rooms, "size":size})

