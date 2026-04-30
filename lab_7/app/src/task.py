from __future__ import annotations

import datetime

from src.descriptors import (
    DescriptionDescriptor,
    PriorityDescriptor,
    StatusDescriptor,
    StatusLabelDescriptor,
    TaskIdDescriptor,
)


class Task:
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
        return self.status == "completed"
