from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Donor, OrganDonor, ContactMessage, DonationHistory


# ================= HOME =================
def home(request):
    return render(request, "home.html")


# ================= SUCCESS =================
def success(request):
    return render(request, "success.html")


# =========================================================
# 🩸 BLOOD DONOR REGISTRATION
# =========================================================
@login_required(login_url="login")
def register_blood(request):
    user = request.user

    if Donor.objects.filter(user=user).exists():
        return render(request, "register_blood.html", {
            "toast": "You are already registered as a blood donor"
        })

    if request.method == "POST":
        if not request.POST.get("agree"):
            return render(request, "register_blood.html", {
                "toast": "You must agree to the eligibility conditions"
            })

        try:
            age = int(request.POST.get("age"))
        except (TypeError, ValueError):
            return render(request, "register_blood.html", {
                "toast": "Invalid age"
            })

        mobile = request.POST.get("mobile", "").strip()

        if age < 18 or age > 65:
            return render(request, "register_blood.html", {
                "toast": "Age must be between 18 and 65"
            })

        if not mobile.isdigit() or len(mobile) != 10:
            return render(request, "register_blood.html", {
                "toast": "Mobile number must be exactly 10 digits"
            })

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


# =========================================================
# 🫀 ORGAN DONOR REGISTRATION
# =========================================================
@login_required(login_url="login")
def register_organ(request):
    user = request.user

    if OrganDonor.objects.filter(user=user).exists():
        return render(request, "register_organ.html", {
            "toast": "You are already registered as an organ donor"
        })

    if request.method == "POST":
        if not request.POST.get("agree"):
            return render(request, "register_organ.html", {
                "toast": "You must agree to the eligibility conditions"
            })

        try:
            age = int(request.POST.get("age"))
        except (TypeError, ValueError):
            return render(request, "register_organ.html", {
                "toast": "Invalid age"
            })

        mobile = request.POST.get("mobile", "").strip()

        if age < 18 or age > 65:
            return render(request, "register_organ.html", {
                "toast": "Age must be between 18 and 65"
            })

        if not mobile.isdigit() or len(mobile) != 10:
            return render(request, "register_organ.html", {
                "toast": "Mobile number must be exactly 10 digits"
            })

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


# ================= SEARCH =================
def search_blood(request):
    donors = Donor.objects.filter(availability=True)

    if request.method == "POST":
        filters = {"availability": True}
        if request.POST.get("blood_group"):
            filters["blood_group"] = request.POST.get("blood_group")
        if request.POST.get("location"):
            filters["location__icontains"] = request.POST.get("location")

        donors = Donor.objects.filter(**filters)

    return render(request, "search_blood.html", {"donors": donors})


def search_organ(request):
    donors = OrganDonor.objects.filter(is_available=True)

    if request.method == "POST":
        filters = {"is_available": True}
        if request.POST.get("organ_type"):
            filters["organ_type"] = request.POST.get("organ_type")
        if request.POST.get("location"):
            filters["location__icontains"] = request.POST.get("location")

        donors = OrganDonor.objects.filter(**filters)

    return render(request, "search_organ.html", {"donors": donors})


# ================= CONTACT =================
def contact(request):
    if request.method == "POST":
        ContactMessage.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            message=request.POST.get("message"),
        )
        return render(request, "contact.html", {
            "toast": "Message sent successfully"
        })

    return render(request, "contact.html")


def about(request):
    return render(request, "about.html")


# =========================================================
# 🔐 AUTH SYSTEM (FIXED)
# =========================================================

# ------------------ SIGNUP ------------------
def signup_view(request):
    if request.method == "POST":
        mobile = request.POST.get("username", "").strip()
        password = request.POST.get("password")
        confirm = request.POST.get("confirm")

        if not mobile.isdigit() or len(mobile) != 10:
            return render(request, "signup.html", {
                "toast": "Mobile number must be exactly 10 digits"
            })

        if len(password) < 6:
            return render(request, "signup.html", {
                "toast": "Password must be at least 6 characters"
            })

        if password != confirm:
            return render(request, "signup.html", {
                "toast": "Passwords do not match"
            })

        if User.objects.filter(username=mobile).exists():
            return render(request, "signup.html", {
                "toast": "Mobile number already registered"
            })

        user = User.objects.create_user(
            username=mobile,
            password=password
        )

        login(request, user)
        return redirect("dashboard")

    return render(request, "signup.html")


# ------------------ LOGIN (FINAL FIX) ------------------
def login_view(request):
    if request.method == "POST":
        mobile = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        if not mobile.isdigit() or len(mobile) != 10:
            return render(request, "login.html", {
                "toast": "Mobile number must be exactly 10 digits"
            })

        try:
            user_obj = User.objects.get(username=mobile)
        except User.DoesNotExist:
            return render(request, "login.html", {
                "toast": "Account does not exist"
            })

        user = authenticate(request, username=mobile, password=password)

        if user is None:
            return render(request, "login.html", {
                "toast": "Incorrect password"
            })

        login(request, user)

        next_url = request.GET.get("next")
        if next_url:
            return redirect(next_url)

        return redirect("dashboard")

    return render(request, "login.html")


# ------------------ LOGOUT ------------------
def logout_view(request):
    logout(request)
    return redirect("login")


# ================= DASHBOARD =================
@login_required(login_url="login")
def dashboard(request):
    donor = Donor.objects.filter(user=request.user).first()
    organ_donor = OrganDonor.objects.filter(user=request.user).first()

    history = DonationHistory.objects.filter(
        user=request.user
    ).order_by("-donated_on")

    return render(request, "dashboard.html", {
        "donor": donor,
        "organ_donor": organ_donor,
        "history": history
    })


# ================= PROFILE =================
@login_required(login_url="login")
def profile_view(request):
    if request.method == "POST":
        request.user.email = request.POST.get("email")
        request.user.save()
        return redirect("profile")

    return render(request, "profile.html")
