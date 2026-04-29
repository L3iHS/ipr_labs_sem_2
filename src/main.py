from src.exceptions import TaskInvariantError, TaskValidationError
from src.task import Task


def print_task_state(task: Task) -> None:
    print("Текущее состояние задачи")
    print(f"id: {task.id}")
    print(f"description: {task.description}")
    print(f"priority: {task.priority}")
    print(f"status: {task.status}")
    print(f"status_label: {task.status_label}")
    print(f"is_completed: {task.is_completed}")
    print(f"created_at: {task.created_at}")


def main() -> None:
    task = Task(1, "сдлать main", 2, "new")

    print("Задача успешно создана")
    print_task_state(task)

    print("\nРазрешенный переход статуса")
    task.status = "in_progress"
    print(f"Новый статус: {task.status}")
    print(f"Подпись статуса: {task.status_label}")

    print("\nОшибка валидации")
    try:
        task.priority = 10
    except TaskValidationError as error:
        print(error)

    print("\nОшибка инварианта")
    task.status = "completed"
    try:
        task.status = "cancelled"
    except TaskInvariantError as error:
        print(error)


if __name__ == "__main__":
    main()
