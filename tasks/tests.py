from django.test import TestCase
from .models import Task, TaskStatus


class TaskModelTest(TestCase):

    def setUp(self):
        # Crear un estado inicial para las tareas
        self.task_status = TaskStatus.objects.create(name="not_started")

        # Crear una tarea de ejemplo
        self.task = Task.objects.create(
            title="Test Task",
            description="Esto es una prueba de Tarea",
            status=self.task_status,
            completed=False
        )

    def test_task_creation(self):
        self.assertEqual(self.task.title, "Test Task")
        self.assertEqual(self.task.description, "Esto es una prueba de Tarea")
        self.assertEqual(self.task.status, self.task_status)
        self.assertFalse(self.task.completed)
        self.assertIsNotNone(self.task.created_at)
        self.assertIsNotNone(self.task.updated_at)

    def test_task_string_representation(self):
        # Verificar la representación en cadena de la tarea
        self.assertEqual(str(self.task), "Test Task")
