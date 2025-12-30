from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from donor_app.models import Donor, OrganDonor, ContactMessage
from .serializers import *

# ---------- SIGNUP ----------
@api_view(['POST'])
def signup(request):
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")

    if User.objects.filter(email=email).exists():
        return Response({"error": "Email already registered"}, status=400)

    user = User.objects.create_user(username=username, email=email, password=password)
    token, _ = Token.objects.get_or_create(user=user)

    return Response({"message": "Signup successful", "token": token.key})
    

# ---------- LOGIN ----------
@api_view(['POST'])
def login_api(request):
    email = request.data.get("email")
    password = request.data.get("password")

    try:
        user = User.objects.get(email=email)
    except:
        return Response({"error": "Invalid email or password"}, status=400)

    auth = authenticate(username=user.username, password=password)
    if not auth:
        return Response({"error": "Invalid credentials"}, status=400)

    token, _ = Token.objects.get_or_create(user=user)

    return Response({"message": "Login successful", "token": token.key})


# ---------- REGISTER BLOOD DONOR ----------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_blood_api(request):
    serializer = BloodDonorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Blood donor registered successfully!"})
    return Response(serializer.errors, status=400)


# ---------- REGISTER ORGAN DONOR ----------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_organ_api(request):
    serializer = OrganDonorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Organ donor registered successfully!"})
    return Response(serializer.errors, status=400)


# ---------- SEARCH BLOOD ----------
@api_view(['POST'])
def search_blood_api(request):
    group = request.data.get("blood_group")
    location = request.data.get("location")

    donors = Donor.objects.filter(blood_group=group, availability=True, location__icontains=location)
    serializer = BloodDonorSerializer(donors, many=True)
    return Response(serializer.data)


# ---------- CONTACT MESSAGE ----------
@api_view(['POST'])
def contact_api(request):
    serializer = ContactSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Message sent successfully!"})
    return Response(serializer.errors, status=400)
