from bs4 import BeautifulSoup
import requests
from itertools import cycle
from datetime import date, timedelta, datetime
import pyodbc

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
urlBase = 'https://www.toctoc.com/resultados/lista/arriendo/departamento/?moneda=2&precioDesde=0&precioHasta=0&dormitoriosDesde=&dormitoriosHasta=&banosDesde=0&banosHasta=0&estado=0&disponibilidadEntrega=&numeroDeDiasTocToc=0&superficieDesdeUtil=0&superficieHastaUtil=0&superficieDesdeConstruida=0&superficieHastaConstruida=0&superficieDesdeTerraza=0&superficieHastaTerraza=0&superficieDesdeTerreno=0&superficieHastaTerreno=0&ordenarPor=5&pagina=1&paginaInterna='
urlBase2 = '&zoom=15&idZonaHomogenea=0&atributos=&texto=Regi%C3%B3n%20Metropolitana%20De%20Santiago,%20Chile&viewport=-34.29093141874961,-71.76629357236627,-32.9224065438268,-69.71863874030997&idPoligono=2240&publicador=0&temporalidad=0'
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
            table_tr2 = soup.find('div',class_='resul')

            if (table_tr2 == None):
                raise Exception('Bloqueado')

        except Exception as e:
            #Most free proxies will often get connection errors. You will have retry the entire request using another proxy to work. 
            #We will just skip retries as its beyond the scope of this tutorial and we are only downloading a single url 
            print(f"Skipping. Connnection error: {e}")   
        else:
            exito = True    
            print(f"Successfully connected, number of tries: {i}")  
            print(f"Proxy: {proxy}")
        i+=1
        if i > 50:
            exito = True  
    return table_tr2

conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                      "Server=localhost,1433;"
                      "Database=ProyectoIngenieriaDatos2;"
                      "uid=sa;"
                      "pwd=myPass123word")

cursor = conn.cursor()   
# try:
#     stop = False
#     pagina = 1
#     fechaInicio = datetime.now()

#     while stop == False:
#         url = f"{urlBase}{pagina}{urlBase2}"
#         data = scrap(url)

#         print(f"Comenzando scraping, página: {pagina}")
#         for datos in data:
pagina = 1
url = f"{urlBase}{pagina}{urlBase2}"
print(scrap(url))