import pytest
from .models import Task, TaskStatus


@pytest.fixture
def task_status(db):
    status, created = TaskStatus.objects.get_or_create(name="not_started")
    return status


@pytest.fixture
def task(db, task_status):
    return Task.objects.create(
        title="Test Task",
        description="Esto es una tarea de pruebas",
        status=task_status,
        completed=False
    )


def test_task_creation(task):
    assert task.title == "Test Task"
    assert task.description == "Esto es una tarea de pruebas 2"
    assert task.status.name == "not_started"
    assert not task.completed
    assert task.created_at is not None
    assert task.updated_at is not None


def test_task_string_representation(task):
    assert str(task) == "Test Task"
