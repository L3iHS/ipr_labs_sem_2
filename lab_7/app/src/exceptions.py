class TaskError(Exception):
    """Базовое исключение модели задачи."""


class TaskValidationError(TaskError):
    """Ошибка валидации значения."""


class TaskInvariantError(TaskError):
    """Ошибка перехода состояния задачи."""
