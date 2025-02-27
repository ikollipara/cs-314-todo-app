from re import compile

from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from django.urls import reverse

from todo.forms import TodoForm
from todo.models import Todo
from todo.testing import E2ETestCase

# Create your tests here.


@tag("e2e")
class TestTodo(E2ETestCase):
    headless = False
    browser = "chromium"

    def test_can_view_home(self):
        with self.trace("trace"):
            self.page.goto(f"{self.live_server_url}/")
            self.expect(self.page).to_have_title("Todo")
            self.assertInHTML("Todos", self.page.content())

    def test_can_create_a_todo(self):
        self.page.goto(f"{self.live_server_url}/")
        self.page.get_by_text("Create a new Todo").click()
        self.expect(self.page).to_have_url(compile(".*create/"))
        self.page.get_by_label("Title:").fill("My title")
        self.page.get_by_label("Description:").fill("My description")
        self.page.get_by_role("button", name="Create").click()
        self.expect(self.page).to_have_url(compile(".*[0-9]+/"))
        self.assertInHTML("My title", self.page.content())


# Create your tests here.


class TestTodoModel(TestCase):
    def test_title_validation(self):
        title = "i" * 257
        todo = Todo(title=title, description="My description")

        with self.assertRaises(ValidationError):
            todo.full_clean()

    def test_is_complete(self):
        todo = Todo(title="My title", description="My description")

        result = todo.is_complete

        self.assertFalse(result)

    def test_str(self):
        todo = Todo(title="My title", description="My description")

        result = str(todo)

        self.assertEqual(result, "My title [ ]")

    def test_absolute_url(self):
        todo = Todo.objects.create(title="My title", description="My description")

        result = todo.get_absolute_url()

        self.assertRegex(result, ".*/[0-9]+/")

    def test_qs_incomplete(self):
        Todo.objects.create(title="My title", description="My description")

        result = Todo.objects.incomplete().count()

        self.assertEqual(1, result)


class TestTodoList(TestCase):
    def test_get__all(self):
        response = self.client.get(reverse("todo_list"))

        self.assertTemplateUsed(response, "todo/todo_list.html")
        self.assertFalse(response.context["incomplete"])

    def test_get__incomplete(self):
        response = self.client.get(reverse("todo_list"), QUERY_STRING="incomplete=on")

        self.assertTemplateUsed(response, "todo/todo_list.html")
        self.assertTrue(response.context["incomplete"])


class TestTodoCreate(TestCase):
    def test_get(self):
        response = self.client.get(reverse("todo_create"))

        self.assertIsInstance(response.context["form"], TodoForm)
        self.assertTemplateUsed(response, "todo/todo_create.html")

    def test_post(self):
        response = self.client.post(
            reverse("todo_create"),
            {"title": "My title", "description": "My description"},
        )

        self.assertEqual(1, Todo.objects.count())
        self.assertRedirects(response, reverse("todo_detail", kwargs={"pk": 1}))


class TestTodoDetail(TestCase):
    def test_get(self):
        todo = Todo.objects.create(title="My title", description="My description")
        response = self.client.get(reverse("todo_detail", kwargs={"pk": todo.pk}))

        self.assertTemplateUsed(response, "todo/todo_detail.html")
        self.assertEqual(todo, response.context["todo"])
        self.assertEqual(todo, response.context["todo"])
