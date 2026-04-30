# Лабораторная работа №6

Тема: Kustomize и Helm.

В этой лабораторной приложение из lab_5 запускается в Kubernetes двумя
способами: через Kustomize и через Helm. PostgreSQL вынесен отдельно от
приложения, чтобы не смешивать инфраструктуру и код сервиса.

## Структура

```text
lab_6/
  infra/  # PostgreSQL
  app/    # task-model
```

В `infra/` лежит база данных PostgreSQL:

- `StatefulSet`
- Headless Service
- Secret
- PVC

В `app/` лежит приложение `task-model`:

- Deployment
- Service
- ConfigMap
- Secret с `DATABASE_URL`

Обе части описаны в двух вариантах:

```text
k8s/kustomization/
k8s/helm/
```

## Запуск через Kustomize

Сначала запускается инфраструктура:

```bash
cd lab_6/infra
kubectl apply -k k8s/kustomization/overlays/dev
```

Потом приложение:

```bash
cd ../app
kubectl apply -k k8s/kustomization/overlays/dev
```

Проверка:

```bash
kubectl get pods,pvc,svc -n lab6-dev
curl http://localhost:30081/health
curl http://localhost:30081/task
```

## Запуск через Helm

Сначала запускается инфраструктура:

```bash
cd lab_6/infra
helm upgrade --install task-model-db ./k8s/helm/postgres-infra \
  --namespace lab6-dev --create-namespace \
  -f ./k8s/helm/postgres-infra/values-dev.yaml
```

Потом приложение:

```bash
cd ../app
helm upgrade --install task-model-app ./k8s/helm/task-model-app \
  --namespace lab6-dev --create-namespace \
  -f ./k8s/helm/task-model-app/values-dev.yaml
```

Проверка:

```bash
kubectl get pods,pvc,svc -n lab6-dev
curl http://localhost:30081/health
curl http://localhost:30081/task
```

## Результат проверки

Kustomize и Helm были проверены локально в Docker Desktop Kubernetes.

После запуска в namespace `lab6-dev` были созданы:

```text
pod/postgres-0
pod/task-model-...
persistentvolumeclaim/postgres-data-postgres-0
service/postgres
service/task-model-service
```

Проверка приложения:

```text
curl http://localhost:30081/health
{"status": "ok", "service": "task-model"}

curl http://localhost:30081/task
{"id": 6, "description": "Task from lab_6 Helm dev values", "priority": 4, "status": "new", ...}
```

## Очистка

Удалить все ресурсы лабораторной:

```bash
kubectl delete namespace lab6-dev
```

Эта команда удаляет Pod, Service, Secret, ConfigMap и PVC из namespace
`lab6-dev`.
