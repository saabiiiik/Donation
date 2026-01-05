from django.db import models
from django.contrib.auth.models import User


# ------------------ BLOOD DONOR ------------------
class Donor(models.Model):
    BLOOD_GROUP_CHOICES = [
        ("A+", "A+"), ("A-", "A-"),
        ("B+", "B+"), ("B-", "B-"),
        ("O+", "O+"), ("O-", "O-"),
        ("AB+", "AB+"), ("AB-", "AB-"),
    ]

    # 🔹 NEW (for login & dashboard)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    name = models.CharField(max_length=50)
    age = models.IntegerField()
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    mobile = models.CharField(max_length=15)
    location = models.CharField(max_length=50)
    availability = models.BooleanField(default=True)

    # 🔹 NEW (stats)
    total_donations = models.IntegerField(default=0)

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

    # 🔹 NEW (for login & dashboard)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    name = models.CharField(max_length=50)
    age = models.IntegerField()
    organ_type = models.CharField(max_length=20, choices=ORGAN_CHOICES)
    mobile = models.CharField(max_length=15)
    location = models.CharField(max_length=50)
    is_available = models.BooleanField(default=True)

    # 🔹 NEW (stats)
    total_donations = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} - {self.organ_type}"


# ------------------ CONTACT ------------------
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"


class DonationHistory(models.Model):
    DONATION_TYPE_CHOICES = [
        ("Blood", "Blood"),
        ("Organ", "Organ"),
    ]

    STATUS_CHOICES = [
        ("Completed", "Completed"),
        ("Pending", "Pending"),
        ("Cancelled", "Cancelled"),
    ]

    donor = models.ForeignKey(
        Donor,
        on_delete=models.CASCADE,
        related_name="donations"
    )

    donation_type = models.CharField(
        max_length=10,
        choices=DONATION_TYPE_CHOICES
    )

    details = models.CharField(
        max_length=100,
        help_text="Blood group or organ type"
    )

    donated_on = models.DateField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Completed"
    )

    def __str__(self):
        return f"{self.donor.name} - {self.donation_type} ({self.status})"
    

    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.donor.total_donations = self.donor.donations.filter(status="Completed").count()
        self.donor.save()
