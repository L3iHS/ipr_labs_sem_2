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

Docker-образ — это упакованное приложение со всем, что нужно для запуска:
Python, зависимости и исходный код.

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

## CI/CD

CI/CD — это автоматическая проверка и сборка проекта.

В этом проекте GitHub Actions делает следующее:

1. Скачивает код из репозитория.
2. Устанавливает Python 3.12.
3. Устанавливает зависимости из `requirements.txt`.
4. Запускает тесты.
5. Если тесты прошли, собирает Docker-образ.
6. Публикует Docker-образ в GitHub Container Registry.

Файл с настройкой GitHub Actions:

```text
.github/workflows/ci-cd.yml
```

## Registry

Registry — это хранилище Docker-образов.

Код проекта хранится в GitHub-репозитории, а собранный Docker-образ хранится
отдельно. Для этого используется GitHub Container Registry, его адрес начинается
с `ghcr.io`.

Пример имени образа:

```text
ghcr.io/l3ihs/ipr_labs_sem_2:latest
```

Дальше Kubernetes сможет взять этот образ из registry и запустить его в
кластере.

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
kubectl apply -f k8s/
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

# Исходная лабораторная работа №2: Модель задачи, дескрипторы и `@property`

## Цель работы

Освоить управление доступом к атрибутам объекта, валидацию состояния и защиту инвариантов модели

## Постановка задачи

Необходимо реализовать модель задачи `Task` в рамках платформы обработки задач

Модель должна:
- валидировать значения атрибутов через пользовательские дескрипторы
- использовать `property` для вычисляемых и защищенных свойств
- предотвращать перевод объекта в некорректное состояние
- выбрасывать специализированные исключения при нарушении правил модели

## Что реализовано

- класс `Task`
- `data descriptors` для атрибутов:
  - `id`
  - `description`
  - `priority`
  - `status`
- `non-data descriptor` `status_label` для текстового представления статуса
- `property` `created_at` для защищенного доступа ко времени создания
- `property` `is_completed` для определения, завершена ли задача
- исключения:
  - `TaskError`
  - `TaskValidationError`
  - `TaskInvariantError`
- защита инвариантов переходов статуса:
  - `new -> in_progress`, `cancelled`
  - `in_progress -> completed`, `cancelled`
  - из `completed` переходы запрещены
  - из `cancelled` переходы запрещены

## Инварианты модели

Для корректного объекта `Task` должны выполняться следующие условия:
- `id` это положительное целое число
- `description` это непустая строка
- `priority` это целое число от 1 до 5
- `status` это один из допустимых статусов
- `created_at` задается при создании объекта
- запрещены некорректные переходы между статусами

## Запуск тестов

```bash
pytest -q
```

## Проверка покрытия

```bash
pytest --cov=src --cov-report=term-missing
```

При запуске `pytest --cov=src --cov-report=term-missing` общий отчет показывает
покрытие 72%, потому что в расчет входит демонстрационный файл `src/main.py`.
Основная бизнес-логика модели задачи покрыта тестами почти полностью.
