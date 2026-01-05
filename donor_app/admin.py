from django.contrib import admin
from .models import Donor, OrganDonor, ContactMessage, DonationHistory


# ---------------- CONTACT MESSAGE ---------------- #
admin.site.register(ContactMessage)


# ---------------- BLOOD DONOR ADMIN ---------------- #
@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):

    list_display = (
        "id", "name", "blood_group", "mobile",
        "location", "availability", "show_status", "total_donations"
    )

    list_filter = ("blood_group", "availability", "location")

    search_fields = ("name", "mobile", "blood_group", "location")

    list_per_page = 10

    readonly_fields = ("id", "total_donations")

    # Colored status badge
    def show_status(self, obj):
        return "🟢 Available" if obj.availability else "🔴 Not Available"
    show_status.short_description = "Status"

    # Custom admin actions
    actions = ["make_available", "make_unavailable"]

    def make_available(self, request, queryset):
        queryset.update(availability=True)
    make_available.short_description = "Mark selected donors as AVAILABLE"

    def make_unavailable(self, request, queryset):
        queryset.update(availability=False)
    make_unavailable.short_description = "Mark selected donors as NOT AVAILABLE"


# ---------------- ORGAN DONOR ADMIN ---------------- #
@admin.register(OrganDonor)
class OrganDonorAdmin(admin.ModelAdmin):

    list_display = (
        "id", "name", "organ_type", "mobile",
        "location", "is_available", "status_label", "total_donations"
    )

    list_filter = ("organ_type", "is_available", "location")

    search_fields = ("name", "mobile", "organ_type", "location")

    readonly_fields = ("id", "total_donations")

    list_per_page = 10

    def status_label(self, obj):
        return "🟢 Available" if obj.is_available else "🔴 Not Available"
    status_label.short_description = "Status"

    actions = ["set_available", "set_unavailable"]

    def set_available(self, request, queryset):
        queryset.update(is_available=True)
    set_available.short_description = "Mark selected donors as AVAILABLE"

    def set_unavailable(self, request, queryset):
        queryset.update(is_available=False)
    set_unavailable.short_description = "Mark selected donors as NOT AVAILABLE"


# ---------------- DONATION HISTORY ADMIN (NEW) ---------------- #
@admin.register(DonationHistory)
class DonationHistoryAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",              # ✅ FIXED
        "donation_type",
        "details",
        "donated_on",
        "status",
    )

    list_filter = ("donation_type", "status", "donated_on")

    search_fields = (
        "user__username",    # ✅ mobile stored as username
        "details",
    )

    readonly_fields = ("donated_on",)
    list_per_page = 20

