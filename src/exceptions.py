class TaskError(Exception):
    """Базовое исключение для всех ошибок модели задачи"""
    pass


class TaskValidationError(TaskError):
    """Выбрасывается при передаче атрибуту задачи недопустимого значения"""
    pass


class TaskInvariantError(TaskError):
    """Выбрасывается при нарушении инвариантов объекта Task"""
    pass

