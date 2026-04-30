# Лабораторная работа №7

Тема: observability, Prometheus, Grafana и Tempo.

В этой лабораторной сделан отдельный сервис `task-model` с метриками и
трейсингом.

## Структура

```text
lab_7/
  app/             # приложение task-model
  observability/   # Prometheus, Grafana, Tempo
  docs/screenshots # скриншоты для отчёта
```

Приложение отдаёт:

- `/health` — проверка работы сервиса
- `/task` — данные задачи
- `/metrics` — метрики Prometheus

## Локальный запуск

Из папки `lab_7`:

```bash
docker compose up -d --build
```

Проверка приложения:

```bash
curl http://localhost:8080/health
curl http://localhost:8080/task
curl http://localhost:8080/metrics
```

Сервисы:

```text
Prometheus: http://localhost:19090
Grafana:    http://localhost:13001
Tempo:      http://localhost:13200
```

Логин и пароль Grafana:

```text
admin / admin
```

## Что проверить

В Prometheus:

```text
Status -> Targets
```

Ожидается, что jobs `prometheus` и `task-model-lab7` в состоянии `UP`.

В Grafana:

```text
Dashboards -> Lab7 -> Task Model Lab7
```

На дашборде должны быть графики по HTTP-запросам, latency и бизнес-метрика
по количеству ответов `/task`.

Для Tempo:

```text
Explore -> Tempo
```

После нескольких запросов к API должны появиться trace-ы сервиса
`task-model-lab7`.

## Нагрузка для проверки

```bash
for i in {1..10}; do
  curl http://localhost:8080/task
done
```

## Kubernetes

Сначала нужно собрать локальный Docker-образ:

```bash
cd lab_7/app
docker build -t task-model-lab7:local .
```

Запуск приложения:

```bash
kubectl apply -k k8s
```

Запуск Tempo:

```bash
cd ../observability
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/tempo-configmap.yaml
kubectl apply -f k8s/tempo-deployment.yaml
kubectl apply -f k8s/tempo-service.yaml
```

Prometheus Operator устанавливается через Helm:

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm upgrade --install prometheus prometheus-community/kube-prometheus-stack \
  --namespace observability --create-namespace \
  -f helm-values-kube-prometheus-stack.yaml
```

ServiceMonitor для приложения:

```bash
kubectl apply -f k8s/servicemonitor-task-model.yaml -n lab7-app
```

Проверка приложения в Kubernetes:

```bash
curl http://localhost:30083/health
curl http://localhost:30083/task
curl http://localhost:30083/metrics
```

## Скриншоты для отчёта

Скриншоты сохранены в `docs/screenshots/`:

- [prometheus-targets.png](docs/screenshots/prometheus-targets.png) — Prometheus Targets, jobs `prometheus` и `task-model-lab7` в состоянии `UP`
- [grafana-dashboard.png](docs/screenshots/grafana-dashboard.png) — dashboard `Task Model Lab7`
- [tempo-trace.png](docs/screenshots/tempo-trace.png) — Grafana Explore с trace-ами `GET /task` из Tempo

## Результат проверки

Локальный запуск через Docker Compose проверен.

```text
curl http://localhost:8080/health
{"status": "ok", "service": "task-model-lab7"}

curl http://localhost:8080/task
{"id": 7, "description": "Task from lab_7 Docker Compose", "priority": 4, "status": "new", ...}
```

В `/metrics` есть метрики:

```text
task_model_http_requests_total
task_model_http_request_duration_seconds
task_model_task_responses_total
```

Prometheus собирает метрики приложения, Grafana показывает dashboard, Tempo
показывает trace-ы запросов к `/task`.

## Очистка

Docker Compose:

```bash
docker compose down
```

Kubernetes:

```bash
kubectl delete namespace lab7-app
kubectl delete namespace observability
```
