from bs4 import BeautifulSoup
import requests
from itertools import cycle
import time

urlProxy = 'https://free-proxy-list.net/'

headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'referrer': 'https://google.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Pragma': 'no-cache',
    }

# def rowgetDataText(tr, coltag='td'): # td (data) or th (header)       
#     return [td.get_text(strip=True) for td in tr.find_all(coltag)] 

def extract_proxies():
    proxies = set()
    html_text = requests.get(urlProxy).text
    soup = BeautifulSoup(html_text, 'html.parser')
    table_tr = soup.find('table',class_='table table-striped table-bordered').findAll("tr")
    for row in table_tr:
        try:
            https = row.findAll("td")[6].text.strip()
            ip = row.findAll("td")[0].text.strip()
            port = row.findAll("td")[1].text.strip()
            if https == "yes":
                proxy = f"http://{ip}:{port}"
                proxies.add(proxy)
        except:
            print("Head")  
    return proxies

## tenia error en que la lista estaba fuera de indice, porque se agrega la columna de head
proxies = extract_proxies()  
proxy_pool = cycle(proxies)
#url = 'https://www.yapo.cl/region_metropolitana/arrendar?ca=15_s&l=0&w=1&cmn=&ret=1'
urlBase = 'https://www.yapo.cl/region_metropolitana/arrendar?ca=15_s&ret=1&cg=1240&o='

def scrap(url):
    exito = False
    i = 1
    while exito== False:
        #Get a proxy from the pool
        proxy = next(proxy_pool)
        print("Request #%d"%i)
        try:
            html_text = requests.get(url, headers = headers, proxies={"http": proxy, "https": proxy}).text
            soup = BeautifulSoup(html_text, 'html.parser')
            table_tr2 = soup.find('table',class_='listing_thumbs').findAll("tr")
        except:
            #Most free proxies will often get connection errors. You will have retry the entire request using another proxy to work. 
            #We will just skip retries as its beyond the scope of this tutorial and we are only downloading a single url 
            print("Skipping. Connnection error")   
        else:
            exito = True    
            print(f"Successfully connected, number of tries: {i}")  
            print(f"Proxy: {proxy}")
        i+=1
        if i > 20:
            exito = True  
    return table_tr2

stop = False
pagina = 1

while stop == False:
    url = f"{urlBase}{pagina}"
    data = scrap(url)

    print(f"Comenzando scraping, página: {pagina}")
    for datos in data:
        try:
            fecha = datos.findAll('td')[0].find('span').text.strip()
            urlPub = datos.findAll('td')[0].find('a', href= True)
            #print(datos.findAll("td")[4])
            if(fecha != "Hoy" and fecha != "Ayer"):
                print("Finalizando scraping")
                stop = True
                break
            print(f"Fecha: {fecha}")
            print(f"Url: {urlPub['href']}")
            print(f"Precio: {datos.findAll('td')[2].find('span', class_='price').text.strip()}")
            print(f"Dormitorios: {datos.findAll('td')[2].find('div', class_='icons').findAll('span')[0].text.strip()}")
            print(f"Baños: {datos.findAll('td')[2].find('div', class_='icons').findAll('span')[1].text.strip()}")
            print(f"Comuna: {datos.findAll('td')[3].find('span', class_='commune').text.strip()}")
        except:
            print("no data")    
    pagina += 1            