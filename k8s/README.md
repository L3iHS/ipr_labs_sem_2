# Kubernetes manifests

Манифесты запускают HTTP-сервис `task-model` в локальном Kubernetes от Docker
Desktop.

## Файлы

- `namespace.yaml` — отдельная область `lab5`
- `configmap.yaml` — обычные настройки приложения
- `secret.yaml` — пример чувствительных данных
- `deployment.yaml` — запуск pod с приложением
- `service.yaml` — доступ к приложению через `localhost:30080`

## Запуск

```bash
kubectl apply -f k8s/
```

## Проверка

```bash
kubectl get all -n lab5
kubectl get pods -n lab5
curl http://localhost:30080/health
curl http://localhost:30080/task
```

## Удаление

```bash
kubectl delete namespace lab5
```
