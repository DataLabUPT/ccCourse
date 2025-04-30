# Demo K3S Cluster Demo
Acesta este un exemplu ce permite crearea unui cluster [K3S](https://k3s.io/) in masini virtuale in Google Cloud Platform (GCP).

## Necesar
Comenziile vor fi rulate de pe calculatorul local. Sunt necesare:
- [Google Cloud CLI](https://cloud.google.com/sdk/docs/install) instalat si configurat.
- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) instalat

Obs! Urmatoarele comenzii sunt pentru sistemul de operare Linux. Pentru alte sisteme trebuie adaptate.

## Constructia clusterului

Urmati pasii pentru a instala clusterul K3S in 2 masini virtuale si a lansa o aplicatie de test.

#### Pas 1. Descarcati fisierele
Puteti utiliza comanda git clone. Modificati directorul de lucru catre k3sClusterDemo.

```bash
git clone https://github.com/DataLabUPT/ccCourse.git
cd ccCourse/k3sClusterDemo
```

#### Pas 2. Crearea unui proiect nou in GCP
Modificati valoarea pentru nume daca este cazul.

```bash
gcloud projects create --name="K3S Demo Project"
```

#### Pas 3. Project ID
Pentru a lansa clsuterul in cadrul propriului proiect aveti nevoie de project-id.  
Utilizand comenzile de mai jos se obtine id-ul proiectului si se modifica valoarea din sesiunea curenta.

```bash
project_id=$(gcloud projects list | grep K3S | awk '{print $1; exit}')
gcloud config set project $project_id
```

#### Pas 4. Activare API
Se activeaza API pentru a permite lansarea masinilor virtuale prin intermediul comenziilor CLI.

```bash
gcloud services enable compute.googleapis.com
```

#### Pas 5. Regului Firewall
Se creaza regulile din firewall pentru a deschide traficul spre masiniile virtuale (Egress si Ingress).

```bash
gcloud compute firewall-rules create allowallegr --direction=EGRESS --priority=1000 --network=default --action=ALLOW --rules=all --destination-ranges=0.0.0.0/0
```

```bash
gcloud compute firewall-rules create allowalling --direction=INGRESS --priority=1000 --network=default --action=ALLOW --rules=all --destination-ranges=0.0.0.0/0
```

#### Pas 6. Creare VMs si configurare cluster
Se creaza masina virtuala pentru master K3s.

```bash
gcloud compute instances create k3s-master \
    --machine-type=e2-medium \
    --create-disk=auto-delete=yes,boot=yes,image=projects/debian-cloud/global/images/debian-12-bookworm-v20240415,mode=rw,size=10
```

Se pastreaza in variabila k3s_master_do prefixul pentru comenziile ce vor fi rulate pe master.

```bash
k3s_master_do="gcloud compute ssh k3s-master --command"
```

Se instaleaza K3s pe master.

```bash
$k3s_master_do 'curl -sfL https://get.k3s.io | sh - '
```

Pentru a putea configura nodul worker se obtine token-ul din master.

```bash
k3s_token=$($k3s_master_do 'sudo cat /var/lib/rancher/k3s/server/node-token')
```

Se creaza masina virtuala pentru nodul de tip worker.

```bash
gcloud compute instances create k3s-worker-1 \
    --machine-type=e2-micro \
    --create-disk=auto-delete=yes,boot=yes,image=projects/debian-cloud/global/images/debian-12-bookworm-v20240415,mode=rw,size=10
```

Ruland urmatoarele comenzi se obtine IP-ul nodului master, se creaza prefixul pentru comenzi pe nodul worker si se   
intaleaza + configureaza ca worker node utilizand k3s_master_ip si k3s_token. 

```bash
# Get the IP address of the master
k3s_master_ip=$(gcloud compute instances describe k3s-master --format='get(networkInterfaces[0].accessConfigs[0].natIP)')
k3s_worker_do="gcloud compute ssh k3s-worker-1 --command"
$k3s_worker_do "curl -sfL https://get.k3s.io | K3S_URL=https://$k3s_master_ip:6443 K3S_TOKEN=$k3s_token sh -"
```


[Optional] Se poate adauga ca nod de tip worker calculatorul curent.

```bash
curl -sfL https://get.k3s.io | K3S_URL=https://$k3s_master_ip:6443 K3S_TOKEN=$k3s_token sh -
```


#### Pas 7. Lansare aplicatie

Din folderul sample_applications se lanseaza nextcloud.

```bash
$k3s_master_do 'sudo kubectl apply -f -' < sample_applications/sample-app.yaml
```

### Pas 8. Inspectie
Accesand in browser Ip-ul VM-ului master se poate testa ca aplicatia ruleaza. 

Pentru a vizualiza obiectele K8s create putem rula comenziile

```bash
$k3s_master_do 'sudo kubectl get pods'
$k3s_master_do 'sudo kubectl get services'
$k3s_master_do 'sudo kubectl get deployments'
```

#### Pas 8. Clean-up
Pentru a ne asigura ca toate resursele sunt eliberate 
se sterge proiectul de la adresa [link](https://console.cloud.google.com/cloud-resource-manager) 