from django.shortcuts import render, redirect
from .models import Donor, OrganDonor
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import ContactMessage
from django.shortcuts import render, redirect
from django.http import HttpResponse

def home(request):
    return HttpResponse("✅ Django is running on Vercel")

# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.decorators import user_passes_test
# from django.contrib.auth.models import User

# ADMIN_EMAIL = "saabiik24@gmail.com"   # put your Gmail here
# def signup(request):
#     if request.method == "POST":
#         username = request.POST.get("username")
#         email = request.POST.get("email")
#         password = request.POST.get("password")

#         if User.objects.filter(email=email).exists():
#             return render(request, "signup.html", {"error": "Email already registered"})

#         User.objects.create_user(username=username, email=email, password=password)
#         return redirect("login")

#     return render(request, "signup.html")

# from django.contrib.auth import authenticate, login
# from django.shortcuts import render, redirect

# def user_login(request):
#     if request.method == "POST":
#         email = request.POST.get("email")
#         password = request.POST.get("password")

#         # Find username from email
#         try:
#             user_obj = User.objects.get(email=email)
#             username = user_obj.username
#         except User.DoesNotExist:
#             return render(request, "login.html", {"error": "Invalid email or password"})

#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)

#             # SPECIAL CASE → Admin email
#             if user.email == "yourgmail@gmail.com":   # <-- SET YOUR ADMIN EMAIL HERE
#                 return redirect("admin_dashboard")

#             # NORMAL USERS → Redirect to donor registration
#             return redirect("home")   # Change to register-blood if you want

#         return render(request, "login.html", {"error": "Invalid credentials"})

#     return render(request, "login.html")




# ------------------ HOME ------------------
def home(request):
    return render(request, 'home.html')



# ------------------ BLOOD DONOR REGISTRATION ------------------
# @login_required(login_url="login")
def register_blood(request):
    if request.method == "POST":
        age = int(request.POST.get("age"))
        mobile = request.POST.get("mobile")

        # Age validation
        if age < 18 or age > 65:
            return render(request, "register_blood.html", {
                "toast": "Age must be between 18 and 65!"
            })

        # Mobile validation
        if not mobile.isdigit() or len(mobile) != 10:
            return render(request, "register_blood.html", {
                "toast": "Mobile number must be 10 digits!"
            })

        # Save donor
        name = request.POST.get("name")
        blood_group = request.POST.get("blood_group")
        location = request.POST.get("location")

        Donor.objects.create(
            name=name,
            age=age,
            blood_group=blood_group,
            mobile=mobile,
            location=location,
            availability=True
        )

        return render(request, "success.html", {
            "toast": "Registration Successful!"
        })

    return render(request, "register_blood.html")





# ------------------ ORGAN DONOR REGISTRATION ------------------
# @login_required(login_url="login")
def register_organ(request):
    if request.method == "POST":
        age = int(request.POST.get("age"))
        mobile = request.POST.get("mobile")

        # AGE VALIDATION
        if age < 18 or age > 65:
            return render(request, "register_organ.html", {
                "toast": "Age must be between 18 and 65!"
            })

        # MOBILE VALIDATION
        if not mobile.isdigit() or len(mobile) != 10:
            return render(request, "register_organ.html", {
                "toast": "Mobile number must be 10 digits!"
            })

        # SAVE DATA
        name = request.POST.get("name")
        organ_type = request.POST.get("organ_type")
        location = request.POST.get("location")

        OrganDonor.objects.create(
            name=name,
            age=age,
            organ_type=organ_type,
            mobile=mobile,
            location=location,
            is_available=True
        )

        return render(request, "success.html", {
            "toast": "Organ Donor Registered Successfully!"
        })

    return render(request, "register_organ.html")







# ------------------ BLOOD DONOR SEARCH ------------------
def search_blood(request):
    # SHOW ALL DONORS BY DEFAULT
    donors = Donor.objects.filter(availability=True)

    if request.method == "POST":
        blood_group = request.POST.get("blood_group")
        location = request.POST.get("location")

        donors = Donor.objects.filter(
            blood_group=blood_group,
            availability=True,
            location__icontains=location
        )

    return render(request, "search_blood.html", {"donors": donors})



def search_organ(request):
    # SHOW ALL ORGAN DONORS BY DEFAULT
    donors = OrganDonor.objects.filter(is_available=True)

    if request.method == "POST":
        organ_type = request.POST.get("organ_type")
        location = request.POST.get("location")

        donors = OrganDonor.objects.filter(
            organ_type=organ_type,
            is_available=True,
            location__icontains=location
        )

    return render(request, "search_organ.html", {"donors": donors})



def contact(request):
    return render(request, "contact.html")

def about(request):
    return render(request, "about.html")




def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        ContactMessage.objects.create(
            name=name,
            email=email,
            message=message
        )

        return render(request, "contact.html", {
            "toast": "Message sent successfully!"
        })

    return render(request, "contact.html")


# @user_passes_test(lambda u: u.email == "saabiik24@gmail.com")
# def admin_dashboard(request):
#     return render(request, "admin_dashboard.html")
