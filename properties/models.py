from django.db import models
from django.contrib.auth.models import User


# =========================================================
# ESTATE
# =========================================================

class Estate(models.Model):

    name = models.CharField(
        max_length=200
    )

    location = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True
    )

    # =====================================================
    # ESTATE MEDIA
    # =====================================================

    image = models.ImageField(
        upload_to='estates/',
        blank=True,
        null=True
    )

    digital_layout = models.FileField(
        upload_to='estates/layouts/',
        blank=True,
        null=True
    )

    # =====================================================
    # ESTATE DEVELOPMENT PLAN
    # =====================================================

    development_plan_title = models.CharField(
        max_length=200,
        blank=True
    )

    development_plan = models.FileField(
        upload_to='estates/development_plans/',
        blank=True,
        null=True
    )

    development_features = models.TextField(
        blank=True
    )

    # =====================================================
    # SYSTEM INFORMATION
    # =====================================================

    created_at = models.DateTimeField(
        null=True,
        blank=True
    )

    updated_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


# =========================================================
# ESTATE TYPE
# =========================================================

class EstateType(models.Model):

    estate = models.ForeignKey(
        Estate,
        on_delete=models.CASCADE,
        related_name='estate_types'
    )

    name = models.CharField(
        max_length=100
    )

    description = models.TextField(
        blank=True
    )

    price = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )

    plot_size = models.CharField(
        max_length=100,
        blank=True
    )

    what_comes_with_it = models.TextField(
        blank=True
    )

    proposed_company_plan = models.FileField(
        upload_to='estates/company_plans/',
        blank=True,
        null=True
    )

    digital_layout = models.FileField(
        upload_to='estates/type_layouts/',
        blank=True,
        null=True
    )

    image = models.ImageField(
        upload_to='estates/types/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = [
            'estate',
            'name'
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    'estate',
                    'name'
                ],
                name='unique_estate_type_name'
            )
        ]

    def __str__(self):
        return f"{self.estate.name} - {self.name}"


# =========================================================
# ESTATE TYPE GALLERY
# =========================================================

class EstateTypeImage(models.Model):

    estate_type = models.ForeignKey(
        EstateType,
        on_delete=models.CASCADE,
        related_name='gallery_images'
    )

    image = models.ImageField(
        upload_to='estates/types/gallery/'
    )

    caption = models.CharField(
        max_length=200,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.estate_type} - "
            f"{self.caption or 'Image'}"
        )


# =========================================================
# AGENT
# =========================================================

class Agent(models.Model):

    name = models.CharField(
        max_length=200
    )

    phone = models.CharField(
        max_length=50
    )

    email = models.EmailField(
        blank=True
    )

    bio = models.TextField(
        blank=True
    )

    def __str__(self):
        return self.name


# =========================================================
# PROPERTY / PLOT
# =========================================================

class Property(models.Model):

    PROPERTY_TYPES = [
        ('land', 'Land'),
        ('house', 'House'),
        ('apartment', 'Apartment'),
        ('commercial', 'Commercial Property'),
    ]

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('reserved', 'Reserved'),
        ('sold', 'Sold'),
    ]

    # =====================================================
    # ESTATE
    # =====================================================

    estate = models.ForeignKey(
        Estate,
        on_delete=models.CASCADE,
        related_name='properties'
    )

    # =====================================================
    # ESTATE TYPE
    # =====================================================

    estate_type = models.ForeignKey(
        EstateType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='properties'
    )

    # =====================================================
    # AGENT
    # =====================================================

    agent = models.ForeignKey(
        Agent,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='properties'
    )

    # =====================================================
    # PROPERTY INFORMATION
    # =====================================================

    title = models.CharField(
        max_length=200
    )

    property_type = models.CharField(
        max_length=50,
        choices=PROPERTY_TYPES
    )

    plot_number = models.CharField(
        max_length=50,
        blank=True
    )

    land_size = models.CharField(
        max_length=100,
        blank=True
    )

    location = models.CharField(
        max_length=200
    )

    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )

    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )

    price = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available'
    )

    description = models.TextField()

    image = models.ImageField(
        upload_to='properties/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.title


# =========================================================
# PROPERTY GALLERY
# =========================================================

class PropertyImage(models.Model):

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='gallery_images'
    )

    image = models.ImageField(
        upload_to='properties/gallery/'
    )

    caption = models.CharField(
        max_length=200,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.property.title} - Gallery Image"


# =========================================================
# PROPERTY INQUIRY
# =========================================================

class Inquiry(models.Model):

    name = models.CharField(
        max_length=200
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=50
    )

    property = models.ForeignKey(
        Property,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='inquiries'
    )

    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name


# =========================================================
# JOB
# =========================================================

class Job(models.Model):

    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
    ]

    EMPLOYMENT_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('temporary', 'Temporary'),
        ('internship', 'Internship'),
    ]

    title = models.CharField(
        max_length=200
    )

    category = models.CharField(
        max_length=100
    )

    location = models.CharField(
        max_length=200
    )

    employment_type = models.CharField(
        max_length=50,
        choices=EMPLOYMENT_TYPE_CHOICES,
        default='full_time'
    )

    salary = models.CharField(
        max_length=100,
        blank=True
    )

    description = models.TextField()

    responsibilities = models.TextField(
        blank=True
    )

    requirements = models.TextField()

    experience_required = models.CharField(
        max_length=100,
        blank=True
    )

    benefits = models.TextField(
        blank=True
    )

    application_deadline = models.DateField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='open'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title


# =========================================================
# JOB APPLICANT
# =========================================================

class JobApplicant(models.Model):

    STATUS_CHOICES = [
        ('received', 'Received'),
        ('under_review', 'Under Review'),
        ('contacted', 'Contacted'),
        ('selected', 'Selected'),
        ('rejected', 'Rejected'),
    ]

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='applicants'
    )

    full_name = models.CharField(
        max_length=200
    )

    phone = models.CharField(
        max_length=50
    )

    email = models.EmailField()

    skill = models.CharField(
        max_length=100
    )

    years_of_experience = models.PositiveIntegerField(
        default=0
    )

    id_type = models.CharField(
        max_length=50,
        choices=[
            ('national_id', 'National ID'),
            ('drivers_license', "Driver's License"),
            ('international_passport', 'International Passport'),
            ('voters_card', "Voter's Card"),
            ('other', 'Other'),
        ],
        blank=True
    )

    id_number = models.CharField(
        max_length=100,
        blank=True
    )

    id_document = models.FileField(
        upload_to='job_applications/id_documents/',
        blank=True,
        null=True
    )

    cv = models.FileField(
        upload_to='job_applications/cv/',
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='received'
    )

    applied_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.full_name


# =========================================================
# CONTACT MESSAGE
# =========================================================

class ContactMessage(models.Model):

    name = models.CharField(
        max_length=150
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=30,
        blank=True
    )

    subject = models.CharField(
        max_length=200
    )

    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.name} - {self.subject}"


# =========================================================
# MARKETPLACE ACCOUNT
# =========================================================

class MarketplaceAccount(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='marketplace_account'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return (
            f"{self.user.get_full_name()} - "
            f"General Account"
        )


# =========================================================
# SKILLED WORKER
# =========================================================

class SkilledWorker(models.Model):

    ID_TYPE_CHOICES = [
        ('national_id', 'National ID'),
        ('drivers_license', "Driver's License"),
        ('international_passport', 'International Passport'),
        ('voters_card', "Voter's Card"),
        ('other', 'Other'),
    ]

    AVAILABILITY_CHOICES = [
        ('available', 'Available'),
        ('not_available', 'Not Available'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='skilled_worker_profile',
        null=True,
        blank=True
    )

    full_name = models.CharField(
        max_length=200
    )

    phone = models.CharField(
        max_length=50
    )

    email = models.EmailField(
        blank=True
    )

    skill = models.CharField(
        max_length=100
    )

    years_of_experience = models.PositiveIntegerField(
        default=0
    )

    location = models.CharField(
        max_length=200
    )

    description = models.TextField()

    services = models.TextField(
        blank=True
    )

    profile_image = models.ImageField(
        upload_to='skilled_workers/profiles/',
        blank=True,
        null=True
    )

    id_type = models.CharField(
        max_length=50,
        choices=ID_TYPE_CHOICES,
        blank=True
    )

    id_number = models.CharField(
        max_length=100,
        blank=True
    )

    id_document = models.FileField(
        upload_to='skilled_workers/id_documents/',
        blank=True,
        null=True
    )

    cv = models.FileField(
        upload_to='skilled_workers/cv/',
        blank=True,
        null=True
    )

    availability = models.CharField(
        max_length=30,
        choices=AVAILABILITY_CHOICES,
        default='available'
    )

    email_verified = models.BooleanField(
    default=False
    )

    is_approved = models.BooleanField(
    default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.full_name


# =========================================================
# CUSTOMER
# =========================================================

class Customer(models.Model):

    ID_TYPE_CHOICES = [
        ('national_id', 'National ID'),
        ('drivers_license', "Driver's Licence"),
        ('passport', 'International Passport'),
        ('voters_card', "Voter's Card"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='customer_profile',
        null=True,
        blank=True
    )

    full_name = models.CharField(
        max_length=200
    )

    phone = models.CharField(
        max_length=50
    )

    email = models.EmailField(
        blank=True
    )

    address = models.CharField(
        max_length=300,
        blank=True
    )

    id_type = models.CharField(
        max_length=30,
        choices=ID_TYPE_CHOICES,
        blank=True,
        default=''
    )

    id_number = models.CharField(
        max_length=100,
        blank=True,
        default=''
    )

    id_document = models.FileField(
        upload_to='customer_ids/',
        blank=True,
        null=True
    )

    email_verified = models.BooleanField(
    default=False
    )

    is_approved = models.BooleanField(
    default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.full_name


# =========================================================
# UNIFIED ACCOUNT SETTINGS
# =========================================================

class AccountSettings(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='account_settings'
    )

    phone = models.CharField(
        max_length=50,
        blank=True
    )

    address = models.CharField(
        max_length=300,
        blank=True
    )

    profile_image = models.ImageField(
        upload_to='account_profiles/',
        blank=True,
        null=True
    )

    property_alerts = models.BooleanField(
        default=True
    )

    plot_availability_alerts = models.BooleanField(
        default=True
    )

    estate_alerts = models.BooleanField(
        default=True
    )

    hire_notifications = models.BooleanField(
        default=True
    )

    security_notifications = models.BooleanField(
        default=True
    )

    profile_visible = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return (
            f"{self.user.get_full_name() or self.user.username} "
            f"- Account Settings"
        )


# =========================================================
# WORKER HIRE
# =========================================================

class WorkerHire(models.Model):

    STATUS_CHOICES = [
        ('requested', 'Pending'),
        ('active', 'Accepted'),
        ('declined', 'Declined'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='worker_hires'
    )

    worker = models.ForeignKey(
        SkilledWorker,
        on_delete=models.CASCADE,
        related_name='customer_hires'
    )

    service = models.CharField(
        max_length=200
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='requested'
    )

    hired_at = models.DateTimeField(
        auto_now_add=True
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    notes = models.TextField(
        blank=True
    )

    def __str__(self):
        return (
            f"{self.customer.full_name} - "
            f"{self.worker.full_name}"
        )

# =========================================================
# SKILLED WORKER ↔ CUSTOMER MESSAGES
# =========================================================

class WorkerMessage(models.Model):

    hire = models.ForeignKey(
        WorkerHire,
        on_delete=models.CASCADE,
        related_name='messages'
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='worker_messages_sent'
    )

    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='worker_messages_received'
    )

    message = models.TextField()

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return (
            f"{self.sender.username} → "
            f"{self.receiver.username}"
        )

    class Meta:

        ordering = ['created_at']
        
# =========================================================
# CUSTOMER → WORKER REVIEW
# =========================================================

class WorkerReview(models.Model):

    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]

    hire = models.OneToOneField(
        WorkerHire,
        on_delete=models.CASCADE,
        related_name='worker_review'
    )

    rating = models.PositiveIntegerField(
        choices=RATING_CHOICES
    )

    comment = models.TextField()

    is_approved = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.hire.customer.full_name} → "
            f"{self.hire.worker.full_name} "
            f"({self.rating} Stars)"
        )


# =========================================================
# WORKER → CUSTOMER REVIEW
# =========================================================

class CustomerReview(models.Model):

    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]

    hire = models.OneToOneField(
        WorkerHire,
        on_delete=models.CASCADE,
        related_name='customer_review'
    )

    rating = models.PositiveIntegerField(
        choices=RATING_CHOICES
    )

    comment = models.TextField()

    is_approved = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.hire.worker.full_name} → "
            f"{self.hire.customer.full_name} "
            f"({self.rating} Stars)"
        )

# =========================================================
# MARKETPLACE LISTING
# =========================================================

class MarketplaceListing(models.Model):

    # =====================================================
    # CATEGORY
    # =====================================================

    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('vehicles', 'Vehicles'),
        ('furniture', 'Furniture'),
        ('building_materials', 'Building Materials'),
        ('home_appliances', 'Home Appliances'),
        ('fashion', 'Fashion'),
        ('services', 'Services'),
        ('land', 'Land'),
        ('property', 'Property'),
        ('tools', 'Tools'),
        ('other', 'Other'),
    ]

    # =====================================================
    # SALES STATUS
    # =====================================================

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('sold', 'Sold'),
        ('reserved', 'Reserved'),
    ]

    # =====================================================
    # ADMIN APPROVAL STATUS
    # =====================================================

    APPROVAL_STATUS_CHOICES = [
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    # =====================================================
    # SELLER
    # =====================================================

    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='marketplace_listings'
    )

    # =====================================================
    # LISTING INFORMATION
    # =====================================================

    title = models.CharField(
        max_length=200
    )

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES
    )

    price = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    location = models.CharField(
        max_length=200
    )

    description = models.TextField()

    image = models.ImageField(
        upload_to='marketplace/',
        blank=True,
        null=True
    )

        # =====================================================
    # LISTING DETAILS
    # =====================================================

    SUBCATEGORY_CHOICES = [
        ('', 'Select subcategory'),
        ('new', 'New'),
        ('used', 'Used'),
        ('refurbished', 'Refurbished'),
    ]

    CONDITION_CHOICES = [
        ('new', 'New'),
        ('used', 'Used'),
        ('refurbished', 'Refurbished'),
        ('fair', 'Fair'),
    ]

    PRICE_TYPE_CHOICES = [
        ('fixed', 'Fixed Price'),
        ('negotiable', 'Negotiable'),
        ('contact', 'Contact Seller'),
    ]

    subcategory = models.CharField(
        max_length=100,
        blank=True
    )

    condition = models.CharField(
        max_length=30,
        choices=CONDITION_CHOICES,
        blank=True
    )

    # =====================================================
    # PRICING
    # =====================================================

    price_type = models.CharField(
        max_length=20,
        choices=PRICE_TYPE_CHOICES,
        default='fixed'
    )

    negotiable = models.BooleanField(
        default=False
    )

    # =====================================================
    # LOCATION
    # =====================================================

    state = models.CharField(
        max_length=100,
        blank=True
    )

    city = models.CharField(
        max_length=100,
        blank=True
    )

    specific_location = models.CharField(
        max_length=200,
        blank=True
    )

    # =====================================================
    # PRODUCT INFORMATION
    # =====================================================

    brand = models.CharField(
        max_length=100,
        blank=True
    )

    model = models.CharField(
        max_length=100,
        blank=True
    )

    year = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    color = models.CharField(
        max_length=50,
        blank=True
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    # =====================================================
    # SELLER PREFERENCES
    # =====================================================

    contact_phone = models.CharField(
        max_length=30,
        blank=True
    )

    whatsapp_available = models.BooleanField(
        default=False
    )

    delivery_available = models.BooleanField(
        default=False
    )
    

    # =====================================================
    # SALES STATUS
    # =====================================================

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available'
    )

    # =====================================================
    # ADMIN APPROVAL STATUS
    # =====================================================

    approval_status = models.CharField(
        max_length=20,
        choices=APPROVAL_STATUS_CHOICES,
        default='under_review'
    )

    # =====================================================
    # LISTING VIEWS
    # =====================================================
    #
    # Number of times people have viewed this listing.
    #
    # A newly submitted listing starts at 0.
    #
    # =====================================================

    views = models.PositiveIntegerField(
        default=0
    )

    # =====================================================
    # CHAT STATISTICS
    # =====================================================
    #
    # Number of people who have started a conversation
    # about this listing.
    #
    # A newly submitted listing starts at 0.
    #
    # =====================================================

    chats_count = models.PositiveIntegerField(
        default=0
    )

    # =====================================================
    # SYSTEM INFORMATION
    # =====================================================

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    # =====================================================
    # STRING REPRESENTATION
    # =====================================================

    def __str__(self):
        return self.title

# =========================================================
# MARKETPLACE GALLERY
# =========================================================
class MarketplaceListingImage(models.Model):

    listing = models.ForeignKey(
        MarketplaceListing,
        on_delete=models.CASCADE,
        related_name='gallery_images'
    )

    image = models.ImageField(
        upload_to='marketplace/gallery/'
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.listing.title} - Image"
        
# =========================================================
# MARKETPLACE FAVOURITE
# =========================================================

class MarketplaceFavourite(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='marketplace_favourites'
    )

    listing = models.ForeignKey(
        MarketplaceListing,
        on_delete=models.CASCADE,
        related_name='favourites'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'user',
                    'listing'
                ],
                name='unique_marketplace_favourite'
            )
        ]

    def __str__(self):
        return (
            f"{self.user.username} - "
            f"{self.listing.title}"
        )


# =========================================================
# MARKETPLACE MESSAGE
# =========================================================

class MarketplaceMessage(models.Model):

    listing = models.ForeignKey(
        MarketplaceListing,
        on_delete=models.CASCADE,
        related_name='messages'
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='marketplace_sent_messages'
    )

    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='marketplace_received_messages'
    )

    message = models.TextField()

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.sender.username} → "
            f"{self.receiver.username}"
        )


# =========================================================
# MARKETPLACE REPORT
# =========================================================

class MarketplaceReport(models.Model):

    REASON_CHOICES = [
        ('fraud', 'Fraud / Scam'),
        ('wrong_category', 'Wrong Category'),
        ('duplicate', 'Duplicate Listing'),
        ('prohibited', 'Prohibited Item'),
        ('wrong_information', 'Wrong Information'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('resolved', 'Resolved'),
    ]

    listing = models.ForeignKey(
        MarketplaceListing,
        on_delete=models.CASCADE,
        related_name='reports'
    )

    reporter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='marketplace_reports'
    )

    reason = models.CharField(
        max_length=50,
        choices=REASON_CHOICES
    )

    description = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.listing.title} - "
            f"{self.reason}"
        )

# =========================================================
# MARKETPLACE SELLER REVIEW
# =========================================================

class MarketplaceReview(models.Model):
    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='marketplace_seller_reviews',
        null=True,
        blank=True
    )

    listing = models.ForeignKey(
        MarketplaceListing,
        on_delete=models.CASCADE,
        related_name='seller_reviews',
        null=True,
        blank=True
    )

    reviewer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='marketplace_reviews_given'
    )

    rating = models.PositiveIntegerField(
        choices=[
            (1, '1 Star'),
            (2, '2 Stars'),
            (3, '3 Stars'),
            (4, '4 Stars'),
            (5, '5 Stars'),
        ]
    )

    comment = models.TextField()

    is_approved = models.BooleanField(
        default=True
)
    created_at = models.DateTimeField(
        auto_now_add=True
    )
def __str__(self):
    seller_name = (
        self.seller.username
        if self.seller
        else 'Unknown Seller'
    )

    reviewer_name = (
        self.reviewer.username
        if self.reviewer
        else 'Unknown Reviewer'
    )

    return (
        f"{reviewer_name} → "
        f"{seller_name} "
        f"({self.rating} Stars)"
    )
# =========================================================
# MARKETPLACE LISTING VIEW
# =========================================================

class MarketplaceListingView(models.Model):

    listing = models.ForeignKey(
        MarketplaceListing,
        on_delete=models.CASCADE,
        related_name='view_records'
    )

    viewer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='marketplace_listing_views'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'listing',
                    'viewer'
                ],
                name='unique_listing_view_per_user'
            )
        ]

    def __str__(self):
        return (
            f"{self.viewer.username} viewed "
            f"{self.listing.title}"
        )


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ("hire_request", "Hire Request"),
        ("hire_accepted", "Hire Accepted"),
        ("hire_declined", "Hire Declined"),
        ("hire_cancelled", "Hire Cancelled"),

        ("worker_message", "Worker Message"),
        ("customer_message", "Customer Message"),

        ("review", "Review"),

        ("listing_approved", "Listing Approved"),
        ("listing_rejected", "Listing Rejected"),

        ("marketplace_message", "Marketplace Message"),

        ("account_approved", "Account Approved"),
        ("account_rejected", "Account Rejected"),

        ("job_completed", "Job Completed"),
    ]

    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    notification_type = models.CharField(
        max_length=50,
        choices=NOTIFICATION_TYPES
    )

    title = models.CharField(max_length=200)

    message = models.TextField()

    link = models.CharField(
        max_length=500,
        blank=True,
        null=True
    )

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.recipient.email} - {self.title}"