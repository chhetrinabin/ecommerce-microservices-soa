Monitoring & Logging (Prometheus, Grafana, Loki)

This subfolder provides lightweight local manifests to run Prometheus, Grafana and a Loki-based logging stack on a local Kubernetes cluster (Kind / Minikube).

What is included
- `prometheus-config.yaml` + `prometheus-deployment.yaml` : Prometheus single-instance with a basic scrape config (static targets). Services must expose `/metrics` for scraping.
- `grafana-datasources.yaml` + `grafana-deployment.yaml` : Grafana, auto-provisioned with Prometheus and Loki datasources. Default admin password: `admin`.
- `loki-config.yaml` + `loki-deployment.yaml` : Loki single-node for log ingestion.
- `promtail-daemonset.yaml` : Promtail daemonset to tail `/var/log/containers/*.log` and push to Loki.

Quick deploy

1) Apply the monitoring manifests (namespace `microservices-demo` must exist):

```bash
kubectl apply -f k8s/monitoring/prometheus-config.yaml
kubectl apply -f k8s/monitoring/prometheus-deployment.yaml
kubectl apply -f k8s/monitoring/loki-config.yaml
kubectl apply -f k8s/monitoring/loki-deployment.yaml
kubectl apply -f k8s/monitoring/promtail-daemonset.yaml
kubectl apply -f k8s/monitoring/grafana-datasources.yaml
kubectl apply -f k8s/monitoring/grafana-deployment.yaml
```

2) Access Grafana (NodePort 32000)

```bash
kubectl -n microservices-demo port-forward svc/grafana 3000:3000
# then open http://localhost:3000 (user: admin, password: admin)
```

Notes & next steps
- Prometheus scrape targets are static in `prometheus-config.yaml`; for production use, enable Kubernetes service discovery or use the Prometheus Operator.
- Instrument your Python services with a Prometheus client (e.g. `prometheus_client`) and expose `/metrics` to get useful metrics.
- Grafana dashboards: import community dashboards for Flask/WSGI, or create custom dashboards using Prometheus queries and Loki logs.
- This stack is intended for local development. For production, prefer the Prometheus Operator (kube-prometheus-stack) and a durable storage backend for Loki.
