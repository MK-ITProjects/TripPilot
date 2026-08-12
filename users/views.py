from django.contrib import messages
from django.contrib.auth import get_user_model, login, authenticate
from django.shortcuts import redirect, render

from .forms import LoginForm, SignUpForm
from .models import Profile

User = get_user_model()

def login_view(request):
    # If user is already logged in
    if request.user.is_authenticated:
        return redirect('dashboard:home')

    next_url = request.POST.get('next') or request.GET.get('next')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            messages.success(request, f'Welcome back, {user.username}!')

            return redirect(next_url or 'dashboard:home')

    else:
        form = LoginForm(request)

    return render(request, 'users/login.html', {
        'form': form,
        'next': next_url,
    })


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard:home")

    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()

            Profile.objects.get_or_create(user=user)

            user = authenticate(
                request,
                username=user.username,
                password=form.cleaned_data["password1"],
            )

            if user:
                login(request, user)

            messages.success(request, "Account created successfully!")

            return redirect("dashboard:home")

    else:
        form = SignUpForm()

    return render(request, "users/signup.html", {"form": form})