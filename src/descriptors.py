from __future__ import annotations

from typing import TYPE_CHECKING

from src.exceptions import TaskValidationError, TaskInvariantError


# для подсказок и аннотаций Task есть
# для runtime импорта нет, чтобы избежать циклических импортов
if TYPE_CHECKING:
    from src.task import Task


class BaseValidatedDescriptor:
    """Базовый дескриптор с общей логикой валидации атрибутов"""

    def __set_name__(self, owner: type, name: str) -> None:
        self.public_name = name  # для сообщений об ошибке и тд
        self.private_name = f"_{name}"

    def __get__(self, instance: object | None, owner: type) -> object:
        if instance is None:
            return self
        return getattr(instance, self.private_name)

    def __set__(self, instance: object, value: object) -> None:
        self.validate(value)  # если не пройдет, выкинет ошибку
        setattr(instance, self.private_name, value)

    def validate(self, value: object) -> None:
        pass


class TaskIdDescriptor(BaseValidatedDescriptor):
    """Дескриптор для валидации id задачи"""

    def validate(self, value: int) -> None:
        if isinstance(value, bool):  # bool - это подкласс int, нужно исключить
            raise TaskValidationError(
                f'Значение атрибута "{self.public_name}" не может быть булевым'
            )
        if not isinstance(value, int) or value <= 0:
            raise TaskValidationError(
                f'Значение атрибута "{self.public_name}" должно быть положительным целым числом'
            )


class DescriptionDescriptor(BaseValidatedDescriptor):
    """Дескриптор для валидации описания задачи"""

    def validate(self, value: str) -> None:
        if not isinstance(value, str):
            raise TaskValidationError(
                f'Значение атрибута "{self.public_name}" должно быть строкой'
            )
        if not value.strip():
            raise TaskValidationError(
                f'Значение атрибута "{self.public_name}" не может быть пустой строкой'
            )


class PriorityDescriptor(BaseValidatedDescriptor):
    """Дескриптор для валидации приоритета задачи"""

    def validate(self, value: int) -> None:
        if isinstance(value, bool):  # bool - это подкласс int, нужно исключить
            raise TaskValidationError(
                f'Значение атрибута "{self.public_name}" не может быть булевым'
            )
        if not isinstance(value, int) or not (1 <= value <= 5):
            raise TaskValidationError(
                f'Значение атрибута "{self.public_name}" должно быть целым числом от 1 до 5'
            )


class StatusDescriptor(BaseValidatedDescriptor):
    """Дескриптор для валидации статуса задачи"""

    def __set__(self, instance: object, value: object) -> None:
        self.validate(value)

        if not hasattr(instance, self.private_name):
            setattr(instance, self.private_name, value)
            return

        current_status = getattr(instance, self.private_name)

        if current_status == value:
            setattr(instance, self.private_name, value)
            return

        allowed_transitions = {
            "new": {"in_progress", "cancelled"},
            "in_progress": {"completed", "cancelled"},
            "completed": set(),
            "cancelled": set(),
        }

        if value not in allowed_transitions[current_status]:
            raise TaskInvariantError(
                f'Переход статуса задачи из "{current_status}" в "{value}" запрещен'
            )

        setattr(instance, self.private_name, value)

    def validate(self, value: str) -> None:
        allowed_statuses = ["new", "in_progress", "completed", "cancelled"]

        if not isinstance(value, str):
            raise TaskValidationError(
                f'Значение атрибута "{self.public_name}" должно быть строкой'
            )
        if value not in allowed_statuses:
            raise TaskValidationError(
                f'Значение атрибута "{self.public_name}" должно быть одним из допустимых статусов: new, in_progress, completed, cancelled'
            )


class StatusLabelDescriptor:
    """non-data дескриптор для получения текстового представления статуса задачи"""

    def __get__(
        self, instance: Task | None, owner: type
    ) -> str | StatusLabelDescriptor:
        status_labels = {
            "new": "Новая",
            "in_progress": "В работе",
            "completed": "Завершена",
            "cancelled": "Отменена",
        }

        if instance is None:
            return self
        return status_labels[instance.status]
