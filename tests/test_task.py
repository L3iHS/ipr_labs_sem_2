from src.task import Task
from src.exceptions import TaskValidationError, TaskInvariantError

import pytest
import datetime


def test_task_is_created_with_valid_data():
    task = Task(id=1, description="Test task", priority=3, status="new")
    assert task.id == 1
    assert task.description == "Test task"
    assert task.priority == 3
    assert task.status == "new"
    assert isinstance(task.created_at, datetime.datetime)
    assert not task.is_completed


def test_task_raises_error_for_zero_id():
    with pytest.raises(TaskValidationError):
        Task(id=0, description="Test task", priority=3, status="new")


def test_task_raises_error_for_negative_id():
    with pytest.raises(TaskValidationError):
        Task(id=-1, description="Test task", priority=3, status="new")


def test_task_raises_error_for_non_integer_id():
    with pytest.raises(TaskValidationError):
        Task(id="one", description="Test task", priority=3, status="new")


def test_task_raises_error_for_boolean_id():
    with pytest.raises(TaskValidationError):
        Task(id=True, description="Test task", priority=3, status="new")


def test_task_raises_error_for_empty_description():
    with pytest.raises(TaskValidationError):
        Task(id=1, description="", priority=3, status="new")


def test_task_raises_error_for_blank_description():
    with pytest.raises(TaskValidationError):
        Task(id=1, description="   ", priority=3, status="new")


def test_task_raises_error_for_non_string_description():
    with pytest.raises(TaskValidationError):
        Task(id=1, description=123, priority=3, status="new")


def test_task_raises_error_for_zero_priority():
    with pytest.raises(TaskValidationError):
        Task(id=1, description="Test task", priority=0, status="new")


def test_task_raises_error_for_priority_greater_than_five():
    with pytest.raises(TaskValidationError):
        Task(id=1, description="Test task", priority=6, status="new")


def test_task_raises_error_for_non_integer_priority():
    with pytest.raises(TaskValidationError):
        Task(id=1, description="Test task", priority="high", status="new")


def test_task_raises_error_for_boolean_priority():
    with pytest.raises(TaskValidationError):
        Task(id=1, description="Test task", priority=False, status="new")


def test_task_raises_error_for_unknown_status():
    with pytest.raises(TaskValidationError):
        Task(id=1, description="Test task", priority=3, status="unknown")


def test_task_raises_error_for_non_string_status():
    with pytest.raises(TaskValidationError):
        Task(id=1, description="Test task", priority=3, status=123)


def test_task_is_completed_returns_true_for_completed_status():
    task = Task(id=1, description="Test task", priority=3, status="completed")
    assert task.is_completed


def test_task_is_completed_returns_false_for_non_completed_status():
    task = Task(id=1, description="Test task", priority=3, status="in_progress")
    assert not task.is_completed


def test_task_returns_correct_status_label():
    task = Task(id=1, description="Test task", priority=3, status="new")
    assert task.status_label == "Новая"
    task.status = "in_progress"
    assert task.status_label == "В работе"
    task.status = "completed"
    assert task.status_label == "Завершена"


def test_task_allows_valid_status_transition():
    task = Task(id=1, description="Test task", priority=3, status="new")
    task.status = "in_progress"
    assert task.status == "in_progress"


def test_task_raises_error_for_invalid_status_transition():
    task = Task(id=1, description="Test task", priority=3, status="completed")
    with pytest.raises(TaskInvariantError):
        task.status = "cancelled"


def test_task_allows_cancellation_from_in_progress():
    task = Task(id=1, description="Test task", priority=3, status="in_progress")
    task.status = "cancelled"
    assert task.status == "cancelled"
