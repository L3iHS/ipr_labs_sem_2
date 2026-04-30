# Лабораторная работа №5

За основу взята моя Python-лабораторная работа №2 про модель задачи,
дескрипторы и `@property`.

В этой лабораторной к проекту добавлены Docker и GitHub Actions. Это нужно,
чтобы проект можно было автоматически проверить, собрать в Docker-образ и потом
запустить в Kubernetes.

## Что было добавлено

- `Dockerfile` — инструкция для сборки Docker-образа
- `.dockerignore` — список файлов, которые не нужно класть в Docker-образ
- `.github/workflows/ci-cd.yml` — сценарий для GitHub Actions
- `src/server.py` — простой HTTP-сервер для запуска приложения в Kubernetes

## HTTP-сервер

Для Kubernetes приложение должно работать постоянно, а не просто быстро
запускаться и завершаться. Поэтому добавлен небольшой HTTP-сервер.

Доступные endpoints:

- `/health` — проверка, что сервис работает
- `/task` — данные тестовой задачи

Значения задачи можно менять через переменные окружения:

- `TASK_ID`
- `TASK_DESCRIPTION`
- `TASK_PRIORITY`
- `TASK_STATUS`

## Docker

Собрать образ локально:

```bash
docker build -t task-model:local .
```

Запустить приложение:

```bash
docker run --rm -p 8000:8000 task-model:local
```

Проверить, что сервер работает:

```bash
curl http://localhost:8000/health
curl http://localhost:8000/task
```

Запустить приложение со своими настройками задачи:

```bash
docker run --rm -p 8000:8000 \
  -e TASK_DESCRIPTION="Task from Docker" \
  -e TASK_PRIORITY=5 \
  task-model:local
```

Запустить тесты внутри контейнера:

```bash
docker run --rm task-model:local pytest -q --cov=src --cov-report=term-missing
```

## Kubernetes

Манифесты Kubernetes лежат в папке `k8s/`.

Они создают:

- `Namespace` `lab5`
- `ConfigMap` с настройками задачи
- `Secret` с примером секретного значения
- `Deployment` с двумя pod приложения
- `Service` для доступа к приложению через `localhost:30080`

Запустить приложение в Kubernetes:

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

Проверить ресурсы:

```bash
kubectl get all -n lab5
kubectl get pods -n lab5
```

Проверить приложение:

```bash
curl http://localhost:30080/health
curl http://localhost:30080/task
```

Удалить ресурсы:

```bash
kubectl delete namespace lab5
```

---

## Результаты проверки

```bash
kubectl get all -n lab5
```

```text
NAME                              READY   STATUS    RESTARTS   AGE
pod/task-model-69966f8f7f-76kp5   1/1     Running   0          18h
pod/task-model-69966f8f7f-v8tnc   1/1     Running   0          18h

NAME                         TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
service/task-model-service   NodePort   10.99.131.238   <none>        80:30080/TCP   18h

NAME                         READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/task-model   2/2     2            2           18h

NAME                                    DESIRED   CURRENT   READY   AGE
replicaset.apps/task-model-56d894496b   0         0         0       18h
replicaset.apps/task-model-69966f8f7f   2         2         2       18h
```

```bash
kubectl get pods -n lab5
```

```text
NAME                          READY   STATUS    RESTARTS   AGE
task-model-69966f8f7f-76kp5   1/1     Running   0          18h
task-model-69966f8f7f-v8tnc   1/1     Running   0          18h
```

```bash
kubectl get configmap -n lab5
```

```text
NAME                DATA   AGE
kube-root-ca.crt    1      18h
task-model-config   4      18h
```

```bash
kubectl get secret -n lab5
```

```text
NAME                TYPE     DATA   AGE
task-model-secret   Opaque   1      18h
```

```bash
curl http://localhost:30080/health
```

```text
{"status": "ok", "service": "task-model"}
```

```bash
curl http://localhost:30080/task
```

```text
{"id": 1, "description": "Task from Kubernetes ConfigMap", "priority": 4, "status": "new", "status_label": "Новая", "is_completed": false, "created_at": "2026-04-30T15:13:07.423844"}
```
