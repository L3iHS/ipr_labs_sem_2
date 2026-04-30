import datetime

from src.descriptors import (
    TaskIdDescriptor,
    DescriptionDescriptor,
    PriorityDescriptor,
    StatusDescriptor,
    StatusLabelDescriptor
)


class Task:
    """Модель задачи с валидацией атрибутов через дескрипторы"""

    id = TaskIdDescriptor()
    description = DescriptionDescriptor()
    priority = PriorityDescriptor()
    status = StatusDescriptor()
    status_label = StatusLabelDescriptor()

    def __init__(self, id: int, description: str, priority: int, status: str) -> None:
        self.id = id
        self.description = description
        self.priority = priority
        self.status = status
        self._created_at = datetime.datetime.now()

    @property
    def created_at(self) -> datetime.datetime:
        return self._created_at

    @property
    def is_completed(self) -> bool:
        """Показывает, завершена ли задача"""
        return self.status == "completed"
