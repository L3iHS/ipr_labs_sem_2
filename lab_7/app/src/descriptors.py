from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union

from src.exceptions import TaskInvariantError, TaskValidationError

if TYPE_CHECKING:
    from src.task import Task


class BaseValidatedDescriptor:
    def __set_name__(self, owner: type, name: str) -> None:
        self.public_name = name
        self.private_name = f"_{name}"

    def __get__(self, instance: Optional[object], owner: type) -> object:
        if instance is None:
            return self
        return getattr(instance, self.private_name)

    def __set__(self, instance: object, value: object) -> None:
        self.validate(value)
        setattr(instance, self.private_name, value)

    def validate(self, value: object) -> None:
        pass


class TaskIdDescriptor(BaseValidatedDescriptor):
    def validate(self, value: int) -> None:
        if isinstance(value, bool):
            raise TaskValidationError("id не может быть булевым")
        if not isinstance(value, int) or value <= 0:
            raise TaskValidationError("id должен быть положительным целым числом")


class DescriptionDescriptor(BaseValidatedDescriptor):
    def validate(self, value: str) -> None:
        if not isinstance(value, str):
            raise TaskValidationError("description должен быть строкой")
        if not value.strip():
            raise TaskValidationError("description не может быть пустым")


class PriorityDescriptor(BaseValidatedDescriptor):
    def validate(self, value: int) -> None:
        if isinstance(value, bool):
            raise TaskValidationError("priority не может быть булевым")
        if not isinstance(value, int) or not (1 <= value <= 5):
            raise TaskValidationError("priority должен быть числом от 1 до 5")


class StatusDescriptor(BaseValidatedDescriptor):
    def __set__(self, instance: object, value: object) -> None:
        self.validate(value)

        if not hasattr(instance, self.private_name):
            setattr(instance, self.private_name, value)
            return

        current_status = getattr(instance, self.private_name)
        allowed_transitions = {
            "new": {"in_progress", "cancelled"},
            "in_progress": {"completed", "cancelled"},
            "completed": set(),
            "cancelled": set(),
        }

        if current_status != value and value not in allowed_transitions[current_status]:
            raise TaskInvariantError(
                f'Переход статуса из "{current_status}" в "{value}" запрещен'
            )

        setattr(instance, self.private_name, value)

    def validate(self, value: str) -> None:
        allowed_statuses = ["new", "in_progress", "completed", "cancelled"]
        if not isinstance(value, str):
            raise TaskValidationError("status должен быть строкой")
        if value not in allowed_statuses:
            raise TaskValidationError("status должен быть одним из допустимых значений")


class StatusLabelDescriptor:
    def __get__(
        self, instance: Optional[Task], owner: type
    ) -> Union[str, StatusLabelDescriptor]:
        labels = {
            "new": "Новая",
            "in_progress": "В работе",
            "completed": "Завершена",
            "cancelled": "Отменена",
        }
        if instance is None:
            return self
        return labels[instance.status]
