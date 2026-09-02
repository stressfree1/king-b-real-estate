from django.contrib.admin import AdminSite
from django.db.models import Count

from .models import (
    Estate,
    Property,
    Customer,
    SkilledWorker,
    MarketplaceListing,
    Inquiry,
    JobApplicant,
)


class KingBAdminSite(AdminSite):
    site_header = "KING B REAL ESTATE"
    site_title = "King B Administration"
    index_title = "Business Management"

    def index(self, request, extra_context=None):
        """
        Premium King B admin dashboard.
        Uses live database information.
        """

        extra_context = extra_context or {}

        # =====================================================
        # BASIC COUNTS
        # =====================================================

        extra_context["property_count"] = Property.objects.count()

        extra_context["estate_count"] = Estate.objects.count()

        extra_context["customer_count"] = Customer.objects.count()

        extra_context["worker_count"] = SkilledWorker.objects.count()

        extra_context["marketplace_count"] = (
            MarketplaceListing.objects.count()
        )

        extra_context["inquiry_count"] = Inquiry.objects.count()

        extra_context["job_application_count"] = (
            JobApplicant.objects.count()
        )

        # =====================================================
        # PROPERTY STATUS
        # =====================================================

        extra_context["available_property_count"] = (
            Property.objects.filter(
                status__iexact="available"
            ).count()
        )

        extra_context["sold_property_count"] = (
            Property.objects.filter(
                status__iexact="sold"
            ).count()
        )

        extra_context["reserved_property_count"] = (
            Property.objects.filter(
                status__iexact="reserved"
            ).count()
        )

        # =====================================================
        # MARKETPLACE APPROVALS
        # =====================================================

        extra_context["pending_marketplace_count"] = (
            MarketplaceListing.objects.filter(
                approval_status="under_review"
            ).count()
        )

        extra_context["pending_count"] = (
            MarketplaceListing.objects.filter(
                approval_status="under_review"
            ).count()
        )

        # =====================================================
        # AVAILABLE PROPERTY PERCENTAGE
        # =====================================================

        total_properties = Property.objects.count()

        available_properties = (
            Property.objects.filter(
                status__iexact="available"
            ).count()
        )

        if total_properties > 0:
            available_percentage = round(
                (available_properties / total_properties) * 100
            )
        else:
            available_percentage = 0

        extra_context["available_percentage"] = (
            available_percentage
        )

        # =====================================================
        # CALL ORIGINAL ADMIN INDEX
        # =====================================================

        return super().index(
            request,
            extra_context=extra_context,
        )


# =============================================================
# KING B ADMIN SITE
# =============================================================

kingb_admin_site = KingBAdminSite(
    name="kingb_admin"
)