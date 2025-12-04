#!/usr/bin/env bash
set -euo pipefail

# Teardown helper: delete k8s resources in this folder and optionally delete the local cluster
# Usage: ./teardown.sh [-c kind|minikube] [-n CLUSTER_NAME] [--delete-cluster]

CLUSTER="kind"
CLUSTER_NAME="microservices-demo"
DELETE_CLUSTER=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    -c|--cluster)
      CLUSTER="$2"; shift 2;;
    -n|--name)
      CLUSTER_NAME="$2"; shift 2;;
    --delete-cluster)
      DELETE_CLUSTER=1; shift;;
    -h|--help)
      echo "Usage: $0 [-c kind|minikube] [-n cluster-name] [--delete-cluster]"; exit 0;;
    *) echo "Unknown arg: $1"; exit 1;;
  esac
done

echo "Deleting Kubernetes resources in namespace 'microservices-demo' (if present)"
kubectl delete -f hpa.yaml -n microservices-demo --ignore-not-found || true
kubectl delete -f product-service-nodeport.yaml -n microservices-demo --ignore-not-found || true
kubectl delete -f product-service.yaml -n microservices-demo --ignore-not-found || true
kubectl delete -f user-service.yaml -n microservices-demo --ignore-not-found || true
kubectl delete -f orders-service.yaml -n microservices-demo --ignore-not-found || true
kubectl delete -f reviews-service.yaml -n microservices-demo --ignore-not-found || true
kubectl delete -f 00-namespace-config-secrets.yaml --ignore-not-found || true

if [[ "$DELETE_CLUSTER" -eq 1 ]]; then
  if [[ "$CLUSTER" == "kind" ]]; then
    if command -v kind >/dev/null 2>&1; then
      echo "Deleting kind cluster '${CLUSTER_NAME}'..."
      kind delete cluster --name "${CLUSTER_NAME}" || true
    else
      echo "kind not found; cannot delete cluster"
    fi
  elif [[ "$CLUSTER" == "minikube" ]]; then
    if command -v minikube >/dev/null 2>&1; then
      echo "Deleting minikube cluster '${CLUSTER_NAME}'..."
      minikube delete -p "${CLUSTER_NAME}" || true
    else
      echo "minikube not found; cannot delete cluster"
    fi
  fi
fi

echo "Teardown complete."
