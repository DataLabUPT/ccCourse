# Example K3S Cluster Demo
This is a simple example of how to create a K3S cluster using VMs on Google Cloud Platform (GCP).

## Prerequisites

- [Google Cloud CLI](https://cloud.google.com/sdk/docs/install) installed and configured.

## Build Cluster

Steps:

- Create a new project on GCP.

```bash
gcloud projects create --name="K3S Demo Project"
```
- Set the project ID in the current session.

```bash
project_id=$(gcloud projects list | grep K3S | awk '{print $1; exit}')
gcloud config set project $project_id
```
- Enable the necessary APIs.

```bash
gcloud services enable compute.googleapis.com
```

<!-- - Generate an SSH key pair.

```bash
ssh-keygen -f ./k3s-demo-key -t rsa -N ""
``` -->
- Create Egress rule to allow all traffic

```bash
gcloud compute firewall-rules create allowallegr --direction=EGRESS --priority=1000 --network=default --action=ALLOW --rules=all --destination-ranges=0.0.0.0/0
```

- Create Ingress rule to allow all traffic

```bash
gcloud compute firewall-rules create allowalling --direction=INGRESS --priority=1000 --network=default --action=ALLOW --rules=all --destination-ranges=0.0.0.0/0
```



- Create a VM instance for the K3S master

```bash
gcloud compute instances create k3s-master \
    --machine-type=e2-medium \
    --create-disk=auto-delete=yes,boot=yes,image=projects/debian-cloud/global/images/debian-12-bookworm-v20240415,mode=rw,size=10
```

- Create prefix for running commands on the master.

```bash
k3s_master_do="gcloud compute ssh k3s-master --command"
```

- Install K3S on the master

```bash
$k3s_master_do 'curl -sfL https://get.k3s.io | sh - '
```

- Get K3S token

```bash
k3s_token=$($k3s_master_do 'sudo cat /var/lib/rancher/k3s/server/node-token')
```

- Create a VM instance for the K3S worker

```bash
gcloud compute instances create k3s-worker-1 \
    --machine-type=e2-micro \
    --create-disk=auto-delete=yes,boot=yes,image=projects/debian-cloud/global/images/debian-12-bookworm-v20240415,mode=rw,size=10
```

- Install/Join K3S on the worker

```bash
# Get the IP address of the master
k3s_master_ip=$(gcloud compute instances describe k3s-master --format='get(networkInterfaces[0].accessConfigs[0].natIP)')
k3s_worker_do="gcloud compute ssh k3s-worker-1 --command"
$k3s_worker_do "curl -sfL https://get.k3s.io | K3S_URL=https://$k3s_master_ip:6443 K3S_TOKEN=$k3s_token sh -"
```

- [Optional] Install/Join your machine as a worker node

```bash
curl -sfL https://get.k3s.io | K3S_URL=https://$k3s_master_ip:6443 K3S_TOKEN=$k3s_token sh -
```


## Deploy a sample application on cluster

- Copy sample aplication to cluster

```bash
$k3s_master_do 'sudo kubectl apply -f -' < sample-app.yaml
```
