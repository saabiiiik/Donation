from django.db import models
from django.contrib.auth.models import User


# ================== BLOOD DONOR ==================
class Donor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    BLOOD_GROUP_CHOICES = [
        ("A+", "A+"), ("A-", "A-"),
        ("B+", "B+"), ("B-", "B-"),
        ("O+", "O+"), ("O-", "O-"),
        ("AB+", "AB+"), ("AB-", "AB-"),
    ]

    name = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    mobile = models.CharField(max_length=10)
    location = models.CharField(max_length=50)
    availability = models.BooleanField(default=True)

    total_donations = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.blood_group})"


# ================== ORGAN DONOR ==================
class OrganDonor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    ORGAN_CHOICES = [
        ("Kidney", "Kidney"),
        ("Liver", "Liver"),
        ("Heart", "Heart"),
        ("Lungs", "Lungs"),
        ("Eyes", "Eyes"),
        ("Bone Marrow", "Bone Marrow"),
    ]

    name = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    organ_type = models.CharField(max_length=20, choices=ORGAN_CHOICES)
    mobile = models.CharField(max_length=10)
    location = models.CharField(max_length=50)
    is_available = models.BooleanField(default=True)

    total_donations = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} - {self.organ_type}"


# ================== DONATION HISTORY ==================
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

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    donation_type = models.CharField(max_length=10, choices=DONATION_TYPE_CHOICES)
    details = models.CharField(max_length=100)
    donated_on = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Completed")

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if self.status == "Completed" and is_new:
            if self.donation_type == "Blood":
                donor = Donor.objects.filter(user=self.user).first()
                if donor:
                    donor.total_donations += 1
                    donor.save(update_fields=["total_donations"])

            elif self.donation_type == "Organ":
                organ_donor = OrganDonor.objects.filter(user=self.user).first()
                if organ_donor:
                    organ_donor.total_donations += 1
                    organ_donor.save(update_fields=["total_donations"])


# ================== CONTACT ==================
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"
