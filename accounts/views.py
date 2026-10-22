from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import SignUpForm


def signup(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = SignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(
            request,
            "Conta criada. Um administrador do laboratório precisa aprovar seu acesso.",
        )
        return redirect("login")
    return render(request, "registration/signup.html", {"form": form})
