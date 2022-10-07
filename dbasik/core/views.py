from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def index(request):
    return render(request, "core/index.html")


@login_required
def dashboard(request):
    return render(request, "core/dashboard.html", {"section": "dashboard"})


@login_required
def profile(request):
    args = {"user": request.user}
    return render(request, "core/profile.html", args)
