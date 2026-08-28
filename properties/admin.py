from django.contrib import admin

from .models import (
    Estate,
    EstateType,
    EstateTypeImage,
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
    MarketplaceFavourite,
    MarketplaceMessage,
    MarketplaceReport,
    MarketplaceReview,
    AccountSettings,
    MarketplaceListingImage,
)


# =========================================================
# ESTATE TYPE IMAGE INLINE
# =========================================================

class EstateTypeImageInline(admin.TabularInline):

    model = EstateTypeImage
    extra = 3

    fields = (
        'image',
        'caption',
    )


# =========================================================
# PROPERTY GALLERY INLINE
# =========================================================

class PropertyImageInline(admin.TabularInline):

    model = PropertyImage
    extra = 3

    fields = (
        'image',
        'caption',
    )


# =========================================================
# ESTATE TYPE INLINE
# =========================================================

class EstateTypeInline(admin.TabularInline):

    model = EstateType
    extra = 1

    fields = (
        'name',
        'price',
        'plot_size',
        'description',
        'image',
        'digital_layout',
        'proposed_company_plan',
    )


# =========================================================
# ESTATE ADMIN
# =========================================================

@admin.register(Estate)
class EstateAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'location',
        'property_count',
        'type_count',
        'created_at',
    )

    search_fields = (
        'name',
        'location',
        'description',
    )

    ordering = (
        'name',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    inlines = [
        EstateTypeInline,
    ]

    fieldsets = (
        (
            'Estate Information',
            {
                'fields': (
                    'name',
                    'location',
                    'description',
                )
            }
        ),
        (
            'Estate Media',
            {
                'fields': (
                    'image',
                    'digital_layout',
                )
            }
        ),
        (
            'System Information',
            {
                'fields': (
                    'created_at',
                    'updated_at',
                )
            }
        ),
    )

    @admin.display(description='Plots')
    def property_count(self, obj):
        return obj.properties.count()

    @admin.display(description='Types')
    def type_count(self, obj):
        return obj.estate_types.count()


# =========================================================
# ESTATE TYPE ADMIN
# =========================================================

@admin.register(EstateType)
class EstateTypeAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'estate',
        'price',
        'plot_size',
        'property_count',
        'created_at',
    )

    list_filter = (
        'estate',
        'created_at',
    )

    search_fields = (
        'name',
        'estate__name',
        'description',
        'plot_size',
        'what_comes_with_it',
    )

    ordering = (
        'estate',
        'name',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    inlines = [
        EstateTypeImageInline,
    ]

    fieldsets = (
        (
            'Estate Type Information',
            {
                'fields': (
                    'estate',
                    'name',
                    'description',
                    'price',
                    'plot_size',
                    'what_comes_with_it',
                )
            }
        ),
        (
            'Documents & Layout',
            {
                'fields': (
                    'proposed_company_plan',
                    'digital_layout',
                )
            }
        ),
        (
            'Images',
            {
                'fields': (
                    'image',
                )
            }
        ),
        (
            'System Information',
            {
                'fields': (
                    'created_at',
                    'updated_at',
                )
            }
        ),
    )

    @admin.display(description='Plots')
    def property_count(self, obj):
        return obj.properties.count()


# =========================================================
# PROPERTY ADMIN
# =========================================================

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'plot_number',
        'estate',
        'estate_type',
        'property_type',
        'land_size',
        'location',
        'price',
        'status',
        'created_at',
    )

    list_filter = (
        'estate',
        'estate_type',
        'property_type',
        'status',
    )

    search_fields = (
        'title',
        'plot_number',
        'location',
        'land_size',
        'estate__name',
        'estate_type__name',
    )

    ordering = (
        '-created_at',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    inlines = [
        PropertyImageInline,
    ]

    fieldsets = (
        (
            'Estate Assignment',
            {
                'fields': (
                    'estate',
                    'estate_type',
                )
            }
        ),
        (
            'Property Information',
            {
                'fields': (
                    'title',
                    'property_type',
                    'plot_number',
                    'land_size',
                    'location',
                    'price',
                    'status',
                    'description',
                )
            }
        ),
        (
            'Location Coordinates',
            {
                'fields': (
                    'latitude',
                    'longitude',
                ),
                'classes': (
                    'collapse',
                ),
            }
        ),
        (
            'Agent',
            {
                'fields': (
                    'agent',
                )
            }
        ),
        (
            'Main Image',
            {
                'fields': (
                    'image',
                )
            }
        ),
        (
            'System Information',
            {
                'fields': (
                    'created_at',
                    'updated_at',
                )
            }
        ),
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
        'created_at',
    )

    list_filter = (
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

class MarketplaceListingImageInline(admin.TabularInline):

    model = MarketplaceListingImage
    extra = 3

    fields = (
        'image',
    )

# =========================================================
# MARKETPLACE LISTING
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
        'approval_status',
        'views',
        'created_at',
    )

    list_filter = (
        'category',
        'status',
        'approval_status',
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
        'approval_status',
    )

    readonly_fields = (
        'views',
        'created_at',
        'updated_at',
    )

    inlines = [
        MarketplaceListingImageInline,
    ]

    ordering = (
        '-created_at',
    )

    fieldsets = (
        (
            'Listing Information',
            {
                'fields': (
                    'seller',
                    'title',
                    'category',
                    'price',
                    'location',
                    'description',
                    'image',
                )
            }
        ),
        (
            'Listing Status',
            {
                'fields': (
                    'status',
                    'approval_status',
                )
            }
        ),
        (
            'Marketplace Statistics',
            {
                'fields': (
                    'views',
                )
            }
        ),
        (
            'System Information',
            {
                'fields': (
                    'created_at',
                    'updated_at',
                )
            }
        ),
    )
# =========================================================
# MARKETPLACE MESSAGE
# =========================================================

@admin.register(MarketplaceMessage)
class MarketplaceMessageAdmin(admin.ModelAdmin):

    list_display = (
        'listing',
        'sender',
        'receiver',
        'is_read',
        'created_at',
    )

    list_filter = (
        'is_read',
        'created_at',
    )

    search_fields = (
        'listing__title',
        'sender__username',
        'sender__email',
        'receiver__username',
        'receiver__email',
        'message',
    )

    ordering = (
        '-created_at',
    )

    readonly_fields = (
        'created_at',
    )


# =========================================================
# MARKETPLACE REPORT
# =========================================================

@admin.register(MarketplaceReport)
class MarketplaceReportAdmin(admin.ModelAdmin):

    list_display = (
        'listing',
        'reporter',
        'reason',
        'status',
        'created_at',
    )

    list_filter = (
        'reason',
        'status',
        'created_at',
    )

    search_fields = (
        'listing__title',
        'reporter__username',
        'reporter__email',
        'description',
    )

    ordering = (
        '-created_at',
    )

    readonly_fields = (
        'created_at',
    )


# =========================================================
# MARKETPLACE REVIEW
# =========================================================

@admin.register(MarketplaceReview)
class MarketplaceReviewAdmin(admin.ModelAdmin):

    list_display = (
        'listing',
        'reviewer',
        'rating',
        'is_approved',
        'created_at',
    )

    list_filter = (
        'rating',
        'is_approved',
        'created_at',
    )

    search_fields = (
        'listing__title',
        'reviewer__username',
        'reviewer__email',
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

    @admin.action(description='Approve selected reviews')
    def approve_reviews(self, request, queryset):

        updated = queryset.update(
            is_approved=True
        )

        self.message_user(
            request,
            f'{updated} marketplace review(s) approved successfully.'
        )

    @admin.action(description='Unapprove selected reviews')
    def unapprove_reviews(self, request, queryset):

        updated = queryset.update(
            is_approved=False
        )

        self.message_user(
            request,
            f'{updated} marketplace review(s) have been unapproved.'
        )


# =========================================================
# ACCOUNT SETTINGS
# =========================================================

@admin.register(AccountSettings)
class AccountSettingsAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'phone',
        'property_alerts',
        'plot_availability_alerts',
        'estate_alerts',
        'hire_notifications',
        'profile_visible',
        'updated_at',
    )

    list_filter = (
        'property_alerts',
        'plot_availability_alerts',
        'estate_alerts',
        'hire_notifications',
        'security_notifications',
        'profile_visible',
    )

    search_fields = (
        'user__username',
        'user__email',
        'user__first_name',
        'phone',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )