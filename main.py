import requests
from bs4 import BeautifulSoup
import json
from smtp import send_mail

header = {"User-agent": "Mozilla/5.0 (X11; U; Linux i686; fr; rv:1.9.1.1) Gecko/20090715 Firefox/3.5.1 "}
euro = 4.3

def items():
    try:
        with open('items.json','r') as file:
            data = file.read()
        global list
        list = json.loads(data)
    except:
        print("Error when reading JSON file")

global min,min_link
def check_price(link):
    # link = "www.cos2.pl/cos.html"
    site_content = BeautifulSoup(requests.get(link, headers=header).content, 'html.parser')
    try:
        global price
        site_url = link.split('/')[2]
        if(site_url == 'www.x-kom.pl'):
            price = int(site_content.find(attrs={'class':'u7xnnm-4 gHPNug'}).get_text().split(',')[0].replace(" ",''))
        elif(site_url == 'www.komputronik.pl'):
            price = site_content.find('span',attrs={'class':'price'}).find('span').get_text()
            if(price == ''):
                price = site_content.find('span',attrs={'class':'price'}).find('span',attrs={'ng-if':'!$ctrl.changeBaseData'}).get_text()
            price = int(''.join([n for n in price if n.isdigit()]))
        elif(site_url == 'www.al.to'):
            name = site_content.find(attrs={'class':'sc-1x6crnh-5'}).get_text()
            price = int(site_content.find(attrs={'class':'u7xnnm-4 gHPNug'}).get_text().split(',')[0].replace(" ",''))
        elif(site_url == 'www.mediamarkt.pl'):
            price = int(site_content.find(attrs={'itemprop':'price'}).get_text())
        elif(site_url == 'www.empik.com'):
            price = int(site_content.find(attrs={'class':'productPriceInfo__price ta-price withoutLpPromo'}).get_text().split(",")[0].strip())
        elif(site_url == 'www.morele.net'):
            try:
                price = int(site_content.find('div','price-new').get_text().split(',')[0].replace(" ",''))
            except:
                price = site_content.find('div','price-new').get_text()
                price = int(''.join([n for n in price if n.isdigit()]))
        elif(site_url == 'www.euro.com.pl'):
            price = site_content.find('div','price-normal selenium-price-normal').get_text()
            price = int(''.join([n for n in price if n.isdigit()]))
        elif(site_url == 'www.mediaexpert.pl'):
            price = int(site_content.find('span','a-price_price').findNext('span','a-price_price').get_text().replace(" ",""))
        elif(site_url == 'www.amazon.de'):
            price = int(site_content.find('span','a-size-medium a-color-price priceBlockBuyingPriceString').get_text().split(',')[0].replace(".","")) * euro
        else:
            print("Site not supported: "+ site_url)
        # print("{} -> {}".format(link.split('/')[2],price))
    except:
        print(link)

def main():
    items()
    # link = list["Macbook AIR"]["2019"]["Space grey"]["128"][0]
    data = {}
    for a in list:
        for b in list[a]:
            for c in list[a][b]:
                for d in list[a][b][c]:
                    min = 10000
                    print("{} {} {} {}GB".format(a,b,c,d))
                    for e in list[a][b][c][d]:
                        check_price(e)
                        if(min>price):
                            min = price
                            min_link = e
                    print("{} -> {}".format(min_link.split('/')[2],min))
                    data["{} {} {} {}GB".format(a,b,c,d)] = [min,min_link]
    comp(data)

# test_data = {"Macbook AIR 2019 Space grey 128GB": [4900, "https://www.x-kom.pl/p/506277-notebook-laptop-133-apple-macbook-air-i5-8gb-128-uhd-617-mac-os-space-grey.html"], "Macbook AIR 2019 Space grey 256GB": [5649, "https://www.x-kom.pl/p/506278-notebook-laptop-133-apple-macbook-air-i5-8gb-256-uhd-617-mac-os-space-grey.html"], "Macbook AIR 2019 Silver 128GB": [4999, "https://www.morele.net/laptop-apple-macbook-air-13-3-2019-srebrny-mvfk2ze-a-6116788/"], "Macbook AIR 2019 Silver 256GB": [5097, "https://www.mediamarkt.pl/komputery-i-tablety/laptop-apple-macbook-air-13-retina-i5-8gb-256gb-ssd-macos-srebrny-mrec2ze-a"], "Macbook PRO 2019 Space grey 128GB": [5699, "https://www.euro.com.pl/laptopy-i-netbooki/apple-laptop-mbp-tb-i5-8gb-128ssd-space-grey.bhtml"], "Macbook PRO 2019 Silver 128GB": [5649, "https://www.euro.com.pl/laptopy-i-netbooki/apple-laptop-mbp-tb-i5-8gb-128ssd-silver.bhtml"], "Macbook PRO 2017 Space grey 128GB": [4797, "https://www.mediamarkt.pl/komputery-i-tablety/laptop-apple-macbook-pro-13-3-i5-8gb-128gb-ssd-iris-plus-640-macos-srebrny-mpxr2ze-a"], "Macbook PRO 2017 Silver 128GB": [4797, "https://www.mediamarkt.pl/komputery-i-tablety/laptop-apple-macbook-pro-13-3-i5-8gb-128gb-ssd-iris-plus-640-macos-gwiezdna-szarosc-mpxq2ze-a"], "Macbook PRO 2017 Silver 256GB": [5599, "https://www.euro.com.pl/laptopy-i-netbooki/apple-macbook-pro-13-13-3-intel-core-i5-7360u-8gb-ram-256gb-dysk-os-x-sierra.bhtml"]}
# test_comp = {"Macbook AIR 2019 Space grey 128GB": [4900, "https://www.x-kom.pl/p/506277-notebook-laptop-133-apple-macbook-air-i5-8gb-128-uhd-617-mac-os-space-grey.html"],"Macbook AIR 2019 Space grey 124GB": [41230, "https://www.x-kom.pl/p/506277-notebook-laptop-133-apple-macbook-air-i5-8gb-128-uhd-617-mac-os-space-grey.html"]}

def comp(data):
    with open('prices.json','r') as file:
        json_data = json.loads(file.read())
        lower = False
        higher = False
        body = {}
        for item in json_data:
            if(data[item][0] < json_data[item][0]):
                body[item] = [json_data[item][0],data[item][0],data[item][1]]
                lower = True
            elif(data[item][0] > json_data[item][0]):
                body[item] = [data[item][0],json_data[item][0],data[item][1]]
                higher = True
        if(lower):
            print("Lower price")

            with open('prices.json','w') as file:
                json.dump(data,file)

            send_mail(body)
            print("Update completed")
        elif(higher):
            print("Higher price")

            with open('prices.json','w') as file:
                json.dump(data,file)
        else:
            print("No changes")

if __name__ == '__main__':
    main()
