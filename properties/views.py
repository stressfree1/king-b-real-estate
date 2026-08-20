from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

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

    # -----------------------------------------------------
    # PREPARE ESTATE STATISTICS
    # -----------------------------------------------------

    for estate in estates:

        estate.total_plots = (
            estate.properties
            .count()
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
#
# Shows:
#
# Estate
# ├── Estate Overview
# ├── Development Plan
# ├── Development Features
# ├── Digital Layout
# └── Estate Types
#
# =========================================================

def estate_detail(
    request,
    estate_id
):

    estate = get_object_or_404(
        Estate.objects.prefetch_related(
            'estate_types',
            'properties'
        ),
        id=estate_id,
    )

    # -----------------------------------------------------
    # ESTATE TYPES
    # -----------------------------------------------------

    estate_types = (
        estate.estate_types
        .all()
        .order_by(
            'name'
        )
    )

    # -----------------------------------------------------
    # ESTATE-LEVEL PLOT COUNTS
    # -----------------------------------------------------

    total_plots = (
        estate.properties
        .count()
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

    # -----------------------------------------------------
    # ESTATE TYPE COUNTS
    # -----------------------------------------------------

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
            estate_type.properties
            .count()
        )

    # -----------------------------------------------------
    # DEVELOPMENT FEATURES
    #
    # Convert the TextField into a clean Python list.
    #
    # Admin example:
    #
    # Perimeter Fencing
    # Main Entrance Gate
    # Internal Road Network
    # Drainage System
    # Security Infrastructure
    #
    # -----------------------------------------------------

    development_features = [
        feature.strip()
        for feature in (
            estate.development_features or ''
        ).splitlines()
        if feature.strip()
    ]

    # -----------------------------------------------------
    # CONTEXT
    # -----------------------------------------------------

    context = {

        'estate': estate,

        'estate_types': estate_types,

        # Estate-level statistics
        'total_plots': total_plots,
        'available_plots': available_plots,
        'reserved_plots': reserved_plots,
        'sold_plots': sold_plots,

        # Development plan
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
#
# Shows one specific type inside an estate and only the
# plots assigned to that type.
#
# Example:
#
# Kings Park Estate
#     Classic
#         Plot 001
#         Plot 002
#         Plot 003
#
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

    # -----------------------------------------------------
    # ESTATE TYPE FEATURES
    # -----------------------------------------------------

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
        Property.objects.select_related(
            'estate',
            'estate_type',
            'agent'
        ).prefetch_related(
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
        'properties/about.html',
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
        id=job_id,
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
        id=job_id,
    )

    if request.method == 'POST':

        form = JobApplicationForm(
            request.POST,
            request.FILES,
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
            request.POST,
        )

        if form.is_valid():

            form.save()

            return render(
                request,
                'properties/contact_success.html',
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

def skilled_worker_profile(
    request,
    worker_id
):

    worker = get_object_or_404(
        SkilledWorker,
        id=worker_id,
        is_approved=True,
    )

    reviews = (
        WorkerReview.objects
        .filter(
            hire__worker=worker,
            is_approved=True,
        )
        .select_related(
            'hire',
            'hire__customer',
            'hire__worker',
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

    return render(
        request,
        'properties/skilled_worker_profile.html',
        {
            'worker': worker,
            'reviews': reviews,
            'reviews_count': reviews_count,
            'average_rating': average_rating,
        }
    )


# =========================================================
# MARKETPLACE
# =========================================================

def marketplace(request):

    return render(
        request,
        'properties/marketplace.html'
    )


# =========================================================
# UNIFIED SITE REGISTRATION
# =========================================================

def site_register(request):

    if request.user.is_authenticated:

        return redirect(
            'marketplace_dashboard'
        )

    if request.method == 'POST':

        form = AccountRegistrationForm(
            request.POST
        )

        if form.is_valid():

            full_name = form.cleaned_data[
                'full_name'
            ].strip()

            email = form.cleaned_data[
                'email'
            ].strip().lower()

            phone = form.cleaned_data[
                'phone'
            ].strip()

            password = form.cleaned_data[
                'password'
            ]

            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=full_name,
            )

            Customer.objects.create(
                user=user,
                full_name=full_name,
                phone=phone,
                email=email,
                address='',
                id_type='',
                id_number='',
                is_verified=False,
            )

            login(
                request,
                user
            )

            messages.success(
                request,
                'Your King B account has been created successfully. '
                'Your account is currently awaiting verification. '
                'You can browse the marketplace, but you must be '
                'verified before you can hire a skilled worker.'
            )

            return redirect(
                'marketplace_dashboard'
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
# ONE LOGIN FOR THE WHOLE WEBSITE
# =========================================================

@ensure_csrf_cookie
def site_login(request):

    if request.user.is_authenticated:

        return redirect(
            'marketplace_dashboard'
        )

    if request.method == 'POST':

        email = request.POST.get(
            'username',
            ''
        ).strip().lower()

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
# ONE LOGOUT
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

    customer_exists = (
        customer is not None
    )

    customer_verified = (
        customer_exists
        and customer.is_verified
    )

    worker_exists = (
        worker is not None
    )

    worker_approved = (
        worker_exists
        and worker.is_approved
    )

    worker_pending = (
        worker_exists
        and not worker.is_approved
    )

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
    }

    return render(
        request,
        'properties/marketplace_dashboard.html',
        context
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
            customer.email = (
                request.user.email
            )

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

    if not customer.is_verified:

        messages.warning(
            request,
            'Your customer profile is still waiting '
            'for verification.'
        )

        return redirect(
            'marketplace_dashboard'
        )

    hires = (
        customer.worker_hires
        .exclude(
            status='cancelled'
        )
        .select_related(
            'worker'
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

    cancelled_hires = WorkerHire.objects.filter(
        customer=customer,
        status='cancelled'
    ).count()

    reviews_count = WorkerReview.objects.filter(
        hire__customer=customer
    ).count()

    reviewed_hire_ids = set(
        WorkerReview.objects.filter(
            hire__customer=customer
        ).values_list(
            'hire_id',
            flat=True
        )
    )

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

    hires = (
        worker.customer_hires
        .select_related(
            'customer'
        )
        .order_by(
            '-hired_at'
        )
    )

    pending_requests = hires.filter(
        status='requested'
    ).count()

    active_jobs = hires.filter(
        status='active'
    ).count()

    completed_jobs = hires.filter(
        status='completed'
    ).count()

    cancelled_jobs = hires.filter(
        status='cancelled'
    ).count()

    declined_requests = hires.filter(
        status='declined'
    ).count()

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
            is_approved=True,
        )
        .select_related(
            'hire',
            'hire__customer',
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

    has_worked_with_customer = WorkerHire.objects.filter(
        worker=worker,
        customer=customer
    ).exists()

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

    worker = get_object_or_404(
        SkilledWorker,
        id=worker_id,
        is_approved=True
    )

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

    if not customer.is_verified:

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

    if worker.availability != 'available':

        messages.warning(
            request,
            'This skilled worker is currently not available.'
        )

        return redirect(
            'skilled_worker_profile',
            worker_id=worker.id
        )

    existing_hire = WorkerHire.objects.filter(
        customer=customer,
        worker=worker,
        status__in=[
            'requested',
            'active'
        ]
    ).first()

    if existing_hire:

        messages.info(
            request,
            f'You already have a pending or active hire '
            f'request with {worker.full_name}.'
        )

        return redirect(
            'marketplace_dashboard'
        )

    if request.method == 'POST':

        service = request.POST.get(
            'service',
            ''
        ).strip()

        notes = request.POST.get(
            'notes',
            ''
        ).strip()

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

        WorkerHire.objects.create(
            customer=customer,
            worker=worker,
            service=service,
            notes=notes,
            status='requested'
        )

        messages.success(
            request,
            f'Your request to hire {worker.full_name} '
            'has been submitted successfully.'
        )

        return redirect(
            'marketplace_dashboard'
        )

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

    messages.success(
        request,
        f'Your request to hire '
        f'{hire.worker.full_name} '
        'has been cancelled successfully.'
    )

    return redirect(
        'marketplace_dashboard'
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

    if not customer.is_verified:

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

    existing_review = WorkerReview.objects.filter(
        hire=hire
    ).first()

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

        comment = request.POST.get(
            'comment',
            ''
        ).strip()

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

    existing_review = CustomerReview.objects.filter(
        hire=hire
    ).first()

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

        comment = request.POST.get(
            'comment',
            ''
        ).strip()

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

    success_url = (
        '/account/settings/'
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

    success_url = (
        '/skilled-workers/password-reset/done/'
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

    success_url = (
        '/skilled-workers/password-reset/complete/'
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

        account_settings_obj = AccountSettings.objects.create(
            user=request.user
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