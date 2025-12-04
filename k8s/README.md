Kubernetes Manifests for ecommerce-microservices

This folder contains Kubernetes manifests for the ecommerce microservices example. The manifests are intended for local development and demonstration on a single-node Kubernetes cluster (Minikube or Kind). They provide namespace, deployments, Services, ConfigMaps, Secrets, and HPA resources for the following services:

- `orders-service` (manifests: `orders-service.yaml`)
- `product-service` (manifests: `product-service.yaml`, `product-service-nodeport.yaml`)
- `reviews-service` (manifests: `reviews-service.yaml`)
- `user-service` (manifests: `user-service.yaml`)
- cluster-level helper: `00-namespace-config-secrets.yaml` (namespace, ConfigMaps, Secrets)
- `hpa.yaml` (HorizontalPodAutoscaler resources)

**Note:** This README documents how to deploy these manifests locally and how to verify basic networking, scaling (HPA), and service discovery.

**Quick file overview:**
- `00-namespace-config-secrets.yaml` : Creates the `ecommerce` namespace and includes shared ConfigMaps and Secrets used by services.
- `*-service.yaml` : Deployment + ClusterIP Service for each microservice.
- `product-service-nodeport.yaml` : NodePort variant for `product-service` (useful for direct access from the host/Minikube).
- `hpa.yaml` : HPA definitions for the deployments (requires metrics-server).

**Assumptions**
- Each service image name/tag referenced in the manifests matches a locally built Docker image or an image available in a registry accessible to your cluster.
- Services listen on ports defined in each service manifest (see service YAMLs for exact ports).

## Prerequisites
- `kubectl` installed and configured.
- Either `minikube` (recommended for beginners) or `kind` for a lightweight cluster.
- `docker` available when building images locally.
- `metrics-server` installed in the cluster for HPA to work.

## Kind Local Setup

```bash
kind create cluster --name microservices-demo
```

## Build images locally

```bash
docker build -t product-service:latest ./product_service
docker build -t user-service:latest ./user_service
docker build -t orders-service:latest ./orders_service
docker build -t reviews-service:latest ./reviews_service
```

## Load images into kind cluster

```bash
kind load docker-image product-service:latest --name microservices-demo
kind load docker-image user-service:latest --name microservices-demo
kind load docker-image orders-service:latest --name microservices-demo
kind load docker-image reviews-service:latest --name microservices-demo
```

## Recommended local setups

1) Minikube (easy local Docker image build + NodePort access):

```bash
minikube start --driver=docker
eval "$(minikube -p minikube docker-env)"
# Build images locally so the cluster can use them
docker build -t user-service:local ./user_service
docker build -t product-service:local ./product_service
docker build -t reviews-service:local ./reviews_service
docker build -t orders-service:local ./orders_service
```

Then apply manifests (see Apply Manifests below).

2) Kind (isolated cluster; load images into the Kind node):

```bash
# create cluster
kind create cluster --name microservices-demo
# build images (on host) and load into kind
docker build -t user-service:local ./user_service
kind load docker-image user-service:local --name microservices-demo
# repeat for other services
```

## Apply manifests

1) Create namespace, ConfigMaps, Secrets first (this file creates namespace `microservices-demo`):

```bash
kubectl apply -f 00-namespace-config-secrets.yaml
```

2) Deploy services and supporting resources (from this folder):

```bash
kubectl apply -f orders-service.yaml
kubectl apply -f product-service.yaml
kubectl apply -f product-service-nodeport.yaml   # optional, for NodePort access
kubectl apply -f reviews-service.yaml
kubectl apply -f user-service.yaml
kubectl apply -f hpa.yaml
```

Tip: You can apply the whole folder with `kubectl apply -f .` from inside `k8s/`, but creating the namespace first is recommended so other objects target the right namespace.

## Verifications and useful commands
- List namespace resources:

```bash
kubectl get all -n microservices-demo
kubectl get configmap,secret -n microservices-demo
```

- Check pods & logs:

```bash
kubectl get pods -n microservices-demo
kubectl logs -n microservices-demo deployment/user-service
kubectl describe pod -n microservices-demo <pod-name>
```

- Services & endpoints:

```bash
kubectl get svc -n microservices-demo
kubectl get endpoints -n microservices-demo
```

- Port-forward a service locally (example for `user-service` on port 5000):

```bash
kubectl port-forward -n microservices-demo svc/user-service 5000:5000
# then access http://localhost:5000
```

- For NodePort (product-service-nodeport), get the node port and use Minikube IP or your node IP:

```bash
kubectl get svc product-service -n ecommerce
minikube service product-service --url -n ecommerce   # opens the NodePort in minikube
```

## HPA and metrics-server
- HPA requires `metrics-server` to be running in the cluster. To install (Minikube example):

```bash
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
# wait a minute, then check:
kubectl top nodes
kubectl top pods -n ecommerce
```

- Check HPA status:

```bash
kubectl get hpa -n ecommerce
kubectl describe hpa -n ecommerce <hpa-name>
```

## Troubleshooting tips
- If Pods stay in ImagePullBackOff or ErrImagePull, either push images to a registry accessible to the cluster or load the images into the cluster (for Kind use `kind load docker-image`).
- If `kubectl top` shows no metrics, confirm `metrics-server` is running and healthy.
- If services are unreachable, check `kubectl describe svc`, `kubectl get endpoints`, and `kubectl logs` for the relevant pods.

## Suggested next steps
- Add small helper scripts in this folder:
	- `deploy.sh` to build images, load them into the cluster (Kind) or use Minikube's Docker environment, and apply manifests.
	- `teardown.sh` to `kubectl delete -f` the manifests and optionally delete the Kind/Minikube cluster.
- Optionally configure a local image registry mirror to speed up repeated builds.

## Security notes
- The `00-namespace-config-secrets.yaml` file contains sample Secrets for local development. Do not commit real credentials to Git.

## Contact / references
- Kubernetes docs: https://kubernetes.io/docs/
- Kind: https://kind.sigs.k8s.io/
- Minikube: https://minikube.sigs.k8s.io/

If you want, I can: add `deploy.sh`/`teardown.sh`, or try to run this locally (I will need permission to run `kind`/`minikube` and `docker` commands). Let me know which environment you prefer (Minikube or Kind) and I will prepare scripts and run instructions.
# Project Progress - Part 2