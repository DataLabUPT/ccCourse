## Demo Google App Engine

Scop: aplicatia gestioneaza o galerie foto. Utilizeaza Vision API si Translation API
pentru a adauga TAG-uri automat pe imaginile urcate. 

Cod adaptat din repo oficial de exemple GCP - 
[Photo Album Example](https://github.com/GoogleCloudPlatform/appengine-photoalbum-example/tree/master)

Aplicatia este scrisa utilizand limbajul de programare Python si utilizeaza din GCP produsele:
[App Engine](https://cloud.google.com/appengine/docs), 
[Cloud Vision API](https://cloud.google.com/vision/), 
[Cloud Translation API](https://cloud.google.com/translate/).

Urmati pasii pentru a lansa aplicatia in GCP.

#### Pas 1. Creati un proiect nou 
Pentru a permite curatarea completa a resurselor utilizate este recomandata crearea unui proiect nou.<br>
*Obs!* App Engine nu permite stergerea aplicatiei default, doar dezactivarea - 
[link](https://cloud.google.com/appengine/docs/standard/python3/building-app/cleaning-up)<br>
Creati un proiect nou de la adresa: [link](https://console.cloud.google.com/cloud-resource-manager)

#### Pas 2. Accesati Cloud Shell
Puteti utiliza Cloud Shell din Google Cloud PLatform sau terminalul propriu. 
In a doua varianta aveti nevoie de [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) 
si [gcloud](https://cloud.google.com/sdk/docs/install) instalate si configurate.

#### Pas 3. Descarcati fisierele
Puteti utiliza comanda git clone. Modificati directorul de lucru catre appEngine.
```
git clone https://github.com/DataLabUPT/ccCourse.git
cd ccCourse/appEngine
```

#### Pas 4. Obtineti project-id
Pentru a lansa aplicatia in cadrul propriului proiect aveti nevoie de project-id. <br>
Il puteti obtine ruland comanda:
```
gcloud projects list
```

#### Pas 5. Setare ID proiect
Setati ID proiect in sesiunea de lucru.<br> 
Specificati project-id obtinut in pasul precedent modificand urmatoarea comandata. 
```
gcloud config set project [PROJECT_ID]
```

#### Pas 6. Activare APIs
Se activeaza API-urile utilizate in aplicatie utilizand urmatoarea comanda:
```
gcloud services enable vision.googleapis.com translate.googleapis.com
```

#### Pas 7. Lansare aplicatie
Se creaza aplicatia App Engine in cadrul proiectului.
```
gcloud app create --region=europe-west1
```

Se creaza index in Datastore ce pastreaza informatia despre fotografiile urcate.
```
gcloud datastore indexes create index.yaml
```

Lansarea aplicatiei de gestiune galerie foto ca si serviciu in aplicatia App Engine 
creata anterior.
```
gcloud app deploy app.yaml
```

Prin executarea acestor comenzi in Cloud Shell, se lanseaza aplicatia in proiectul 
ce are identificatorul project-id si aceasta devine accesibila la o adresa similara: 
`https://<project id>.appspot.com`.

#### Pas 8. Clean-up
Pentru a ne asigura ca toate resursele sunt eliberate (inclusiv instanta de App Engine) 
se sterge proiectul de la adresa [link](https://console.cloud.google.com/cloud-resource-manager) 

