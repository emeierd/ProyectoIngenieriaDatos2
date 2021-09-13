from bs4 import BeautifulSoup
import requests
from itertools import cycle
from datetime import date, timedelta
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

unouno = False
dosuno = False
tresuno = False
cuatrouno = False
cincouno = False
unodos = False
dosdos = False
tresdos = False
cuatrodos = False
cincodos = False
unotres = False
dostres = False
trestres = False
cuatrotres = False
cincotres = False

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
            dormitorios = datos.findAll('td')[2].find('div', class_='icons').findAll('span')[0].text.strip()
            baños = datos.findAll('td')[2].find('div', class_='icons').findAll('span')[1].text.strip()
            if(dormitorios == "1" and baños == "1"):
                unouno = True
            if(dormitorios == "2" and baños == "1"):
                dosuno = True
            if(dormitorios == "3" and baños == "1"):
                tresuno = True
            if(dormitorios == "4" and baños == "1"):
                cuatrouno = True
            if(dormitorios == "5" and baños == "1"):
                cincouno = True
            if(dormitorios == "1" and baños == "2"):
                unodos = True        
            if(dormitorios == "2" and baños == "2"):
                dosdos = True   
            if(dormitorios == "3" and baños == "2"):
                tresdos = True   
            if(dormitorios == "4" and baños == "2"):
                cuatrodos = True   
            if(dormitorios == "5" and baños == "2"):
                cincodos = True    
            if(dormitorios == "1" and baños == "3"):
                unotres = True     
            if(dormitorios == "2" and baños == "3"):
                dostres = True     
            if(dormitorios == "3" and baños == "3"):
                trestres = True     
            if(dormitorios == "4" and baños == "3"):
                cuatrotres = True     
            if(dormitorios == "5" and baños == "3"):
                cincotres = True                                             
        except:
            print("no data")    
    pagina += 1       

conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                      "Server=localhost,1433;"
                      "Database=ProyectoIngenieriaDatos2;"
                      "uid=sa;"
                      "pwd=myPass123word")

cursor = conn.cursor()    

if unouno:
    query = f"INSERT INTO d_departamento (dormitorios, baños) values(1,1)"
    cursor.execute(query)
if dosuno:
    query = f"INSERT INTO d_departamento (dormitorios, baños) values(2,1)"
    cursor.execute(query)
if tresuno:
    query = f"INSERT INTO d_departamento (dormitorios, baños) values(3,1)"
    cursor.execute(query)
if cuatrouno:
    query = f"INSERT INTO d_departamento (dormitorios, baños) values(4,1)"
    cursor.execute(query)
if cincouno:
    query = f"INSERT INTO d_departamento (dormitorios, baños) values(5,1)"
    cursor.execute(query)
if unodos:
    query = f"INSERT INTO d_departamento (dormitorios, baños) values(1,2)"
    cursor.execute(query)
if dosdos:
    query = f"INSERT INTO d_departamento (dormitorios, baños) values(2,2)"
    cursor.execute(query)
if tresdos:
    query = f"INSERT INTO d_departamento (dormitorios, baños) values(3,2)"
    cursor.execute(query)
if cuatrodos:
    query = f"INSERT INTO d_departamento (dormitorios, baños) values(4,2)"
    cursor.execute(query)
if cincodos:
    query = f"INSERT INTO d_departamento (dormitorios, baños) values(5,2)"
    cursor.execute(query)
if unotres:
    query = f"INSERT INTO d_departamento (dormitorios, baños) values(1,3)"
    cursor.execute(query)
if dostres:
    query = f"INSERT INTO d_departamento (dormitorios, baños) values(2,3)"
    cursor.execute(query)
if trestres:
    query = f"INSERT INTO d_departamento (dormitorios, baños) values(3,3)"
    cursor.execute(query)
if cuatrotres:
    query = f"INSERT INTO d_departamento (dormitorios, baños) values(4,3)"
    cursor.execute(query)
if cincotres:
    query = f"INSERT INTO d_departamento (dormitorios, baños) values(5,3)"
    cursor.execute(query)

conn.commit()    