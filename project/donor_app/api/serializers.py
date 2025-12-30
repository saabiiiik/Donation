from rest_framework import serializers
from django.contrib.auth.models import User
from donor_app.models import Donor, OrganDonor, ContactMessage

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]

class BloodDonorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donor
        fields = "__all__"

class OrganDonorSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganDonor
        fields = "__all__"

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = "__all__"
