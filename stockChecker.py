import requests
from bs4 import BeautifulSoup

class stockChecker():
    def __init__(self, name, url):
        self.name = name
        self.url = url

    def loadProductData(self):
        try:
            response = requests.get(self.url)
            if response.status_code != 200:
                print(response.status_code)
                print(response.content)
                return None
        except requests.exceptions.RequestException as e:
            print(e)
            return None
        return response.content
    '''
    format of parsed data:
    [{'retailer': 'retailer name', 'productName': 'product name', 'inStock': bool, 'price': float, 'lastInStock' : 'date'},
     {...},...]
    '''
    def parseData(self, soup):
        rawData = soup.find_all('td')
        data = []
        i = 0
        while i < len(rawData):
            entry = {}
            productNameRaw = rawData[i].find('a').text #from here we will get product name and retailer
            j = len(productNameRaw) - 1
            split = 0
            while j >= 0:
                if productNameRaw[j] == ':':
                    split = j
                    break
                j -= 1
            entry['productName'] = productNameRaw[:split - 1]
            if entry['productName'] == 'Item alerting temporarily suspended':
                i += 4
                continue
            if entry['productName'] == 'Ebay':
                return data
            entry['retailer'] = productNameRaw[split + 2: -1].strip()
            entry['inStock'] = not (rawData[i + 1].text == 'Out of Stock') #from here we will get stock information
            try:
                entry['price'] = float(rawData[i + 2].text[1:]) #from here we will get price information
            except ValueError:
                entry['price'] = rawData[i + 2].text
            entry['lastInStock'] = rawData[i + 3].text #from ehre we will get the date it was last in stock
            #print(entry)
            data.append(entry)
            i += 4
        return data

    def checkStock(self):
        rawData = self.loadProductData()
        if rawData == None:
            return []
        soup = BeautifulSoup(self.loadProductData(), 'lxml')
        data = self.parseData(soup)
        return sorted(data, key = lambda i: i['retailer'])