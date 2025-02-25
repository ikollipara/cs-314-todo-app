"""
urls.py
Ian Kollipara <ian.kollipara@cune.edu>
2025-02-25

Todo Urls
"""

from django.urls import path

from todo import views

urlpatterns = [
    path("", views.todo_list, name="todo_list"),
    path("create/", views.todo_create, name="todo_create"),
    path("<int:pk>/", views.todo_detail, name="todo_detail"),
]
