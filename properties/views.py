from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from .models import Notification
from django.db import transaction
from django.db.models import Avg
from django.utils import timezone
import secrets
from datetime import timedelta
from django.contrib.auth.tokens import default_token_generator
from .notification_utils import create_notification
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.urls import reverse, reverse_lazy
from django.contrib.auth.hashers import (
    make_password,
    check_password,
)
from django.utils.http import (
    urlsafe_base64_encode,
    urlsafe_base64_decode,
)
from django.db.models import Q, F,Count
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    PasswordChangeView,
)

from .forms import (
    AccountRegistrationForm,
    JobApplicationForm,
    ContactMessageForm,
    SkilledWorkerRegistrationForm,
    CustomerForm,
    SkilledWorkerPasswordResetForm,
    AccountSettingsForm,
    MarketplaceListingForm,
    MarketplaceSellerReviewForm,
)

from .models import (
    Estate,
    EstateType,
    Property,
    Job,
    SkilledWorker,
    Customer,
    WorkerHire,
    WorkerReview,
    CustomerReview,
    AccountSettings,
    MarketplaceListing,
    MarketplaceListingView,
    MarketplaceMessage,
    MarketplaceReview,
    MarketplaceListingImage,
    WorkerMessage,
    Notification,
    
)

# =========================================================
# HOME
# =========================================================

def home(request):

    properties = (
        Property.objects
        .filter(
            status='available'
        )
        .select_related(
            'estate',
            'estate_type'
        )
        .order_by(
            '-created_at'
        )[:3]
    )

    return render(
        request,
        'properties/home.html',
        {
            'properties': properties,
        }
    )


# =========================================================
# ESTATES
# =========================================================

def estate_list(request):

    estates = (
        Estate.objects
        .prefetch_related(
            'estate_types',
            'properties'
        )
        .order_by(
            'name'
        )
    )

    for estate in estates:

        estate.total_plots = (
            estate.properties.count()
        )

        estate.available_plots = (
            estate.properties
            .filter(
                status='available'
            )
            .count()
        )

        estate.reserved_plots = (
            estate.properties
            .filter(
                status='reserved'
            )
            .count()
        )

        estate.sold_plots = (
            estate.properties
            .filter(
                status='sold'
            )
            .count()
        )

    return render(
        request,
        'properties/estates.html',
        {
            'estates': estates,
        }
    )


# =========================================================
# ESTATE DETAIL
# =========================================================
def estate_detail(
    request,
    estate_id
):

    estate = get_object_or_404(
        Estate.objects.prefetch_related(
            'estate_types__properties',
            'properties',
        ),
        id=estate_id,
    )

    # =====================================================
    # ESTATE TYPES
    # =====================================================

    estate_types = (
        estate.estate_types
        .all()
        .order_by('name')
    )

    # =====================================================
    # DIRECT PROPERTIES
    #
    # These are properties that belong to the estate
    # but do NOT belong to an Estate Type.
    # =====================================================

    direct_properties = (
        estate.properties
        .filter(
            estate_type__isnull=True
        )
        .order_by(
            'title'
        )
    )

    # =====================================================
    # TOTAL ESTATE PROPERTY COUNTS
    # =====================================================

    total_plots = (
        estate.properties.count()
    )

    available_plots = (
        estate.properties
        .filter(
            status='available'
        )
        .count()
    )

    reserved_plots = (
        estate.properties
        .filter(
            status='reserved'
        )
        .count()
    )

    sold_plots = (
        estate.properties
        .filter(
            status='sold'
        )
        .count()
    )

    # =====================================================
    # ESTATE TYPE COUNTS
    # =====================================================

    for estate_type in estate_types:

        estate_type.available_plot_count = (
            estate_type.properties
            .filter(
                status='available'
            )
            .count()
        )

        estate_type.reserved_plot_count = (
            estate_type.properties
            .filter(
                status='reserved'
            )
            .count()
        )

        estate_type.sold_plot_count = (
            estate_type.properties
            .filter(
                status='sold'
            )
            .count()
        )

        estate_type.total_plot_count = (
            estate_type.properties.count()
        )

    # =====================================================
    # DEVELOPMENT FEATURES
    # =====================================================

    development_features = [
        feature.strip()
        for feature in (
            estate.development_features or ''
        ).splitlines()
        if feature.strip()
    ]

    # =====================================================
    # CONTEXT
    # =====================================================

    context = {

        'estate': estate,

        # Estate types
        'estate_types': estate_types,

        # Direct estate properties
        'direct_properties': direct_properties,

        # Estate totals
        'total_plots': total_plots,
        'available_plots': available_plots,
        'reserved_plots': reserved_plots,
        'sold_plots': sold_plots,

        # Development
        'development_features': development_features,
    }

    return render(
        request,
        'properties/estate_detail.html',
        context
    )

# =========================================================
# ESTATE TYPE DETAIL
# =========================================================

def estate_type_detail(
    request,
    estate_id,
    estate_type_id
):

    estate = get_object_or_404(
        Estate,
        id=estate_id
    )

    estate_type = get_object_or_404(
        EstateType.objects.select_related(
            'estate'
        ),
        id=estate_type_id,
        estate=estate
    )

    properties = (
        Property.objects
        .filter(
            estate=estate,
            estate_type=estate_type,
        )
        .select_related(
            'estate',
            'estate_type',
            'agent',
        )
        .prefetch_related(
            'gallery_images'
        )
        .order_by(
            'plot_number',
            '-created_at'
        )
    )

    available_properties = properties.filter(
        status='available'
    )

    reserved_properties = properties.filter(
        status='reserved'
    )

    sold_properties = properties.filter(
        status='sold'
    )

    type_features = [
        feature.strip()
        for feature in (
            estate_type.what_comes_with_it or ''
        ).splitlines()
        if feature.strip()
    ]

    context = {
        'estate': estate,
        'estate_type': estate_type,

        'properties': properties,

        'available_properties': available_properties,
        'reserved_properties': reserved_properties,
        'sold_properties': sold_properties,

        'total_properties': properties.count(),
        'available_count': available_properties.count(),
        'reserved_count': reserved_properties.count(),
        'sold_count': sold_properties.count(),

        'type_features': type_features,
    }

    return render(
        request,
        'properties/estate_type_detail.html',
        context
    )


# =========================================================
# PROPERTY LIST
# =========================================================

def property_list(request):

    properties = (
        Property.objects
        .all()
        .select_related(
            'estate',
            'estate_type'
        )
        .order_by(
            '-created_at'
        )
    )

    search = request.GET.get(
        'search',
        ''
    ).strip()

    property_type = request.GET.get(
        'property_type',
        ''
    ).strip()

    status = request.GET.get(
        'status',
        ''
    ).strip()

    if search:

        properties = properties.filter(
            Q(title__icontains=search)
            |
            Q(location__icontains=search)
            |
            Q(plot_number__icontains=search)
            |
            Q(estate__name__icontains=search)
            |
            Q(estate_type__name__icontains=search)
        )

    if property_type:

        properties = properties.filter(
            property_type=property_type
        )

    if status:

        properties = properties.filter(
            status=status
        )

    return render(
        request,
        'properties/properties.html',
        {
            'properties': properties,
            'search': search,
            'property_type': property_type,
            'status': status,
        }
    )


# =========================================================
# PROPERTY DETAIL
# =========================================================

def property_detail(
    request,
    property_id
):

    property_obj = get_object_or_404(
        Property.objects
        .select_related(
            'estate',
            'estate_type',
            'agent'
        )
        .prefetch_related(
            'gallery_images'
        ),
        id=property_id,
    )

    return render(
        request,
        'properties/property_detail.html',
        {
            'property': property_obj,
        }
    )


# =========================================================
# ABOUT
# =========================================================

def about(request):

    return render(
        request,
        'properties/about.html'
    )

# =========================================================
# OUR SERVICES
# =========================================================

def our_services(request):

    return render(
        request,
        'properties/our_services.html'
    )

# =========================================================
# JOBS
# =========================================================

def jobs(request):

    jobs_list = (
        Job.objects
        .filter(
            status='open'
        )
        .order_by(
            '-created_at'
        )
    )

    return render(
        request,
        'properties/jobs.html',
        {
            'jobs': jobs_list,
        }
    )


# =========================================================
# JOB DETAIL
# =========================================================

def job_detail(
    request,
    job_id
):

    job = get_object_or_404(
        Job,
        id=job_id
    )

    return render(
        request,
        'properties/job_detail.html',
        {
            'job': job,
        }
    )


# =========================================================
# JOB APPLY
# =========================================================

def job_apply(
    request,
    job_id
):

    job = get_object_or_404(
        Job,
        id=job_id
    )

    if request.method == 'POST':

        form = JobApplicationForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            application = form.save(
                commit=False
            )

            application.job = job
            application.save()

            return render(
                request,
                'properties/application_success.html',
                {
                    'job': job,
                }
            )

    else:

        form = JobApplicationForm()

    return render(
        request,
        'properties/job_apply.html',
        {
            'job': job,
            'form': form,
        }
    )


# =========================================================
# CONTACT
# =========================================================

def contact(request):

    if request.method == 'POST':

        form = ContactMessageForm(
            request.POST
        )

        if form.is_valid():

            # =================================================
            # SAVE CONTACT MESSAGE TO DATABASE
            # =================================================

            contact_message = form.save()


            # =================================================
            # KING B WHATSAPP NUMBER
            #
            # IMPORTANT:
            # Replace this with your actual WhatsApp number.
            #
            # Nigerian format:
            # 2348012345678
            #
            # Do NOT use:
            # +234...
            # 080...
            # spaces
            # =================================================

            whatsapp_number = '2348035780632'


            # =================================================
            # BUILD WHATSAPP MESSAGE
            # =================================================

            whatsapp_message = (
                "Hello King B Real Estate,\n\n"
                "I recently submitted an enquiry "
                "through your website.\n\n"
                f"Name: {contact_message.name}\n"
                f"Phone: {contact_message.phone}\n"
                f"Email: {contact_message.email}\n"
                f"Subject: {contact_message.subject}\n\n"
                f"Message:\n{contact_message.message}\n\n"
                "Thank you."
            )


            # =================================================
            # URL ENCODE WHATSAPP MESSAGE
            # =================================================

            from urllib.parse import quote

            whatsapp_url = (
                f"https://wa.me/"
                f"{whatsapp_number}"
                f"?text={quote(whatsapp_message)}"
            )


            # =================================================
            # SUCCESS PAGE
            # =================================================

            return render(
                request,
                'properties/contact_success.html',
                {
                    'contact_message': contact_message,
                    'whatsapp_url': whatsapp_url,
                }
            )


    else:

        form = ContactMessageForm()


    return render(
        request,
        'properties/contact.html',
        {
            'form': form,
        }
    )
# =========================================================
# PUBLIC SKILLED WORKERS
# =========================================================

def skilled_workers(request):

    workers = (
        SkilledWorker.objects
        .filter(
            is_approved=True
        )
        .order_by(
            '-created_at'
        )
    )

    search = request.GET.get(
        'search',
        ''
    ).strip()

    skill = request.GET.get(
        'skill',
        ''
    ).strip()

    location = request.GET.get(
        'location',
        ''
    ).strip()

    if search:

        workers = workers.filter(
            Q(full_name__icontains=search)
            |
            Q(skill__icontains=search)
        )

    if skill:

        workers = workers.filter(
            skill__icontains=skill
        )

    if location:

        workers = workers.filter(
            location__icontains=location
        )

    return render(
        request,
        'properties/skilled_workers.html',
        {
            'workers': workers,
            'search': search,
            'skill': skill,
            'location': location,
        }
    )


# =========================================================
# SKILLED WORKER PROFILE
# =========================================================

def skilled_worker_profile(request, worker_id):

    worker = get_object_or_404(
        SkilledWorker,
        id=worker_id,
        is_approved=True
    )

    reviews = (
        WorkerReview.objects
        .filter(
            hire__worker=worker,
            is_approved=True
        )
        .select_related(
            'hire',
            'hire__customer',
            'hire__worker'
        )
        .order_by('-created_at')
    )

    reviews_count = reviews.count()

    if reviews_count:
        total_rating = sum(
            review.rating
            for review in reviews
        )

        average_rating = round(
            total_rating / reviews_count,
            1
        )
    else:
        average_rating = 0

    # =====================================================
    # CUSTOMER HIRING / REVIEW STATUS
    # =====================================================

    can_hire = False
    can_review = False
    review_hire = None

    if request.user.is_authenticated:

        # -------------------------------------------------
        # Check whether logged-in user has a customer
        # profile
        # -------------------------------------------------

        customer = getattr(
            request.user,
            'customer_profile',
            None
        )

        if customer:

            # -------------------------------------------------
            # CUSTOMER MUST BE VERIFIED AND APPROVED TO HIRE
            # -------------------------------------------------

            if (
                customer.email_verified
                and customer.is_approved
            ):

                # -------------------------------------------------
                # Prevent customer from hiring their own worker
                # profile
                # -------------------------------------------------

                if request.user != worker.user:

                    can_hire = True

            # -------------------------------------------------
            # FIND COMPLETED HIRE THAT CAN BE REVIEWED
            # -------------------------------------------------

            review_hire = (
                WorkerHire.objects
                .filter(
                    customer=customer,
                    worker=worker,
                    status='completed'
                )
                .exclude(
                    worker_review__isnull=False
                )
                .first()
            )

            if review_hire:
                can_review = True


            print("====================================")
            print("LOGGED USER:", request.user)
            print("AUTHENTICATED:", request.user.is_authenticated)

            customer = getattr(
                request.user,
                'customer_profile',
                None
            )

            print("CUSTOMER:", customer)

            if customer:
                print("EMAIL VERIFIED:", customer.email_verified)
                print("APPROVED:", customer.is_approved)

            print("CAN HIRE:", can_hire)
            print("====================================")

    return render(
        request,
        'properties/skilled_worker_profile.html',
        {
            'worker': worker,
            'reviews': reviews,
            'reviews_count': reviews_count,
            'average_rating': average_rating,

            # Hiring
            'can_hire': can_hire,

            # Reviews
            'can_review': can_review,
            'review_hire': review_hire,
        }
    )



# =========================================================
# MARKETPLACE
# =========================================================

def marketplace(request):

    listings = (
        MarketplaceListing.objects
        .filter(
            status='available',
            approval_status='approved'
        )
        .select_related(
            'seller'
        )
        .prefetch_related(
            'gallery_images'
        )
        .order_by(
            '-created_at'
        )
    )

    search = request.GET.get(
        'search',
        ''
    ).strip()

    category = request.GET.get(
        'category',
        ''
    ).strip()

    location = request.GET.get(
        'location',
        ''
    ).strip()

    if search:

        listings = listings.filter(
            Q(title__icontains=search)
            |
            Q(description__icontains=search)
            |
            Q(location__icontains=search)
        )

    if category:

        listings = listings.filter(
            category=category
        )

    if location:

        listings = listings.filter(
            location__icontains=location
        )

    return render(
        request,
        'properties/marketplace.html',
        {
            'listings': listings,
            'search': search,
            'category': category,
            'location': location,
        }
    )


# =========================================================
# CREATE MARKETPLACE LISTING
# =========================================================
@login_required(login_url='site_login')
def marketplace_create(request):

    if request.method == 'POST':

        form = MarketplaceListingForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            listing = form.save(
                commit=False
            )

            listing.seller = request.user

            listing.approval_status = 'under_review'

            listing.status = 'available'

            images = form.cleaned_data.get(
                'images'
            )

            if images:

                listing.image = images[0]

            listing.save()

            # =========================================
            # SAVE ADDITIONAL GALLERY IMAGES
            # =========================================

            if images:

                for image in images[1:]:

                    MarketplaceListingImage.objects.create(
                        listing=listing,
                        image=image,
                    )

            messages.success(
                request,
                'Your listing has been submitted successfully. '
                'It is currently under review.'
            )

            return redirect(
                'my_listing_detail',
                listing_id=listing.id
            )

    else:

        form = MarketplaceListingForm()

    return render(
        request,
        'properties/marketplace_create.html',
        {
            'form': form,
        }
    )
    
# =========================================================
# EDIT MARKETPLACE ADVERTISEMENT
# =========================================================
@login_required
def marketplace_edit(request, listing_id):

    # =========================================================
    # GET THE SELLER'S LISTING
    # =========================================================

    listing = get_object_or_404(
        MarketplaceListing,
        id=listing_id,
        seller=request.user,
    )


    # =========================================================
    # GET ALL GALLERY PHOTOS
    # =========================================================

    gallery_images = MarketplaceListingImage.objects.filter(
        listing=listing
    ).order_by('id')


    # =========================================================
    # EDIT LISTING
    # =========================================================

    if request.method == 'POST':

        form = MarketplaceListingForm(
            request.POST,
            request.FILES,
            instance=listing,
        )

        if form.is_valid():

            listing = form.save(commit=False)

            # -------------------------------------------------
            # IMPORTANT
            # -------------------------------------------------
            # Editing an advertisement sends it back for review.
            # Remove this block if you do NOT want that behavior.
            # -------------------------------------------------

            if listing.approval_status == 'approved':
                listing.approval_status = 'under_review'

            listing.save()


            # =================================================
            # ADD NEW GALLERY PHOTOS
            # =================================================

            uploaded_images = request.FILES.getlist('images')

            for image in uploaded_images:

                MarketplaceListingImage.objects.create(
                    listing=listing,
                    image=image,
                )


            messages.success(
                request,
                'Your advertisement has been updated successfully.'
            )

            return redirect(
                'my_listing_detail',
                listing_id=listing.id
            )

    else:

        form = MarketplaceListingForm(
            instance=listing
        )


    # =========================================================
    # REFRESH GALLERY AFTER SAVE
    # =========================================================

    gallery_images = MarketplaceListingImage.objects.filter(
        listing=listing
    ).order_by('id')


    # =========================================================
    # PAGE
    # =========================================================

    return render(
        request,
        'properties/marketplace_edit.html',
        {
            'form': form,
            'listing': listing,
            'gallery_images': gallery_images,
        }
    )

# =========================================================
# DELETE PRIMARY MARKETPLACE IMAGE
# =========================================================

@login_required
def marketplace_delete_primary_image(request, listing_id):

    listing = get_object_or_404(
        MarketplaceListing,
        id=listing_id,
        seller=request.user,
    )

    if request.method != 'POST':
        return redirect(
            'marketplace_edit',
            listing_id=listing.id
        )

    # -----------------------------------------------------
    # DELETE PRIMARY IMAGE
    # -----------------------------------------------------

    if listing.image:

        listing.image.delete(save=False)

        listing.image = None

        listing.save(
            update_fields=['image']
        )

        messages.success(
            request,
            'Primary photo deleted successfully.'
        )

    else:

        messages.info(
            request,
            'There is no primary photo to delete.'
        )

    return redirect(
        'marketplace_edit',
        listing_id=listing.id
    )
    
# =========================================================
# PUBLIC MARKETPLACE LISTING DETAIL
# =========================================================

def marketplace_detail(
    request,
    listing_id
):

    listing = get_object_or_404(
        MarketplaceListing.objects
        .select_related(
            'seller'
        )
        .prefetch_related(
            'gallery_images'
        ),
        id=listing_id,
        status='available',
        approval_status='approved',
    )

   # =========================================================
# PUBLIC MARKETPLACE LISTING DETAIL
# =========================================================

def marketplace_detail(
    request,
    listing_id
):

    listing = get_object_or_404(
        MarketplaceListing.objects
        .select_related(
            'seller'
        )
        .prefetch_related(
            'gallery_images'
        ),
        id=listing_id,
        status='available',
        approval_status='approved',
    )

    # =====================================================
    # UNIQUE VIEW COUNT
    # =====================================================

    if (
        request.user.is_authenticated
        and request.user != listing.seller
    ):

        view_record, created = (
            MarketplaceListingView.objects.get_or_create(
                listing=listing,
                viewer=request.user
            )
        )

        if created:

            MarketplaceListing.objects.filter(
                id=listing.id
            ).update(
                views=F('views') + 1
            )

            listing.refresh_from_db(
                fields=['views']
            )

    # =====================================================
    # SELLER PHONE NUMBER
    # =====================================================
    #
    # AccountSettings is connected to User through:
    #
    #     related_name='account_settings'
    #
    # The actual phone field is:
    #
    #     phone
    #
    # NOT phone_number.
    #
    # If the seller does not have AccountSettings,
    # seller_phone becomes None.
    #
    # =====================================================

    seller_phone = None

    try:

        seller_phone = (
            listing.seller
            .account_settings
            .phone
        )

        # Treat an empty phone field as no phone number.

        if not seller_phone:
            seller_phone = None

    except AccountSettings.DoesNotExist:

        seller_phone = None

    # =====================================================
    # RENDER PAGE
    # =====================================================

    return render(
        request,
        'properties/marketplace_detail.html',
        {
            'listing': listing,

            'seller_phone': seller_phone,
        }
    )

# =========================================================
# MY MARKETPLACE LISTING DETAIL
# =========================================================

@login_required(login_url='site_login')
def my_listing_detail(
    request,
    listing_id
):

    listing = get_object_or_404(
        MarketplaceListing.objects
        .select_related(
            'seller'
        )
        .prefetch_related(
            'gallery_images'
        ),
        id=listing_id,
        seller=request.user,
    )

    # =====================================================
    # UNIQUE PEOPLE WHO CHATTED
    # =====================================================

    chatters_count = (
        MarketplaceMessage.objects
        .filter(
            listing=listing
        )
        .exclude(
            sender=listing.seller
        )
        .values(
            'sender'
        )
        .distinct()
        .count()
    )

    # =====================================================
    # SYNCHRONIZE STORED CHAT COUNT
    # =====================================================

    if listing.chats_count != chatters_count:

        listing.chats_count = chatters_count

        listing.save(
            update_fields=[
                'chats_count'
            ]
        )

    # =====================================================
    # TOTAL MESSAGES
    # =====================================================

    messages_count = (
        MarketplaceMessage.objects
        .filter(
            listing=listing
        )
        .count()
    )

    return render(
        request,
        'properties/my_listing_detail.html',
        {
            'listing': listing,
            'chatters_count': chatters_count,
            'messages_count': messages_count,
        }
    )

# =========================================================
# UNIFIED SITE REGISTRATION
# =========================================================


# =========================================================
# UNIFIED SITE REGISTRATION
# =========================================================

def site_register(request):

    if request.user.is_authenticated:
        return redirect('marketplace_dashboard')

    if request.method == 'POST':

        form = AccountRegistrationForm(request.POST)

        if form.is_valid():

            full_name = (
                form.cleaned_data['full_name']
                .strip()
            )

            email = (
                form.cleaned_data['email']
                .strip()
                .lower()
            )

            phone = (
                form.cleaned_data['phone']
                .strip()
            )

            password = form.cleaned_data['password']

            # =================================================
            # CHECK EMAIL BEFORE DOING ANYTHING
            # =================================================

            if User.objects.filter(
                email__iexact=email
            ).exists():

                messages.error(
                    request,
                    'An account with this email already exists.'
                )

                return render(
                    request,
                    'properties/site_register.html',
                    {'form': form}
                )

            # =================================================
            # CREATE ACCOUNT + SEND VERIFICATION
            # =================================================

            try:

                with transaction.atomic():

                    # -----------------------------------------
                    # CREATE USER
                    # -----------------------------------------

                    user = User.objects.create_user(
                        username=email,
                        email=email,
                        password=password,
                        first_name=full_name,
                        is_active=True,
                    )

                    # -----------------------------------------
                    # CREATE CUSTOMER PROFILE
                    # -----------------------------------------

                    Customer.objects.create(
                        user=user,
                        full_name=full_name,
                        phone=phone,
                        email=email,
                        address='',
                        id_type='',
                        id_number='',
                        email_verified=False,
                        is_approved=False,
                    )

                    # -----------------------------------------
                    # CREATE VERIFICATION TOKEN
                    # -----------------------------------------

                    uid = urlsafe_base64_encode(
                        force_bytes(user.pk)
                    )

                    token = default_token_generator.make_token(
                        user
                    )

                    verification_url = request.build_absolute_uri(
                        reverse(
                            'verify_email',
                            kwargs={
                                'uidb64': uid,
                                'token': token,
                            }
                        )
                    )

                    # -----------------------------------------
                    # SEND VERIFICATION EMAIL
                    # -----------------------------------------

                    send_mail(
                        subject='Verify Your King B Account',

                        message=(
                            f'Hello {full_name},\n\n'

                            f'Thank you for creating your '
                            f'King B Real Estate account.\n\n'

                            f'Please verify your email address '
                            f'by clicking the link below:\n\n'

                            f'{verification_url}\n\n'

                            f'After verifying your email, you '
                            f'will be able to log in to your '
                            f'King B account.\n\n'

                            f'If you did not create this account, '
                            f'you can ignore this email.\n\n'

                            f'King B Real Estate & Construction Ltd'
                        ),

                        from_email=None,

                        recipient_list=[email],

                        fail_silently=False,
                    )

                # =================================================
                # ONLY REACHES HERE IF EVERYTHING SUCCEEDED
                # =================================================

                messages.success(
                    request,
                    (
                        'Your account has been created successfully. '
                        'Please check your email and click the '
                        'verification link before logging in.'
                    )
                )

                return redirect('site_login')

            except Exception as e:

                # =================================================
                # EMAIL FAILED / ACCOUNT CREATION FAILED
                # =================================================

                messages.error(
                    request,
                    (
                        'We could not complete your registration '
                        'because the verification email could not '
                        'be sent. Please check your email address '
                        'or try again later.'
                    )
                )

                print(
                    'REGISTRATION ERROR:',
                    repr(e)
                )

                return render(
                    request,
                    'properties/site_register.html',
                    {'form': form}
                )

    else:

        form = AccountRegistrationForm()

    return render(
        request,
        'properties/site_register.html',
        {
            'form': form,
        }
    )

# =========================================================
# VERIFY EMAIL
# =========================================================

def verify_email(request, uidb64, token):

    try:

        uid = urlsafe_base64_decode(
            uidb64
        ).decode()

        user = User.objects.get(
            pk=uid
        )

    except (
        TypeError,
        ValueError,
        OverflowError,
        User.DoesNotExist,
    ):

        user = None

    if user is None:

        return render(
            request,
            'properties/email_verification_failed.html'
        )

    if not default_token_generator.check_token(
        user,
        token
    ):

        return render(
            request,
            'properties/email_verification_failed.html'
        )

    try:

        customer = user.customer_profile

        customer.email_verified = True

        customer.save(
            update_fields=[
                'email_verified'
            ]
        )

    except Customer.DoesNotExist:

        pass

    try:

        worker = user.skilled_worker_profile

        worker.email_verified = True

        worker.save(
            update_fields=[
                'email_verified'
            ]
        )

    except SkilledWorker.DoesNotExist:

        pass

    messages.success(
        request,
        'Your email address has been verified successfully.'
    )

    return render(
        request,
        'properties/email_verified.html'
    )

# =========================================================
# OLD CUSTOMER REGISTRATION
# =========================================================

def customer_register(request):

    return redirect(
        'site_register'
    )


# =========================================================
# OLD SKILLED WORKER REGISTRATION
# =========================================================

def skilled_worker_register(request):

    return redirect(
        'site_register'
    )


# =========================================================
# UNIFIED SITE LOGIN
# =========================================================

@ensure_csrf_cookie
def site_login(request):

    if request.user.is_authenticated:

        return redirect(
            'marketplace_dashboard'
        )

    if request.method == 'POST':

        email = (
            request.POST.get(
                'username',
                ''
            )
            .strip()
            .lower()
        )

        password = request.POST.get(
            'password',
            ''
        )

        if not email or not password:

            return render(
                request,
                'properties/site_login.html',
                {
                    'error': (
                        'Please enter your email and password.'
                    ),
                }
            )

        user = authenticate(
            request,
            username=email,
            password=password,
        )

        if user is None:

            return render(
                request,
                'properties/site_login.html',
                {
                    'error': (
                        'Invalid email or password.'
                    ),
                }
            )

        has_customer = False
        has_worker = False

        try:

            user.customer_profile
            has_customer = True

        except Customer.DoesNotExist:

            pass

        try:

            user.skilled_worker_profile
            has_worker = True

        except SkilledWorker.DoesNotExist:

            pass

        if not has_customer and not has_worker:

            return render(
                request,
                'properties/site_login.html',
                {
                    'error': (
                        'This account is not registered '
                        'with King B.'
                    ),
                }
            )

                # =================================================
        # EMAIL VERIFICATION CHECK
        # =================================================

        email_verified = False

        try:

            customer = user.customer_profile

            email_verified = customer.email_verified

        except Customer.DoesNotExist:

            pass

        if not email_verified:

            return render(
                request,
                'properties/site_login.html',
                {
                    'error': (
                        'Please verify your email address '
                        'before logging in. Check your inbox '
                        'for the verification email.'
                    ),
                }
            )

        login(
            request,
            user
        )

        messages.success(
            request,
            f'Welcome back, '
            f'{user.first_name or user.username}.'
        )

        return redirect(
            'marketplace_dashboard'
        )

    return render(
        request,
        'properties/site_login.html'
    )


# =========================================================
# LOGOUT
# =========================================================

@login_required(login_url='site_login')
def site_logout(request):

    logout(request)

    messages.success(
        request,
        'You have been logged out successfully.'
    )

    return redirect(
        'site_login'
    )


# =========================================================
# OLD CUSTOMER LOGIN
# =========================================================

@ensure_csrf_cookie
def customer_login(request):

    return site_login(request)


# =========================================================
# OLD CUSTOMER LOGOUT
# =========================================================

@login_required(login_url='site_login')
def customer_logout(request):

    return site_logout(request)


# =========================================================
# OLD SKILLED WORKER LOGIN
# =========================================================

@ensure_csrf_cookie
def skilled_worker_login(request):

    return site_login(request)


# =========================================================
# OLD SKILLED WORKER LOGOUT
# =========================================================

@login_required(login_url='site_login')
def skilled_worker_logout(request):

    return site_logout(request)


# =========================================================
# GENERAL ACCOUNT DASHBOARD
# =========================================================
@login_required(login_url='site_login')
def marketplace_dashboard(request):

    user = request.user

    customer = None

    try:
        customer = user.customer_profile

    except Customer.DoesNotExist:
        pass

    worker = None

    try:
        worker = user.skilled_worker_profile

    except SkilledWorker.DoesNotExist:
        pass

    customer_exists = customer is not None

    customer_verified = (
        customer_exists
        and customer.email_verified
    )

    worker_exists = worker is not None

    worker_approved = (
        worker_exists
        and worker.is_approved
    )

    worker_pending = (
        worker_exists
        and not worker.is_approved
    )

    # =====================================================
    # CUSTOMER HIRES
    # =====================================================

    customer_hires = WorkerHire.objects.none()

    total_hires = 0
    customer_active_hires = 0
    customer_pending_hires = 0
    customer_completed_hires = 0

    if customer_exists:

        customer_hires = (
            WorkerHire.objects
            .filter(
                customer=customer
            )
            .select_related(
                'worker'
            )
            .order_by(
                '-hired_at'
            )
        )

        total_hires = customer_hires.count()

        customer_active_hires = (
            customer_hires
            .filter(
                status='active'
            )
            .count()
        )

        customer_pending_hires = (
            customer_hires
            .filter(
                status='requested'
            )
            .count()
        )

        customer_completed_hires = (
            customer_hires
            .filter(
                status='completed'
            )
            .count()
        )

    # =====================================================
    # WORKER HIRES
    # =====================================================

    worker_hires = WorkerHire.objects.none()

    worker_pending_requests = 0
    worker_active_jobs = 0
    worker_completed_jobs = 0

    if worker_exists:

        worker_hires = (
            WorkerHire.objects
            .filter(
                worker=worker
            )
            .select_related(
                'customer'
            )
            .order_by(
                '-hired_at'
            )
        )

        worker_pending_requests = (
            worker_hires
            .filter(
                status='requested'
            )
            .count()
        )

        worker_active_jobs = (
            worker_hires
            .filter(
                status='active'
            )
            .count()
        )

        worker_completed_jobs = (
            worker_hires
            .filter(
                status='completed'
            )
            .count()
        )

    # =====================================================
    # CUSTOMER'S MARKETPLACE LISTINGS
    # =====================================================

    marketplace_listings = (
        MarketplaceListing.objects
        .filter(
            seller=user
        )
        .prefetch_related(
            'gallery_images'
        )
        .order_by(
            '-created_at'
        )
    )

    # =====================================================
    # LISTING STATISTICS
    # =====================================================

    listing_count = marketplace_listings.count()

    approved_listings_count = (
        marketplace_listings
        .filter(
            approval_status='approved'
        )
        .count()
    )

    under_review_listings_count = (
        marketplace_listings
        .filter(
            approval_status='under_review'
        )
        .count()
    )

    rejected_listings_count = (
        marketplace_listings
        .filter(
            approval_status='rejected'
        )
        .count()
    )

    total_listing_views = 0

    for listing in marketplace_listings:

        total_listing_views += (
            listing.views or 0
        )

    # =====================================================
    # UNREAD MARKETPLACE MESSAGES
    # =====================================================

    unread_marketplace_messages = (
        MarketplaceMessage.objects
        .filter(
            receiver=request.user,
            is_read=False
        )
        .values(
            'listing_id'
        )
        .distinct()
        .count()
    )

    # =====================================================
    # WORKER / CUSTOMER MESSAGE CONVERSATIONS
    # =====================================================

    worker_message_hires = WorkerHire.objects.none()

    if customer_exists and worker_exists:

        worker_message_hires = (
            WorkerHire.objects
            .filter(
               Q(customer=customer) |
                    Q(worker=worker)
            )
            .select_related(
                'customer',
                'customer__user',
                'worker',
                'worker__user'
            )
            .order_by(
                '-hired_at'
            )
        )

    elif customer_exists:

        worker_message_hires = (
            WorkerHire.objects
            .filter(
                customer=customer
            )
            .select_related(
                'worker',
                'worker__user'
            )
            .order_by(
                '-hired_at'
            )
        )

    elif worker_exists:

        worker_message_hires = (
            WorkerHire.objects
            .filter(
                worker=worker
            )
            .select_related(
                'customer',
                'customer__user'
            )
            .order_by(
                '-hired_at'
            )
        )

    # =====================================================
    # UNREAD WORKER / CUSTOMER MESSAGES
    # =====================================================

    unread_worker_messages = (
        WorkerMessage.objects
        .filter(
            receiver=request.user,
            is_read=False
        )
        .count()
    )

    # =====================================================
    # CONTEXT
    # =====================================================

    context = {

        'user': user,

        'customer': customer,
        'worker': worker,

        'customer_exists': customer_exists,
        'customer_verified': customer_verified,

        'worker_exists': worker_exists,
        'worker_approved': worker_approved,
        'worker_pending': worker_pending,

        'customer_hires': customer_hires,

        'total_hires': total_hires,
        'customer_active_hires': customer_active_hires,
        'customer_pending_hires': customer_pending_hires,
        'customer_completed_hires': customer_completed_hires,

        'worker_hires': worker_hires,

        'worker_pending_requests': worker_pending_requests,
        'worker_active_jobs': worker_active_jobs,
        'worker_completed_jobs': worker_completed_jobs,

        'marketplace_listings': marketplace_listings,

        'listing_count': listing_count,
        'approved_listings_count': approved_listings_count,
        'under_review_listings_count': under_review_listings_count,
        'rejected_listings_count': rejected_listings_count,
        'total_listing_views': total_listing_views,

        'unread_marketplace_messages': unread_marketplace_messages,

        'unread_worker_messages': unread_worker_messages,

        'worker_message_hires': worker_message_hires,
    }

    return render(
        request,
        'properties/marketplace_dashboard.html',
        context
    )

@login_required(login_url='site_login')
def delete_marketplace_listing(request, listing_id):

    # =====================================================
    # ONLY POST REQUESTS ARE ALLOWED
    # =====================================================

    if request.method != 'POST':

        messages.error(
            request,
            'Invalid request.'
        )

        return redirect(
            'marketplace_dashboard'
        )

    # =====================================================
    # GET LISTING BELONGING TO CURRENT USER
    # =====================================================

    listing = get_object_or_404(
        MarketplaceListing,
        id=listing_id,
        seller=request.user
    )

    # =====================================================
    # SAVE TITLE FOR SUCCESS MESSAGE
    # =====================================================

    listing_title = listing.title

    # =====================================================
    # DELETE MAIN LISTING IMAGE
    # =====================================================

    if listing.image:

        try:
            listing.image.delete(
                save=False
            )
        except Exception:
            pass

    # =====================================================
    # DELETE GALLERY IMAGES
    # =====================================================
    #
    # Your dashboard already uses:
    #
    #     prefetch_related('gallery_images')
    #
    # so we safely remove those uploaded files too.
    #
    # =====================================================

    try:

        gallery_images = listing.gallery_images.all()

        for gallery_image in gallery_images:

            # Try common image field names safely
            image_file = getattr(
                gallery_image,
                'image',
                None
            )

            if image_file:

                try:
                    image_file.delete(
                        save=False
                    )
                except Exception:
                    pass

            gallery_image.delete()

    except Exception:
        pass

    # =====================================================
    # DELETE LISTING
    # =====================================================

    listing.delete()

    # =====================================================
    # SUCCESS MESSAGE
    # =====================================================

    messages.success(
        request,
        f'Your marketplace listing "{listing_title}" '
        f'has been permanently deleted.'
    )

    # =====================================================
    # RETURN TO MARKETPLACE DASHBOARD
    # =====================================================

    return redirect(
        'marketplace_dashboard'
    )

# =========================================================
# BECOME A SKILLED WORKER
# =========================================================

@login_required(login_url='site_login')
def become_skilled_worker(request):

    user = request.user

    try:

        worker = user.skilled_worker_profile

        if worker.is_approved:

            messages.info(
                request,
                'You are already an approved skilled worker.'
            )

            return redirect(
                'my_worker_profile'
            )

        messages.info(
            request,
            'Your skilled worker application is already '
            'waiting for approval.'
        )

        return redirect(
            'marketplace_dashboard'
        )

    except SkilledWorker.DoesNotExist:

        pass

    if request.method == 'POST':

        form = SkilledWorkerRegistrationForm(
            request.POST,
            request.FILES,
            current_user=user,
        )

        if form.is_valid():

            worker = form.save(
                commit=False
            )

            worker.user = user

            if user.email:

                worker.email = (
                    user.email
                    .strip()
                    .lower()
                )

            worker.is_approved = False

            worker.save()

            messages.success(
                request,
                'Your skilled worker application has been '
                'submitted successfully. King B will review '
                'your application before approval.'
            )

            return redirect(
                'marketplace_dashboard'
            )

    else:

        form = SkilledWorkerRegistrationForm(
            initial={
                'full_name': (
                    user.get_full_name()
                    or ''
                ),
                'email': user.email,
            },
            current_user=user,
        )

    return render(
        request,
        'properties/become_skilled_worker.html',
        {
            'form': form,
        }
    )


# =========================================================
# CUSTOMER PROFILE EDIT
# =========================================================

@login_required(login_url='site_login')
def customer_profile_edit(request):

    try:

        customer = request.user.customer_profile

    except Customer.DoesNotExist:

        messages.error(
            request,
            'You do not have a customer profile yet.'
        )

        return redirect(
            'marketplace_dashboard'
        )

    if request.method == 'POST':

        form = CustomerForm(
            request.POST,
            request.FILES,
            instance=customer,
        )

        if form.is_valid():

            customer = form.save(
                commit=False
            )

            customer.user = request.user
            customer.email = request.user.email

            customer.save()

            messages.success(
                request,
                'Your profile has been updated successfully.'
            )

            return redirect(
                'marketplace_dashboard'
            )

    else:

        form = CustomerForm(
            instance=customer
        )

    return render(
        request,
        'properties/customer_profile_edit.html',
        {
            'customer': customer,
            'form': form,
        }
    )


# =========================================================
# CUSTOMER DASHBOARD
# =========================================================
@login_required(login_url='site_login')
def customer_dashboard(request):

    try:

        customer = request.user.customer_profile

    except Customer.DoesNotExist:

        messages.error(
            request,
            'You do not have a customer profile.'
        )

        return redirect(
            'marketplace_dashboard'
        )

    if not customer.email_verified:

        messages.warning(
            request,
            'Your customer profile is still waiting '
            'for verification.'
        )

        return redirect(
            'marketplace_dashboard'
        )

    # =====================================================
    # CUSTOMER HIRES
    # =====================================================

    hires = (
        WorkerHire.objects
        .filter(
            customer=customer
        )
        .exclude(
            status='cancelled'
        )
        .select_related(
            'worker',
            'worker__user'
        )
        .order_by(
            '-hired_at'
        )
    )

    total_hires = hires.count()

    active_hires = hires.filter(
        status='active'
    ).count()

    completed_hires = hires.filter(
        status='completed'
    ).count()

    pending_hires = hires.filter(
        status='requested'
    ).count()

    cancelled_hires = (
        WorkerHire.objects
        .filter(
            customer=customer,
            status='cancelled'
        )
        .count()
    )

    # =====================================================
    # REVIEWS
    # =====================================================

    reviews_count = (
        WorkerReview.objects
        .filter(
            hire__customer=customer
        )
        .count()
    )

    reviewed_hire_ids = set(
        WorkerReview.objects
        .filter(
            hire__customer=customer
        )
        .values_list(
            'hire_id',
            flat=True
        )
    )

    # =====================================================
    # UNREAD WORKER MESSAGES
    #
    # Messages sent TO the current customer
    # =====================================================

    unread_worker_messages_count = (
        WorkerMessage.objects
        .filter(
            receiver=request.user,
            is_read=False
        )
        .count()
    )

    # =====================================================
    # CONVERSATIONS
    #
    # Get hires that have at least one message
    # =====================================================

    message_hire_ids = (
        WorkerMessage.objects
        .filter(
            Q(sender=request.user) |
            Q(receiver=request.user)
        )
        .values_list(
            'hire_id',
            flat=True
        )
        .distinct()
    )

    message_hires = []

    for hire in hires:

        if hire.id in message_hire_ids:

            unread_messages = (
                WorkerMessage.objects
                .filter(
                    hire=hire,
                    receiver=request.user,
                    is_read=False
                )
                .count()
            )

            hire.unread_messages = unread_messages

            message_hires.append(hire)

    # =====================================================
    # CONTEXT
    # =====================================================

    context = {

        'customer': customer,

        'hires': hires,

        'total_hires': total_hires,
        'active_hires': active_hires,
        'completed_hires': completed_hires,
        'pending_hires': pending_hires,
        'cancelled_hires': cancelled_hires,

        'active_hires_count': active_hires,
        'completed_hires_count': completed_hires,

        'reviews_count': reviews_count,
        'reviewed_hire_ids': reviewed_hire_ids,

        # MESSAGE DATA
        'unread_worker_messages_count': unread_worker_messages_count,
        'message_hires': message_hires,
    }

    return render(
        request,
        'properties/customer_dashboard.html',
        context
    )

# =========================================================
# WORKER DASHBOARD
# =========================================================


@login_required(login_url='site_login')
def worker_dashboard(request):

    try:

        worker = request.user.skilled_worker_profile

    except SkilledWorker.DoesNotExist:

        messages.error(
            request,
            'You do not have a skilled worker profile.'
        )

        return redirect(
            'marketplace_dashboard'
        )

    if not worker.is_approved:

        messages.warning(
            request,
            'Your skilled worker application is still '
            'waiting for approval.'
        )

        return redirect(
            'marketplace_dashboard'
        )

    # =====================================================
    # WORKER HIRES
    # =====================================================

    hires = (
        WorkerHire.objects
        .filter(
            worker=worker
        )
        .select_related(
            'customer'
        )
        .order_by(
            '-hired_at'
        )
    )

    pending_requests = (
        hires
        .filter(
            status='requested'
        )
        .count()
    )

    active_jobs = (
        hires
        .filter(
            status='active'
        )
        .count()
    )

    completed_jobs = (
        hires
        .filter(
            status='completed'
        )
        .count()
    )

    cancelled_jobs = (
        hires
        .filter(
            status='cancelled'
        )
        .count()
    )

    declined_requests = (
        hires
        .filter(
            status='declined'
        )
        .count()
    )

    # =====================================================
    # WORKER REVIEWS
    # =====================================================

    reviews = (
        WorkerReview.objects
        .filter(
            hire__worker=worker,
            is_approved=True
        )
        .select_related(
            'hire',
            'hire__customer'
        )
        .order_by(
            '-created_at'
        )
    )

    reviews_count = reviews.count()

    reviewed_hire_ids = set(
        reviews.values_list(
            'hire_id',
            flat=True
        )
    )

    if reviews_count:

        total_rating = sum(
            review.rating
            for review in reviews
        )

        average_rating = round(
            total_rating / reviews_count,
            1
        )

    else:

        average_rating = 0

    # =====================================================
    # CUSTOMER REVIEWS GIVEN BY WORKER
    # =====================================================

    customer_reviewed_hire_ids = set(
        CustomerReview.objects
        .filter(
            hire__worker=worker
        )
        .values_list(
            'hire_id',
            flat=True
        )
    )

    # =====================================================
    # WORKER MESSAGES
    #
    # WorkerHire has a reverse relationship called
    # "messages", so use messages__ instead of
    # workermessage__.
    # =====================================================

    message_hires = (
        WorkerHire.objects
        .filter(
            worker=worker,
            messages__isnull=False
        )
        .select_related(
            'customer'
        )
        .annotate(
            unread_messages=Count(
                'messages',
                filter=Q(
                    messages__receiver=request.user,
                    messages__is_read=False
                )
            )
        )
        .order_by(
            '-hired_at'
        )
        .distinct()
    )

    # =====================================================
    # TOTAL UNREAD WORKER MESSAGES
    # =====================================================

    worker_unread_messages_count = (
        WorkerMessage.objects
        .filter(
            receiver=request.user,
            is_read=False
        )
        .count()
    )

    # =====================================================
    # CONTEXT
    # =====================================================

    context = {

        'worker': worker,

        'hires': hires,

        'pending_requests': pending_requests,
        'active_jobs': active_jobs,
        'completed_jobs': completed_jobs,
        'cancelled_jobs': cancelled_jobs,
        'declined_requests': declined_requests,

        'reviews': reviews,
        'reviews_count': reviews_count,
        'average_rating': average_rating,

        'reviewed_hire_ids': reviewed_hire_ids,
        'customer_reviewed_hire_ids': customer_reviewed_hire_ids,

        # MESSAGES
        'message_hires': message_hires,
        'worker_unread_messages_count': worker_unread_messages_count,
    }

    return render(
        request,
        'properties/worker_dashboard.html',
        context
    )

# =========================================================
# MY SKILLED WORKER PROFILE
# =========================================================

@login_required(login_url='site_login')
def my_worker_profile(request):

    try:

        worker = request.user.skilled_worker_profile

    except SkilledWorker.DoesNotExist:

        messages.error(
            request,
            'You do not have a skilled worker profile.'
        )

        return redirect(
            'marketplace_dashboard'
        )

    if not worker.is_approved:

        messages.warning(
            request,
            'Your skilled worker application is still '
            'waiting for approval.'
        )

        return redirect(
            'marketplace_dashboard'
        )

    reviews = (
        WorkerReview.objects
        .filter(
            hire__worker=worker,
            is_approved=True
        )
        .select_related(
            'hire',
            'hire__customer'
        )
        .order_by(
            '-created_at'
        )
    )

    reviews_count = reviews.count()

    if reviews_count:

        total_rating = sum(
            review.rating
            for review in reviews
        )

        average_rating = round(
            total_rating / reviews_count,
            1
        )

    else:

        average_rating = 0

    hires = (
        WorkerHire.objects
        .filter(
            worker=worker
        )
        .select_related(
            'customer'
        )
        .order_by(
            '-hired_at'
        )
    )

    total_hires = hires.count()

    active_hires = hires.filter(
        status='active'
    ).count()

    completed_hires = hires.filter(
        status='completed'
    ).count()

    pending_hires = hires.filter(
        status='requested'
    ).count()

    context = {

        'worker': worker,

        'reviews': reviews,
        'reviews_count': reviews_count,
        'average_rating': average_rating,

        'hires': hires,
        'total_hires': total_hires,
        'active_hires': active_hires,
        'completed_hires': completed_hires,
        'pending_hires': pending_hires,
    }

    return render(
        request,
        'properties/my_worker_profile.html',
        context
    )


# =========================================================
# WORKER VIEW CUSTOMER PROFILE
# =========================================================

@login_required(login_url='site_login')
def customer_profile(
    request,
    customer_id
):

    try:

        worker = request.user.skilled_worker_profile

    except SkilledWorker.DoesNotExist:

        messages.error(
            request,
            'You do not have a skilled worker profile.'
        )

        return redirect(
            'marketplace_dashboard'
        )

    if not worker.is_approved:

        messages.warning(
            request,
            'Your skilled worker account is still waiting '
            'for approval.'
        )

        return redirect(
            'marketplace_dashboard'
        )

    customer = get_object_or_404(
        Customer,
        id=customer_id
    )

    has_worked_with_customer = (
        WorkerHire.objects
        .filter(
            worker=worker,
            customer=customer
        )
        .exists()
    )

    if not has_worked_with_customer:

        messages.error(
            request,
            'You can only view customers you have worked with.'
        )

        return redirect(
            'worker_dashboard'
        )

    reviews = (
        CustomerReview.objects
        .filter(
            hire__customer=customer,
            is_approved=True
        )
        .select_related(
            'hire',
            'hire__worker'
        )
        .order_by(
            '-created_at'
        )
    )

    reviews_count = reviews.count()

    if reviews_count:

        total_rating = sum(
            review.rating
            for review in reviews
        )

        average_rating = round(
            total_rating / reviews_count,
            1
        )

    else:

        average_rating = 0

    completed_hires = (
        WorkerHire.objects
        .filter(
            customer=customer,
            status='completed'
        )
        .select_related(
            'worker'
        )
        .order_by(
            '-completed_at'
        )
    )

    worker_review = (
        CustomerReview.objects
        .filter(
            hire__customer=customer,
            hire__worker=worker
        )
        .select_related(
            'hire'
        )
        .order_by(
            '-created_at'
        )
        .first()
    )

    my_reviews = (
        CustomerReview.objects
        .filter(
            hire__customer=customer,
            hire__worker=worker,
            is_approved=True
        )
        .select_related(
            'hire'
        )
        .order_by(
            '-created_at'
        )
    )

    context = {

        'worker': worker,
        'customer': customer,

        'reviews': reviews,
        'reviews_count': reviews_count,
        'average_rating': average_rating,

        'completed_hires': completed_hires,

        'worker_review': worker_review,
        'my_reviews': my_reviews,
    }

    return render(
        request,
        'properties/customer_profile.html',
        context
    )


# =========================================================
# HIRE SKILLED WORKER
# =========================================================
@login_required(login_url='site_login')
def worker_hire(
    request,
    worker_id
):

    # =====================================================
    # GET SKILLED WORKER
    # =====================================================

    worker = get_object_or_404(
        SkilledWorker,
        id=worker_id,
        is_approved=True
    )


    # =====================================================
    # PREVENT SKILLED WORKER FROM HIRING THEMSELVES
    # =====================================================

    if worker.user_id == request.user.id:

        messages.warning(
            request,
            'You cannot hire yourself as a skilled worker.'
        )

        return redirect(
            'skilled_worker_profile',
            worker_id=worker.id
        )

    # =====================================================
    # GET CUSTOMER PROFILE
    # =====================================================

    try:

        customer = request.user.customer_profile

    except Customer.DoesNotExist:

        messages.warning(
            request,
            'Your account does not currently have '
            'a customer profile.'
        )

        return redirect(
            'marketplace_dashboard'
        )


    # =====================================================
    # CUSTOMER VERIFICATION
    # =====================================================

    if not customer.email_verified:

        messages.warning(
            request,
            'Your customer profile is still waiting '
            'for verification. You can browse skilled '
            'workers, but you must be verified before '
            'you can hire a worker.'
        )

        return redirect(
            'marketplace_dashboard'
        )


    # =====================================================
    # WORKER AVAILABILITY
    # =====================================================

    if worker.availability != 'available':

        messages.warning(
            request,
            'This skilled worker is currently not available.'
        )

        return redirect(
            'skilled_worker_profile',
            worker_id=worker.id
        )


    # =====================================================
    # CHECK EXISTING HIRE
    # =====================================================

    existing_hire = (
        WorkerHire.objects
        .filter(
            customer=customer,
            worker=worker,
            status__in=[
                'requested',
                'active'
            ]
        )
        .first()
    )


    if existing_hire:

        messages.info(
            request,
            f'You already have a pending or active hire '
            f'request with {worker.full_name}.'
        )

        return redirect(
            'marketplace_dashboard'
        )


    # =====================================================
    # HANDLE POST
    # =====================================================

    if request.method == 'POST':

        service = request.POST.get(
            'service',
            ''
        ).strip()

        notes = request.POST.get(
            'notes',
            ''
        ).strip()


        # =================================================
        # SERVICE REQUIRED
        # =================================================

        if not service:

            messages.error(
                request,
                'Please enter the service you want '
                'this worker to provide.'
            )

            return redirect(
                'worker_hire',
                worker_id=worker.id
            )


        # =================================================
        # CREATE HIRE REQUEST
        # =================================================

        hire = WorkerHire.objects.create(
                customer=customer,
                worker=worker,
                service=service,
                notes=notes,
                status='requested'
            )

        # =====================================================
        # NOTIFY WORKER
        # =====================================================

        create_notification(
            recipient=worker.user,
            notification_type='hire_request',
            title='New Hire Request',
            message=(
                f'{customer.full_name} has requested to hire you '
                f'for {service}.'
            ),
            link=reverse(
                'worker_dashboard'
            )
        )
        # =================================================
        # SUCCESS MESSAGE
        # =================================================

        messages.success(
            request,
            f'Your request to hire {worker.full_name} '
            'has been submitted successfully.'
        )


        return redirect(
            'marketplace_dashboard'
        )


    # =====================================================
    # DISPLAY HIRE PAGE
    # =====================================================

    return render(
        request,
        'properties/worker_hire.html',
        {
            'worker': worker,
            'customer': customer,
        }
    )

# =========================================================
# CANCEL WORKER HIRE
# =========================================================

@login_required(login_url='site_login')
def cancel_worker_hire(
    request,
    hire_id
):

    try:

        customer = request.user.customer_profile

    except Customer.DoesNotExist:

        messages.error(
            request,
            'You must have a customer profile to '
            'cancel a request.'
        )

        return redirect(
            'marketplace_dashboard'
        )

    hire = get_object_or_404(
        WorkerHire,
        id=hire_id,
        customer=customer
    )

    if request.method != 'POST':

        messages.warning(
            request,
            'Invalid cancellation request.'
        )

        return redirect(
            'marketplace_dashboard'
        )

    if hire.status not in [
        'requested',
        'active'
    ]:

        messages.warning(
            request,
            'This request can no longer be cancelled.'
        )

        return redirect(
            'marketplace_dashboard'
        )

    hire.status = 'cancelled'

    hire.save(
        update_fields=[
            'status'
        ]
    )
    # =====================================================
    # NOTIFY CUSTOMER
    # =====================================================

    create_notification(
        recipient=hire.customer.user,
        notification_type='hire_accepted',
        title='Hire Request Accepted',
        message=(
            f'{hire.worker.full_name} has accepted your '
            f'hire request for {hire.service}.'
        ),
        link=reverse(
            'customer_dashboard'
        )
    )

    # =====================================================
    # NOTIFY CUSTOMER
    # =====================================================

    create_notification(
        recipient=hire.customer.user,
        notification_type='hire_declined',
        title='Hire Request Declined',
        message=(
            f'{hire.worker.full_name} has declined your '
            f'hire request for {hire.service}.'
        ),
        link=reverse(
            'customer_dashboard'
        )
    )

    messages.success(
        request,
        f'Your request to hire '
        f'{hire.worker.full_name} '
        'has been cancelled successfully.'
    )

    return redirect(
        'marketplace_dashboard'
    )

    # =====================================================
    # NOTIFY WORKER
    # =====================================================

    create_notification(
        recipient=hire.worker.user,
        notification_type='hire_cancelled',
        title='Hire Request Cancelled',
        message=(
            f'{hire.customer.full_name} has cancelled the '
            f'hire request for {hire.service}.'
        ),
        link=reverse(
            'worker_dashboard'
        )
    )

        # =====================================================
    # NOTIFY CUSTOMER
    # =====================================================

    create_notification(
        recipient=hire.customer.user,
        notification_type='job_completed',
        title='Job Completed',
        message=(
            f'{hire.worker.full_name} has marked your '
            f'{hire.service} job as completed.'
        ),
        link=reverse(
            'customer_dashboard'
        )
    )


# =========================================================
# WORKER ACCEPT HIRE
# =========================================================

@login_required(login_url='site_login')
def accept_worker_hire(
    request,
    hire_id
):

    try:

        worker = request.user.skilled_worker_profile

    except SkilledWorker.DoesNotExist:

        messages.error(
            request,
            'You do not have a skilled worker profile.'
        )

        return redirect(
            'marketplace_dashboard'
        )

    if not worker.is_approved:

        return redirect(
            'marketplace_dashboard'
        )

    hire = get_object_or_404(
        WorkerHire,
        id=hire_id,
        worker=worker
    )

    if request.method != 'POST':

        messages.warning(
            request,
            'Invalid request.'
        )

        return redirect(
            'worker_dashboard'
        )

    if hire.status != 'requested':

        messages.warning(
            request,
            'This request is no longer available for acceptance.'
        )

        return redirect(
            'worker_dashboard'
        )

    hire.status = 'active'

    hire.save(
        update_fields=[
            'status'
        ]
    )

    messages.success(
        request,
        f'You have accepted the hire request from '
        f'{hire.customer.full_name}.'
    )

    return redirect(
        'worker_dashboard'
    )


# =========================================================
# WORKER DECLINE HIRE
# =========================================================

@login_required(login_url='site_login')
def decline_worker_hire(
    request,
    hire_id
):

    try:

        worker = request.user.skilled_worker_profile

    except SkilledWorker.DoesNotExist:

        messages.error(
            request,
            'You do not have a skilled worker profile.'
        )

        return redirect(
            'marketplace_dashboard'
        )

    if not worker.is_approved:

        return redirect(
            'marketplace_dashboard'
        )

    hire = get_object_or_404(
        WorkerHire,
        id=hire_id,
        worker=worker
    )

    if request.method != 'POST':

        messages.warning(
            request,
            'Invalid request.'
        )

        return redirect(
            'worker_dashboard'
        )

    if hire.status != 'requested':

        messages.warning(
            request,
            'This request is no longer available.'
        )

        return redirect(
            'worker_dashboard'
        )

    hire.status = 'declined'

    hire.save(
        update_fields=[
            'status'
        ]
    )

    messages.success(
        request,
        f'You have declined the hire request from '
        f'{hire.customer.full_name}.'
    )

    return redirect(
        'worker_dashboard'
    )


# =========================================================
# WORKER COMPLETE HIRE
# =========================================================

@login_required(login_url='site_login')
def complete_worker_hire(
    request,
    hire_id
):

    try:

        worker = request.user.skilled_worker_profile

    except SkilledWorker.DoesNotExist:

        messages.error(
            request,
            'You do not have a skilled worker profile.'
        )

        return redirect(
            'marketplace_dashboard'
        )

    if not worker.is_approved:

        return redirect(
            'marketplace_dashboard'
        )

    hire = get_object_or_404(
        WorkerHire,
        id=hire_id,
        worker=worker
    )

    if request.method != 'POST':

        messages.warning(
            request,
            'Invalid request.'
        )

        return redirect(
            'worker_dashboard'
        )

    if hire.status != 'active':

        messages.warning(
            request,
            'Only active jobs can be marked as completed.'
        )

        return redirect(
            'worker_dashboard'
        )

    hire.status = 'completed'
    hire.completed_at = timezone.now()

    hire.save(
        update_fields=[
            'status',
            'completed_at'
        ]
    )

    messages.success(
        request,
        f'The job for {hire.customer.full_name} '
        'has been marked as completed.'
    )

    return redirect(
        'worker_dashboard'
    )


# =========================================================
# CUSTOMER REVIEWS WORKER
# =========================================================

@login_required(login_url='site_login')
def worker_review(
    request,
    hire_id
):

    try:

        customer = request.user.customer_profile

    except Customer.DoesNotExist:

        messages.warning(
            request,
            'You need a customer profile to submit a review.'
        )

        return redirect(
            'marketplace_dashboard'
        )

    hire = get_object_or_404(
        WorkerHire,
        id=hire_id,
        customer=customer
    )

    if not customer.email_verified:

        messages.warning(
            request,
            'Your customer profile must be verified '
            'before you can submit a review.'
        )

        return redirect(
            'marketplace_dashboard'
        )

    if hire.status != 'completed':

        messages.warning(
            request,
            'You can only review a worker after the job '
            'has been completed.'
        )

        return redirect(
            'customer_dashboard'
        )

    existing_review = (
        WorkerReview.objects
        .filter(
            hire=hire
        )
        .first()
    )

    if existing_review:

        messages.info(
            request,
            'You have already reviewed this worker.'
        )

        return redirect(
            'skilled_worker_profile',
            worker_id=hire.worker.id
        )

    if request.method == 'POST':

        rating = request.POST.get(
            'rating'
        )

        comment = (
            request.POST.get(
                'comment',
                ''
            )
            .strip()
        )

        try:

            rating = int(rating)

        except (
            TypeError,
            ValueError
        ):

            messages.error(
                request,
                'Please provide a valid rating.'
            )

            return redirect(
                'worker_review',
                hire_id=hire.id
            )

        if rating < 1 or rating > 5:

            messages.error(
                request,
                'Rating must be between 1 and 5.'
            )

            return redirect(
                'worker_review',
                hire_id=hire.id
            )

        if not comment:

            messages.error(
                request,
                'Please provide a comment.'
            )

            return redirect(
                'worker_review',
                hire_id=hire.id
            )

        WorkerReview.objects.create(
            hire=hire,
            rating=rating,
            comment=comment,
            is_approved=True
        )
        # =====================================================
        # NOTIFY WORKER
        # =====================================================

        create_notification(
            recipient=hire.worker.user,
            notification_type='review',
            title='New Worker Review',
            message=(
                f'{customer.full_name} left you a '
                f'{rating}-star review.'
            ),
            link=reverse(
                'my_worker_profile'
            )
        )

        messages.success(
            request,
            'Thank you! Your review has been submitted '
            'successfully.'
        )

        return redirect(
            'skilled_worker_profile',
            worker_id=hire.worker.id
        )

    return render(
        request,
        'properties/worker_review.html',
        {
            'hire': hire,
            'worker': hire.worker,
        }
    )


# =========================================================
# EDIT MY SKILLED WORKER PROFILE
# =========================================================

@login_required(login_url='site_login')
def edit_worker_profile(request):

    try:

        worker = request.user.skilled_worker_profile

    except SkilledWorker.DoesNotExist:

        messages.error(
            request,
            'You do not have a skilled worker profile.'
        )

        return redirect(
            'marketplace_dashboard'
        )

    # =====================================================
    # HANDLE FORM SUBMISSION
    # =====================================================

    if request.method == 'POST':

        form = SkilledWorkerRegistrationForm(
            request.POST,
            request.FILES,
            instance=worker,
            current_user=request.user,
        )

        if form.is_valid():

            worker = form.save(
                commit=False
            )

            # -------------------------------------------------
            # KEEP PROFILE CONNECTED TO CURRENT USER
            # -------------------------------------------------

            worker.user = request.user

            # -------------------------------------------------
            # KEEP EMAIL SYNCHRONIZED WITH USER ACCOUNT
            # -------------------------------------------------

            if request.user.email:

                worker.email = (
                    request.user.email
                    .strip()
                    .lower()
                )

            worker.save()

            messages.success(
                request,
                'Your skilled worker profile has been '
                'updated successfully.'
            )

            # -------------------------------------------------
            # RETURN TO WORKER DASHBOARD AFTER SAVING
            # -------------------------------------------------

            return redirect(
                'worker_dashboard'
            )

    # =====================================================
    # DISPLAY FORM
    # =====================================================

    else:

        form = SkilledWorkerRegistrationForm(
            instance=worker,
            current_user=request.user,
        )

    return render(
        request,
        'properties/edit_worker_profile.html',
        {
            'worker': worker,
            'form': form,
        }
    )



# =========================================================
# DELETE MY SKILLED WORKER PROFILE
# =========================================================

@login_required(login_url='site_login')
def delete_worker_profile(request):

    try:

        worker = request.user.skilled_worker_profile

    except SkilledWorker.DoesNotExist:

        messages.error(
            request,
            'You do not have a skilled worker profile.'
        )

        return redirect(
            'marketplace_dashboard'
        )

    # =====================================================
    # DELETE MUST BE POST
    # =====================================================

    if request.method != 'POST':

        messages.warning(
            request,
            'Invalid delete request.'
        )

        return redirect(
            'my_worker_profile'
        )

    # =====================================================
    # DELETE SKILLED WORKER PROFILE ONLY
    # =====================================================

    worker.delete()

    messages.success(
        request,
        'Your skilled worker profile has been deleted successfully.'
    )

    return redirect(
        'marketplace_dashboard'
    )

# =========================================================
# WORKER REVIEWS CUSTOMER
# =========================================================

@login_required(login_url='site_login')
def customer_review(
    request,
    hire_id
):

    try:

        worker = request.user.skilled_worker_profile

    except SkilledWorker.DoesNotExist:

        messages.error(
            request,
            'You do not have a skilled worker profile.'
        )

        return redirect(
            'marketplace_dashboard'
        )

    if not worker.is_approved:

        messages.warning(
            request,
            'Your skilled worker account is not approved yet.'
        )

        return redirect(
            'marketplace_dashboard'
        )

    hire = get_object_or_404(
        WorkerHire,
        id=hire_id,
        worker=worker
    )

    if hire.status != 'completed':

        messages.warning(
            request,
            'You can only review a customer after completing '
            'the job.'
        )

        return redirect(
            'worker_dashboard'
        )

    existing_review = (
        CustomerReview.objects
        .filter(
            hire=hire
        )
        .first()
    )

    if existing_review:

        messages.info(
            request,
            'You have already reviewed this customer.'
        )

        return redirect(
            'customer_profile',
            customer_id=hire.customer.id
        )

    if request.method == 'POST':

        rating = request.POST.get(
            'rating'
        )

        comment = (
            request.POST.get(
                'comment',
                ''
            )
            .strip()
        )

        try:

            rating = int(rating)

        except (
            TypeError,
            ValueError
        ):

            messages.error(
                request,
                'Please select a valid rating.'
            )

            return render(
                request,
                'properties/customer_review.html',
                {
                    'hire': hire,
                    'worker': worker,
                }
            )

        if rating < 1 or rating > 5:

            messages.error(
                request,
                'Rating must be between 1 and 5 stars.'
            )

            return render(
                request,
                'properties/customer_review.html',
                {
                    'hire': hire,
                    'worker': worker,
                }
            )

        if not comment:

            messages.error(
                request,
                'Please write a review.'
            )

            return render(
                request,
                'properties/customer_review.html',
                {
                    'hire': hire,
                    'worker': worker,
                }
            )

        CustomerReview.objects.create(
            hire=hire,
            rating=rating,
            comment=comment,
            is_approved=True
        )

        # =====================================================
        # NOTIFY CUSTOMER
        # =====================================================

        create_notification(
            recipient=hire.customer.user,
            notification_type='review',
            title='New Customer Review',
            message=(
                f'{worker.full_name} left you a '
                f'{rating}-star review.'
            ),
            link=reverse(
                'customer_dashboard'
            )
        )

        messages.success(
            request,
            'Your review has been submitted successfully.'
        )

        return redirect(
            'customer_profile',
            customer_id=hire.customer.id
        )

    return render(
        request,
        'properties/customer_review.html',
        {
            'hire': hire,
            'worker': worker,
        }
    )


# =========================================================
# ACCOUNT PASSWORD CHANGE
# =========================================================

class AccountPasswordChangeView(
    PasswordChangeView
):

    template_name = (
        'properties/account_password_change.html'
    )

    success_url = reverse_lazy(
        'account_settings'
    )


# =========================================================
# SKILLED WORKER PASSWORD RESET
# =========================================================

class SkilledWorkerPasswordResetView(
    PasswordResetView
):

    template_name = (
        'properties/skilled_worker_password_reset.html'
    )

    form_class = SkilledWorkerPasswordResetForm

    email_template_name = (
        'properties/skilled_worker_password_reset_email.html'
    )

    subject_template_name = (
        'properties/skilled_worker_password_reset_subject.txt'
    )

    success_url = reverse_lazy(
        'worker_password_reset_done'
    )


# =========================================================
# PASSWORD RESET DONE
# =========================================================

class SkilledWorkerPasswordResetDoneView(
    PasswordResetDoneView
):

    template_name = (
        'properties/skilled_worker_password_reset_done.html'
    )


# =========================================================
# PASSWORD RESET CONFIRM
# =========================================================

class SkilledWorkerPasswordResetConfirmView(
    PasswordResetConfirmView
):

    template_name = (
        'properties/skilled_worker_password_reset_confirm.html'
    )

    success_url = reverse_lazy(
        'worker_password_reset_complete'
    )


# =========================================================
# PASSWORD RESET COMPLETE
# =========================================================

class SkilledWorkerPasswordResetCompleteView(
    PasswordResetCompleteView
):

    template_name = (
        'properties/skilled_worker_password_reset_complete.html'
    )


# =========================================================
# ACCOUNT SETTINGS
# =========================================================

@login_required(login_url='site_login')
def account_settings(request):

    try:

        account_settings_obj = (
            request.user.account_settings
        )

    except AccountSettings.DoesNotExist:

        account_settings_obj = (
            AccountSettings.objects.create(
                user=request.user
            )
        )

    if request.method == 'POST':

        form = AccountSettingsForm(
            request.POST,
            request.FILES,
            instance=account_settings_obj,
            user=request.user,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Your account settings have been updated successfully.'
            )

            return redirect(
                'account_settings'
            )

    else:

        form = AccountSettingsForm(
            instance=account_settings_obj,
            user=request.user,
        )

    return render(
        request,
        'properties/account_settings.html',
        {
            'form': form,
            'account_settings': account_settings_obj,
            'user': request.user,
        }
    )


# =========================================================
# MARKETPLACE SELLER DASHBOARD
# =========================================================

@login_required(login_url='site_login')
def marketplace_seller_dashboard(request):

    user = request.user

    # =====================================================
    # SELLER LISTINGS
    # =====================================================

    listings = (
        MarketplaceListing.objects
        .filter(
            seller=user
        )
        .prefetch_related(
            'gallery_images',
            'favourites',
        )
        .order_by(
            '-created_at'
        )
    )

    # =====================================================
    # LISTING COUNTS
    # =====================================================

    total_listings = listings.count()

    approved_listings = (
        listings
        .filter(
            approval_status='approved'
        )
        .count()
    )

    under_review_listings = (
        listings
        .filter(
            approval_status='under_review'
        )
        .count()
    )

    rejected_listings = (
        listings
        .filter(
            approval_status='rejected'
        )
        .count()
    )

    # =====================================================
    # ADVERTISEMENT STATUS
    # =====================================================

    available_listings = (
        listings
        .filter(
            status='available'
        )
        .count()
    )

    reserved_listings = (
        listings
        .filter(
            status='reserved'
        )
        .count()
    )

    sold_listings = (
        listings
        .filter(
            status='sold'
        )
        .count()
    )

    # =====================================================
    # VIEWS
    # =====================================================

    total_views = sum(
        listing.views or 0
        for listing in listings
    )

    # =====================================================
    # UNIQUE PEOPLE WHO CHATTED
    #
    # One buyer chatting multiple times about the same
    # advertisement counts as ONE interested person.
    # =====================================================

    total_chats = 0

    for listing in listings:

        chatters_count = (
            MarketplaceMessage.objects
            .filter(
                listing=listing
            )
            .exclude(
                sender=user
            )
            .values(
                'sender_id'
            )
            .distinct()
            .count()
        )

        # Store this value so the template can use it.
        listing.unique_chatters_count = chatters_count

        total_chats += chatters_count

    # =====================================================
    # FAVOURITES
    # =====================================================

    total_favourites = 0

    for listing in listings:

        favourite_count = (
            listing.favourites
            .count()
        )

        listing.favourite_count = favourite_count

        total_favourites += favourite_count

    # =====================================================
    # MARKETPLACE REVIEWS
    #
    # We query MarketplaceReview directly instead of using
    # listing.reviews / listing.seller_reviews so this view
    # does not depend on the related_name.
    # =====================================================

    approved_reviews = (
        MarketplaceReview.objects
        .filter(
            seller=user,
            is_approved=True
        )
    )

    total_reviews = approved_reviews.count()

    # =====================================================
    # ADD REVIEW COUNT TO EACH LISTING
    # =====================================================

    for listing in listings:

        listing.review_count = (
            approved_reviews
            .filter(
                listing_id=listing.id
            )
            .count()
        )

    # =====================================================
    # PERFORMANCE RATING
    # =====================================================

    average_rating = (
        approved_reviews
        .aggregate(
            average=Avg('rating')
        )['average']
    )

    if average_rating:

        average_rating = round(
            float(average_rating),
            1
        )

    else:

        average_rating = 0

    # =====================================================
    # RATING BREAKDOWN
    # =====================================================

    five_star_reviews = (
        approved_reviews
        .filter(
            rating=5
        )
        .count()
    )

    four_star_reviews = (
        approved_reviews
        .filter(
            rating=4
        )
        .count()
    )

    three_star_reviews = (
        approved_reviews
        .filter(
            rating=3
        )
        .count()
    )

    two_star_reviews = (
        approved_reviews
        .filter(
            rating=2
        )
        .count()
    )

    one_star_reviews = (
        approved_reviews
        .filter(
            rating=1
        )
        .count()
    )

    # =====================================================
    # LISTING VALUES
    #
    # These are kept because your existing dashboard may
    # still use them.
    # =====================================================

    sold_value = sum(
        listing.price or 0
        for listing in listings
        if listing.status == 'sold'
    )

    available_value = sum(
        listing.price or 0
        for listing in listings
        if listing.status == 'available'
    )

    reserved_value = sum(
        listing.price or 0
        for listing in listings
        if listing.status == 'reserved'
    )

    # =====================================================
    # CONTEXT
    # =====================================================

    context = {

        'user': user,

        # Listings
        'listings': listings,
        'total_listings': total_listings,
        'approved_listings': approved_listings,
        'under_review_listings': under_review_listings,
        'rejected_listings': rejected_listings,

        # Advertisement status
        'available_listings': available_listings,
        'reserved_listings': reserved_listings,
        'sold_listings': sold_listings,

        # Performance
        'total_views': total_views,
        'total_chats': total_chats,
        'total_favourites': total_favourites,

        # Reviews
        'total_reviews': total_reviews,
        'average_rating': average_rating,

        # Rating breakdown
        'five_star_reviews': five_star_reviews,
        'four_star_reviews': four_star_reviews,
        'three_star_reviews': three_star_reviews,
        'two_star_reviews': two_star_reviews,
        'one_star_reviews': one_star_reviews,

        # Values
        'sold_value': sold_value,
        'available_value': available_value,
        'reserved_value': reserved_value,
    }

    return render(
        request,
        'properties/marketplace_seller_dashboard.html',
        context
    )

# =========================================================
# REVIEW MARKETPLACE SELLER
# =========================================================

@login_required(login_url='site_login')
def marketplace_review_seller(
    request,
    listing_id
):

    listing = get_object_or_404(
        MarketplaceListing.objects
        .select_related(
            'seller'
        ),
        id=listing_id,
        approval_status='approved',
    )

    seller = listing.seller

    # =====================================================
    # SELLER CANNOT REVIEW THEMSELVES
    # =====================================================

    if request.user == seller:

        messages.error(
            request,
            'You cannot review your own advertisement.'
        )

        return redirect(
            'marketplace_detail',
            listing_id=listing.id
        )

    # =====================================================
    # CHECK EXISTING REVIEW
    # =====================================================

    existing_review = (
        MarketplaceReview.objects
        .filter(
            listing=listing,
            reviewer=request.user,
        )
        .first()
    )

    if existing_review:

        messages.info(
            request,
            'You have already reviewed this advertisement.'
        )

        return redirect(
            'marketplace_detail',
            listing_id=listing.id
        )

    # =====================================================
    # SUBMIT REVIEW
    # =====================================================

    if request.method == 'POST':

        form = MarketplaceSellerReviewForm(
            request.POST
        )

        if form.is_valid():

            review = form.save(
                commit=False
            )

            review.listing = listing
            review.reviewer = request.user
            review.seller = listing.seller

            # Automatically approved
            review.is_approved = True

            review.save()

            messages.success(
                request,
                'Thank you. Your review has been submitted '
                'successfully.'
            )

            return redirect(
                'marketplace_detail',
                listing_id=listing.id
            )

    else:

        form = MarketplaceSellerReviewForm()

    return render(
        request,
        'properties/marketplace_review_seller.html',
        {
            'form': form,
            'listing': listing,
            'seller': seller,
        }
    )


# =========================================================
# MARKETPLACE SELLER PROFILE
# =========================================================

@login_required(login_url='site_login')
def marketplace_seller_profile(
    request,
    seller_id
):

    seller = get_object_or_404(
        User,
        id=seller_id
    )

    # =====================================================
    # SELLER APPROVED ADVERTISEMENTS
    # =====================================================

    listings = (
        MarketplaceListing.objects
        .filter(
            seller=seller,
            approval_status='approved',
        )
        .prefetch_related(
            'gallery_images'
        )
        .order_by(
            '-created_at'
        )
    )

    # =====================================================
    # SELLER REVIEWS
    # =====================================================

    reviews = (
        MarketplaceReview.objects
        .filter(
            seller=seller,
            is_approved=True,
        )
        .select_related(
            'reviewer',
            'listing',
        )
        .order_by(
            '-created_at'
        )
    )

    total_reviews = reviews.count()

    # =====================================================
    # AVERAGE RATING
    # =====================================================

    average_rating = (
        reviews.aggregate(
            average=Avg('rating')
        )['average']
    )

    if average_rating:

        average_rating = round(
            float(average_rating),
            1
        )

    else:

        average_rating = 0

    # =====================================================
    # RATING BREAKDOWN
    # =====================================================

    five_star_reviews = reviews.filter(
        rating=5
    ).count()

    four_star_reviews = reviews.filter(
        rating=4
    ).count()

    three_star_reviews = reviews.filter(
        rating=3
    ).count()

    two_star_reviews = reviews.filter(
        rating=2
    ).count()

    one_star_reviews = reviews.filter(
        rating=1
    ).count()

    # =====================================================
    # TOTAL SELLER LISTINGS
    # =====================================================

    total_listings = listings.count()

    # =====================================================
    # TOTAL VIEWS
    # =====================================================

    total_views = sum(
        listing.views or 0
        for listing in listings
    )

    return render(
        request,
        'properties/marketplace_seller_profile.html',
        {
            'seller': seller,
            'listings': listings,

            'reviews': reviews,
            'total_reviews': total_reviews,
            'average_rating': average_rating,

            'five_star_reviews': five_star_reviews,
            'four_star_reviews': four_star_reviews,
            'three_star_reviews': three_star_reviews,
            'two_star_reviews': two_star_reviews,
            'one_star_reviews': one_star_reviews,

            'total_listings': total_listings,
            'total_views': total_views,
        }
    )


# =========================================================
# MARKETPLACE CHAT
# BUYER + SELLER TWO-WAY CHAT
# =========================================================
# =========================================================
# MARKETPLACE CHAT
# BUYER + SELLER TWO-WAY CHAT
#
# UNDER REVIEW:
# - Chat page can be opened
# - Existing messages can be viewed
# - New messages cannot be sent
#
# APPROVED:
# - Chat page can be opened
# - New messages can be sent
# =========================================================

@login_required(login_url='site_login')
def marketplace_chat(
    request,
    listing_id,
    buyer_id=None
):

    # =====================================================
    # GET LISTING
    #
    # IMPORTANT:
    # Do not filter approval_status here.
    # This allows under-review listings to open the chat.
    # =====================================================

    listing = get_object_or_404(
        MarketplaceListing.objects
        .select_related(
            'seller'
        )
        .prefetch_related(
            'gallery_images'
        ),
        id=listing_id,
    )

    current_user = request.user

    # =====================================================
    # CHAT PERMISSION
    # =====================================================

    can_chat = (
        listing.approval_status == 'approved'
    )

    is_under_review = (
        listing.approval_status == 'under_review'
    )

    is_rejected = (
        listing.approval_status == 'rejected'
    )

    # =====================================================
    # DETERMINE OTHER USER
    # =====================================================

    if current_user != listing.seller:

        # -------------------------------------------------
        # BUYER
        # -------------------------------------------------

        other_user = listing.seller

    else:

        # -------------------------------------------------
        # SELLER
        # -------------------------------------------------

        if buyer_id is None:

            messages.info(
                request,
                'Please select a buyer conversation.'
            )

            return redirect(
                'marketplace_messages'
            )

        # =================================================
        # PREVENT SELLER FROM CHATTING WITH THEMSELVES
        # =================================================

        if buyer_id == current_user.id:

            messages.error(
                request,
                'You cannot chat with yourself.'
            )

            return redirect(
                'marketplace_messages'
            )

        other_user = get_object_or_404(
            User,
            id=buyer_id
        )

        # =================================================
        # SELLER CAN ONLY OPEN EXISTING CONVERSATION
        # =================================================

        conversation_exists = (
            MarketplaceMessage.objects
            .filter(
                listing=listing
            )
            .filter(
                Q(
                    sender=current_user,
                    receiver=other_user
                )
                |
                Q(
                    sender=other_user,
                    receiver=current_user
                )
            )
            .exists()
        )

        if not conversation_exists:

            messages.error(
                request,
                'This conversation does not exist.'
            )

            return redirect(
                'marketplace_messages'
            )

    # =====================================================
    # LOAD CONVERSATION
    # =====================================================

    conversation = (
        MarketplaceMessage.objects
        .filter(
            listing=listing
        )
        .filter(
            Q(
                sender=current_user,
                receiver=other_user
            )
            |
            Q(
                sender=other_user,
                receiver=current_user
            )
        )
        .select_related(
            'sender',
            'receiver'
        )
        .order_by(
            'created_at'
        )
    )

    # =====================================================
    # MARK RECEIVED MESSAGES AS READ
    # =====================================================

    MarketplaceMessage.objects.filter(
        listing=listing,
        sender=other_user,
        receiver=current_user,
        is_read=False
    ).update(
        is_read=True
    )

    # =====================================================
    # SEND MESSAGE
    # =====================================================

    if request.method == 'POST':

        # =================================================
        # BLOCK MESSAGING UNTIL APPROVED
        # =================================================

        if not can_chat:

            if is_under_review:

                messages.warning(
                    request,
                    'This advertisement is still under review. '
                    'You can view the conversation, but you '
                    'cannot send messages until the advertisement '
                    'has been approved.'
                )

            elif is_rejected:

                messages.warning(
                    request,
                    'This advertisement was not approved. '
                    'Messaging is unavailable.'
                )

            else:

                messages.warning(
                    request,
                    'Messaging is currently unavailable '
                    'for this advertisement.'
                )

            # -------------------------------------------------
            # RETURN TO CORRECT CHAT
            # -------------------------------------------------

            if current_user == listing.seller:

                return redirect(
                    'marketplace_chat_with_buyer',
                    listing_id=listing.id,
                    buyer_id=other_user.id
                )

            return redirect(
                'marketplace_chat',
                listing_id=listing.id
            )

        # =================================================
        # GET MESSAGE TEXT
        # =================================================

        message_text = (
            request.POST.get(
                'message',
                ''
            )
            .strip()
        )

        # =================================================
        # MESSAGE REQUIRED
        # =================================================

        if not message_text:

            messages.error(
                request,
                'Please enter a message.'
            )

            if current_user == listing.seller:

                return redirect(
                    'marketplace_chat_with_buyer',
                    listing_id=listing.id,
                    buyer_id=other_user.id
                )

            return redirect(
                'marketplace_chat',
                listing_id=listing.id
            )

        # =================================================
        # CREATE MESSAGE
        # =================================================

        new_message = MarketplaceMessage.objects.create(
            listing=listing,
            sender=current_user,
            receiver=other_user,
            message=message_text,
        )

        # =====================================================
        # MARKETPLACE MESSAGE NOTIFICATION LINK
        # =====================================================

        if current_user == listing.seller:

            notification_link = reverse(
                'marketplace_chat_with_buyer',
                kwargs={
                    'listing_id': listing.id,
                    'buyer_id': other_user.id,
                }
            )

        else:

            notification_link = reverse(
                'marketplace_chat',
                kwargs={
                    'listing_id': listing.id,
                }
            )


        # =====================================================
        # CREATE MARKETPLACE MESSAGE NOTIFICATION
        # =====================================================

        create_notification(
            recipient=other_user,
            notification_type='marketplace_message',
            title='New Marketplace Message',
            message=(
                f'{current_user.get_full_name() or current_user.email} '
                f'sent you a message about "{listing.title}".'
            ),
            link=notification_link
        )

        # =================================================
        # UPDATE UNIQUE CHATTERS
        #
        # One buyer sending many messages = one chatter.
        # Seller's own messages are excluded.
        # =================================================

        unique_chatters = (
            MarketplaceMessage.objects
            .filter(
                listing=listing
            )
            .exclude(
                sender=listing.seller
            )
            .values(
                'sender'
            )
            .distinct()
            .count()
        )

        listing.chats_count = unique_chatters

        listing.save(
            update_fields=[
                'chats_count'
            ]
        )

        # =================================================
        # SELLER REDIRECT
        # =================================================

        if current_user == listing.seller:

            return redirect(
                'marketplace_chat_with_buyer',
                listing_id=listing.id,
                buyer_id=other_user.id
            )

        # =================================================
        # BUYER REDIRECT
        # =================================================

        return redirect(
            'marketplace_chat',
            listing_id=listing.id
        )

    # =====================================================
    # RENDER CHAT PAGE
    #
    # IMPORTANT:
    # This MUST be outside the POST block.
    # =====================================================

    return render(
        request,
        'properties/marketplace_chat.html',
        {
            'listing': listing,
            'conversation': conversation,
            'other_user': other_user,

            'can_chat': can_chat,

            'is_under_review': is_under_review,

            'is_rejected': is_rejected,
        }
    )

# =========================================================
# MARKETPLACE MESSAGES
# UNIFIED BUYER + SELLER INBOX
# =========================================================

@login_required(login_url='site_login')
def marketplace_messages(request):

    user = request.user

    # =====================================================
    # GET ALL MESSAGES INVOLVING CURRENT USER
    # =====================================================

    messages_queryset = (
        MarketplaceMessage.objects
        .filter(
            Q(sender=user) |
            Q(receiver=user)
        )
        .select_related(
            'sender',
            'receiver',
            'listing',
            'listing__seller',
        )
        .order_by('-created_at')
    )

    # =====================================================
    # BUILD UNIQUE CONVERSATIONS
    # =====================================================

    conversations = {}

    for message in messages_queryset:

        listing = message.listing

        if not listing:
            continue

        # =================================================
        # SAFETY:
        # SELLER MUST NOT CHAT WITH THEMSELVES
        # =================================================

        if (
            message.sender_id == listing.seller_id
            and
            message.receiver_id == listing.seller_id
        ):
            continue

        # =================================================
        # DETERMINE OTHER USER
        # =================================================

        if message.sender_id == user.id:
            other_user = message.receiver
        else:
            other_user = message.sender

        if not other_user:
            continue

        # =================================================
        # PREVENT SELF CONVERSATION
        # =================================================

        if other_user.id == user.id:
            continue

        # =================================================
        # CONVERSATION KEY
        #
        # One conversation per:
        # LISTING + OTHER USER
        # =================================================

        key = (
            listing.id,
            other_user.id
        )

        # =================================================
        # CREATE CONVERSATION
        # =================================================

        if key not in conversations:

            conversations[key] = {
                'listing': listing,
                'other_user': other_user,
                'latest_message': message,
                'unread_count': 0,
            }

        # =================================================
        # UPDATE LATEST MESSAGE
        # =================================================

        elif (
            message.created_at >
            conversations[key]['latest_message'].created_at
        ):

            conversations[key]['latest_message'] = message

        # =================================================
        # COUNT UNREAD
        # =================================================

        if (
            message.receiver_id == user.id
            and not message.is_read
        ):

            conversations[key]['unread_count'] += 1

    # =====================================================
    # BUILD CHAT URLS
    # =====================================================

    conversation_list = []

    for conversation in conversations.values():

        listing = conversation['listing']
        other_user = conversation['other_user']

        # =================================================
        # SELLER
        # =================================================

        if listing.seller_id == user.id:

            conversation['chat_url'] = reverse(
                'marketplace_chat_with_buyer',
                kwargs={
                    'listing_id': listing.id,
                    'buyer_id': other_user.id,
                }
            )

        # =================================================
        # BUYER
        # =================================================

        else:

            conversation['chat_url'] = reverse(
                'marketplace_chat',
                kwargs={
                    'listing_id': listing.id,
                }
            )

        conversation_list.append(conversation)

    # =====================================================
    # SORT BY MOST RECENT MESSAGE
    # =====================================================

    conversation_list.sort(
        key=lambda conversation: (
            conversation['latest_message'].created_at
        ),
        reverse=True
    )

    # =====================================================
    # TOTAL UNREAD
    # =====================================================

    unread_messages = (
        MarketplaceMessage.objects
        .filter(
            receiver=user,
            is_read=False
        )
        .count()
    )

    # =====================================================
    # TOTAL CONVERSATIONS
    # =====================================================

    total_conversations = len(
        conversation_list
    )

    # =====================================================
    # RENDER
    # =====================================================

    return render(
        request,
        'properties/marketplace_messages.html',
        {
            'conversations': conversation_list,
            'unread_messages': unread_messages,
            'total_conversations': total_conversations,
        }
    )
# =========================================================
    # DELETE PHOTOS
# =========================================================
@login_required(login_url='site_login')
@require_POST
def marketplace_delete_photo(request, listing_id, photo_id):

    # =========================================================
    # GET THE SELLER'S LISTING
    # =========================================================

    listing = get_object_or_404(
        MarketplaceListing,
        id=listing_id,
        seller=request.user
    )

    # =========================================================
    # FIND PHOTO
    # =========================================================

    photo = MarketplaceListingImage.objects.filter(
        id=photo_id,
        listing=listing
    ).first()

    # =========================================================
    # PHOTO DOES NOT EXIST
    # =========================================================

    if not photo:

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':

            return JsonResponse(
                {
                    'success': False,
                    'message': (
                        'This photo could not be found. '
                        'It may have already been deleted.'
                    ),
                },
                status=404
            )

        messages.warning(
            request,
            'This photo could not be found. '
            'It may have already been deleted.'
        )

        return redirect(
            'marketplace_edit',
            listing_id=listing.id
        )

    # =========================================================
    # DELETE PHYSICAL IMAGE FILE
    # =========================================================

    if photo.image:

        try:

            photo.image.delete(
                save=False
            )

        except Exception:

            pass

    # =========================================================
    # DELETE DATABASE RECORD
    # =========================================================

    photo.delete()

    # =========================================================
    # AJAX RESPONSE
    # =========================================================

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':

        return JsonResponse(
            {
                'success': True,
                'message': 'Photo deleted successfully.',
                'photo_id': photo_id,
            }
        )

    # =========================================================
    # NORMAL FALLBACK
    # =========================================================

    messages.success(
        request,
        'Photo deleted successfully.'
    )

    return redirect(
        'marketplace_edit',
        listing_id=listing.id
    )

@login_required
@require_POST
def marketplace_delete_main_photo(request, listing_id):

    listing = get_object_or_404(
        MarketplaceListing,
        id=listing_id,
        seller=request.user
    )

    # =========================================================
    # SAVE CURRENT PRIMARY IMAGE
    # =========================================================

    old_image = listing.image

    # =========================================================
    # FIND NEXT GALLERY PHOTO
    # =========================================================

    next_gallery_image = (
        listing.gallery_images
        .exclude(image__isnull=True)
        .exclude(image="")
        .order_by("id")
        .first()
    )

    # =========================================================
    # PROMOTE NEXT GALLERY PHOTO
    # =========================================================

    if next_gallery_image:

        listing.image = next_gallery_image.image

        listing.save(
            update_fields=[
                "image"
            ]
        )

        # The image has now become the primary image,
        # so remove its gallery record.
        next_gallery_image.delete()

    else:

        listing.image = None

        listing.save(
            update_fields=[
                "image"
            ]
        )

    # =========================================================
    # DELETE OLD PRIMARY IMAGE FILE
    # =========================================================

    if old_image:

        try:

            old_image.delete(
                save=False
            )

        except Exception:

            pass

    # =========================================================
    # AJAX RESPONSE
    # =========================================================

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':

        return JsonResponse(
            {
                'success': True,
                'message': (
                    'Primary photo deleted successfully.'
                ),
                'has_new_primary': bool(
                    next_gallery_image
                ),
                'new_primary_url': (
                    next_gallery_image.image.url
                    if next_gallery_image
                    and next_gallery_image.image
                    else None
                ),
            }
        )

    # =========================================================
    # NORMAL FALLBACK
    # =========================================================

    messages.success(
        request,
        "Primary photo deleted successfully."
        + (
            " The next advertisement photo is now "
            "your primary photo."
            if next_gallery_image
            else ""
        )
    )

    return redirect(
        "marketplace_edit",
        listing_id=listing.id
    )

# =========================================================
# GENERAL ACCOUNT PASSWORD RESET
# =========================================================

class AccountPasswordResetView(
    PasswordResetView
):

    template_name = (
        'properties/account_password_reset.html'
    )

    email_template_name = (
        'properties/account_password_reset_email.html'
    )

    subject_template_name = (
        'properties/account_password_reset_subject.txt'
    )

    success_url = reverse_lazy(
        'account_password_reset_done'
    )


# =========================================================
# PASSWORD RESET EMAIL SENT
# =========================================================

class AccountPasswordResetDoneView(
    PasswordResetDoneView
):

    template_name = (
        'properties/account_password_reset_done.html'
    )


# =========================================================
# PASSWORD RESET CONFIRM
# =========================================================

class AccountPasswordResetConfirmView(
    PasswordResetConfirmView
):

    template_name = (
        'properties/account_password_reset_confirm.html'
    )

    success_url = reverse_lazy(
        'account_password_reset_complete'
    )


# =========================================================
# PASSWORD RESET COMPLETE
# =========================================================

class AccountPasswordResetCompleteView(
    PasswordResetCompleteView
):

    template_name = (
        'properties/account_password_reset_complete.html'
    )

# =========================================================
# WORKER / CUSTOMER MESSAGES
# =========================================================

@login_required(login_url='site_login')
def worker_messages(request, hire_id):

    # -----------------------------------------------------
    # GET THE HIRE
    # -----------------------------------------------------

    hire = get_object_or_404(
        WorkerHire.objects.select_related(
            'customer',
            'customer__user',
            'worker',
            'worker__user',
        ),
        id=hire_id,
    )

    user = request.user

    # -----------------------------------------------------
    # MAKE SURE USER BELONGS TO THIS HIRE
    # -----------------------------------------------------

    is_customer = (
        hire.customer.user_id == user.id
    )

    is_worker = (
        hire.worker.user_id == user.id
    )

    if not is_customer and not is_worker:

        messages.error(
            request,
            'You are not authorized to access this conversation.'
        )

        return redirect(
            'marketplace_dashboard'
        )

    # -----------------------------------------------------
    # DETERMINE OTHER PERSON
    # -----------------------------------------------------

    if is_customer:

        other_user = hire.worker.user

    else:

        other_user = hire.customer.user

    # -----------------------------------------------------
    # SEND MESSAGE
    # -----------------------------------------------------

    if request.method == 'POST':

        message_text = (
            request.POST.get(
                'message',
                ''
            )
            .strip()
        )

        if not message_text:

            messages.error(
                request,
                'Please enter a message.'
            )

            return redirect(
                'worker_messages',
                hire_id=hire.id
            )

        WorkerMessage.objects.create(
            hire=hire,
            sender=user,
            receiver=other_user,
            message=message_text,
        )

        return redirect(
            'worker_messages',
            hire_id=hire.id
        )

    # -----------------------------------------------------
    # MARK RECEIVED MESSAGES AS READ
    # -----------------------------------------------------

    WorkerMessage.objects.filter(
        hire=hire,
        receiver=user,
        is_read=False,
    ).update(
        is_read=True
    )

    # -----------------------------------------------------
    # GET CONVERSATION
    # -----------------------------------------------------

    conversation = (
        WorkerMessage.objects
        .filter(
            hire=hire
        )
        .select_related(
            'sender',
            'receiver',
        )
        .order_by(
            'created_at'
        )
    )

    context = {

        'hire': hire,

        'conversation': conversation,

        'other_user': other_user,

        'is_customer': is_customer,
        'is_worker': is_worker,

    }

    return render(
        request,
        'properties/worker_messages.html',
        context
    )

def terms_and_conditions(request):
    return render(request, "properties/terms_and_conditions.html")


# =========================================================
# WORKER / CUSTOMER MESSAGES
# =========================================================

@login_required(login_url='site_login')
def worker_messages(request, hire_id):

    # =====================================================
    # GET THE HIRE
    # =====================================================

    hire = get_object_or_404(
        WorkerHire.objects.select_related(
            'customer',
            'customer__user',
            'worker',
            'worker__user',
        ),
        id=hire_id
    )


    # =====================================================
    # GET CUSTOMER AND WORKER USERS
    # =====================================================

    customer_user = hire.customer.user
    worker_user = hire.worker.user


    # =====================================================
    # SECURITY CHECK
    #
    # Only the customer OR worker connected to this
    # specific WorkerHire can access the conversation.
    # =====================================================

    if (
        request.user.id != customer_user.id
        and
        request.user.id != worker_user.id
    ):

        return HttpResponseForbidden(
            'You are not authorized to access this conversation.'
        )


    # =====================================================
    # DETERMINE THE OTHER PERSON
    # =====================================================

    if request.user.id == customer_user.id:

        other_user = worker_user
        other_person = hire.worker
        current_role = 'customer'

    else:

        other_user = customer_user
        other_person = hire.customer
        current_role = 'worker'


    # =====================================================
    # HANDLE SENDING MESSAGE
    # =====================================================

    if request.method == 'POST':

        message_text = request.POST.get(
            'message',
            ''
        ).strip()


        # =================================================
        # MESSAGE REQUIRED
        # =================================================

        if not message_text:

            messages.error(
                request,
                'Please enter a message.'
            )

            return redirect(
                'worker_messages',
                hire_id=hire.id
            )


        # =================================================
        # CREATE MESSAGE
        # =================================================

        new_message = WorkerMessage.objects.create(
                hire=hire,
                sender=request.user,
                receiver=other_user,
                message=message_text
            )

        # =====================================================
        # CREATE WORKER / CUSTOMER MESSAGE NOTIFICATION
        # =====================================================

        create_notification(
            recipient=other_user,
            notification_type=(
                'customer_message'
                if current_role == 'customer'
                else 'worker_message'
            ),
            title='New Message',
            message=(
                f'{request.user.get_full_name() or request.user.email} '
                f'sent you a message regarding your '
                f'{hire.service} job.'
            ),
            link=reverse(
                'worker_messages',
                kwargs={
                    'hire_id': hire.id,
                }
            )
        )


        # =================================================
        # REDIRECT BACK TO CONVERSATION
        # =================================================

        return redirect(
            'worker_messages',
            hire_id=hire.id
        )


    # =====================================================
    # GET MESSAGES
    # =====================================================

    conversation = (
        WorkerMessage.objects
        .filter(
            hire=hire
        )
        .select_related(
            'sender',
            'receiver'
        )
        .order_by(
            'created_at'
        )
    )


    # =====================================================
    # MARK MESSAGES SENT TO CURRENT USER AS READ
    # =====================================================

    WorkerMessage.objects.filter(
        hire=hire,
        receiver=request.user,
        is_read=False
    ).update(
        is_read=True
    )


    # =====================================================
    # CONTEXT
    # =====================================================

    context = {

        'hire': hire,

        'conversation': conversation,

        'other_user': other_user,

        'other_person': other_person,

        'current_role': current_role,

        'customer': hire.customer,

        'worker': hire.worker,
    }


    # =====================================================
    # RENDER CHAT PAGE
    # =====================================================

    return render(
        request,
        'properties/worker_messages.html',
        context
    )

@login_required(login_url='site_login')
def notifications(request):
    user_notifications = Notification.objects.filter(
        recipient=request.user
    ).order_by('-created_at')

    return render(
        request,
        'properties/notifications.html',
        {
            'notifications': user_notifications,
        }
    )


@login_required(login_url='site_login')
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(
        Notification,
        id=notification_id,
        recipient=request.user
    )

    notification.is_read = True
    notification.save(update_fields=['is_read'])

    if notification.link:
        return redirect(notification.link)

    return redirect('notifications')


@login_required(login_url='site_login')
def mark_all_notifications_read(request):
    Notification.objects.filter(
        recipient=request.user,
        is_read=False
    ).update(is_read=True)

    return redirect('notifications')