from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import User


class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=[
            (User.Roles.QA, "QA"),
            (User.Roles.DEVELOPER, "Developer"),
            (User.Roles.MANAGER, "Manager"),
        ]
    )

    class Meta:
        model = User
        fields = ("username", "role")
