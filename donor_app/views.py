from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Donor, OrganDonor, ContactMessage


# ------------------ HOME ------------------
def home(request):
    return render(request, "home.html")


# ------------------ BLOOD DONOR REGISTRATION ------------------
@login_required(login_url="login")
def register_blood(request):
    if request.method == "POST":

        # CHECK AGREEMENT
        if not request.POST.get("agree"):
            return render(request, "register_blood.html", {
                "toast": "You must agree to the eligibility conditions!"
            })

        # SAFE AGE PARSING
        try:
            age = int(request.POST.get("age"))
        except (TypeError, ValueError):
            return render(request, "register_blood.html", {
                "toast": "Invalid age value!"
            })

        mobile = request.POST.get("mobile", "").strip()

        # AGE VALIDATION
        if age < 18 or age > 65:
            return render(request, "register_blood.html", {
                "toast": "Age must be between 18 and 65!"
            })

        # MOBILE VALIDATION
        if not mobile.isdigit() or len(mobile) != 10:
            return render(request, "register_blood.html", {
                "toast": "Mobile number must be exactly 10 digits!"
            })

        # 🔹 CREATE USER (for login)
        user = User.objects.create_user(
            username=mobile,
            password=mobile
        )

        # SAVE DATA
        Donor.objects.create(
            user=user,
            name=request.POST.get("name"),
            age=age,
            blood_group=request.POST.get("blood_group"),
            mobile=mobile,
            location=request.POST.get("location"),
            availability=True
        )

        return redirect("success")

    return render(request, "register_blood.html")


# ------------------ ORGAN DONOR REGISTRATION ------------------
@login_required(login_url="login")
def register_organ(request):
    if request.method == "POST":

        # CHECK AGREEMENT
        if not request.POST.get("agree"):
            return render(request, "register_organ.html", {
                "toast": "You must agree to the eligibility conditions!"
            })

        # SAFE AGE PARSING
        try:
            age = int(request.POST.get("age"))
        except (TypeError, ValueError):
            return render(request, "register_organ.html", {
                "toast": "Invalid age value!"
            })

        mobile = request.POST.get("mobile", "").strip()

        # AGE VALIDATION
        if age < 18 or age > 65:
            return render(request, "register_organ.html", {
                "toast": "Age must be between 18 and 65!"
            })

        # MOBILE VALIDATION
        if not mobile.isdigit() or len(mobile) != 10:
            return render(request, "register_organ.html", {
                "toast": "Mobile number must be exactly 10 digits!"
            })

        # 🔹 CREATE USER (for login)
        user = User.objects.create_user(
            username=mobile,
            password=mobile
        )

        # SAVE DATA
        OrganDonor.objects.create(
            user=user,
            name=request.POST.get("name"),
            age=age,
            organ_type=request.POST.get("organ_type"),
            mobile=mobile,
            location=request.POST.get("location"),
            is_available=True
        )

        return redirect("success")

    return render(request, "register_organ.html")


# ------------------ BLOOD DONOR SEARCH ------------------
def search_blood(request):
    donors = Donor.objects.filter(availability=True)

    if request.method == "POST":
        blood_group = request.POST.get("blood_group")
        location = request.POST.get("location")

        filters = {"availability": True}

        if blood_group:
            filters["blood_group"] = blood_group
        if location:
            filters["location__icontains"] = location

        donors = Donor.objects.filter(**filters)

    return render(request, "search_blood.html", {"donors": donors})


# ------------------ ORGAN DONOR SEARCH ------------------
def search_organ(request):
    donors = OrganDonor.objects.filter(is_available=True)

    if request.method == "POST":
        organ_type = request.POST.get("organ_type")
        location = request.POST.get("location")

        filters = {"is_available": True}

        if organ_type:
            filters["organ_type"] = organ_type
        if location:
            filters["location__icontains"] = location

        donors = OrganDonor.objects.filter(**filters)

    return render(request, "search_organ.html", {"donors": donors})


# ------------------ CONTACT ------------------
def contact(request):
    if request.method == "POST":
        ContactMessage.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            message=request.POST.get("message"),
        )

        return render(request, "contact.html", {
            "toast": "Message sent successfully!"
        })

    return render(request, "contact.html")


# ------------------ ABOUT ------------------
def about(request):
    return render(request, "about.html")


# ------------------ SUCCESS ------------------
def success(request):
    return render(request, "success.html")


# =========================================================
# 🔐 AUTH SECTION (NEW — STEP 2)
# =========================================================

# ------------------ LOGIN ------------------
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            # 🔹 redirect back to intended page
            next_url = request.GET.get("next")
            return redirect(next_url or "dashboard")

        return render(request, "login.html", {
            "toast": "Invalid login credentials"
        })

    return render(request, "login.html")




# ------------------ LOGOUT ------------------
def logout_view(request):
    logout(request)
    return redirect("login")


# ------------------ DASHBOARD ------------------
@login_required(login_url="login")
def dashboard(request):
    donor = None
    organ_donor = None
    donations = []

    try:
        donor = Donor.objects.get(user=request.user)
        donations = donor.donations.all().order_by("-donated_on")
    except Donor.DoesNotExist:
        pass

    try:
        organ_donor = OrganDonor.objects.get(user=request.user)
    except OrganDonor.DoesNotExist:
        pass

    return render(request, "dashboard.html", {
        "donor": donor,
        "organ_donor": organ_donor,
        "donations": donations
    })



def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm = request.POST.get("confirm")

        if password != confirm:
            return render(request, "signup.html", {
                "error": "Passwords do not match"
            })

        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {
                "error": "User already exists"
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)
        return redirect("dashboard")

    return render(request, "signup.html")


@login_required(login_url="login")
def profile_view(request):
    if request.method == "POST":
        request.user.email = request.POST.get("email")
        request.user.save()
        return redirect("profile")

    return render(request, "profile.html")
