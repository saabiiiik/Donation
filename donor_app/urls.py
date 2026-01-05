from django.urls import path
from . import views

urlpatterns = [
    path("register-blood/", views.register_blood, name="register_blood"),
    path("register-organ/", views.register_organ, name="register_organ"),
    path("search-blood/", views.search_blood, name="search_blood"),
    path("search-organ/", views.search_organ, name="search_organ"),
    path("contact/", views.contact, name="contact"),
    path("about/", views.about, name="about"),
    path("success/", views.success, name="success"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("signup/", views.signup_view, name="signup"),
    path("profile/", views.profile_view, name="profile"),




]

