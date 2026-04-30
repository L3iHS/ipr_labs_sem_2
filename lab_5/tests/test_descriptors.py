import pytest

from src.descriptors import StatusLabelDescriptor, TaskIdDescriptor
from src.exceptions import TaskInvariantError
from src.task import Task


def test_task_class_attribute_id_returns_descriptor():
    assert isinstance(Task.id, TaskIdDescriptor)


def test_task_class_attribute_status_label_returns_descriptor():
    assert isinstance(Task.status_label, StatusLabelDescriptor)


def test_status_descriptor_allows_transition_from_new_to_cancelled():
    task = Task(id=1, description="Test task", priority=3, status="new")
    task.status = "cancelled"
    assert task.status == "cancelled"


def test_status_descriptor_raises_error_for_transition_from_cancelled_to_completed():
    task = Task(id=1, description="Test task", priority=3, status="cancelled")
    with pytest.raises(TaskInvariantError):
        task.status = "completed"


def test_status_descriptor_allows_setting_same_status():
    task = Task(id=1, description="Test task", priority=3, status="new")
    task.status = "new"
    assert task.status == "new"


def test_status_label_changes_after_status_update():
    task = Task(id=1, description="Test task", priority=3, status="new")
    task.status = "in_progress"
    assert task.status_label == "В работе"
