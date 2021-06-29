import requests
from bs4 import BeautifulSoup
import os
from time import sleep
from discordBot import DiscordBot
from stockChecker import stockChecker

urls = {'PS5':'https://www.nowinstock.net/videogaming/consoles/sonyps5/',
        'RTX 3060':'https://www.nowinstock.net/computers/videocards/nvidia/rtx3060/',
        'RTX 3060Ti':'https://www.nowinstock.net/computers/videocards/nvidia/rtx3060ti/',
        'RTX 3070':'https://www.nowinstock.net/computers/videocards/nvidia/rtx3070/',
        'RTX 3070Ti':'https://www.nowinstock.net/computers/videocards/nvidia/rtx3070ti/',
        'RTX 3080':'https://www.nowinstock.net/computers/videocards/nvidia/rtx3080/',
        'RTX 3080Ti':'https://www.nowinstock.net/computers/videocards/nvidia/rtx3080ti/'}
ps5URL = 'https://www.nowinstock.net/videogaming/consoles/sonyps5/'
rtx3080 = 'https://www.nowinstock.net/computers/videocards/nvidia/rtx3080/'
#response = requests.get(ps5URL)
#print(response.status_code)
#soup = BeautifulSoup(response.content, 'lxml')
#print(soup.find_all('td')[84])

'''
    format of parsed data:
    [{'retailer': 'retailer name', 'productName': 'product name', 'inStock': bool, 'price': float, 'lastInStock' : 'date'},
     {...},...]
    '''
def main():
    openingRemarks = 'Hi! I\'m StockBot. I track various listings for the PS5 and RTX 30 series GPUs.\n\n'
    dBot = DiscordBot(os.getenv('ps5BotWebhook'))
    stockBots = []
    for key in urls.keys():
        stockBots.append(stockChecker(key, urls[key]))
    initData = []
    for bot in stockBots:
        initData += bot.checkStock()
    retailers = []
    openingRemarks += 'So far, I\'m tracking listings from the following retailers:\n'
    for d in initData:
        if d['retailer'] in retailers:
            continue
        retailers.append(d['retailer'])
        openingRemarks += d['retailer'] + '\n'
    openingRemarks += '\nI will @ everyone when I find something in stock'
    dBot.execute(openingRemarks)
    print(openingRemarks)
    #print(retailers)
    while True:
        print('searching')
        data = []
        for bot in stockBots:
            data += bot.checkStock()
        for d in data:
            if d['inStock']:
                content = '@everyone ' + d['productName'] + ' is in stock at ' + d['retailer'] + '!\n'
                content += 'Tips:\nKeep adding to cart.\nFor Amazon, try adding to a list and adding to cart from there.\n'
                content += 'For Best Buy, don\'t refresh after the add-to-cart button goes gray - it will turn yellow again'
                dBot.execute(content)
        print('searching complete')
        sleep(60)
                

    return

main()