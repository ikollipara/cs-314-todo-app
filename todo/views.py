from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render

from todo.forms import TodoForm
from todo.models import Todo

# Create your views here.


def todo_list(request: HttpRequest):
    """List the given todos."""

    if request.GET.get("incomplete", None):
        todos = Todo.objects.incomplete()
    else:
        todos = Todo.objects.all()

    return render(
        request,
        "todo/todo_list.html",
        {"todos": todos, "incomplete": request.GET.get("incomplete") is not None},
    )


def todo_create(request: HttpRequest):
    if request.method == "GET":
        form = TodoForm()
        return render(request, "todo/todo_create.html", {"form": form})

    elif request.method == "POST":
        form = TodoForm(request.POST, request.FILES)

        if form.is_valid():
            instance: Todo = form.save()

            return redirect(instance)


def todo_detail(request: HttpRequest, pk: int):
    todo = get_object_or_404(Todo, id=pk)

    return render(request, "todo/todo_detail.html", {"todo": todo})
