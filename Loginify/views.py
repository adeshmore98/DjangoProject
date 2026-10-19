import json

from django.http import JsonResponse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_GET, require_http_methods

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password

from .models import UserDetails
from .forms import SignupForm, LoginForm


def hello_world(request):
    return HttpResponse("Hello, world!")


def signup_view(request):
    form = SignupForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        username = form.cleaned_data["username"]
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]

        UserDetails.objects.create(
            username=username,
            email=email,
            password=make_password(password)
        )

        messages.success(request, "Account created successfully! Please log in.")
        return redirect("login")

    return render(request, "Loginify/signup.html", {"form": form})


def login_view(request):
    form = LoginForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]

        user = UserDetails.objects.filter(email__iexact=email).first()

        if user and check_password(password, user.password):
            request.session.cycle_key()
            request.session["username"] = user.username
            return redirect("confirmation")

        form.add_error(None, "Invalid email or password.")

    return render(request, "Loginify/login.html", {"form": form})


def confirmation_view(request):
    username = request.session.get("username")

    if not username:
        return redirect("login")

    return render(
        request,
        "Loginify/confirmation.html",
        {"username": username}
    )


def get_current_user(request):
    username = request.session.get("username")

    if not username:
        return None

    return UserDetails.objects.filter(username=username).first()


def user_to_dict(user):
    return {
        "username": user.username,
        "email": user.email
    }


@require_GET
def get_all_users(request):
    current_user = get_current_user(request)

    if current_user is None:
        return JsonResponse({"error": "Login required"}, status=401)

    users = UserDetails.objects.all()
    user_list = [user_to_dict(user) for user in users]

    return JsonResponse({"users": user_list}, status=200)


@require_GET
def get_user_by_email(request):
    if get_current_user(request) is None:
        return JsonResponse({"error": "Login required"}, status=401)

    email = request.GET.get("email", "").strip()

    if not email:
        return JsonResponse({"error": "Email is required"}, status=400)

    user = UserDetails.objects.filter(email__iexact=email).first()

    if user is None:
        return JsonResponse({"error": "User not found"}, status=404)

    return JsonResponse({"user": user_to_dict(user)}, status=200)


@require_http_methods(["PUT"])
def update_user(request):
    current_user = get_current_user(request)

    if current_user is None:
        return JsonResponse({"error": "Login required"}, status=401)

    try:
        data = json.loads(request.body)
    except (ValueError, UnicodeDecodeError):
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    if not isinstance(data, dict):
        return JsonResponse({"error": "Expected a JSON object"}, status=400)

    email = data.get("email")
    new_email = data.get("new_email")
    new_password = data.get("new_password")

    if not isinstance(email, str) or not email.strip():
        return JsonResponse({"error": "Current email is required"}, status=400)

    if email.strip().lower() != current_user.email.lower():
        return JsonResponse({"error": "Permission denied"}, status=403)

    if new_email is None and new_password is None:
        return JsonResponse({"error": "No updates provided"}, status=400)

    if new_email is not None:
        if not isinstance(new_email, str):
            return JsonResponse({"error": "Invalid email"}, status=400)

        new_email = new_email.strip().lower()

        try:
            validate_email(new_email)
        except ValidationError:
            return JsonResponse({"error": "Invalid email"}, status=400)

        duplicate = UserDetails.objects.filter(
            email__iexact=new_email
        ).exclude(username=current_user.username).exists()

        if duplicate:
            return JsonResponse({"error": "Email already exists"}, status=409)

        current_user.email = new_email

    if new_password is not None:
        if not isinstance(new_password, str) or len(new_password) < 8:
            return JsonResponse(
                {"error": "Password must have at least 8 characters"},
                status=400
            )

        current_user.password = make_password(new_password)

    current_user.save()

    return JsonResponse({
        "message": "User updated successfully",
        "user": user_to_dict(current_user)
    }, status=200)


@require_http_methods(["DELETE"])
def delete_user(request):
    current_user = get_current_user(request)

    if current_user is None:
        return JsonResponse({"error": "Login required"}, status=401)

    email = request.GET.get("email", "").strip()

    if not email:
        return JsonResponse({"error": "Email is required"}, status=400)

    if email.lower() != current_user.email.lower():
        return JsonResponse({"error": "Permission denied"}, status=403)

    current_user.delete()
    request.session.flush()

    return JsonResponse({
        "message": "User deleted successfully"
    }, status=200)
