
from django.urls import path
from . import views

urlpatterns = [
    path("", views.hello_world, name="hello_world"),
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("confirmation/", views.confirmation_view, name="confirmation"),

    # CRUD API URLs
    path("api/users/", views.get_all_users, name="get_all_users"),
    path("api/users/by-email/", views.get_user_by_email, name="get_user_by_email"),
    path("api/users/update/", views.update_user, name="update_user"),
    path("api/users/delete/", views.delete_user, name="delete_user"),
]
