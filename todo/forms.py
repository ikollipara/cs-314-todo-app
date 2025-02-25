"""
forms.py
Ian Kollipara <ian.kollipara@cune.edu>
2025-02-25

Todo Forms
"""

from django import forms

from todo.models import Todo


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ["title", "description"]
