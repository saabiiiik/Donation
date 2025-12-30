from django.db import models


# ------------------ BLOOD DONOR ------------------
class Donor(models.Model):
    BLOOD_GROUP_CHOICES = [
        ("A+", "A+"), ("A-", "A-"),
        ("B+", "B+"), ("B-", "B-"),
        ("O+", "O+"), ("O-", "O-"),
        ("AB+", "AB+"), ("AB-", "AB-"),
    ]

    name = models.CharField(max_length=50)
    age = models.IntegerField()
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    mobile = models.CharField(max_length=15)
    location = models.CharField(max_length=50)
    availability = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.blood_group})"


# ------------------ ORGAN DONOR ------------------
class OrganDonor(models.Model):
    ORGAN_CHOICES = [
        ("Kidney", "Kidney"),
        ("Liver", "Liver"),
        ("Heart", "Heart"),
        ("Lungs", "Lungs"),
        ("Eyes", "Eyes"),
        ("Bone Marrow", "Bone Marrow"),
    ]

    name = models.CharField(max_length=50)
    age = models.IntegerField()
    organ_type = models.CharField(max_length=20, choices=ORGAN_CHOICES)
    mobile = models.CharField(max_length=15)
    location = models.CharField(max_length=50)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.organ_type}"
    


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"

