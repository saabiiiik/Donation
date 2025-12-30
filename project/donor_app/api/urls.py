from django.urls import path
from .views import *

urlpatterns = [
    path("signup/", signup),
    path("login/", login_api),

    path("register-blood/", register_blood_api),
    path("register-organ/", register_organ_api),

    path("search-blood/", search_blood_api),

    path("contact/", contact_api),
]
