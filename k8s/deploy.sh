#!/usr/bin/env bash
set -euo pipefail

# Deploy helper for local clusters (Kind or Minikube)
# Usage: ./deploy.sh [-c kind|minikube] [-n CLUSTER_NAME] [--no-build]

CLUSTER="kind"
CLUSTER_NAME="microservices-demo"
NO_BUILD=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    -c|--cluster)
      CLUSTER="$2"; shift 2;;
    -n|--name)
      CLUSTER_NAME="$2"; shift 2;;
    --no-build)
      NO_BUILD=1; shift;;
    -h|--help)
      echo "Usage: $0 [-c kind|minikube] [-n cluster-name] [--no-build]"; exit 0;;
    *) echo "Unknown arg: $1"; exit 1;;
  esac
done

command_exists() { command -v "$1" >/dev/null 2>&1; }

echo "Deploying to cluster type='$CLUSTER' name='$CLUSTER_NAME' (no-build=$NO_BUILD)"

if [[ "$CLUSTER" == "kind" ]]; then
  if ! command_exists kind; then
    echo "kind is required but not found. Install from https://kind.sigs.k8s.io/"; exit 1
  fi
  if ! kind get clusters | grep -q "^${CLUSTER_NAME}$"; then
    echo "Creating kind cluster '${CLUSTER_NAME}'..."
    kind create cluster --name "${CLUSTER_NAME}"
  else
    echo "Kind cluster '${CLUSTER_NAME}' already exists"
  fi
fi

if [[ "$NO_BUILD" -eq 0 ]]; then
  echo "Building Docker images..."
  docker build -t product-service:local ./product_service
  docker build -t user-service:local ./user_service
  docker build -t orders-service:local ./orders_service
  docker build -t reviews-service:local ./reviews_service

  if [[ "$CLUSTER" == "kind" ]]; then
    echo "Loading images into kind cluster '${CLUSTER_NAME}'..."
    kind load docker-image product-service:local --name "${CLUSTER_NAME}"
    kind load docker-image user-service:local --name "${CLUSTER_NAME}"
    kind load docker-image orders-service:local --name "${CLUSTER_NAME}"
    kind load docker-image reviews-service:local --name "${CLUSTER_NAME}"
  elif [[ "$CLUSTER" == "minikube" ]]; then
    if ! command_exists minikube; then
      echo "minikube not found. Install minikube or use kind."; exit 1
    fi
    echo "Using minikube docker-env to build images inside minikube"
    eval "$(minikube -p minikube docker-env)"
    docker build -t product-service:local ./product_service
    docker build -t user-service:local ./user_service
    docker build -t orders-service:local ./orders_service
    docker build -t reviews-service:local ./reviews_service
  fi
else
  echo "Skipping image build/load (--no-build)"
fi

echo "Ensuring metrics-server is installed (required for HPA)..."
kubectl get deployment metrics-server -n kube-system >/dev/null 2>&1 || \
  kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

echo "Applying manifests..."
kubectl apply -f 00-namespace-config-secrets.yaml
kubectl apply -f product-service.yaml
kubectl apply -f product-service-nodeport.yaml || true
kubectl apply -f user-service.yaml
kubectl apply -f orders-service.yaml
kubectl apply -f reviews-service.yaml
kubectl apply -f hpa.yaml || true

echo "Waiting for deployments to become ready (120s timeout each)..."
kubectl -n microservices-demo rollout status deploy/product-service --timeout=120s || true
kubectl -n microservices-demo rollout status deploy/user-service --timeout=120s || true
kubectl -n microservices-demo rollout status deploy/orders-service --timeout=120s || true
kubectl -n microservices-demo rollout status deploy/reviews-service --timeout=120s || true

echo "Deployment finished. Run 'kubectl get all -n microservices-demo' to inspect resources."
