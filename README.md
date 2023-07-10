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


## 5. Endpoint-uri

FastAPI_Scrap are trei endpoint-uri principale pe care le puteți folosi pentru a interacționa cu aplicația.

### 5.1 /scrap_data/

Acest endpoint inițiază procesul de scraping al datelor. Trebuie să faceți un request la `127.0.0.1:80/scrap_data/` cu datele necesare pentru a demara procesul.

Atunci când un request este primit, fiecare link din pagina web inițiază un task separat. Aceste task-uri sunt salvate în baza de date pentru a evita rularea de mai multe ori a aceluiași task. În timpul procesului de scraping, FastAPI_Scrap selectează informațiile necesare și, dacă sunt disponibile, alte link-uri din pagina web. Aceste noi link-uri devin la rândul lor task-uri separate, creând astfel un flux de lucru recursiv.

Acest proces recursiv continuă până când se ajunge la un "nod" (sau link) ale cărui informații au fost deja scrapuite sau când "rankul" acestui nod este egal cu rankul maxim specificat. În acest moment, procesul de scraping pentru acel nod se oprește.


### 5.2 /merge_data

După ce datele au fost scrapuite, puteți utiliza acest endpoint pentru a combina datele colectate cu cele existente în fișierele CSV. Faceți un request la `127.0.0.1:80/merge_data`.

### 5.3 /get_company_profile

Acest endpoint este utilizat pentru a căuta și recupera profilurile companiilor. Faceți un request la `127.0.0.1:80/get_company_profile` pentru a căuta un profil.

### 6. Accesare external services
127.0.0.1:5555 flower pentru a monitoriza workerii username: admin parola Teilor.24
127.0.0.1: 5601 kibana
