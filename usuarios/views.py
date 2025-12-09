from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse

def login_view(request):
    if request.user.is_authenticated:
        return redirect('cliente:cliente-list')

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('cliente:cliente-list')
        else:
            return render(request, "usuarios/login.html", {
                "error": "Usuario o contraseña incorrectos."
            })

    return render(request, "usuarios/login.html")


def logout_view(request):
    logout(request)
    return redirect(reverse('usuarios:login'))
