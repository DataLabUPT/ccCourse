## Demo Google Cloud Functions

Scop: functia returneaza un pdf din datele primite in cererea HTTP POST. 
Formatul datelor se gaseste in fisierul rest_call.json

Urmati pasii pentru a lansa functia in cadrul proiectului vostru din GCP.

#### Pas 1. Accesati consola  
Puteti utiliza Cloud Shell din Google Cloud PLatform sau terminalul propriu. 
In a doua varianta aveti nevoie de [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) 
si [gcloud](https://cloud.google.com/sdk/docs/install) instalate si configurate.

#### Pas 2. Descarcati fisierele
Puteti utiliza comanda git clone. Modificati directorul de lucru catre cloudFunction.
```
git clone https://github.com/DataLabUPT/ccCourse.git
cd ccCourse/cloudFunction
```

#### Pas 3. Obtineti project-id
Pentru a lansa functia in cadrul propriului proiect aveti nevoie de project-id. 
Il puteti obtine ruland comanda:
```
gcloud projects list
```

#### Pas 4. Modificati fisierul YAML
In fisierul cloudbuild.yaml inlocuiti \<project-ID\> cu valoare obtinuta in pasul precedent.
Utilizati orice editor doriti (pico, nano, vim).

#### Pas 5. Lansati functia
Activati Cloud Functions si Cloud Build [link](https://cloud.google.com/functions/docs/quickstart-python).<br>
In interfata web a Google Cloud Platform accesati CI/CD > Cloud Build > Settings. 
Activati optiunea pentru Cloud Functions.

Pentru a lansa functia apelati comanda:
```
gcloud builds submit --config cloudbuild.yaml
```

Ca alternativa puteti rula comanda de mai jos inlocuind \<project-ID\> cu valoarea voastra.
```
gcloud functions deploy declaratiepdf --runtime python37 --trigger-http --project <project-ID> --region europe-west1 --allow-unauthenticated
```
Puteti vizualiza functiile active din interfata web sau ruland comanda:
```
gcloud functions list
```

Pentru a permite executia functiei fara autentificare urmati instructiunile de la 
[link](https://cloud.google.com/functions/docs/securing/managing-access-iam#gcloud_4).

Pentru a testa functia puteti utiliza aplicatia [POSTMAN](https://www.postman.com/)

#### Pas 6. Clean-up
Daca nu mai aveti nevoie de functie o puteti sterge utilizand comanda:
```
gcloud functions delete --region europe-west1 declaratiepdf
```
