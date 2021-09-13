import pyodbc
from bs4 import BeautifulSoup
import requests
from itertools import cycle
from datetime import date, timedelta

urlProxy = 'https://free-proxy-list.net/'

headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'referrer': 'https://google.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Pragma': 'no-cache',
    }

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


proxies = extract_proxies()  
proxy_pool = cycle(proxies)
urlBase = 'https://es.wikipedia.org/wiki/Anexo:Comunas_de_Santiago_de_Chile'

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
            table_tr2 = soup.findAll('table')[5].tbody
        except Exception as e:
            #Most free proxies will often get connection errors. You will have retry the entire request using another proxy to work. 
            #We will just skip retries as its beyond the scope of this tutorial and we are only downloading a single url 
            print(e)
            print("Skipping. Connnection error")   
        else:
            exito = True    
            print(f"Successfully connected, number of tries: {i}")  
            print(f"Proxy: {proxy}")
        i+=1
        if i > 20:
            exito = True  
    return table_tr2


conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                      "Server=localhost,1433;"
                      "Database=ProyectoIngenieriaDatos2;"
                      "uid=sa;"
                      "pwd=myPass123word")

data = scrap(urlBase)
cursor = conn.cursor()

for row in data:
    try:
        comuna = row.findAll("td")[0].text.strip()
        sector = row.findAll("td")[1].text.strip()
        query = f"INSERT INTO d_comuna values('{comuna}','{sector}',0)"
        cursor.execute(query)
        print(f"Comuna: {comuna}")
        print(f"Sector: {sector}")
        print("")
    except Exception as e:    
        print(e)


conn.commit()        