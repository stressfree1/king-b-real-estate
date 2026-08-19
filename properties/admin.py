from django.contrib import admin

from .models import (
    Estate,
    Property,
    PropertyImage,
    Agent,
    Inquiry,
    Job,
    JobApplicant,
    ContactMessage,
    SkilledWorker,
    Customer,
    WorkerHire,
    WorkerReview,
    CustomerReview,
    MarketplaceListing,
    MarketplaceImage,
    MarketplaceListing,
    MarketplaceImage,
    MarketplaceFavourite,
    MarketplaceMessage,
    MarketplaceReport,
    MarketplaceReview,
)


# =========================================================
# PROPERTY GALLERY
# =========================================================

class PropertyImageInline(admin.TabularInline):

    model = PropertyImage

    extra = 3

    fields = (
        'image',
        'caption',
    )


# =========================================================
# PROPERTY ADMIN
# =========================================================

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'estate',
        'property_type',
        'location',
        'price',
        'status',
        'latitude',
        'longitude',
        'created_at',
    )

    list_filter = (
        'property_type',
        'status',
        'estate',
    )

    search_fields = (
        'title',
        'location',
        'plot_number',
        'estate__name',
    )

    ordering = (
        '-created_at',
    )

    inlines = [
        PropertyImageInline,
    ]


# =========================================================
# ESTATE
# =========================================================

@admin.register(Estate)
class EstateAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'location',
    )

    search_fields = (
        'name',
        'location',
    )


# =========================================================
# AGENT
# =========================================================

@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'phone',
        'email',
    )

    search_fields = (
        'name',
        'phone',
        'email',
    )


# =========================================================
# INQUIRY
# =========================================================

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'email',
        'phone',
        'property',
        'created_at',
    )

    list_filter = (
        'created_at',
    )

    search_fields = (
        'name',
        'email',
        'phone',
        'property__title',
    )

    ordering = (
        '-created_at',
    )

    readonly_fields = (
        'created_at',
    )


# =========================================================
# JOB
# =========================================================

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'category',
        'location',
        'employment_type',
        'status',
        'application_deadline',
        'created_at',
    )

    list_filter = (
        'status',
        'employment_type',
        'category',
        'created_at',
    )

    search_fields = (
        'title',
        'category',
        'location',
        'description',
    )

    ordering = (
        '-created_at',
    )

    readonly_fields = (
        'created_at',
    )


# =========================================================
# JOB APPLICANTS
# =========================================================

@admin.register(JobApplicant)
class JobApplicantAdmin(admin.ModelAdmin):

    list_display = (
        'full_name',
        'job',
        'phone',
        'email',
        'skill',
        'years_of_experience',
        'status',
        'applied_at',
    )

    list_filter = (
        'status',
        'job',
        'applied_at',
    )

    search_fields = (
        'full_name',
        'email',
        'phone',
        'skill',
        'job__title',
    )

    ordering = (
        '-applied_at',
    )

    readonly_fields = (
        'applied_at',
    )


# =========================================================
# CONTACT MESSAGES
# =========================================================

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'email',
        'phone',
        'subject',
        'created_at',
    )

    list_filter = (
        'created_at',
    )

    search_fields = (
        'name',
        'email',
        'phone',
        'subject',
        'message',
    )

    ordering = (
        '-created_at',
    )

    readonly_fields = (
        'created_at',
    )


# =========================================================
# SKILLED WORKERS
# =========================================================

@admin.register(SkilledWorker)
class SkilledWorkerAdmin(admin.ModelAdmin):

    list_display = (
        'full_name',
        'skill',
        'phone',
        'email',
        'location',
        'years_of_experience',
        'availability',
        'is_approved',
        'created_at',
    )

    list_filter = (
        'skill',
        'availability',
        'is_approved',
        'created_at',
    )

    search_fields = (
        'full_name',
        'phone',
        'email',
        'skill',
        'location',
    )

    ordering = (
        '-created_at',
    )

    readonly_fields = (
        'created_at',
    )


# =========================================================
# CUSTOMERS
# =========================================================

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):

    list_display = (
        'full_name',
        'phone',
        'email',
        'address',
        'is_verified',
        'created_at',
    )

    list_filter = (
        'is_verified',
        'created_at',
    )

    search_fields = (
        'full_name',
        'phone',
        'email',
        'address',
    )

    ordering = (
        '-created_at',
    )

    readonly_fields = (
        'created_at',
    )


# =========================================================
# WORKER HIRES
# =========================================================

@admin.register(WorkerHire)
class WorkerHireAdmin(admin.ModelAdmin):

    list_display = (
        'customer',
        'worker',
        'service',
        'status',
        'hired_at',
        'completed_at',
    )

    list_filter = (
        'status',
        'hired_at',
        'completed_at',
    )

    search_fields = (
        'customer__full_name',
        'customer__email',
        'worker__full_name',
        'worker__skill',
        'service',
    )

    ordering = (
        '-hired_at',
    )

    readonly_fields = (
        'hired_at',
    )


# =========================================================
# CUSTOMER → WORKER REVIEWS
# =========================================================

@admin.register(WorkerReview)
class WorkerReviewAdmin(admin.ModelAdmin):

    list_display = (
        'customer_name',
        'worker_name',
        'rating',
        'is_approved',
        'created_at',
    )

    list_filter = (
        'is_approved',
        'rating',
        'created_at',
    )

    search_fields = (
        'hire__customer__full_name',
        'hire__customer__email',
        'hire__worker__full_name',
        'hire__worker__skill',
        'comment',
    )

    ordering = (
        '-created_at',
    )

    readonly_fields = (
        'created_at',
    )

    actions = (
        'approve_reviews',
        'unapprove_reviews',
    )

    @admin.display(description='Customer')
    def customer_name(self, obj):
        return obj.hire.customer.full_name

    @admin.display(description='Worker')
    def worker_name(self, obj):
        return obj.hire.worker.full_name

    @admin.action(description='Approve selected reviews')
    def approve_reviews(self, request, queryset):

        updated = queryset.update(
            is_approved=True
        )

        self.message_user(
            request,
            f'{updated} review(s) approved successfully.'
        )

    @admin.action(description='Unapprove selected reviews')
    def unapprove_reviews(self, request, queryset):

        updated = queryset.update(
            is_approved=False
        )

        self.message_user(
            request,
            f'{updated} review(s) have been unapproved.'
        )


# =========================================================
# WORKER → CUSTOMER REVIEWS
# =========================================================

@admin.register(CustomerReview)
class CustomerReviewAdmin(admin.ModelAdmin):

    list_display = (
        'worker_name',
        'customer_name',
        'rating',
        'is_approved',
        'created_at',
    )

    list_filter = (
        'is_approved',
        'rating',
        'created_at',
    )

    search_fields = (
        'hire__worker__full_name',
        'hire__worker__skill',
        'hire__customer__full_name',
        'hire__customer__email',
        'comment',
    )

    ordering = (
        '-created_at',
    )

    readonly_fields = (
        'created_at',
    )

    actions = (
        'approve_reviews',
        'unapprove_reviews',
    )

    @admin.display(description='Worker')
    def worker_name(self, obj):
        return obj.hire.worker.full_name

    @admin.display(description='Customer')
    def customer_name(self, obj):
        return obj.hire.customer.full_name

    @admin.action(description='Approve selected reviews')
    def approve_reviews(self, request, queryset):

        updated = queryset.update(
            is_approved=True
        )

        self.message_user(
            request,
            f'{updated} customer review(s) approved successfully.'
        )

    @admin.action(description='Unapprove selected reviews')
    def unapprove_reviews(self, request, queryset):

        updated = queryset.update(
            is_approved=False
        )

        self.message_user(
            request,
            f'{updated} customer review(s) have been unapproved.'
        )

# =========================================================
# MARKETPLACE IMAGE INLINE
# =========================================================

class MarketplaceImageInline(admin.TabularInline):

    model = MarketplaceImage

    extra = 3

    fields = (
        'image',
    )


# =========================================================
# MARKETPLACE LISTING ADMIN
# =========================================================

@admin.register(MarketplaceListing)
class MarketplaceListingAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'seller',
        'category',
        'price',
        'location',
        'status',
        'is_approved',
        'created_at',
    )

    list_filter = (
        'category',
        'status',
        'is_approved',
        'created_at',
    )

    search_fields = (
        'title',
        'description',
        'location',
        'seller__username',
        'seller__email',
    )

    list_editable = (
        'status',
        'is_approved',
    )

    inlines = [
        MarketplaceImageInline
    ]

    ordering = (
        '-created_at',
    )