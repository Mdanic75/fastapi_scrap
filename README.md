# Documentație pentru FastAPI_Scrap

## 1. Descriere Generală

**FastAPI_Scrap** este o aplicație de web scraping creată pentru a extrage și selecta informații specifice din pagini web. A fost dezvoltată utilizând framework-ul FastAPI pentru a crea un server web, împreună cu Celery pentru sarcini asincrone. Aplicația se bazează pe Docker pentru a asigura o implementare ușoară și scalabilă.

## 2. Configurația și Pornirea Aplicației

Pentru a rula FastAPI_Scrap, trebuie să aveți Docker instalat pe sistemul dvs. Dacă nu aveți deja Docker, puteți descărca și instala Docker de pe site-ul oficial Docker.

După instalarea Docker, deschideți un terminal și navigați până în directorul în care se află aplicația FastAPI_Scrap. Introduceți următoarea comandă pentru a porni serverul:

docker-compose up --build --scale worker=2


Această comandă va construi imaginea Docker și va scala aplicația cu doi workeri.

## 3. Utilizarea Aplicației

După ce serverul a fost pornit cu succes, puteți utiliza următoarele puncte finale pentru a interacționa cu aplicația:

1. **Scraping de date:** Faceți un request la `127.0.0.1:80/scrap_data/` cu datele necesare pentru a iniția procesul de scraping.

2. **Fuzionarea datelor:** Odată ce scraping-ul de date a fost completat, puteți utiliza `127.0.0.1:80/merge_data` pentru a combina datele extrase cu datele existente în fișierele CSV.

3. **Căutarea profilurilor companiei:** Utilizați `127.0.0.1:80/get_company_profile` pentru a căuta și a recupera profilurile companiilor.

## 4. Documentația OpenAPI

FastAPI_Scrap include documentație OpenAPI, care oferă un ghid detaliat privind utilizarea fiecărei caracteristici a aplicației. Puteți accesa documentația OpenAPI la următorul URL: `127.0.0.1:80/docs`.


